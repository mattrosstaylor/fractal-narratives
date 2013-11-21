from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os

class Story(models.Model):
	owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
#	versions = models.ManyToManyField('application.Version')

	def __unicode__(self):
		return self.latest.title +" by " +self.owner.username

	def _get_latest_version(self):
		latest = self.versions.order_by('-created')[0]
		return latest

	def delete(self, *args, **kwargs):
		self.delete_illustration()
	        super(Story, self).delete(*args, **kwargs) # super delete, yo

	def delete_illustration(self):
		path = settings.STATIC_ROOT +"illustrations/" +str(self.id)
		try:
			os.remove(path +".raw")
		except:
			pass
		try:
			os.remove(path +".jpg")
		except:			
			pass

	latest = property(_get_latest_version)


class Version(models.Model):
	story = models.ForeignKey('application.Story',related_name="versions");
	title = models.CharField(max_length=200)
	description = models.TextField()
	published = models.BooleanField()
	xml_data = models.TextField()
	created = models.DateTimeField(auto_now_add=True, auto_now=True)
	
	def __unicode__(self):
		return str(self.created) + " story " +str(self.story.id) +" version " +str(self.id)

	class Meta:
		ordering =['-created']
