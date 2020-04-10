import html
import os, sys
import pickle
import re
import sqlite3

from website.models import Annotation, AnnotationUpdate, Command, \
    Notification, URL, URLTag
from website.utils import get_tag, get_command, get_url

learning_module_dir = os.path.join(os.path.dirname(__file__), '..', '..',
                                   "tellina_learning_module")
sys.path.append(learning_module_dir)

from bashlint import data_tools

CODE_REGEX = re.compile(r"<pre><code>([^<]+\n[^<]*)<\/code><\/pre>")


def extract_code(text):
    for match in CODE_REGEX.findall(text):
        if match.strip():
            yield html.unescape(match.replace("<br>", "\n"))

def extract_oneliners_from_code(code_block):
    for cmd in code_block.splitlines():
        if cmd.startswith('$ '):
            cmd = cmd[2:]
        if cmd.startswith('# '):
            cmd = cmd[2:]
        comment = re.search(r'\s+#\s+', cmd)
        if comment:
            old_cmd = cmd
            cmd = cmd[:comment.start()]
            print('Remove comment: {} -> {}'.format(old_cmd, cmd))
        cmd = cmd.strip()

        # discard code block opening line
        if cmd and not cmd[-1] in ['{', '[', '(']:
            yield cmd

def load_urls(input_file_path):
    with open(input_file_path, 'rb') as f:
        urls_by_utility = pickle.load(f)

    for utility in urls_by_utility:
        for url in urls_by_utility[utility]:
            if not URLTag.objects.filter(url__str=url, tag=utility):
                URLTag.objects.create(url=get_url(url), tag=utility)
                print("Add {}, {}".format(url, utility))

def load_commands_in_url(stackoverflow_dump_path):
    url_prefix = 'https://stackoverflow.com/questions/'
    with sqlite3.connect(stackoverflow_dump_path,
                         detect_types=sqlite3.PARSE_DECLTYPES) as db:
        for url in URL.objects.all():
            # url = URL.objects.get(str='https://stackoverflow.com/questions/127669')
            url.commands.clear()
            print(url.str)
            for answer_body, in db.cursor().execute("""
                    SELECT answers.Body FROM answers 
                    WHERE answers.ParentId = ?""", (url.str[len(url_prefix):],)):
                url.html_content = answer_body
                for code_block in extract_code(url.html_content):
                    for cmd in extract_oneliners_from_code(code_block):
                        ast = data_tools.bash_parser(cmd)
                        if ast:
                            command = get_command(cmd)                        
                            print('extracted: {}'.format(cmd))
                            url.commands.add(command)
            url.save()

def populate_command_tags():
    for cmd in Command.objects.all():
        if len(cmd.str) > 600:
            cmd.delete()
        else:
            cmd.tags.clear()
            print(cmd.str)
            ast = data_tools.bash_parser(cmd.str)
            for utility in data_tools.get_utilities(ast):
                print(utility)
                cmd.tags.add(get_tag(utility))
            cmd.save()

def populate_command_template():
    for cmd in Command.objects.all():
        if len(cmd.str) > 600:
            cmd.delete()
        else:
            ast = data_tools.bash_parser(cmd.str)
            template = data_tools.ast2template(ast, loose_constraints=True)
            cmd.template = template
            cmd.save()

def populate_tag_commands():
    for tag in Tag.objects.all():
        tag.commands.clear()
    for url_tag in URLTag.objects.all():
        print(url_tag.url.str)
        tag = get_tag(url_tag.tag)
        for cmd in url_tag.url.commands.all():
            if tag in cmd.tags.all():
                tag.commands.add(cmd)
        tag.save()

def populate_url_tags():
    for url in URL.objects.all():
        for annotation in Annotation.objects.filter(url=url):
            for tag in annotation.cmd.tags.all():
                url.tags.add(tag)

def populate_tag_annotations():
    for annotation in Annotation.objects.all():
        for tag in annotation.cmd.tags.all():
            tag.annotations.add(annotation)

def create_notifications():
    for annotation_update in AnnotationUpdate.objects.all():
        annotation = annotation_update.annotation
        Notification.objects.create(sender=annotation_update.judger,
            receiver=annotation.annotator, type='annotation_update',
            annotation_update=annotation_update, url=annotation.url)

if __name__ == '__main__':
    load_urls()
