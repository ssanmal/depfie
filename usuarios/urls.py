from django.conf.urls import url

from . import views

urlpatterns = [url(r'^formulario/$', views.formulario),
               url(r'^postregistro/$', views.postregistro),
               url(r'^login/$', views.logon, name='logon'),
               url(r'^logot/$', views.logot),
               url(r'^cambiopass/$', views.cambiopass),
               url(r'^cambiopassad/$', views.cambiopassad),
               url(r'^postanunreg/$', views.postanunreg),
               url(r'^postanunad/$', views.postanunad),
               url(r'^postcambiocon/$', views.postcambiocon),
               url(r'^anuque/$', views.anuque),
               url(r'^bannque/$', views.bannque),
               url(r'^depque/$', views.depque),
               url(r'^creanunreg/$', views.creanunreg),
               url(r'^creanunad/$', views.creanunad),
               url(r'^aproban/$', views.aproban),
               url(r'^postchan/$', views.postchan),
               url(r'^postdescan/$', views.postdescan),
               url(r'^rechan/$', views.rechan),
               url(r'^edian/$', views.edian),
               url(r'^borraus/$', views.borraus),
               url(r'^borraan/$', views.borraan),
               url(r'^sesion/$', views.sesion),
               url(r'^userque/$', views.userque),
               url(r'^formanun/$', views.formulario),
               ]
# urlpatterns = [
#    url(r'^$', views.index, name='index'),
# ]