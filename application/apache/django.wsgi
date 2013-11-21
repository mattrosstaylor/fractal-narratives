import os
import sys

sys.stdout = sys.stderr

sys.path.append('/opt/fractal-narratives')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
