import logging
import boto3
from botocore.exceptions import ClientError
import os


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to your S3 bucket!

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    if object_name is None:
        object_name = os.path.basename(file_name)
    session = boto3.session.Session()
    s3_client = session.client("s3")
    try:
        s3_client.upload_file(file_name, bucket, object_name)
        os.remove(file_name)
        return True
    except ClientError as e:
        logging.error(e)
        return False
