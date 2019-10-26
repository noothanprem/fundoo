from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from note.models import Label


class LabelOperations:

    def create_label(self,request):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            print (request.user,"userrrrrrrrrrrrrrrrrr")
            name = request.data['name']


            user=request.user
            user_id=request.user
            print(user,"111111111111111111111111111")
            print (user.id,"isddddddddddddddddddddddd")
            userobject=User.objects.get(id=user.id)

            if Label.objects.filter(user_id=user_id,name=name).exists():
                response['success'] = False
                response['message'] = "Label already exists."
                response['data'] = ""
                return response

            print (type(userobject),"typeeeeeeeeeeeee")
            labelobject=Label.objects.create(name=name, user=userobject)
            response['success']=True
            response['message']="Label created successfully"
            response['data']=name

        except ObjectDoesNotExist:
            response['success'] = False
            response['message'] = "Exception occured while accessing the user"
            response['data'] = ""
            user = request.user
            print(user,"111111111111111111111111111")
        return response

    def get_label(self,request):

        response = {"success": False,
                    "message": "",
                    "data": ""}
        try:
            print (request,"requestttttttttttttttttttttttt")
            user = request.user
            print (user,"userrrrrrrrrrrrrrr")
            print (user.id,"userrrrrrrrriddddddddd")
            labels = Label.objects.filter(user_id=user.id)
            print (labels,"labellllllllllllssssssssssss")
            labels_list = []
            for label in labels:
                labels_list.append(label.name)
            print(labels_list,"labelsssssssssslisttttttt")
            response=labels_list
        except Label.DoesNotExist:
            response['success']=False
            response['message']="Exception occured while getting the Label"
            response['data']=""
        return response

    def update_label(self,request,label_id):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            user=request.user
            print (label_id,"label idddddd")

            print (user,"User in update labellllllllll")
            request_body=request.body
            print (request_body,"request bodyyyyyyyyyyyyyyyyy")
            print (type(request_body),"typeeeeeee requestttttt bodyyyy")
            #body_unicode = request.body.decode('utf-8')

            body_unicode = request_body.decode('utf-8')

            print (body_unicode,"unicooooodddeeeeee")
            print(type(body_unicode),"type uniiiccooodeee")

            label_object=Label.objects.get(id=label_id)
            label_object.name=body_unicode
            label_object.save()
            response['success'] = True
            response['message'] = "Label Updated Successfully"
            response['data'] = ""

            print ("Successsssssssssssssssssssssssssssssssss")
        except Label.ObjectDoesnotExist:
            response['success'] = False
            response['message'] = "Exception occured while getting the Label object"
            response['data'] = ""

        return response

    def delete_label(self,request,label_id):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:
            user = request.user
            user_id = user.id
            print (user_id, "userrrrrrriddddddddddddddd")
            label_object = Label.objects.get(id=label_id, user_id=user_id)
            label_object.delete()
            print ("Successssssssssssssssssssssssssss")
            response['success'] = True
            response['message'] = "Label Deleted Successfully"
            response['data'] = ""
        except Label.DoesNotExist:
            response['success'] = False
            response['message'] = "Exception occured while getting the Label object"
            response['data'] = ""

        return response



