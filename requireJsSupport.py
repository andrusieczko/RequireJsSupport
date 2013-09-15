import sublime, sublime_plugin
from require_parser import RequireParser

class RequireJsSupportCommand(RequireParser, sublime_plugin.TextCommand):
  def run(self, edit):
    self.edit = edit
    content = self.getContent()
    defineRegion = self.getDefineRegion(content)
    defineContent = self.view.substr(defineRegion)
    imports = self.getDefineImports(defineContent)
    args = self.getDefineArgs(defineContent)
    self.define = self.createDefineObj(imports, args)
    self.view.window().show_quick_panel(imports, self.onSelected)

  def onSelected(self, index):
    args = self.define['args']
    if (index < len(args)):
      module = args[index]
      for selection in self.view.sel():
        pos = selection.begin()
        self.view.insert(self.edit, pos, module)

class CleanUpRequire(RequireParser, sublime_plugin.TextCommand):
  def run(self, edit):
    content = self.getContent()
    defineRegion = self.getDefineRegion(content)
    defineContent = self.view.substr(defineRegion)
    imports = self.getDefineImports(defineContent)
    args = self.getDefineArgs(defineContent)
    define = self.createDefineObj(imports, args)

    self.cleanUpDefine(define, defineRegion, edit)

  def cleanUpDefine(self, defineObj, defineRegion, edit):
    wrappedImports = map(self.wrap, defineObj['imports'])
    imports = ", ".join(wrappedImports)
    args = ", ".join(defineObj['args'])

    define = "define([" + imports + "],\n\tfunction(" + args + ") {"

    self.view.replace(edit, defineRegion, define)