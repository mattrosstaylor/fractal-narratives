from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.conf import settings
from PIL import Image
import logging

from application.models import Story, User, Version

def index(request):
	return render_to_response('application/index.html', None ,context_instance=RequestContext(request));

def help(request):
	story = get_object_or_404(Story, pk=1)
	return render_to_response('application/help.html', { 'story' : story } ,context_instance=RequestContext(request));

def about(request):
	return render_to_response('application/about.html', None ,context_instance=RequestContext(request));


def story_index(request):
	story_list = [x for x in Story.objects.all() if x.latest.published]
	return render_to_response('application/story_index.html', {'story_list': story_list}, context_instance=RequestContext(request));

@login_required
def story_index_admin(request):
	if (request.user.is_staff):
		story_list = Story.objects.all()
		return render_to_response('application/story_index_admin.html', {'story_list': story_list}, context_instance=RequestContext(request));
	else:
		return HttpResponseForbidden("You do not have permission to view this page.")

def story_view(request, story_id):
	story = get_object_or_404(Story, pk=story_id)
	if (story.latest.published or story.owner == request.user or request.user.is_staff):
		return render_to_response('application/story_view.html', {'story': story}, context_instance=RequestContext(request))
	else:
		return HttpResponseForbidden("You do not have permission to view this story.")

def story_randomise(request, story_id):
	story = get_object_or_404(Story, pk=story_id)
	if (story.latest.published or story.owner == request.user or request.user.is_staff):
		return render_to_response('application/story_randomise.html', {'story': story}, context_instance=RequestContext(request))
	else:
		return HttpResponseForbidden("You do not have permission to view this story.")

def user_view(request, user_name):
	profile_user = get_object_or_404(User, username=user_name)
	if profile_user == request.user:
		story_list = Story.objects.filter(owner=profile_user)
		return render_to_response('application/user_homepage.html', {'story_list': story_list}, context_instance=RequestContext(request))

	else:
		story_list = [x for x in Story.objects.filter(owner=profile_user) if x.latest.published]
		return render_to_response('application/user_view.html', {'profile_user': profile_user, 'story_list': story_list}, context_instance=RequestContext(request))

@login_required
def login_redirect(request):
	return redirect("/user/" +request.user.username)

@login_required
def story_new(request):
	story = Story.objects.create()
	story.owner = request.user
	story.save()
	version = Version(xml_data = "<story><text>Beginning</text><text>End</text></story>", story = story)
	version.save()
	return redirect("/story/edit/" +str(story.id))

@login_required
def story_edit(request, story_id):
	story = get_object_or_404(Story, pk=story_id)
	if story.owner == request.user or request.user.is_staff:
		return render_to_response('application/story_edit.html', {'story': story}, context_instance=RequestContext(request))
	else:
		return HttpResponseForbidden("You do not have permission to edit this story.")

@login_required
@require_http_methods(["POST"])
def story_save(request):
	story = get_object_or_404(Story, pk=request.POST["id"])
	if story.owner == request.user or request.user.is_staff:
		version = Version(xml_data=request.POST["xml"], title=request.POST["title"], description=request.POST["description"], published = (request.POST["published"] == "true"), story = story)
		version.save()
		return HttpResponse("Saved story " +str(story.id) +" version " +str(story.latest.id))
	else:
		return HttpResponseForbidden("You do not have permission to save this story.")

@login_required
@require_http_methods(["POST"])
def story_delete(request):
	story = get_object_or_404(Story, pk=request.POST["id"])
	if story.owner == request.user or request.user.is_staff:
		story.delete()
		return HttpResponse("Deleted")
	else:
		return HttpResponseForbidden("You do not have permission to delete this story.")

@login_required
@require_http_methods(["POST"])
def upload(request):
	story = get_object_or_404(Story, pk=request.POST["id"])
	if story.owner == request.user or request.user.is_staff:
		try:
			path = settings.STATIC_ROOT + "illustrations/" +request.POST["id"];
			f = request.FILES['myFile']
			destination = open(path +".raw", 'wb+')
		 	for chunk in f.chunks():
		        	destination.write(chunk)
			destination.close()

			size = 100,100

			im = Image.open(path+".raw")
			im.thumbnail(size, Image.ANTIALIAS)
			im.save(path + ".jpg", "JPEG")
		except IOError:
			self.delete_illustration()
			return HttpResponseServerError("Error uploading illustration")	
		
		return HttpResponse("Upload successful")
	else:
		return HttpResponseForbidden("You do not have permission to change the illustration for this story.")


@require_http_methods(["POST"])
def logger(request):

	data = dict()
	data["REMOTE_ADDR"] = str(request.META["REMOTE_ADDR"])
	data["id"] = str(request.POST["log_id"])
	data["username"] = str(request.user.username)
	data["HTTP_REFERER"] = str(request.META["HTTP_REFERER"])
	data["message"] = str(request.POST["message"])

	logging.getLogger("logview.info_log").info(str(data))
	return HttpResponse("Logged")

def analysis(request):
	story_list = [x for x in Story.objects.all() if x.latest.published]
	return render_to_response('application/analysis.html', {'story_list': story_list}, context_instance=RequestContext(request));

