from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.driver.dtos.drop_off_order_verify_dto import \
    DropOffOrderVerifyDto


class DropOffOrderVerifyDtoValidator(ABCDtoValidator[DropOffOrderVerifyDto]):
    def validate(self, dto: DropOffOrderVerifyDto) -> ValidationResponse:
        errors = []

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
