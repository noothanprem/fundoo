from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns=[
    path('uploadimage',views.UploadImage.as_view(), name='upload_view'),
    path('noteshare',views.NoteShare.as_view(), name='noteshare_view'),
    path('notes',views.CreateNote.as_view(), name='createnote_view'),
    path('labels',views.CreateLabel.as_view(), name='createlabel_view'),
    path('labels/<label_id>',views.UpdateLabel.as_view(), name='updatelabel_view'),
    path('notes/<note_id>',views.UpdateNote.as_view(), name='updatenote_view'),
    path('trash',views.Trash.as_view(),name='trashview'),
    path('archieve',views.Archieve.as_view(), name="archieveview"),
    path('reminder',views.Reminder.as_view(), name="reminderveview"),
    path('lazy',views.LazyLoadng.as_view(),name='lazyloading')
]