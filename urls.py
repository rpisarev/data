from django.conf.urls.defaults import *
from data import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	('^$', views.hello),
	(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
	(r'^choice/([a-z]+)/$',views.objects_form),
	(r'^choice/([a-z]+)/([a-z]+)/in/$',views.objects_in_form),
	(r'^choice/([a-z]+)/([a-z]+)/one/in/$',views.objects_in_form),
	(r'^choice/([a-z]+)/([a-z]+)/one/$',views.objects_one_form),
	(r'^choice/([a-z]+)/([a-z]+)/$',views.objects_tab_form),

	(r'^choice/sites/cms/$', views.sites_admins_form),

	(r'^admin/', include(admin.site.urls)),
)
