from . import (
    Configuration,
    MachineAttributes,
    Job,
    ConfigurationCreate,
    CustomFields,
)


def fake_read_configuration_response(configuration_id: int = 123456789):
    return Configuration(
        id=configuration_id,
        name="configuration name",
        folder_name="folder name for machines",
        user_id=40,
        created_at="2022-06-24T11:57:58.299Z",
        updated_at="2022-06-24T11:57:58.299Z",
        deleted=True,
        machines_attributes=[
            MachineAttributes(
                id=359999,
                name='virtual machine 1',
                image='image_name',
                cluster='cluster_name',
                template='cluster_name.image_name',
                state='queued',
                configuration_id=2,
                created_at='2022-06-11T10:34:09.299Z',
                updated_at='2022-06-11T10:34:09.299Z',
                ip=None,
                provider_id=None,
                environment=CustomFields(custom_fields={'ips': "a,b", "moid": "m", "state": "excited"}),
            )
        ],
    )


def fake_read_configurations_response():
    return [fake_read_configuration_response()]


def fake_create_configurations_response(configuration: ConfigurationCreate):
    return Job(
        status='success',
        configuration=Configuration(
            id=567,
            name=configuration.name,
            folder_name="folder name for machines",
            user_id=40,
            created_at="2022-06-24T11:57:58.299Z",
            updated_at="2022-06-24T11:57:58.299Z",
            deleted=True,
            machines_attributes=[
                MachineAttributes(
                    name=machine.name,
                    template=machine.template,
                    environment=CustomFields(custom_fields=machine.environment),
                    id=359999,
                    image=machine.template.split('.', maxsplit=1)[1],
                    cluster=machine.template.split('.', maxsplit=1)[0],
                    state='queued',
                    configuration_id=567,
                    created_at='2022-06-11T10:34:09.299Z',
                    updated_at='2022-06-11T10:34:09.299Z',
                    ip=None,
                    provider_id=None,
                )
                for machine in configuration.machines_attributes
            ],
        ),
    )


def fake_update_configurations_response(job):
    return Job(
        status='success',
        configuration=Configuration(
            id=job.id,
            name="my configuration name",
            folder_name="folder name for machines",
            user_id=40,
            created_at="2022-06-24T11:57:58.299Z",
            updated_at="2022-06-24T11:57:58.299Z",
            deleted=True,
            machines_attributes=[
                MachineAttributes(
                    name='some virtual machine name',
                    template='cluster_name.image_name',
                    environment=CustomFields(custom_fields={'ips': "a,b", "moid": "m", "state": "excited"}),
                    id=machine.id,
                    image='image_name',
                    cluster='cluster_name',
                    state='queued',
                    configuration_id=job.id,
                    created_at='2022-06-11T10:34:09.299Z',
                    updated_at='2022-06-11T10:34:09.299Z',
                    ip=None,
                    provider_id=None,
                )
                for machine in job.machines_attributes
            ],
        ),
    )


def fake_delete_job_response(job):
    return Job(
        status='success',
        configuration=Configuration(
            id=job.id,
            name="configuration name",
            folder_name="folder name for machines",
            user_id=40,
            created_at="2022-06-24T11:57:58.299Z",
            updated_at="2022-06-24T11:57:58.299Z",
            deleted=True,
            machines_attributes=[
                MachineAttributes(
                    id=357777,
                    name='virtual machine 1',
                    image='image_name',
                    cluster='cluster_name',
                    template='cluster_name.image_name',
                    state='queued',
                    configuration_id=job.id,
                    created_at='2022-06-11T10:34:09.299Z',
                    updated_at='2022-06-11T10:34:09.299Z',
                    ip=None,
                    provider_id=None,
                    environment=CustomFields(custom_fields={'ips': "a,b", "moid": "m", "state": "excited"}),
                )
            ],
        ),
    )


def fake_read_templates_response():
    return ['dummy template 1', 'dummy template 2', 'dummy template 3']
