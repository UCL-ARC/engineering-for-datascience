from json import dumps, load
from minio import Minio
from minio.error import S3Error
import io
import urllib3

httpclient = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
#    ca_certs='/home/almalinux/.mc/certs/CAs/local.crt'
)

def make_client(configfile):
    data = {
        "endpoint": "localhost",
        "access_key": "",
        "secret_key": ""
    }

    with open(configfile, 'r') as file:
        data = load(file)

    client = Minio(data["endpoint"], access_key=data["access_key"], secret_key=data["secret_key"], http_client=httpclient)
    return client

s3_resource = make_client("s3.json")

def json_to_s3(uri, name, data):
    found = s3_resource.bucket_exists(uri)
    if not found:
        s3_resource.make_bucket(uri)
   
    content = dumps(data).encode("utf-8")
    s3_resource.put_object(uri, name, io.BytesIO(content), len(content))