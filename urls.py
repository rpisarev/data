from django.conf.urls.defaults import *
from data import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	('^$', views.hello),
	(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
#	(r'^choice/projects/projects/$', views.projects_projects_form),
#    (r'^choice/projects/clients/$', views.projects_clients_form),
	(r'^choice/([a-z]+)/$',views.objects_form),
	(r'^choice/([a-z]+)/([a-z]+)/in/$',views.objects_in_form),
	(r'^choice/([a-z]+)/([a-z]+)/one/in/$',views.objects_in_form),
	(r'^choice/([a-z]+)/([a-z]+)/one/$',views.objects_one_form),
	(r'^choice/([a-z]+)/([a-z]+)/$',views.objects_tab_form),
#	(r'^choice/domains/clients/$', views.domains_clients_form),
#	(r'^choice/domains/domains/$', views.domains_domains_form),
#	(r'^choice/domains/dates/$', views.domains_dates_form),
#	(r'^choice/domains/projects/$', views.domains_projects_form),
#	(r'^choice/projects/projects/$', views.projects_projects_form),
#    (r'^choice/sites/sites/$', views.sites_sites_form),
#	(r'^choice/sites/clients/$', views.sites_clients_form),
#	(r'^choice/sites/projects/$', views.sites_projects_form),
#	(r'^choice/sites/domains/$', views.sites_domains_form),
	(r'^choice/sites/cms/$', views.sites_admins_form),
#    (r'^choice/mails/mails/$', views.mails_mails_form),
    #(r'^choice/mails/clients/in/$', views.choice_mails_cli_in_form),

    (r'^admin/', include(admin.site.urls)),
)
