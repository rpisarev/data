# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template.loader import get_template
from django import template
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, get_list_or_404
from data.aplic.models import *
from django.template.context import RequestContext
import datetime, unicodedata
import settings

def hello(request):
	return HttpResponse('<p>1</p>')

def func1(current):
	now = datetime.datetime.now()
        links = {
	'Client': [u'Клиенты', '/choice/clients/'],
        'Project': [u'Проекты', '/choice/projects/'],
        'Domain': [u'Домены', '/choice/domains/'],
        'Site': [u'Сайты', '/choice/sites/'],
        'Mail': [u'Почта', '/choice/mails/'],
        'Websystem': [u'Веб-системы', '/choice/websys/'],
        'Websystem_list': [u'Список веб-систем', '/choice/websyslist/'],
        'Contact': [u'Контакты', '/choice/contactes'],
        'Cms_acc': [u'Аккаунты админки', 'http://www.mid.ua/'],
        'Cms': [u'Админки', '/choice/adminlists/']
	}
	menu = [ # Убрать костыль
        [u'Клиенты', '/choice/clients/'],
        [u'Проекты', '/choice/projects/'],
        [u'Домены', '/choice/domains/'],
        [u'Сайты', '/choice/sites/'],
        [u'Почта', '/choice/mails/'],
        [u'Веб-системы', '/choice/websys/'],
        [u'Список веб-систем', '/choice/websyslist/'],
        [u'Контакты', '/choice/contactes'],
        [u'Аккаунты админки', 'http://www.mid.ua/'],
        [u'Админки', '/choice/adminlists/']
        ]
	return (now, links, menu, current)

def names_of_classes(classname):
	name = {
	'Client': [Client, 'name'],
	'Project': [Project,'name'],
	'Domain': [Domain, 'dns_url'],
	'Site': [Site, 'url'],
	'Websystem_list': [Websystem_list, 'name'],
	'Websystem': [Websystem_list, 'web_login_name'],
	'Cms': [Cms, 'name'],
	'Mail': [Mail, 'login'],
	'Contact': [Contact, 'fio'],
	'Cms_acc': [Cms_acc, 'login']
	}
	return name[classname]

def headers_tab(what):
	list_head = {
	'cl_cl': [u'Клиент'],
	'pr_pr': [u'Клиент', u'Проект'],
	'pr_cl': [u'Проект'],
	'dm_cl': [u'Проект', u'Домены', u'Дата окончания'],
	'dm': [u'Клиент', u'Проект', u'Домен', u'Сервис-код', u'Дата окончания'],
	'dm_1': [u'Клиент', u'Проект', u'Домены', u'Сервис-код', u'Логин к управлению', u'Пароль', u'Дата окончания', u'Владелец'],
	'st': [u'Клиент', u'Проект', u'Домен', u'Адрес сайта', u'Тестовый сайт?'],
    'st_ad': [u'Клиент', u'Проект', u'Домен', u'Адрес сайта', u'Тип админкм', u'Тестовый сайт?'],
    'st_cl': [u'Проект', u'Домен', u'Адрес сайта', u'Тестовый сайт?'],
	'ml_cl': [u'Полное имя', u'Электронный адрес'],
    'ml_cli': [u'Клиент', u'Проект', u'Полное имя', u'Электронный адрес'],
	'ws_cl': [],
	'ws_list': [u'Тип веб-системы', u'URL веб-системы'],
	'cn_cl': [],
	'ad_cl': [],
	'ad_list': [u'Название админки', u'Кодовое название', u'Версия']
	}
	return list_head[what]

# Статические формы
def choice_clients_form(request):
	now, links, menu, notlink = func1('Client')
	return render_to_response('form_choice_clients.html',
	{
		'current_date': now,
		'choice_get': menu,
		'current': links[notlink][0], 
		'headers': headers_tab('cl_cl'),
		'data': [[cli.name] for cli in Client.objects.filter(enable = 1)]
	}
	)

def choice_projects_form(request):
        now, links, menu, notlink = func1('Project')
        return render_to_response('form_choice_projects.html',
	{
		'current_date': now,
		'choice_get': menu,
		'current': links[notlink][0]
	}
	)

def choice_domains_form(request):
        now, links, menu, notlink = func1('Domain')
        return render_to_response('form_choice_domains.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0]
        }
        )

def choice_sites_form(request):
        now, links, menu, notlink = func1('Site')
        return render_to_response('form_choice_sites.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0]
        }
        )

#Input-формы с комбобоксами

#def choice_in_abstr_form(request,)

def choice_projects_cli_in_form(request):
        now, links, menu, notlink = func1('Project')
	select_from, name = names_of_classes('Client')
        return render_to_response('form_choice_projects_cli_in.html',
	{
		'current_date': now,
		'choice_get': menu,
		'current': links[notlink][0],
		'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
	}
	)

def choice_domains_cli_in_form(request):
        now, links, menu, notlink = func1('Domain')
	select_from, name = names_of_classes('Client')
        return render_to_response('form_choice_domains_cli_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
        }
        )

def choice_domains_pro_in_form(request):
        now, links, menu, notlink = func1('Domain')
	select_from, name = names_of_classes('Project')
        return render_to_response('form_choice_domains_pro_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
        }
        )

def choice_domains_dom_one_in_form(request):
        now, links, menu, notlink = func1('Domain')
	select_from, name = names_of_classes('Domain')
        return render_to_response('form_choice_domains_domain_one_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
        }
        )

def choice_domains_dom_in_form(request):
        now, links, menu, notlink = func1('Domain')
        return render_to_response('form_choice_domains_dom_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[1, u'1 неделя'], [2, u'2 недели'], [4, u'1 месяц'], [8, u'2 месяца']]
        }
        )

def choice_sites_cli_in_form(request):
        now, links, menu, notlink = func1('Site')
	select_from, name = names_of_classes('Client')
        return render_to_response('form_choice_sites_cli_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
        }
        )
def choice_sites_pro_in_form(request):
        now, links, menu, notlink = func1('Site')
	select_from, name = names_of_classes('Project')
        return render_to_response('form_choice_sites_pro_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
        }
        )

def choice_sites_dom_in_form(request):
        now, links, menu, notlink = func1('Site')
	select_from, name = names_of_classes('Domain')
        return render_to_response('form_choice_sites_dom_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
        }
        )

def choice_sites_sites_one_in_form(request):
        now, links, menu, notlink = func1('Site')
	select_from, name = names_of_classes('Site')
        return render_to_response('form_choice_sites_sites_one_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
        }
        )

def choice_sites_adm_in_form(request):
        now, links, menu, notlink = func1('Site')
	select_from, name = names_of_classes('Cms')
        return render_to_response('form_choice_sites_adm_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[getattr(pro,name), getattr(pro,name)] for pro in select_from.objects.all()]
        }
        )



# Результирующие формы
def choice_projects_projects_form(request):
        now, links, menu, notlink = func1('Project')
        return render_to_response('form_choice_projects_projects.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('pr_pr'),
                'data': Project.objects.all()
        }
        )

def choice_projects_clients_form(request):
        now, links, menu, notlink = func1('Project')
	a = get_object_or_404(Client, name=request.POST.get('pst'))

	return render_to_response('form_choice_projects_clients.html', 
	{
		'current_date': now, 
		'choice_get': menu, 
		'current': links[notlink][0],
		'headers': headers_tab('pr_cl'),
		'data': a, 
		'bu': request.POST.get('pst')
	}#,
	#context_instance=RequestContext(request)
	)

def choice_domains_clients_form(request):
        now, links, menu, notlink = func1('Domain')
        a = get_object_or_404(Client, name=request.POST.get('pst'))

        return render_to_response('form_choice_domains_clients.html', 
        {
                'current_date': now, 
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('dm_cl'),
                'data': a, 
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def choice_domains_domains_form(request):
        now, links, menu, notlink = func1('Domain')
        return render_to_response('form_choice_domains_domains.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('dm'),
                #'data': Domain.objects.all()
		'data': Client.objects.all()
        }
        )

def choice_domains_projects_form(request):
        now, links, menu, notlink = func1('Domain')
        a = get_object_or_404(Project, name=request.POST.get('pst'))

        return render_to_response('form_choice_domains_projects.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('dm_cl'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )


def choice_domains_dates_form(request):
        now, links, menu, notlink = func1('Domain')
        a = get_list_or_404(Domain, dns_date__lt = (datetime.datetime.now() + datetime.timedelta(weeks = int(request.POST.get('pst')))))

        return render_to_response('form_choice_domains_dates.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('dm'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def choice_domains_domian_one_form(request):
        now, links, menu, notlink = func1('Domain')
        a = get_object_or_404(Domain, dns_url = request.POST.get('pst'))

        return render_to_response('form_choice_domains_domain_one.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('dm_1'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def choice_sites_sites_form(request):
        now, links, menu, notlink = func1('Site')
        return render_to_response('form_choice_sites_sites.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('st'),
		        'data': Client.objects.all()
        }
        )

def choice_sites_clients_form(request):
        now, links, menu, notlink = func1('Site')
        a = get_object_or_404(Client, name=request.POST.get('pst'))

        return render_to_response('form_choice_sites_clients.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('st_cl'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def choice_sites_projects_form(request):
        now, links, menu, notlink = func1('Site')
        a = get_object_or_404(Project, name=request.POST.get('pst'))

        return render_to_response('form_choice_sites_projects.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('st_cl'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )


def choice_sites_domains_form(request):
        now, links, menu, notlink = func1('Site')
        a = get_object_or_404(Domain, dns_url = request.POST.get('pst'))

        return render_to_response('form_choice_sites_domains.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('st'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def choice_sites_sites_one_form(request):
        now, links, menu, notlink = func1('Site')
        a = get_object_or_404(Site, url = request.POST.get('pst'))

        return render_to_response('form_choice_sites_sites_one.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('st'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def choice_sites_admins_form(request):
        now, links, menu, notlink = func1('Site')
        a = get_object_or_404(Cms, name = request.POST.get('pst'))

        return render_to_response('form_choice_sites_adm.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('st'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def choice_mails_form(request):
        now, links, menu, notlink = func1('Mail')
        return render_to_response('form_choice_mails.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0]
        }
        )

def choice_websys_form(request):
        now, links, menu, notlink = func1('Websystem_list')
        return render_to_response('form_choice_websys.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0]
        }
        )

def choice_websyslist_form(request):
        now, links, menu, notlink = func1('Websystem_list')
        return render_to_response('form_choice_websyslist.html',
	    {
		        'current_date': now,
		        'choice_get': menu,
		        'current': links[notlink][0],
		        'headers': headers_tab('ws_list'),
		        'data': [[pro.name, pro.url] for pro in Websystem_list.objects.all()]
	    }
	    )

def choice_adminlists_form(request):
        now, links, menu, notlink = func1('Cms')
        return render_to_response('form_choice_adminlists.html',
	    {
		        'current_date': now,
		        'choice_get': menu,
		        'current': links[notlink][0],
		        'headers': headers_tab('ad_list'),
		        'data': [[pro.name, pro.codename, pro.version] for pro in Cms.objects.all()]
	    }
	    )

def choice_mails_mails_form(request):
        now, links, menu, notlink = func1('Mail')
        return render_to_response('form_choice_mails_mails.html',
	    {
		        'current_date': now,
		        'choice_get': menu,
		        'current': links[notlink][0],
		        'headers': headers_tab('ml_cl'),
		        'data': [[pro.fullemail(), pro.email()] for pro in Mail.objects.all()]
	    }
	    )

def choice_mails_domains_form(request):
        now, links, menu, notlink = func1('Mail')
        a = get_object_or_404(Domain, dns_url = request.POST.get('pst'))

        return render_to_response('form_choice_mails_domains.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': headers_tab('ml_cli'),
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def current_datetime(request):
	now = datetime.datetime.now()
	return render_to_response('current_datetime.html', {'current_date': now})

#def what_form(request):
#	now, links, nl = func1(-1)
#        return render_to_response('form_what.html', {'current_date': now, 'choice_get': links})

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
	dn = datetime.datetime.now()
	return render_to_response('hours_ahead.html', {'next_time': dt, 'hour_offset': offset, 'current_date': dn})
