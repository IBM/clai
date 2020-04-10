import os
import sys
import json

from django.http import HttpResponse
sys.path.append(os.path.join(os.path.dirname(__file__),"..", "tellina_learning_module"))
from bashlint import data_tools

## load the manpage expl file, note that the root should be before tellina 
with open(os.path.join('website', 'manpage_expl.json'), encoding='UTF-8') as data_file:
    manpage_json = json.loads(data_file.read())

def explain_cmd(request):
  """ This is the responser for flag explanation:
    it takes in a request consist of a tuple (cmd_head, flag_name, node_kind) and returns the explanation of the flag.
    Arguments:
      request {
        cmd_head: the command to query
        flag_name: the flag to query
        node_kind: the type of span that the query is issued from
      }
    Returns:
      returns the manpage explanation of the cmd_head/flag_name
  """

  if request.method == 'POST':
    cmd_head = request.POST.get('cmd_head')
    flag_name = request.POST.get('flag_name')
    node_kind = request.POST.get('node_kind')
  else:
    cmd_head = request.GET.get('cmd_head')
    flag_name = request.GET.get('flag_name')
    node_kind = request.GET.get('node_kind')

  if cmd_head:
    # retrieve the explanation of the command
    for cmd_obj in manpage_json:
      if cmd_head in cmd_obj["aliases"]:
        #cmd_expl = "Aliases:" + " ".join(cmd_obj["aliases"]) + "\n\n" + cmd_obj["description"]
      
        # note that we use "None" due to the serialized field is of string type
        if flag_name != "None":
          # in this case, our goal is to explain a command
          flag_expl_list = []
          for option_desc in cmd_obj["optionDesc"]:
            if flag_name == option_desc["name"].split()[0]:
              flag_expl_list.append(option_desc["description"])
          if flag_expl_list:
            return HttpResponse("".join(flag_expl_list))
          else:
            return HttpResponse("")

        # if the flag is not provided, or we cannot find the flag
        if node_kind == "argument":
          return HttpResponse(cmd_obj["rawSynopsis"])
        elif node_kind == "utility":
          return HttpResponse(cmd_obj["description"])
  
  # in this case, either the thead is not provided or the head cannot be retrieved
  return HttpResponse("")

def cmd2html(cmd_str):
  """ A wrapper for the function ast2html (see below) that takes in a cmd string 
  and translate into a html string with highlinghting.
  """
  return " ".join(ast2html(data_tools.bash_parser(cmd_str)))

def tokens2html(cmd_str):
  """ A wrapper for the function ast2html (see below) that takes in a cmd string 
  and translate into a html string with highlinghting.
  """
  return " ".join(ast2html(cmd_str))

def ast2html(node):

  """ Translate a bash AST from tellina_learning_module/bashlint/nast.py into html code,
    with proper syntax highlighting.
    Argument:
      node: an ast returned from tellina_learning_module.data_tools.bash_parser(cmd_str)
    Returns:
      a html string that can be embedded into your browser with appropriate syntax highlighting
  """

  dominator = retrieve_dominators(node)

  # the documation of the span
  span_doc = "dominate_cmd=\"" + (str(dominator[0]) if dominator[0] else "None") \
                + "\" dominate_flag=\"" + (str(dominator[1]) if dominator[1] else "None") \
                + "\" node_kind=\"" + node.kind + "\"";

  html_spans = []

  # switching among node kinds for the generation of different spans 
  if node.kind == "root":
    for child in node.children:
      html_spans.extend(ast2html(child))
  elif node.kind == "pipeline":
    is_first = True
    for child in node.children:
      if is_first:
        is_first = False
      else:
        html_spans.append("|")
      html_spans.extend(ast2html(child))
  elif node.kind == "utility":
    span = "<span class=\"hljs-built_in\" " + span_doc + " >" + node.value + "</span>"
    html_spans.append(span)
    for child in node.children:
      html_spans.extend(ast2html(child))
  elif node.kind == "flag":
    # note there are two corner cases of flags:
    #   -exec::; and -exec::+ since they have different endings
    if node.value == "-exec::;" or node.value == "-exec::+":
      head_span = "<span class=\"hljs-keyword\" " + span_doc + " >" + "-exec" + "</span>"
    else:
      head_span = "<span class=\"hljs-keyword\" " + span_doc + " >" + node.value + "</span>"
    html_spans.append(head_span)
    for child in node.children:
      html_spans.extend(ast2html(child))
    if node.value == "-exec::;":
      html_spans.append("\\;")
    elif node.value == "-exec::+":
      html_spans.append("+");
  elif node.kind == "argument" and node.arg_type != "ReservedWord":
    span = "<span class=\"hljs-semantic_types\" " + span_doc + " >" + node.value + "</span>"
    html_spans.append(span)
    for child in node.children:
      html_spans.extend(ast2html(child))
  elif node.kind == "bracket":
    html_spans.append("\\(")
    for child in node.children:
      html_spans.extend(ast2html(child))
    html_spans.append("\\)")
  elif node.kind in ["binarylogicop", "unarylogicop", "redirect"]:
    span = "<span class=\"hljs-keyword\" " + span_doc + " >" + node.value + "</span>"
    html_spans.append(span)
  elif node.kind in ["commandsubstitution", "processsubstitution"]:
    html_spans.append(node.value)
    html_spans.append("(")
    for child in node.children:
      html_spans.extend(ast2html(child))
    html_spans.append(")")
  else:
    html_spans.append(node.value)

  return html_spans

def retrieve_dominators(node):
  """ Given a node, retrieve its dominator, 
    i.e., its utility and/or its dominate flag
  """ 
  dominate_headcmd = None
  dominate_flag = None

  current_node = node

  while True:
    if current_node and current_node.kind == "flag":
      if not dominate_flag: 
        dominate_flag = current_node.value
        # this is resulted from a corner case by Victoria, 
        #   for -exec::; -exec::+ and potentially others
        if "::" in dominate_flag:
          dominate_flag = dominate_flag[0: dominate_flag.index("::")]
    elif current_node and current_node.kind == "utility":
      dominate_headcmd = current_node.value
      return (dominate_headcmd, dominate_flag) 

    # we have already find dominate_headcmd or we have reached root
    if current_node and (not current_node.parent):
      return (dominate_headcmd, dominate_flag)
    elif current_node:
      current_node = current_node.parent

  if dominate_headcmd is None:
    return ('', '')
  return (dominate_headcmd, dominate_flag)

def test():
  cmd_str_list = [
    "find Path -iname Regex -exec grep -i -l Regex {} \;",
    "find Path -type f -iname Regex | xargs -I {} grep -i -l Regex {}",
    "find Path \( -name Regex-01 -or -name Regex-02 \) -print",
    "find Path -not -name Regex",
    "find . \( -mtime 10d -or -atime Timespan -or -atime Timespan -or -atime Timespan -or -atime Timespan \) -print",
    "find Documents \( -name \"*.py\" -o -name \"*.html\" \)"
  ];
  for cmd_str in cmd_str_list:
    print(cmd2html(cmd_str)) 

if __name__ == '__main__':
  test()
