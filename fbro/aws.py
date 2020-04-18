# Core Library modules
from typing import List, Optional

# Third party modules
import boto3


def main():
    return get_bucket_names()


def get_bucket_names():
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    buckets = response["Buckets"]  # There is also the creation date
    return [b["Name"] for b in buckets]


def list_files(
    bucket: str, prefix: str = "", profile_name: Optional[str] = None
) -> List[str]:
    """
    List up to 1000 files in a bucket.

    Parameters
    ----------
    bucket : str
    profile_name : str, optional
        AWS profile

    Returns
    -------
    s3_paths : List[str]
    """
    session = boto3.Session(profile_name=profile_name)
    conn = session.client("s3")
    keys = []
    ret = conn.list_objects_v2(Bucket=bucket, Prefix=prefix)
    if "Contents" not in ret:
        return []
    # Make this a generator in future and use the marker:
    # https://boto3.readthedocs.io/en/latest/reference/services/
    #     s3.html#S3.Client.list_objects
    resp = conn.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter="/")
    if "CommonPrefixes" in resp:
        for prefix_dict in resp["CommonPrefixes"]:
            keys.append(prefix_dict["Prefix"])
    if "Contents" in resp:
        for key in resp["Contents"]:
            keys.append(key["Key"])
    return keys
