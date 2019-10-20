import boto3
#class UploadFile:

def upload_file(image):
    try:
        print("insideeeeeeeeeeeeeeeeeeeeeeeeeeee")
        s3 = boto3.resource('s3')
        s3.meta.client.upload_fileobj(image, "hat123", "pqr")
        return "success"
    except Exception:
        print ("Exception occured while uploading image to s3 bucket")
        return "failed"
