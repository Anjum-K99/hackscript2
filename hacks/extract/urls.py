from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="extract-home"),
    path('about/',views.about,name="extract-about"),
    path('contact/',views.contact,name="extract-contact"),
    path('comment/',views.comment,name = "extract-comment"),
]