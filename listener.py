import sublime
import sublime_plugin
import re

from .processor import process

def get_modifications(selection, prefix, postfix):
  match = re.search(r',(\s*)$', prefix)

  if match != None:
    return ([selection - len(match.group(1)), selection], ' ')

  return None

class Listener(sublime_plugin.EventListener):

  def __init__(self):
    self._modificating = False
    self._last_command = None

  def on_text_command(self, view, command_name, args):
    self._last_command = command_name

  def on_modified(self, view):
    ignore = (
      self._last_command != None and (
        "delete" in self._last_command or
        "undo" in self._last_command or
        "redo" in self._last_command or
        "insert" in self._last_command or
        "ensure" in self._last_command or
        "snippet" in self._last_command or
        "completion" in self._last_command or
        "extract" in self._last_command
      )
    )

    if ignore:
      self._last_command = None
      return

    # prevent modification cycle
    if self._modificating:
      return

    self._modificating = True

    try:
      for index, sel in enumerate(view.sel()):
        self._update_selection(view, index)
    finally:
      self._modificating = False

  def _update_selection(self, view, index):
    sel = view.sel()[index]
    if not sel.empty():
      return

    scope_left = view.scope_name(sel.a - 1)
    scope_right = view.scope_name(sel.a)

    expr1 = r'source(?!.*(comment|string|css|yaml))'
    expr2 = r'^text.html(?!.*source)'

    ignore = (
      (
        re.search(expr1, scope_left) == None and
        re.search(expr1, scope_right) == None
      ) or (
        re.search(expr2, scope_left) != None or
        re.search(expr2, scope_right) != None
      )
    )

    if ignore:
      return

    point = sel.a
    modifications = process(
      view.substr(sublime.Region(view.line(point).a, point)),
      view.substr(sublime.Region(point, view.line(point).b))
    )

    for modification in modifications:
      point = view.sel()[index].a

      if modification[0] == modification[1]:
        view.run_command('insert_text', {
          'point': point + modification[0],
          'text': modification[2],
        })
      else:
        view.run_command('replace_text', {
          'region': [point + modification[0], point + modification[1]],
          'text': modification[2],
        })