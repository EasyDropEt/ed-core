from ed_domain.validation import ABCValidator, ValidationResponse
from ed_infrastructure.validation.default import (NameValidator,
                                                  PhoneNumberValidator)

from ed_core.application.features.admin.dtos.create_admin_dto import \
    CreateAdminDto
from ed_core.application.features.common.dtos.validators.create_location_dto_validator import \
    CreateLocationDtoValidator


class CreateAdminDtoValidator(ABCValidator[CreateAdminDto]):
    def __init__(self) -> None:
        self._location_validator = CreateLocationDtoValidator()
        self._name_validator = NameValidator()
        self._phone_number_validator = PhoneNumberValidator()

    def validate(
        self,
        value: CreateAdminDto,
        location: str = ABCValidator.DEFAULT_ERROR_LOCATION,
    ) -> ValidationResponse:
        errors = []

        errors.extend(
            self._phone_number_validator.validate(
                value["phone_number"], f"{location}.phone_number"
            ).errors
        )
        errors.extend(
            self._name_validator.validate(
                value["first_name"], f"{location}.first_name"
            ).errors
        )
        errors.extend(
            self._name_validator.validate(
                value["last_name"], f"{location}.last_name"
            ).errors
        )

        return ValidationResponse(errors)
