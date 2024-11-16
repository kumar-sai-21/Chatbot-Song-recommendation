from django.urls import path,include
from . import views
urlpatterns = [
   path("",views.home,name='home'),
   path("getchat/<str:id>",views.getchat,name='getchat'),
]
