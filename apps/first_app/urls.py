from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^register$', views.register, name='regester'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^show$', views.show, name='show'),
    url(r'^create', views.new_task, name='create'),
    url(r'^(?P<id>\d+)/edit$', views.update_page, name='update'),
    url(r'^(?P<id>\d+)/delete$', views.delete, name='delete'),
    url(r'^edit_info$', views.edit, name='edit'),


]