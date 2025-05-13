"""Azure Blob Storage Service."""

from azure.storage.blob import BlobServiceClient
from io import BytesIO
from app.services.constant import AZURE_STORAGE_CONTAINER_NAME, AZURE_STORAGE_CONNECTION_STR
import base64


class AzureBlobService:
    def __init__(self, container_name: str = AZURE_STORAGE_CONTAINER_NAME, connecting_string: str = AZURE_STORAGE_CONNECTION_STR):
        self.blob_service_client = BlobServiceClient.from_connection_string(connecting_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload_binary_image(self, binary_data: bytes, blob_name: str) -> None:
        """Upload a binary image to Azure Blob Storage.

        Args:
            binary_data (bytes): The binary data of the image.
            blob_name (str): The blob name to use for the uploaded file.

        Raises:
            Exception: When the upload fails, an exception is raised with the error message.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(binary_data, overwrite=True)
            return
        except Exception as e:
            error_message = f"Failed to upload a image file to {blob_name}, Exception={str(e)}"
            raise Exception(error_message)

    def upload_base64_image(self, base64_str: str, blob_name: str) -> None:
        """Upload a base64 encoded image to Azure Blob Storage.

        Args:
            base64_str (str): The base64 encoded string of the image.
            blob_name (str): The blob name to use for the uploaded file.

        Raises:
            Exception: When the upload fails, an exception is raised with the error message.
        """
        try:
            image_data = base64.b64decode(base64_str)
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(BytesIO(image_data), overwrite=True)
            return
        except Exception as e:
            error_message = f"Failed to upload a image file to {blob_name}, Exception={str(e)}"
            raise Exception(error_message)

    def upload_file(self, file_path: str, blob_name: str) -> None:
        """Upload a file to Azure Blob Storage.

        Args:
            file_path (str): The path of the file to upload.
            blob_name (str): The blob name to use for the uploaded file.

        Raises:
            Exception: When the upload fails, an exception is raised with the error message.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
        except Exception as e:
            error_message = f"Failed to upload a file to {blob_name}, Exception={str(e)}"
            raise Exception(error_message)

    def get_result_image(self, save_path: str, blob_name: str) -> None:
        """Download a file from Azure Blob Storage.

        Args:
            save_path (str): The path where the downloaded file will be saved.
            blob_name (str): The blob name to download.

        Raises:
            Exception: When the download fails, an exception is raised with the error message.
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            with open(save_path, "wb") as file:
                blob_client.download_blob().download_to_stream(file)

        except Exception as e:
            error_message = f"Failed to download a image file from {blob_name}, Exception={str(e)}"
            raise Exception(error_message)
