"""Azure Blob Storage Service."""

from azure.storage.blob import BlobServiceClient
from io import BytesIO
from app.api.v1.constant import AZURE_STORAGE_CONTAINER_NAME, AZURE_STORAGE_CONNECTION_STR
import base64


class AzureBlobService:
    def __init__(self, container_name: str = AZURE_STORAGE_CONTAINER_NAME, connecting_string: str = AZURE_STORAGE_CONNECTION_STR):
        self.blob_service_client = BlobServiceClient.from_connection_string(connecting_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload_base64_image(self, base64_str: str, blob_name: str) -> None:
        try:
            image_data = base64.b64decode(base64_str)
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(BytesIO(image_data), overwrite=True)
            return
        except Exception as e:
            error_message = f"Failed to upload a image file to {blob_name}, Exception={str(e)}"
            raise Exception(error_message)
