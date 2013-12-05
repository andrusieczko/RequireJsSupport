import sublime_plugin, sublime

from app.core.require_file_parser import RequireFileParser

from app.utils.define_utils import DefineUtils

class CleanUpCommand(RequireFileParser, sublime_plugin.TextCommand):
  def perform(self, edit):
    window = self.view.window()
    path =  window.active_view().file_name()

    moduleId = "my-module"
    content, defineObj = self.parse(path, moduleId);

    defineUtils = DefineUtils()
    newContent = defineUtils.cleanUpDefine(content, defineObj)

    defineRegion = sublime.Region(0, len(content)-1)
    self.view.replace(edit, defineRegion, newContent)