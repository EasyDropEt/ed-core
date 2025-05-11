from ed_core.application.features.common.dtos.validators.abc_dto_validator import (
    ABCDtoValidator, ValidationResponse)
from ed_core.application.features.driver.dtos.pick_up_order_verify_dto import \
    PickUpOrderVerifyDto


class PickUpOrderVerifyDtoValidator(ABCDtoValidator[PickUpOrderVerifyDto]):
    def validate(self, dto: PickUpOrderVerifyDto) -> ValidationResponse:
        errors = []

        if len(errors):
            return ValidationResponse.invalid(errors)

        return ValidationResponse.valid()
