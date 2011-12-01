from django.conf.urls.defaults import *
from data import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	('^$', views.hello),
	(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
	(r'^choice/clients/$', views.clients_form),
	(r'^choice/projects/$', views.projects_form),
	(r'^choice/projects/projects/$', views.projects_projects_form),
    (r'^choice/projects/clients/$', views.projects_clients_form),
	(r'^choice/domains/$', views.domains_form),
	(r'^choice/domains/dates/in/$', views.domains_dom_in_form),
	(r'^choice/([a-z]+)/([a-z]+)/in/$',views.objects_in_form),
	(r'^choice/([a-z]+)/([a-z]+)/one/in/$',views.objects_in_form),
	(r'^choice/domains/clients/$', views.domains_clients_form),
	(r'^choice/domains/domains/$', views.domains_domains_form),
	(r'^choice/domains/dates/$', views.domains_dates_form),
	(r'^choice/domains/projects/$', views.domains_projects_form),
	(r'^choice/projects/projects/$', views.projects_projects_form),
	(r'^choice/domains/domains/one/$', views.domains_domian_one_form),
    (r'^choice/sites/$', views.sites_form),
    (r'^choice/sites/sites/$', views.sites_sites_form),
	(r'^choice/sites/clients/$', views.sites_clients_form),
	(r'^choice/sites/projects/$', views.sites_projects_form),
	(r'^choice/sites/domains/$', views.sites_domains_form),
	(r'^choice/sites/admins/$', views.sites_admins_form),
    (r'^choice/sites/sites/one/$', views.sites_sites_one_form),
    (r'^choice/mails/$', views.mails_form),
    (r'^choice/mails/mails/$', views.mails_mails_form),
    #(r'^choice/mails/clients/in/$', views.choice_mails_cli_in_form),
	#(r'^choice/mails/clients/$', views.choice_mails_clients_form),
    #(r'^choice/mails/projects/in/$', views.choice_mails_pro_in_form),
	#(r'^choice/mails/projects/$', views.choice_mails_projects_form),
    #(r'^choice/mails/domains/in/$', views.choice_mails_dom_in_form),
	#(r'^choice/mails/domains/$', views.choice_mails_domains_form),
    (r'^choice/websys/$', views.websys_form),
    (r'^choice/websyslist/$', views.websyslist_form),
    (r'^choice/adminlists/$', views.adminlists_form),
    (r'^choice/contactes/$', views.contactes_form),
	(r'^choice/cms_acc/$', views.cms_acc_form),


    # Example:
    # (r'^data/', include('data.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
