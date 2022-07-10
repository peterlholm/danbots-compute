"template tags for pathname"
#import os
#from pathlib import Path
from django import template

register = template.Library()

@register.filter
def pathname(value):
    "return the full pathname"
    return value
    