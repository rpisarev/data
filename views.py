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
        'Cms_acc': [u'Аккаунты админки', '/choice/cms_acc'],
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
        [u'Аккаунты админки', '/choice/cms_acc'],
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

# Статические результирующие
def choice_stat_result_abstr_form(request, category, title):
	now, links, menu, notlink = func1(category)
	select_from, name = names_of_classes(category)
	data_choice = {
	'Cms': (lambda cl: [[getattr(cli, name)] for cli in cl.objects.all()])(select_from),
	'Websystem_list': (lambda cl: [[getattr(cli, name)] for cli in cl.objects.all()])(select_from),
	}
	if category == 'Client':
		data_choice[category] = (lambda cl: [[getattr(cli, name)] for cli in cl.objects.filter(enable = 1)])(select_from)
        return render_to_response('form_choice_clients.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
		'titl': [title],
                'data': data_choice[category]
        }
        )

def adminlists_form(request):
	return choice_stat_result_abstr_form(request, 'Cms', u'Админки')

def websyslist_form(request):
	return choice_stat_result_abstr_form(request, 'Websystem_list', u'Веб-системы')

def clients_form(request):
	return choice_stat_result_abstr_form(request, 'Client', u'Клиенты')

# Статические нерезультирующие
def choice_stat_abstr_form(request, category):
	now, links, menu, notlink = func1(category)
	link_list={
        'Project': [[u'Выбрать все проекты', '/choice/projects/projects/'],[u'Выбрать проекты по клиенту', '/choice/projects/clients/in/']],
        'Domain': [[u'Выбрать все домены', '/choice/domains/domains/'],[u'Выбрать домены по клиенту', '/choice/domains/clients/in/'],[u'Выбрать домены по проекту', '/choice/domains/projects/in/'],[u'Выбрать все домены, которые требуется продлить в течение', '/choice/domains/domains/in'],[u'Инфомация о домене', '/choice/domains/domains/one/in']],
        'Site': [[u'Выбрать все сайты', '/choice/sites/sites/'],[u'Выбрать сайты по клиенту', '/choice/sites/clients/in/'],[u'Выбрать сайты по проекту', '/choice/sites/projects/in/'],[u'Выбрать сайты по домену', '/choice/sites/domains/in/'],[u'Выбрать сайты по админке', '/choice/sites/admins/in/'],[u'Инфомация о сайте', '/choice/sites/sites/one/in/']],
        'Mail': [[u'Выбрать все email', '/choice/mails/mails/'],[u'Выбрать email по клиенту', '/choice/mails/clients/in/'],[u'Выбрать email по проекту', '/choice/mails/projects/in/'],[u'Выбрать email по домену', '/choice/mails/domains/in/']],
        'Websystem': [[u'Выбрать все веб-системы', '/choice/websys/websys/'],[u'Выбрать веб-системы по клиенту', '/choice/websys/clients/in/'],[u'Выбрать веб-системы по проекту', '/choice/websys/projects/in/']],
        'Websystem_list': [[u'Список веб-систем', '/choice/websyslist/']],
        'Contact': [[u'Контакты', '/choice/contactes']],
        'Cms_acc': [[u'Аккаунты админки', '/choice/cms_acc']],
        'Cms': [[u'Админки', '/choice/adminlists/']]
	}
        return render_to_response('form_choice_domains.html',
        {
                'current_date': now,
                'choice_get': menu,
		'links': link_list[category],
                'current': links[notlink][0]
        }
	)

def projects_form(request):
        return choice_stat_abstr_form(request, 'Project')

def domains_form(request):
	return choice_stat_abstr_form(request, 'Domain')

def sites_form(request):
        return choice_stat_abstr_form(request, 'Site')

def mails_form(request):
        return choice_stat_abstr_form(request, 'Mail')

def websys_form(request):
        return choice_stat_abstr_form(request, 'Websystem')

def contactes_form(request):
        return choice_stat_abstr_form(request, 'Contact')

def cms_acc_form(request):
        return choice_stat_abstr_form(request, 'Cms_acc')

#Input-формы с комбобоксами

def choice_in_abstr_form(request, data, kriterij, html):
	now, links, menu, notlink = func1(data)
        select_from, name = names_of_classes(kriterij)
        return render_to_response('form_choice_domains_cli_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
		'url': html,
                'combo': [getattr(pro, name) for pro in select_from.objects.all()]
        }
        )

def projects_cli_in_form(request):
	return choice_in_abstr_form(request, 'Project', 'Client', '/choice/projects/clients/')

def domains_cli_in_form(request):
	return choice_in_abstr_form(request, 'Domain', 'Client', '/choice/domains/clients/')
        
def domains_pro_in_form(request):
	return choice_in_abstr_form(request, 'Domain', 'Project', '/choice/domains/projects/')

def domains_dom_one_in_form(request):
	return choice_in_abstr_form(request, 'Domain', 'Domain', '/choice/domains/domains/one/')
        
def sites_cli_in_form(request):
	return choice_in_abstr_form(request, 'Site', 'Client', '/choice/sites/clients/')

def sites_pro_in_form(request):
	return choice_in_abstr_form(request, 'Site', 'Project', '/choice/sites/projects/')      

def sites_dom_in_form(request):
	return choice_in_abstr_form(request, 'Site', 'Domain', '/choice/sites/domains/')

def sites_sites_one_in_form(request):
	return choice_in_abstr_form(request, 'Site', 'Site', '/choice/sites/sites/one/')
        
def sites_adm_in_form(request):
        return choice_in_abstr_form(request, 'Site', 'Cms', '/choice/sites/admins/')

def domains_dom_in_form(request):
        now, links, menu, notlink = func1('Domain')
        return render_to_response('form_choice_domains_dom_in.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[1, u'1 неделя'], [2, u'2 недели'], [4, u'1 месяц'], [8, u'2 месяца']]
        }
        )

# Результирующие формы
# "Всё-формы"

def get_headers_tables(leng, category):
	sh = {
	'Project': [[u'Клиент', u'Проект'],['client', 'name']],
        'Domain': [[u'Клиент', u'Проект', u'Домен', u'Сервис-код', u'Дата окончания'],['project.client', 'project', 'dns_url', 'sercode', 'dns_date']],
        'Site': [[u'Клиент', u'Проект', u'Домен', u'Сайт', u'Тестовый сайт?'],['domain.project.client', 'domain.project', 'domain', 'url', 'test_flag']],
        'Mail': [[u'Клиент', u'Проект',u'Емайл', u'Владелец'],['domain.project.client', 'domain.project', 'login', 'owner_name']],
        'Websystem': [[u'Клиент', u'Проект', u'Название службы'],['project.client', 'project', 'websystems_list.name']],
#        'Websystem_list': [[u'Клиент', u'Проект'],['client', 'name']],
        'Contact': [[u'Клиент', u'Проект', u'Сайт', u'ФИО', u'Должность', u'Телефон', u'Эл. адрес'],['site.domain.project.client', 'site.domain.project', 'site', 'fio', 'function', 'phone1', 'mail1']],
        'Cms_acc': [[u'Клиент', u'Проект', u'Сайт', u'Имя', u'Логин', u'Эл. адрес'],['site.domain.project.client', 'site.domain.project', 'site', 'name', 'login', 'mail']],
#        'Cms': [[u'Клиент', u'Проект'],['client', 'name']]
	}
	md = {
        'Project': [[u'Клиент', u'Проект'],['client', 'name']],
        'Domain': [[u'Клиент', u'Проект', u'Домен', u'Сервис-код', u'Логин к управлению', u'Пароль', u'Дата окончания', u'Владелец'],['project.client', 'project', 'dns_url', 'sercode', 'dns_login', 'dns_pass', 'dns_date', 'dns_owner']],
        'Site': [[u'Клиент', u'Проект', u'Домен', u'Название сайта', u'Сайт', u'Адрес FTP', u'Логин FTP', u'Пароль FTP', u'Адрес статистики', u'Логин к статистике', u'Пароль к статистике', u'Тестовый сайт?', u'Название админки', u'Версия админки'],['domain.project.client', 'domain.project', 'domain', 'title', 'url', 'ftp_url', 'ftp_login', 'ftp_pass', 'stat_url', 'stat_login', 'stat_pass', 'test_flag', 'cms.name', 'cms.version']],
        'Mail': [[u'Клиент', u'Проект',u'Емайл', u'Пароль', u'Владелец'],['domain.project.client', 'domain.project', 'login', 'passwd', 'owner_name']],
        'Websystem': [[u'Клиент', u'Проект', u'Название службы', u'Адрес доступа', u'Тип авторизации', u'Логин', u'Пароль'],['project.client', 'project', 'websystems_list.name', 'websystems_list.url', 'web_login_type', 'web_login_name', 'web_pass']],
#        'Websystem_list': [[u'Клиент', u'Проект'],['client', 'name']],
        'Contact': [[u'Клиент', u'Проект', u'Сайт', u'ФИО', u'Должность', u'Телефон 1', u'Телефон 2', u'Телефон 3', u'Эл. адрес 1', u'Эл. адрес 2'],['site.domain.project.client', 'site.domain.project', 'site', 'fio', 'function', 'phone1', 'phone2', 'phone3', 'mail1', 'mail2']],
        'Cms_acc': [[u'Клиент', u'Проект', u'Сайт', u'Имя', u'Логин', u'Пароль', u'Эл. адрес', u'OpenID'],['site.domain.project.client', 'site.domain.project', 'site', 'name', 'login', 'passwd', 'mail', 'openid']],
 #       'Cms': [[u'Клиент', u'Проект'],['client', 'name']]
        }
	lg = {
	'Project': [[u'Клиент', u'Проект'],['client', 'name']],
        'Domain': [[u'Клиент', u'Проект', u'Домен', u'Сервис-код', u'Логин к управлению', u'Пароль', u'Дата окончания', u'Владелец'],['project.client', 'project', 'dns_url', 'sercode', 'dns_login', 'dns_pass', 'dns_date', 'dns_owner']],
        'Site': [[u'Клиент', u'Проект', u'Домен', u'Название сайта', u'Сайт', u'Адрес FTP', u'Логин FTP', u'Пароль FTP', u'Адрес статистики', u'Логин к статистике', u'Пароль к статистике', u'Тестовый сайт?', u'Название админки', u'Версия админки'],['domain.project.client', 'domain.project', 'domain', 'title', 'url', 'ftp_url', 'ftp_login', 'ftp_pass', 'stat_url', 'stat_login', 'stat_pass', 'test_flag', 'cms.name', 'cms.version']],
        'Mail': [[u'Клиент', u'Проект',u'Емайл', u'Пароль', u'Владелец'],['domain.project.client', 'domain.project', 'login', 'passwd', 'owner_name']],
        'Websystem': [[u'Клиент', u'Проект', u'Название службы', u'Адрес доступа', u'Тип авторизации', u'Логин', u'Пароль'],['project.client', 'project', 'websystems_list.name', 'websystems_list.url', 'web_login_type', 'web_login_name', 'web_pass']],
#        'Websystem_list': [[u'Клиент', u'Проект'],['client', 'name']],
        'Contact': [[u'Клиент', u'Проект', u'Сайт', u'ФИО', u'Должность', u'Телефон 1', u'Телефон 2', u'Телефон 3', u'Эл. адрес 1', u'Эл. адрес 2'],['site.domain.project.client', 'site.domain.project', 'site', 'fio', 'function', 'phone1', 'phone2', 'phone3', 'mail1', 'mail2']],
        'Cms_acc': [[u'Клиент', u'Проект', u'Сайт', u'Имя', u'Логин', u'Пароль', u'Эл. адрес', u'OpenID'],['site.domain.project.client', 'site.domain.project', 'site', 'name', 'login', 'passwd', 'mail', 'openid']],
 #       'Cms': [[u'Клиент', u'Проект'],['client', 'name']]
	}
	head = {
	'short': sh,
	'medium': md,
	'long': lg
	}
	return head[leng][category]

def rgetattr(o, n):
	ns = n.split(".", 1)
	x = getattr(o, ns[0])
	return rgetattr(x, ns[1]) if len(ns)>1 else x

def choice_all_abstr_form(request, length, category):
	now, links, menu, notlink = func1(category)
	select_from, name = names_of_classes(category)
	h = get_headers_tables(length, category)
	return render_to_response('form_choice_domains_domains1.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': h[0],
		'combo':  [[rgetattr(pro, uname) for uname in h[1]] for pro in select_from.objects.all()]
        }
        )

def projects_projects_form(request):
	return choice_all_abstr_form(request, 'long','Project')

def domains_domains_form(request):
	return choice_all_abstr_form(request, 'short','Domain')

def sites_sites_form(request):
	return choice_all_abstr_form(request, 'short','Site')

def mails_mails_form(request):
	return choice_all_abstr_form(request, 'short','Mail')

def websys_websys_form(request):
        return choice_all_abstr_form(request, 'short','Websystem')

def contactes_contactes_form(request):
        return choice_all_abstr_form(request, 'short','Contact')

def cms_acc_cms_acc_form(request):
        return choice_all_abstr_form(request, 'short','Cms_acc')

# Результирующие "избирательные" формы

def path_of_classes(classname1):
        name1= {
        'Project': ['client', ['projects']],
        'Domain': ['project.client', ['projects', 'domains']],
        'Site': ['domain.project.client', ['projects', 'domains', 'sites']],
        'Websystem': ['project.client', ['projects', 'websystems']],
        'Mail': ['domain.project.client', ['projects', 'domains', 'mails']],
        'Contact': ['site.domain.project.client', ['projects', 'domains', 'sites', 'conacts']],
        'Cms_acc': ['site.domain.project.client', ['projects', 'domains', 'sites', 'cms_accnts']]
        }
        return name1[classname1]

def path_of_parent(classname, a):
	name = {
	'Client': 0,
        'Project': 1,
        'Domain': 2,
        'Site': 3,
	}
	return a[name[classname]:]

def recursive_iter(cl, iterator, k = 0):
        if len(iterator) == 0:
                return [cl]
        s = []
        u = getattr(cl, iterator[0]).all()
        for i in u:
                s += recursive_iter(i, iterator[1:], k + 1)
        return s

def choice_choice_abstr_form(request, length, category, kriterij):
	now, links, menu, notlink = func1(category)
        select_from, name = names_of_classes(category)
	class_type = 0
	class_record = 1
	a = get_object_or_404(names_of_classes(kriterij)[class_type], **{names_of_classes(kriterij)[class_record]: request.POST.get('pst')} )
	child_class = path_of_classes(category)
        path_for_parent = path_of_parent(kriterij, child_class[class_record])
        list_of_classes_for_iteration = recursive_iter(a, path_for_parent)
        h = get_headers_tables(length, category)
	return render_to_response('form_choice_domains_domains1.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': h[0],
                'combo':  [[rgetattr(pro, uname) for uname in h[1]] for pro in list_of_classes_for_iteration]
        }
        )


def domains_dates_form(request):
        now, links, menu, notlink = func1('Domain')
        a = get_list_or_404(Domain, dns_date__lt = (datetime.datetime.now() + datetime.timedelta(weeks = int(request.POST.get('pst')))))

        return render_to_response('form_choice_domains_dates.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'data': a,
                'bu': request.POST.get('pst')
        }#,
        #context_instance=RequestContext(request)
        )

def projects_clients_form(request):
	return choice_choice_abstr_form(request, 'medium', 'Project', 'Client')

def domains_clients_form(request):
	return choice_choice_abstr_form(request, 'medium', 'Domain', 'Client')

def domains_projects_form(request):
        return choice_choice_abstr_form(request, 'medium', 'Domain', 'Project')

def domains_domian_one_form(request):
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

def sites_clients_form(request):
	return choice_choice_abstr_form(request, 'medium', 'Site', 'Client')

def sites_projects_form(request):
        return choice_choice_abstr_form(request, 'medium', 'Site', 'Project')

def sites_domains_form(request):
        return choice_choice_abstr_form(request, 'medium', 'Site', 'Domain')

def sites_sites_one_form(request):
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

def sites_admins_form(request):
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

def mails_domains_form(request):
        return choice_choice_abstr_form(request, 'medium', 'Mail', 'Domain')


def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
	dn = datetime.datetime.now()
	return render_to_response('hours_ahead.html', {'next_time': dt, 'hour_offset': offset, 'current_date': dn})
