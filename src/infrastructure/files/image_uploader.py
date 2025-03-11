import cloudinary
import cloudinary.uploader

from src.application.contracts.infrastructure.files.abc_image_uploader import (
    ABCImageUploader, InputImage, UploadedImage)
from src.common.typing.config import CloudinaryConfig


class ImageUploader(ABCImageUploader):
    def __init__(self, config: CloudinaryConfig) -> None:
        cloudinary.config(
            cloud_name=config["cloud_name"],
            api_key=config["api_key"],
            api_secret=config["api_secret"],
            secure=True
        )

    async def upload(self, file: InputImage) -> UploadedImage:
        return cloudinary.uploader.upload(file.file)

