import typing

import fastapi

from app import schemas

router = fastapi.APIRouter()


@router.get('/', response_model=typing.List[schemas.Configuration])
def read_configurations():
    return schemas.fake_read_configurations_response()


@router.post('/', response_model=schemas.Job)
def create_configurations(configuration: schemas.JobCreate):
    return schemas.fake_create_configurations_response(configuration.configuration)


@router.get('/{configuration_id}', response_model=schemas.Configuration)
def read_configuration(configuration_id: int):
    return schemas.fake_read_configuration_response(configuration_id)


# TODO - check that id is "duplicated" (configuration_id: int needed for documentation)
@router.put('/{job_id}', response_model=schemas.Job)
def update_configuration(job_id: int, job: schemas.JobUpdate):
    return schemas.fake_update_configurations_response(job.configuration)


@router.delete('/{job_id}', response_model=schemas.Job)
def delete_job(job_id: int, job: schemas.JobDelete):
    return schemas.fake_delete_job_response(job)
