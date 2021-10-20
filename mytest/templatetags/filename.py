import os
from pathlib import Path
from django import template

register = template.Library()

@register.filter
def filename(value):
    return os.path.basename(Path(value).name)
    