from fastapi import APIRouter, Depends
from app.services.user import UserService
from app.models.user import RoleEnum
from app.schemas.user import UserRead
from app.dependencies.auth import require_role

router = APIRouter()

@router.patch(
    "/{user_id}/role/{new_role}",
    response_model=UserRead,
    dependencies=[Depends(require_role(RoleEnum.ADMIN))]
)
def set_user_role(
    user_id: int,
    new_role: RoleEnum,
    service: UserService = Depends()
):
    """
    ADMINs only: promote/demote any user to REPORTER, MAINTAINER, or ADMIN.
    """
    return service.change_role(user_id, new_role)
