from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.registration, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^add_weighin/$', views.add_weighin, name='add_weighin'),
    url(r'^add_progress_photos/$', views.add_progress_photos, name='add_progress_photos'),
]
