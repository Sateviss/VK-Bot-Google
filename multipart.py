import json
import

def listbucketandobjects () :
    with open("credentials.json", 'r') as f:
        data = json.loads(f.read())
        bucket_target = data["aws"]["targetBucket"]
        s3ressource = client(
            service_name='s3',
            endpoint_url= data["aws"]["hostEndPoint"],
            aws_access_key_id= data["aws"]["idKey"],
            aws_secret_access_key=data["aws"]["secretKey"],
            use_ssl=True,
            )

        key = 'mp-test.txt'
        mpu = s3ressource.create_multipart_upload(Bucket=bucket_target, Key=key)
        part1 = s3ressource.upload_part(Bucket=bucket_target, Key=key, PartNumber=1,
                                UploadId=mpu['UploadId'], Body='Hello, world!')
        # Next, we need to gather information about each part to complete
        # the upload. Needed are the part number and ETag.
        part_info = {
            'Parts': [
                {
                    'PartNumber': 1,
                    'ETag': part1['ETag']
                }
            ]
        }
        IDofUploadedMPU=mpu['UploadId']
        print ('**********************PRINT THE  ULPOAD ID **********************')
        print IDofUploadedMPU
        print ('**********************PRINT THE COMPLETE LIST PARTS  **********************')
        jacko=s3ressource.list_parts(Bucket=bucket_target,Key=key,UploadId=IDofUploadedMPU)
        print (jacko)
        print ('**********************PRINT THE RECURSIVE COMPLETE LIST PARTS  **********************')
        for jack in s3ressource.list_parts(Bucket=bucket_target,Key=key, UploadId=IDofUploadedMPU)["Parts"]:
            print(jack)
        print ('********************** NOW UPLOADING **********************')
        s3ressource.complete_multipart_upload(Bucket=bucket_target, Key=key, UploadId=mpu['UploadId'],
                                        MultipartUpload=part_info)

listbucketandobjects ()