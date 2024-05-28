import logging
from django.shortcuts import render
from django.template.loader import get_template
import os

logger = logging.getLogger(__name__)

def landing_page(request):
    logger.debug("Rendering home/index.html")
    return render(request, 'home/index.html')

def landing_page(request):
    template_path = 'home/index.html'
    template = get_template(template_path)
    print(os.path.abspath(template.origin.name))  # Output template file path
    return render(request, template_path)
