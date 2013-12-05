import sublime, sublime_plugin

from app.core.require_file_parser import RequireFileParser

class UseImportCommand(RequireFileParser, sublime_plugin.TextCommand):
  def perform(self, edit):
    self.edit = edit
    window = self.view.window()
    path =  window.active_view().file_name()
    content = self.getContent(path)
    startIndex, endIndex = self.getDefineRegion(content)
    defineRegion = sublime.Region(startIndex, endIndex)
    defineContent = self.view.substr(defineRegion)
    imports = self.getDefineImports(defineContent)
    args = self.getDefineArgs(defineContent)
    self.define = self.createDefineObj(imports, args)
    self.view.window().show_quick_panel(imports, self.onSelected)

  def onSelected(self, index):
    if (index != -1):
        args = self.define['args']
        if (index < len(args)):
          module = args[index]
          for selection in self.view.sel():
            pos = selection.begin()
            self.view.insert(self.edit, pos, module)