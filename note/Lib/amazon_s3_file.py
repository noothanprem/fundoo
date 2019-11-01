import boto3

class UploadImage:

    def smd_response(self,success,message,data):
        response={
            "success":"",
            "message":"",
            "data":""
        }
        response['success']=success
        response['message']=message
        response['data']=data
        return response

    def upload_file(self,image):
        """

        :param image: image to upload
        :return: uploads the image and returns the object returned

        """
        try:

            s3 = boto3.resource('s3')
            s3.meta.client.upload_fileobj(image, "hat123", "jkl")
            response = self.smd_response(True, 'Image upload successful', '')
            return response
        except Exception:
            response = self.smd_response(False, 'Image upload Failed', '')
            return response
