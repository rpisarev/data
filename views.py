# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django import template
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, get_list_or_404
from data.aplic.models import *
from django.template.context import RequestContext
import datetime, unicodedata
import settings

def all_classes():
	return ['clients', 'projects', 'domains', 'sites', 'mails', 'websys', 'websyslist', 'contactes', 'cms', 'cmsacc']

def all_one_classes():
	return ['domains', 'sites', 'contactes', 'cmsacc']

def all_in_classes():
	return ['projects', 'domains', 'sites', 'mails', 'websys', 'contactes', 'cmsacc']

def all_krit_in_classes():
        return ['clients', 'projects', 'domains', 'sites', 'mails', 'websys', 'websyslist', 'contactes', 'cms', 'cmsacc']

def hello(request):
#	raise Http404() 
	return HttpResponse('<p>1</p>')
def flinks():
	return {
        'clients': [u'Клиенты', '/choice/clients/'],
        'projects': [u'Проекты', '/choice/projects/'],
        'domains': [u'Домены', '/choice/domains/'],
        'sites': [u'Сайты', '/choice/sites/'],
        'mails': [u'Почта', '/choice/mails/'],
        'websys': [u'Веб-системы', '/choice/websys/'],
        'websyslist': [u'Список веб-систем', '/choice/websyslist/'],
        'contactes': [u'Контакты', '/choice/contactes'],
        'cmsacc': [u'Аккаунты админки', '/choice/cmsacc'],
        'cms': [u'Админки', '/choice/cms/']
        }
def fmenu():
	return [
        [u'Клиенты', '/choice/clients/'],
        [u'Проекты', '/choice/projects/'],
        [u'Домены', '/choice/domains/'],
        [u'Сайты', '/choice/sites/'],
        [u'Почта', '/choice/mails/'],
        [u'Веб-системы', '/choice/websys/'],
        [u'Список веб-систем', '/choice/websyslist/'],
        [u'Контакты', '/choice/contactes'],
        [u'Аккаунты админки', '/choice/cmsacc'],
        [u'Админки', '/choice/cms/']
        ]

def names_of_classes(classname):
	return {
        'clients': [Client, 'name'],
        'projects': [Project,'name'],
        'domains': [Domain, 'dns_url'],
        'sites': [Site, 'url'],
        'websyslist': [Websystem_list, 'name'],
        'websys': [Websystem, 'web_login_name'],
        'cms': [Cms, 'name'],
        'mails': [Mail, 'login'],
        'contactes': [Contact, 'fio'],
        'cmsacc': [Cms_acc, 'login']
        }[classname]

# Статические формы

# Статические результирующие
def choice_stat_result_abstr_form(request, category):
	now, links, menu, notlink = datetime.datetime.now(), flinks(), fmenu(), category
	select_from, name = names_of_classes(category)
	title = {
	'cms': u'Админки',
	'websyslist': u'Веб-системы',
	'clients': u'Клиенты'
	} [category]
	data_choice = {
	'cms': (lambda cl: [[getattr(cli, name)] for cli in cl.objects.all()])(select_from),
	'websyslist': (lambda cl: [[getattr(cli, name)] for cli in cl.objects.all()])(select_from),
	}
	if category == 'clients':
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

def choice_stat_abstr_form(request, category):
        now, links, menu, notlink = datetime.datetime.now(), flinks(), fmenu(), category
        link_list={
        'projects': [[u'Выбрать все проекты', '/choice/projects/projects/'],[u'Выбрать проекты по клиенту', '/choice/projects/clients/in/']],
        'domains': [[u'Выбрать все домены', '/choice/domains/domains/'],[u'Выбрать домены по клиенту', '/choice/domains/clients/in/'],[u'Выбрать домены по проекту', '/choice/domains/projects/in/'],[u'Выбрать все домены, которые требуется продлить в течение', '/choice/domains/dates/in'],[u'Инфомация о домене', '/choice/domains/domains/one/in']],
        'sites': [[u'Выбрать все сайты', '/choice/sites/sites/'],[u'Выбрать сайты по клиенту', '/choice/sites/clients/in/'],[u'Выбрать сайты по проекту', '/choice/sites/projects/in/'],[u'Выбрать сайты по домену', '/choice/sites/domains/in/'],[u'Выбрать сайты по админке', '/choice/sites/cms/in/'],[u'Инфомация о сайте', '/choice/sites/sites/one/in/']],
        'mails': [[u'Выбрать все email', '/choice/mails/mails/'],[u'Выбрать email по клиенту', '/choice/mails/clients/in/'],[u'Выбрать email по проекту', '/choice/mails/projects/in/'],[u'Выбрать email по домену', '/choice/mails/domains/in/']],
        'websys': [[u'Выбрать все веб-системы', '/choice/websys/websys/'],[u'Выбрать веб-системы по клиенту', '/choice/websys/clients/in/'],[u'Выбрать веб-системы по проекту', '/choice/websys/projects/in/'], [u'Выбрать веб-системы по типу', '/choice/websys/websyslist/in/']],
        'contactes': [[u'Контакты', '/choice/contactes']],
        'cmsacc': [[u'Аккаунты админки', '/choice/cmsacc']],
        }
        return render_to_response('form_choice_domains.html',
        {
                'current_date': now,
                'choice_get': menu,
                'links': link_list[category],
                'current': links[notlink][0]
        }
        )

def objects_form(request, category):
	if category in ['cms', 'websyslist', 'clients']:
		return choice_stat_result_abstr_form(request, category)
	if category in ['projects', 'domains', 'sites', 'mails', 'websys', 'contactes', 'cmsacc']:
		return choice_stat_abstr_form(request, category)
	raise Http404()

#Input-формы с комбобоксами

def choice_in_abstr_form(request, data, kriterij, html):
	now, links, menu, notlink = datetime.datetime.now(), flinks(), fmenu(), data
        try:
		select_from, name = names_of_classes(kriterij)
	except ValueError:
                raise Http404()
        return render_to_response('form_choice_domains_cli_in.html',
        {
               	'current_date': now,
               	'choice_get': menu,
               	'current': links[notlink][0],
		'url': html,
               	'combo': [getattr(pro, name) for pro in select_from.objects.all()]
        }
        )

def objects_in_form(request, category, kriterij):
	if kriterij in ['dates'] and category == 'domains':
		now, links, menu, notlink = datetime.datetime.now(), flinks(), fmenu(), 'domains'
		return render_to_response('form_choice_domains_dom_in.html',
	        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'combo': [[1, u'1 неделя'], [2, u'2 недели'], [4, u'1 месяц'], [8, u'2 месяца']]
        	}
        	)
	elif kriterij in all_krit_in_classes() and category in all_in_classes():
		return choice_in_abstr_form(request, category, kriterij, request.META.get('REQUEST_URI')[:-3])
	else:
		raise Http404()

# Результирующие формы
# "Всё-формы"

def get_headers_tables(leng, category):
	sh = {
	'projects': [[u'Клиент', u'Проект'],['client', 'name']],
        'domains': [[u'Клиент', u'Проект', u'Домен', u'Сервис-код', u'Дата окончания'],['project.client', 'project', 'dns_url', 'sercode', 'dns_date']],
        'sites': [[u'Клиент', u'Проект', u'Домен', u'Сайт', u'Тестовый сайт?'],['domain.project.client', 'domain.project', 'domain', 'url', 'test_flag']],
        'mails': [[u'Клиент', u'Проект',u'Емайл', u'Владелец'],['domain.project.client', 'domain.project', 'login', 'owner_name']],
        'websys': [[u'Клиент', u'Проект', u'Название службы'],['project.client', 'project', 'websystems_list.name']],
#        'Websystem_list': [[u'Клиент', u'Проект'],['client', 'name']],
        'contactes': [[u'Клиент', u'Проект', u'Сайт', u'ФИО', u'Должность', u'Телефон', u'Эл. адрес'],['site.domain.project.client', 'site.domain.project', 'site', 'fio', 'function', 'phone1', 'mail1']],
        'cmsacc': [[u'Клиент', u'Проект', u'Сайт', u'Имя', u'Логин', u'Эл. адрес'],['site.domain.project.client', 'site.domain.project', 'site', 'name', 'login', 'mail']],
#        'Cms': [[u'Клиент', u'Проект'],['client', 'name']]
	}
	md = {
        'projects': [[u'Клиент', u'Проект'],['client', 'name']],
        'domains': [[u'Клиент', u'Проект', u'Домен', u'Сервис-код', u'Логин к управлению', u'Пароль', u'Дата окончания', u'Владелец'],['project.client', 'project', 'dns_url', 'sercode', 'dns_login', 'dns_pass', 'dns_date', 'dns_owner']],
        'sites': [[u'Клиент', u'Проект', u'Домен', u'Название сайта', u'Сайт', u'Адрес FTP', u'Логин FTP', u'Пароль FTP', u'Адрес статистики', u'Логин к статистике', u'Пароль к статистике', u'Тестовый сайт?', u'Название админки', u'Версия админки'],['domain.project.client', 'domain.project', 'domain', 'title', 'url', 'ftp_url', 'ftp_login', 'ftp_pass', 'stat_url', 'stat_login', 'stat_pass', 'test_flag', 'cms.name', 'cms.version']],
        'mails': [[u'Клиент', u'Проект',u'Емайл', u'Пароль', u'Владелец'],['domain.project.client', 'domain.project', 'login', 'passwd', 'owner_name']],
        'websys': [[u'Клиент', u'Проект', u'Название службы', u'Адрес доступа', u'Тип авторизации', u'Логин', u'Пароль'],['project.client', 'project', 'websystems_list.name', 'websystems_list.url', 'web_login_type', 'web_login_name', 'web_pass']],
#        'Websystem_list': [[u'Клиент', u'Проект'],['client', 'name']],
        'contactes': [[u'Клиент', u'Проект', u'Сайт', u'ФИО', u'Должность', u'Телефон 1', u'Телефон 2', u'Телефон 3', u'Эл. адрес 1', u'Эл. адрес 2'],['site.domain.project.client', 'site.domain.project', 'site', 'fio', 'function', 'phone1', 'phone2', 'phone3', 'mail1', 'mail2']],
        'cmsacc': [[u'Клиент', u'Проект', u'Сайт', u'Имя', u'Логин', u'Пароль', u'Эл. адрес', u'OpenID'],['site.domain.project.client', 'site.domain.project', 'site', 'name', 'login', 'passwd', 'mail', 'openid']],
 #       'Cms': [[u'Клиент', u'Проект'],['client', 'name']]
        }
	lg = {
	'projects': [[u'Клиент', u'Проект'],['client', 'name']],
        'domains': [[u'Клиент', u'Проект', u'Домен', u'Сервис-код', u'Логин к управлению', u'Пароль', u'Дата окончания', u'Владелец'],['project.client', 'project', 'dns_url', 'sercode', 'dns_login', 'dns_pass', 'dns_date', 'dns_owner']],
        'sites': [[u'Клиент', u'Проект', u'Домен', u'Название сайта', u'Сайт', u'Адрес FTP', u'Логин FTP', u'Пароль FTP', u'Адрес статистики', u'Логин к статистике', u'Пароль к статистике', u'Тестовый сайт?', u'Название админки', u'Версия админки'],['domain.project.client', 'domain.project', 'domain', 'title', 'url', 'ftp_url', 'ftp_login', 'ftp_pass', 'stat_url', 'stat_login', 'stat_pass', 'test_flag', 'cms.name', 'cms.version']],
        'mails': [[u'Клиент', u'Проект',u'Емайл', u'Пароль', u'Владелец'],['domain.project.client', 'domain.project', 'login', 'passwd', 'owner_name']],
        'websys': [[u'Клиент', u'Проект', u'Название службы', u'Адрес доступа', u'Тип авторизации', u'Логин', u'Пароль'],['project.client', 'project', 'websystems_list.name', 'websystems_list.url', 'web_login_type', 'web_login_name', 'web_pass']],
#        'Websystem_list': [[u'Клиент', u'Проект'],['client', 'name']],
        'contactes': [[u'Клиент', u'Проект', u'Сайт', u'ФИО', u'Должность', u'Телефон 1', u'Телефон 2', u'Телефон 3', u'Эл. адрес 1', u'Эл. адрес 2'],['site.domain.project.client', 'site.domain.project', 'site', 'fio', 'function', 'phone1', 'phone2', 'phone3', 'mail1', 'mail2']],
        'cmsacc': [[u'Клиент', u'Проект', u'Сайт', u'Имя', u'Логин', u'Пароль', u'Эл. адрес', u'OpenID'],['site.domain.project.client', 'site.domain.project', 'site', 'name', 'login', 'passwd', 'mail', 'openid']],
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
	now, links, menu, notlink = datetime.datetime.now(), flinks(), fmenu(), category
	select_from, name = names_of_classes(category)
	hdr = get_headers_tables(length, category)
	return render_to_response('form_choice_domains_domains1.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': hdr[0],
		'combo':  [[rgetattr(pro, uname) for uname in hdr[1]] for pro in select_from.objects.all()]
        }
        )
	
def objects_tab_form(request, category, kriterij):
	if category in all_in_classes() and kriterij in (all_classes() + ['dates']):
		if kriterij in ['dates'] and category == 'domains':
			now, links, menu, notlink = datetime.datetime.now(), flinks(), fmenu(), 'domains'
        		a = get_list_or_404(Domain, dns_date__lt = (datetime.datetime.now() + datetime.timedelta(weeks = int(request.POST.get('pst')))))

        		return render_to_response('form_choice_domains_dates.html',
        		{
                		'current_date': now,
                		'choice_get': menu,
                		'current': links[notlink][0],
                		'data': a,
                		'headers': get_headers_tables('short', category)[0],
                		'bu': request.POST.get('pst')
        		}#,
        		#context_instance=RequestContext(request)
        		)
		elif category == kriterij:
			return choice_all_abstr_form(request, 'short', category)
		else:
			return choice_choice_abstr_form(request, 'medium', category, kriterij)
	else:
		raise Http404()

# Результирующие "избирательные" формы

def path_of_classes(classname):
	return {
        'projects': ['client', ['projects']],
        'domains': ['project.client', ['projects', 'domains']],
        'sites': ['domain.project.client', ['projects', 'domains', 'sites']],
        'websys': ['project.client', ['projects', 'websyslist']],
        'mails': ['domain.project.client', ['projects', 'domains', 'mails']],
        'contactes': ['site.domain.project.client', ['projects', 'domains', 'sites', 'conacts']],
        'cmsacc': ['site.domain.project.client', ['projects', 'domains', 'sites', 'cms_accnts']]
        }[classname]

def path_of_parent(classname, a):
	name = {
	'clients': 0,
        'projects': 1,
        'domains': 2,
        'sites': 3,
	'cmsacc': 3,
	'websys':2,
	}
	return a[name[classname]:]

def recursive_iter(cl, iterator):
        if len(iterator) == 0:
                return [cl]
        res = []
        for i in getattr(cl, iterator[0]).all():
                res += recursive_iter(i, iterator[1:])
        return res

def choice_choice_abstr_form(request, length, category, kriterij):
	now, links, menu, notlink = datetime.datetime.now(), flinks(), fmenu(), category
        select_from, name = names_of_classes(category)
	class_type = 0
	class_record = 1
	obj = get_object_or_404(names_of_classes(kriterij)[class_type], **{names_of_classes(kriterij)[class_record]: request.POST.get('pst')} )
	child_class = path_of_classes(category)
	if kriterij == 'cms':
		list_of_classes_for_iteration = obj.sites_cms.all()
	elif kriterij == 'websyslist':
		list_of_classes_for_iteration = obj.ws_lists.all()
	else:
        	path_for_parent = path_of_parent(kriterij, child_class[class_record])
        	list_of_classes_for_iteration = recursive_iter(obj, path_for_parent)
        hdr = get_headers_tables(length, category)
	return render_to_response('form_choice_domains_domains1.html',
        {
                'current_date': now,
                'choice_get': menu,
                'current': links[notlink][0],
                'headers': hdr[0],
                'combo':  [[rgetattr(pro, uname) for uname in hdr[1]] for pro in list_of_classes_for_iteration]
        }
        )

def objects_one_form(request, category, kriterij):
	if kriterij in all_one_classes() and category in all_one_classes():
		if category == kriterij:
			return choice_choice_abstr_form(request, 'long', category, category)
		else:
			raise Http404()
	else:
		raise Http404()

def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours = offset)
	dn = datetime.datetime.now()
	return render_to_response('hours_ahead.html', {'next_time': dt, 'hour_offset': offset, 'current_date': dn})
