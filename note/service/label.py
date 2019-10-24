from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from note.models import Label
class LabelOperations:

    def create_label(self,request):

        response = {"success": False,
                    "message": "",
                    "data": ""}

        try:

            name = request.data['name']
            user = request.data['user']
            # print(user)
            userobject=User.objects.get(id=user)
            print (type(userobject),"typeeeeeeeeeeeee")
            labelobject=Label.objects.create(name=name, user=userobject)
            response['success']=True
            response['message']="Label created successfully"
            response['data']=name

        except ObjectDoesNotExist:
            response['success'] = False
            response['message'] = "Exception occured while accessing the user"
            response['data'] = ""
        return response

