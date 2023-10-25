import boto3
from pprint import pprint

# Creates an S3 bucket.
# Loads two text files to the bucket.
# Prints a listing of the files, saving the filenames in a readable list.
# Reads one of the files and prints it to the console.
# Deletes the files in the bucket.
# Deletes the bucket.
# Checks that the bucket is deleted by listing the available buckets (should be none).

s3 = boto3.client("s3")

# s3.create_bucket(
#     Bucket="josh-nc-test-bucket",
#     CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
# )

# s3.upload_file("../test-file-1.txt", "josh-nc-test-bucket", "test-file-1.txt")
# s3.upload_file("../test-file-2.txt", "josh-nc-test-bucket", "test-file-2.txt")

# res = s3.list_objects_v2(Bucket="josh-nc-test-bucket")
# files = [file["Key"] for file in res["Contents"]]
# pprint(files)

# contents = s3.get_object(Bucket="josh-nc-test-bucket", Key=f"{files[0]}")
# text = contents["Body"].read().decode("utf-8")
# pprint(text)

# s3.delete_object(Bucket="josh-nc-test-bucket", Key=f"{files[0]}")

# s3.delete_object(Bucket="josh-nc-test-bucket", Key=f"{files[1]}")

# s3.delete_bucket(Bucket="josh-nc-test-bucket")

res = s3.list_buckets()
buckets = res["Buckets"]
pprint(buckets)
