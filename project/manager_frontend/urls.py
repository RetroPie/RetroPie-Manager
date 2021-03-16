from django.conf.urls import url
from django.views.generic import TemplateView

from .views import HomeView
from .views.config import RecalboxConfigFormView
from .views.configes import RecalboxConfigEsFormView
from .views.configas import RecalboxConfigAsFormView
from .views.logs import LogsView
from .views.bios import BiosListView, BiosUploadJsonView
from .views.roms import RomListView, RomUploadJsonView
#from .views.saves import SavesListView
from .views.systems import SystemsListView
from .views.monitor import MonitoringView
from .views.monitor import update_context

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    
    url(r'^bios/$', BiosListView.as_view(), name='bios'),
    url(r'^bios/upload$', BiosUploadJsonView.as_view(), name='bios-upload'),
    
    url(r'^config/$', RecalboxConfigFormView.as_view(), name='config'),
	
	url(r'^configes/$',  RecalboxConfigEsFormView.as_view(), name='configes'),
	
	url(r'^configas/$',  RecalboxConfigAsFormView.as_view(), name='configas'),
    
    url(r'^monitoring/$', MonitoringView.as_view(), name='monitoring'),
    
    url(r'^logs/$', LogsView.as_view(), name='logs'),
    
    url(r'^systems/$', SystemsListView.as_view(), name='roms-systems'),
    
    #url(r'^systems/roms/saves/$', SavesListView.as_view(), name='roms-saves-list'),
    
    url(r'^systems/roms/(?P<system>[-\w]+)$', RomListView.as_view(), name='roms-list'),
    url(r'^systems/roms/(?P<system>\w+)/$', RomListView.as_view(), name='roms-list'),
    url(r'^systems/roms/(?P<system>[-\w]+)/upload/$', RomUploadJsonView.as_view(), name='roms-upload'),

    url(r'^monitor_update/$', update_context, name="monitor-update"),

]
