import typing
import hashlib
from enum import Enum

from pydantic import BaseModel

# TODO - check what fields would be Optional

SCHEMA_EXAMPLE_CONFIGURATION = {
    'id': 1,
    'name': 'my configuration name',
    'folder_name': '',
    'user_id': 42,
    'created_at': '2022-08-14T10:23:15.299Z',
    'updated_at': '2022-08-14T10:23:26.299Z',
    'deleted': False,
    'machines_attributes': [
        {
            'name': 'some virtual machine name',
            'template': 'cluster_name.image_name',
            'environment': {
                'custom_fields': {
                    'ips': [],
                    'moid': '',
                    'state': '',
                },
            },
            'id': 12345,
            'image': 'image_name',
            'cluster': 'cluster_name',
            'state': 'ready',
            'configuration_id': 1,
            'created_at': '2022-06-11T10:34:09.299Z',
            'updated_at': '2022-06-11T10:34:09.299Z',
            'ip': None,
            'provider_id': None,
        },
    ],
}


class CustomFields(BaseModel):
    custom_fields: dict  # fields ips: list, moid: str, state: str

    def __hash__(self):
        return int(
            hashlib.md5(
                f'{self.custom_fields["ips"]},{self.custom_fields["moid"],self.custom_fields["state"]}'.encode('utf-8')
            ).hexdigest(),
            16,
        )

    def __eq__(self, other):
        return (
            self.custom_fields['ips'] == other['ips']
            and self.custom_fields['moid'] == other['moid']
            and self.custom_fields['state'] == other['state']
        )


# Machine attributes


# TODO - confirm machine states
class MachineState(str, Enum):
    queued = 'queued'
    deployed = 'deployed'
    ready = 'ready'
    destroy_queued = 'destroy_queued'
    deleted = 'deleted'
    failed = 'failed'


class MachineAttributesCreate(BaseModel):
    name: str
    template: str  # cluster.image :D # TODO - we could add extra validation
    environment: CustomFields


class MachineAttributesUpdate(BaseModel):
    id: int
    _destroy: bool


class MachineAttributes(MachineAttributesCreate):
    id: int
    image: str
    cluster: str
    state: MachineState
    configuration_id: int  # reference to containing configuration
    created_at: str
    updated_at: str
    ip: str | None  # list of IP values, but as string. Example: "1.2.3.4, ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff" or "n/a now"
    provider_id: str | None  # name of the machine in virtualization provider


# Configuration

# TODO - confirm configuration states
class ConfigurationState(str, Enum):
    ready = 'ready'
    destroy_queued = 'destroy_queued'
    updating = 'updating'


class ConfigurationCreate(BaseModel):
    name: str
    machines_attributes: typing.List[MachineAttributesCreate]


class ConfigurationUpdate(BaseModel):
    id: int
    machines_attributes: typing.List[MachineAttributesUpdate]


class Configuration(BaseModel):
    id: int
    name: str
    folder_name: str
    user_id: int
    created_at: str
    updated_at: str
    deleted: bool
    machines_attributes: typing.List[MachineAttributes]

    class Config:
        schema_extra = {'example': SCHEMA_EXAMPLE_CONFIGURATION}


# Job

# TODO - confirm the job statuses
class JobStatus(str, Enum):
    success = 'success'
    unprocessable_entity = 'unprocessable_entity'


class JobCreate(BaseModel):
    configuration: ConfigurationCreate


class JobUpdate(BaseModel):
    configuration: ConfigurationUpdate

    class Config:
        # needs to be here to enforce the _destroy in example
        schema_extra = {
            'example': {'configuration': {'id': 1, 'machines_attributes': [{'id': 1234, '_destroy': True}]}}
        }


class JobDelete(BaseModel):
    id: int


class Job(BaseModel):
    status: JobStatus
    configuration: Configuration

    class Config:
        schema_extra = {
            'example': {'status': 'success', 'configuration': SCHEMA_EXAMPLE_CONFIGURATION},
        }
