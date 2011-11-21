from django.db import models

# Create your models here.

class Client(models.Model):
	name = models.CharField(max_length=255)
	enable = models.PositiveIntegerField()
	
	def __unicode__(self):
		return self.name
	
	class Meta:
		ordering = ["name"]
	
class Project(models.Model):
	client = models.ForeignKey(Client, related_name='projects')
	name = models.CharField(max_length=255)
	
	def __unicode__(self):
                return self.name
        
        class Meta:
                ordering = ["name"]
	
class Domain(models.Model):
	project = models.ForeignKey(Project, related_name='domains')
	dns_url = models.URLField()
	dns_login = models.CharField(max_length=255)
	dns_pass = models.CharField(max_length=255)
	dns_date = models.DateField()
	dns_owner = models.CharField(blank = True, max_length=255)
	enable = models.PositiveIntegerField()
	sercode = models.CharField(blank = True, max_length=25)

	def __unicode__(self):
                return self.dns_url
        
        class Meta:
                ordering = ["dns_url", "dns_date"]
	
class Websystem_list(models.Model):
        name = models.CharField(max_length=255)
        url = models.URLField()

	def __unicode__(self):
                return self.name
        
        class Meta:
                ordering = ["name"]
	
class Websystem(models.Model):
	websystems_list = models.ForeignKey(Websystem_list, related_name='ws_lists')
	project = models.ForeignKey(Project, related_name='websystems')
	web_login_type = models.CharField(max_length=255, blank=True)
	web_login_name = models.CharField(max_length=255)
	web_pass = models.CharField(max_length=255)
	
	def __unicode__(self):
                return self.web_login_name
        
        class Meta:
                ordering = ["web_login_name"]
	
class Cms(models.Model):
        name = models.CharField(max_length=255)
        codename = models.CharField(max_length=255, blank=True)
        version = models.CharField(max_length=255)

	def __unicode__(self):
                return self.name

        class Meta:
                ordering = ["name"]
	
class Site(models.Model):
	domain = models.ForeignKey(Domain, related_name='sites')
	title = models.CharField(max_length=255, blank=True)
	url = models.URLField()
	test_flag = models.PositiveIntegerField()
	ftp_login = models.CharField(max_length=255)
	ftp_pass = models.CharField(max_length=255)
	ftp_url = models.URLField(blank=True)
	cms = models.ForeignKey(Cms, related_name='sites_cms')
	stat_url = models.URLField(blank = True)
	stat_login = models.CharField(blank=True, max_length=255)
	stat_pass = models.CharField(blank=True, max_length=255)
	enable = models.PositiveIntegerField()

	def __unicode__(self):
                return self.url

        class Meta:
                ordering = ["url"]
	
class Mail(models.Model):
    domain = models.ForeignKey(Domain, related_name='mails')
    login = models.CharField(max_length=255)
    passwd = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)

    def email(self):
        return u"%s@%s" % (self.login, self.domain.dns_url[7:-1])

    def fullemail(self):
        return u"%s <%s@%s>" % (self.owner_name, self.login, self.domain.dns_url[7:-1])

	def __unicode__(self):
                return self.owner_name

        class Meta:
                ordering = ["owner_name"]
	
class Contact(models.Model):
	site = models.ForeignKey(Site, related_name='conacts')
	function = models.CharField(max_length=255)
	fio = models.CharField(max_length=255)
	phone1 = models.CharField(max_length=255)
	phone2 = models.CharField(max_length=255, blank=True)
	phone3 = models.CharField(max_length=255, blank=True)
	mail1 = models.EmailField()
	mail2 = models.EmailField(blank=True)

	def __unicode__(self):
                return self.fio

        class Meta:
                ordering = ["fio"]
	
class Cms_acc(models.Model):
        site = models.ForeignKey(Site, related_name='cms_accnts')
        login = models.CharField(max_length=255)
        passwd = models.CharField(max_length=255)
        name = models.CharField(max_length=255)
        mail = models.EmailField()
        openid = models.URLField(blank=True)

	def __unicode__(self):
                return self.name

        class Meta:
                ordering = ["name"]
