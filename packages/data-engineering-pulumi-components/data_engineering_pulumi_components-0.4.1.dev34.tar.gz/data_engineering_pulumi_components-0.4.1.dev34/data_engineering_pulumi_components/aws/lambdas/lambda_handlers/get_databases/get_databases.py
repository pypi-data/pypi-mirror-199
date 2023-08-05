import json
import os
from typing import List

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError, NoCredentialsError


def get_s3_objects(client: BaseClient, bucket: str) -> List[str]:
    """Get list of all objects in an S3 bucket (get keys).
    Parameters
    ----------
    client : S3
        Boto3 s3 client initialised with boto3.client("s3")
    bucket : str
        Name of the bucket to get objects from.
    Returns
    -------
    List
        List of S3 objects.
    """
    bucket_objects = []
    try:
        response = client.list_objects_v2(Bucket=bucket)
        if response.get("Contents"):
            for item in response["Contents"]:
                bucket_objects.append(item["Key"])
        else:
            print("Bucket empty")
    except (ClientError, NoCredentialsError) as e:
        print(e)
        raise

    return bucket_objects


def get_database_names(s3_objects: List[str]) -> List[str]:
    """Get database names from a list of s3 objects.
    Parameters
    ----------
    s3_objects : list
        List of keys of objects in the bucket.
    Returns
    -------
    list
        Sorted list of database names.
    """
    databases = set()
    for bucket_object in s3_objects:
        # Get database name from each file and add it to a set
        # NB hive partitioning used for defining directory hierarchy
        # hence split at "="
        try:
            components = bucket_object.split("/")
            database_name = [item.split("=")[1]
                             for item in components
                             if item.startswith("database")
                             ][0]
            databases.add(database_name)
        except IndexError:
            print(f"Could not split database name from {bucket_object}")
            continue
    return sorted(list(databases))


def handler(event, context):
    # The endpoint_url is only needed for when we run integration tests using localstack
    endpoint_url = (
        f"http://{os.getenv('LOCALSTACK_HOSTNAME')}:{os.getenv('EDGE_PORT')}"
        if os.getenv("LOCALSTACK_HOSTNAME")
        else None
    )
    s3 = boto3.client("s3", endpoint_url=endpoint_url)

    # Fetch bucket_name and file_name using proxy integration method from API Gateway
    bucket = os.environ["bucket_name"]

    # Get list of objects from bucket and work out database names from them
    s3_objects = get_s3_objects(s3, bucket)
    database_names = get_database_names(s3_objects)

    # Return API response json
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"databases": database_names}),
    }
