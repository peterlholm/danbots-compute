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

"""
TF_CPP_MIN_LOG_LEVEL - which has 3 or 4 basic levels - low numbers = more messages.
    0 outputs Information, Warning, Error, and Fatals (default)
    1 outputs Warning, and above
    2 outputs Errors and above.
"""
os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "0"

#os.environ['LD_LIBRARY_PATH'] = "/usr/local/cuda-11.6/lib64"
#os.environ["DISPLAY"] = "0.0"

application = get_wsgi_application()
