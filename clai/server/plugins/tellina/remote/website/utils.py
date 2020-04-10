import os, sys
import socket
import ssl
import time
import urllib

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from website.models import NL, Command, Tag, URL

sys.path.append(os.path.join(
    os.path.dirname(__file__), "..", "tellina_learning_module"))

from bashlint import data_tools


# Number of translations to show
NUM_TRANSLATIONS = 20


def extract_html(url):
    hypothes_prefix = "https://via.hypothes.is/"
    try:
        time.sleep(0.1)
        html = urllib.request.urlopen(hypothes_prefix + url, timeout=2)
    except urllib.error.URLError:
        print("Error: extract_text_from_url() urllib2.URLError")
        # return "", randomstr(180)
        return None, None
    except socket.timeout:
        print("Error: extract_text_from_url() socket.timeout")
        # return "", randomstr(180)
        return None, None
    except ssl.SSLError:
        print("Error: extract_text_from_url() ssl.SSLError")
        # return "", randomstr(180)
        return None, None
    return html.read()

def get_nl(nl_str):
    nl, _ = NL.objects.get_or_create(str=nl_str.strip())
    return nl

def get_command(command_str):
    command_str=command_str.strip()
    if Command.objects.filter(str=command_str).exists():
        cmd = Command.objects.get(str=command_str)
    else:
        cmd = Command.objects.create(str=command_str)
        ast = data_tools.bash_parser(command_str)
        for utility in data_tools.get_utilities(ast):
            cmd.tags.add(get_tag(utility))    
        template = data_tools.ast2template(
	        ast, loose_constraints=True)
        cmd.template = template
        cmd.save()
    return cmd

def get_tag(tag_str):
    tag, _ = Tag.objects.get_or_create(str=tag_str.strip())
    return tag

def get_url(url_str):
    url_str = url_str.strip()
    try:
        url = URL.objects.get(str=url_str)
    except ObjectDoesNotExist:
        html = extract_html(url_str)
        if html is None:
            url = URL.objects.create(str=url_str)
        else:
            url = URL.objects.create(str=url_str, html_content=html)
    return url

def json_response(d={}, status='SUCCESS'):
    d.update({'status': status})
    resp = JsonResponse(d)
    return resp
