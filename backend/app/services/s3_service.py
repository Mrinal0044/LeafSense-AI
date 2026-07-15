import logging
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger("s3_service")

class S3Service:
    _s3_client = None

    @classmethod
    def get_client(cls):
        """
        Return cached S3 client instance, or initialize it.
        """
        if cls._s3_client is None:
            try:
                # Initializes credentials automatically from environment variables,
                # ~/.aws/credentials, or EC2 instance metadata roles.
                cls._s3_client = boto3.client('s3', region_name=settings.AWS_REGION)
            except Exception as e:
                logger.error(f"Failed to initialize S3 client: {e}")
                raise e
        return cls._s3_client

    @classmethod
    def upload_file(cls, file_bytes: bytes, object_name: str, content_type: str = "image/jpeg") -> bool:
        """
        Upload binary payload directly to private S3 bucket.
        """
        try:
            s3 = cls.get_client()
            s3.put_object(
                Bucket=settings.AWS_S3_BUCKET,
                Key=object_name,
                Body=file_bytes,
                ContentType=content_type
            )
            logger.info(f"Successfully uploaded {object_name} to S3 bucket {settings.AWS_S3_BUCKET}")
            return True
        except ClientError as e:
            logger.error(f"S3 ClientError uploading {object_name}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error uploading {object_name} to S3: {e}")
            return False

    @classmethod
    def generate_presigned_url(cls, object_name: str, expiration: int = 3600) -> str:
        """
        Generate temporary secure pre-signed GET URL for accessing private images.
        """
        try:
            s3 = cls.get_client()
            url = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': settings.AWS_S3_BUCKET,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate pre-signed URL for {object_name}: {e}")
            return f"/api/uploads/{object_name}"  # Fallback to local endpoint path if S3 fails
        except Exception as e:
            logger.error(f"Unexpected error generating URL for {object_name}: {e}")
            return f"/api/uploads/{object_name}"

    @classmethod
    def delete_file(cls, object_name: str) -> bool:
        """
        Delete file from S3.
        """
        try:
            s3 = cls.get_client()
            s3.delete_object(
                Bucket=settings.AWS_S3_BUCKET,
                Key=object_name
            )
            logger.info(f"Successfully deleted {object_name} from S3 bucket {settings.AWS_S3_BUCKET}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete {object_name} from S3: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting {object_name} from S3: {e}")
            return False
