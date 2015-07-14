# == Schema Information
#
# Table name: machines
#
#  id                  :integer          not null, primary key
#  name                :string
#  template            :string
#  environment         :text
#  configuration_id_id :integer
#  created_at          :datetime         not null
#  updated_at          :datetime         not null
#

class Machine < ActiveRecord::Base
  belongs_to :configuration, inverse_of: :machines

  validates :name,
    presence: true,
    length: {minimum: 3},
    uniqueness: { scope: :configuration_id },
    format: {
      with: /\A[A-Za-z0-9_\.]+\z/,
      message: "only allows letters, digits, underscore and dots"
    }

  validates :template, inclusion: { in: ProviderTemplate.all }
  validates :state, inclusion: { in: %w(queued ready destroy_queued deleted) }
  validate  :environment_has_allowed_structure

  after_create :schedule_provision_vm

  serialize :environment, JSON

  strip_attributes :except => :environment

  delegate :user, :folder_name, to: :configuration

  def job_id
   "%d.%d" % [configuration.id, id]
  end

  def deleted?
    state == 'deleted'
  end

  def destroy_queued?
    state == 'destroy_queued'
  end

  def deleted_or_destroy_queued?
    deleted? or destroy_queued?
  end

  def destroy
    if deleted?
      #VM is not running therefore I can delete AR object
      OnlineKitchen.logger.info "Destroying machine: #{self.id}"
      super
    elsif state == 'destroy_queued'
      OnlineKitchen.logger.info "Machine: #{self.id} is already scheduled to destroy."
    else
      OnlineKitchen.logger.info "Scheduling releasing for machine: #{self.id}"
      OnlineKitchen::LabManagerRelease.perform_async(self.id)
      self.state = 'destroy_queued'
      self.save
      run_callbacks :destroy
      freeze
    end
  end

  def schedule_destroy
    OnlineKitchen.logger.info "Scheduling releasing for machine: #{self.id}"
    OnlineKitchen::LabManagerRelease.perform_async(self.id)
    update_attributes(state: :destroy_queued)
  end

  private

    def schedule_provision_vm
      OnlineKitchen.logger.info "Scheduling provision for machine: #{self.id}"
      OnlineKitchen::LabManagerProvision.perform_async(self.id)
    end

    def environment_has_allowed_structure
      return if self.environment.nil?

      unless Hash === environment
        errors.add(:environment, "has to be Hash (key-value) like structure")
        return false
      end

      environment.each do |key, value|
        unless key =~ /\A[A-Za-z][A-Za-z0-9_]*\z/
          errors.add(:environment, "keys has to be Literal (e.g. start on letter followed by letter, digits or underscore)")
          return false
        end
        unless String === value
          errors.add(:environment, "value has to be String")
          return false
        end
      end
      true
    end
end
