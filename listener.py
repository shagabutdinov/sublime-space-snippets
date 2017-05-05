import sublime
import sublime_plugin
import re

from .processor import process

def get_modifications(selection, prefix, postfix):
  match = re.search(r',(\s*)$', prefix)

  if match != None:
    return ([selection - len(match.group(1)), selection], ' ')

  return None

class SpaceSnippetsUpdate(sublime_plugin.TextCommand):
  def run(self, edit, modifications):
    for modification_with_index in modifications:
      if modification_with_index == None:
        continue

      index, modifications = modification_with_index
      for modification in modifications:
        point = self.view.sel()[index].a

        if modification[0] == modification[1]:
          self.view.insert(
            edit,
            point + modification[0],
            modification[2]
          )
        else:
          if modification[0] < 0 and modification[1] > 0:
            self.view.replace(
              edit,
              sublime.Region(point + modification[0], point),
              modification[2][0 : -modification[0]]
            )

            self.view.replace(
              edit,
              sublime.Region(point, point + modification[1]),
              modification[2][-modification[0] :]
            )

          else:
            self.view.replace(
              edit,
              sublime.Region(point + modification[0], point + modification[1]),
              modification[2]
            )

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
      modifications = []
      for index, sel in enumerate(view.sel()):
        modifications.append(self._update_selection(view, index))

      view.run_command('space_snippets_update', {
        'modifications': modifications,
      })
    finally:
      self._modificating = False

  def _update_selection(self, view, index):
    sel = view.sel()[index]
    if not sel.empty():
      return

    scope_left = view.scope_name(sel.a - 1)
    scope_right = view.scope_name(sel.a)

    expr1 = r'source(?!.*(comment|string|css|yaml|makefile|shell))'
    expr2 = r'^text(?!.*source.php)'

    ignore = (
      re.search(expr1, scope_left) == None and
      re.search(expr1, scope_right) == None
    )

    if ignore:
      return

    ignore = (
      re.search(expr2, scope_left) != None or
      re.search(expr2, scope_right) != None
    )

    if ignore:
      return

    if re.search(r'\.jsx(\.js)?\s*$', scope_left) != None:
      return

    point = sel.a
    modifications = process(
      view.substr(sublime.Region(view.line(point).a, point)),
      view.substr(sublime.Region(point, view.line(point).b)),
      scope_right,
    )

    if len(modifications) == 0:
      return [index, []]

    return [index, modifications]