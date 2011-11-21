from django.conf.urls.defaults import *
from data import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	('^$', views.hello),
	('^time/$', views.current_datetime),
	(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
	(r'^choice/clients/$', views.choice_clients_form),
	(r'^choice/projects/$', views.choice_projects_form),
	(r'^choice/projects/projects/$', views.choice_projects_projects_form),
	(r'^choice/projects/clients/in/$', views.choice_projects_cli_in_form),
    (r'^choice/projects/clients/$', views.choice_projects_clients_form),
	(r'^choice/domains/$', views.choice_domains_form),
	(r'^choice/domains/domains/in/$', views.choice_domains_dom_in_form),
	(r'^choice/domains/clients/in/$', views.choice_domains_cli_in_form),
	(r'^choice/domains/clients/$', views.choice_domains_clients_form),
	(r'^choice/domains/domains/$', views.choice_domains_domains_form),
	(r'^choice/domains/dates/$', views.choice_domains_dates_form),
	(r'^choice/domains/projects/in/$', views.choice_domains_pro_in_form),
	(r'^choice/domains/projects/$', views.choice_domains_projects_form),
	(r'^choice/projects/projects/$', views.choice_projects_projects_form),
	(r'^choice/domains/domains/one/in/$', views.choice_domains_dom_one_in_form),
	(r'^choice/domains/domains/one/$', views.choice_domains_domian_one_form),
    (r'^choice/sites/$', views.choice_sites_form),
    (r'^choice/sites/sites/$', views.choice_sites_sites_form),
    (r'^choice/sites/clients/in/$', views.choice_sites_cli_in_form),
	(r'^choice/sites/clients/$', views.choice_sites_clients_form),
    (r'^choice/sites/projects/in/$', views.choice_sites_pro_in_form),
	(r'^choice/sites/projects/$', views.choice_sites_projects_form),
    (r'^choice/sites/domains/in/$', views.choice_sites_dom_in_form),
	(r'^choice/sites/domains/$', views.choice_sites_domains_form),
    (r'^choice/sites/admins/in/$', views.choice_sites_adm_in_form),
	(r'^choice/sites/admins/$', views.choice_sites_admins_form),
    (r'^choice/sites/sites/one/in/$', views.choice_sites_sites_one_in_form),
    (r'^choice/sites/sites/one/$', views.choice_sites_sites_one_form),
    (r'^choice/mails/$', views.choice_mails_form),
    (r'^choice/mails/mails/$', views.choice_mails_mails_form),
    #(r'^choice/mails/clients/in/$', views.choice_mails_cli_in_form),
	#(r'^choice/mails/clients/$', views.choice_mails_clients_form),
    #(r'^choice/mails/projects/in/$', views.choice_mails_pro_in_form),
	#(r'^choice/mails/projects/$', views.choice_mails_projects_form),
    #(r'^choice/mails/domains/in/$', views.choice_mails_dom_in_form),
	#(r'^choice/mails/domains/$', views.choice_mails_domains_form),
    #(r'^choice/websys/$', views.choice_websys_form),
    #(r'^choice/websyslist/$', views.choice_websyslist_form),
    #(r'^choice/adminlists/$', views.choice_adminlists_form),


    # Example:
    # (r'^data/', include('data.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
