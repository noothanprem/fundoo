from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns=[
    path('uploadimage',views.UploadImage.as_view(), name='upload_view'),
    path('noteshare',views.NoteShare.as_view(), name='noteshare_view'),
    path('api/notes',views.CreateNote.as_view(), name='createnote_view'),
    path('api/labels',views.CreateLabel.as_view(), name='createlabel_view'),
    path('api/labels/<label_id>',views.UpdateLabel.as_view(), name='updatelabel_view'),
    path('api/notes/<note_id>',views.UpdateNote.as_view(), name='updatenote_view')
]