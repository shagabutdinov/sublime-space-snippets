import sublime
import sublime_plugin
import re

class InsertSpacedChar(sublime_plugin.TextCommand):
  def run(
    self,
    edit,
    char,
    insert_space_before_regexp = None,
    remove_space_before_regexp = None,
    insert_space_after_regexp = None,
    remove_space_after_regexp = None,
  ):

    selections = []
    for sel in self.view.sel():
      new_char = char
      offset = sel.begin() - sel.end() + len(new_char)
      sel.a, sel.b = sel.begin(), sel.end()

      preceding_region = sublime.Region(self.view.line(sel.a).a, sel.a)
      following_region = sublime.Region(sel.b, self.view.line(sel.b).b)

      preceding_text = self.view.substr(preceding_region)
      following_text = self.view.substr(following_region)

      text = preceding_text +'__CURSOR__' + following_text

      remove_space_before = (
        remove_space_before_regexp != None and
        re.search(remove_space_before_regexp, text) != None
      )

      insert_space_before = (
        insert_space_before_regexp != None and
        re.search(insert_space_before_regexp, text) != None
      )

      if remove_space_before:
        before_space_match = re.search(r'\S(\s*)$', preceding_text)
        if before_space_match != None:
          before_space_length = len(before_space_match.group(1))
          sel.a -= before_space_length
          offset -= before_space_length
      elif insert_space_before:
        offset += 1
        new_char = ' ' + new_char

      remove_space_after = (
        remove_space_after_regexp != None and
        re.search(remove_space_after_regexp, text) != None
      )

      insert_space_after = (
        insert_space_after_regexp != None and
        re.search(insert_space_after_regexp, text) != None
      )

      if remove_space_after:
        after_space_length = len(re.search(r'^(\s*)\S', following_text).
          group(1))

        sel.b += after_space_length
        offset -= after_space_length
      elif insert_space_after:
        new_char += ' '
        offset += 1

      self.view.replace(edit, sel, new_char)
      sel.a, sel.b = sel.end() + offset, sel.end() + offset
      selections.append(sel)

    self.view.sel().clear()
    self.view.sel().add_all(selections)