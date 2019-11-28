from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns=[
    path('upload_image',views.UploadImage.as_view(), name='upload_view'),
    path('note_share',views.NoteShare.as_view(), name='noteshare_view'),
    path('notes',views.CreateNote.as_view(), name='createnote_view'),
    path('labels',views.CreateLabel.as_view(), name='createlabel_view'),
    path('labels/<label_id>',views.UpdateLabel.as_view(), name='updatelabel_view'),
    path('notes/<note_id>',views.UpdateNote.as_view(), name='updatenote_view'),
    path('notes_trash',views.Trash.as_view(),name='trashview'),
    path('notes_archieve',views.Archieve.as_view(), name="archieveview"),
    path('notes_reminder',views.Reminder.as_view(), name="reminderveview"),
    path('lazy_loading',views.LazyLoadng.as_view(),name='lazyloading')
]