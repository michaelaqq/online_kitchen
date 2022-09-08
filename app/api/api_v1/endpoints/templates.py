from typing import List

import fastapi

from app import schemas

router = fastapi.APIRouter()


@router.get('/', response_model=List[str])  # TODO we could add the templates validation
def read_templates():
    return schemas.fake_read_templates_response()
