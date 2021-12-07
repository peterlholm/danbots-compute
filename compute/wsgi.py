"""
WSGI config for compute project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'compute.settings')

os.environ['MPLCONFIGDIR'] = '/tmp/'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
#os.environ["DISPLAY"] = "0.0"

application = get_wsgi_application()

