import sublime_plugin, sublime
from core.require_parser import RequireParser
from core.require_file_parser import RequireFileParser
from core.define_utils import DefineUtils
from core.file_utils import FileUtils
import shutil

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

    maxLineWidth = 140
    s = "dfefine(["
    count = len(s)
    sep = ", "
    args = sep.join(defineObj['args'])

    # TODO: do it more general + arguments
    importsList = [[]]
    importsListCurrentLine = 0
    for imp in wrappedImports:
      if count + len(imp) < maxLineWidth:
        count = count + len(imp) + len(sep)
      else:
        importsListCurrentLine = importsListCurrentLine + 1
        importsList.append([])
        count = 0

      importsList[importsListCurrentLine].append(imp)

    importsString = ",\n\t".join([sep.join(x) for x in importsList])

    define = s + importsString + "],\n\tfunction(" + args + ") {"

    self.view.replace(edit, defineRegion, define)

# ######### MOVE ###########

class MyCleanUp(RequireFileParser, sublime_plugin.TextCommand):
  def run(self, edit):
    window = self.view.window()
    path =  window.active_view().file_name()

    moduleId = "my-module"
    content, defineObj = self.parse(path, moduleId);

    defineUtils = DefineUtils()
    newContent, defineContent = defineUtils.cleanUpDefine(content, defineObj)

    defineRegion = sublime.Region(0, len(content)-1)
    self.view.replace(edit, defineRegion, defineContent)

class MoveRequireJsModuleCommand(RequireFileParser, sublime_plugin.TextCommand):
  def run(self, edit, cmd, file):
    window = self.view.window()
    file_name =  window.active_view().file_name()
    self.original_name = file_name

    # file to be changed
    window.show_input_panel("Move to", file_name, self.onDone, self.empty, self.empty)

  def onDone(self, new_file_name):
    shutil.move(self.original_name, new_file_name)
    self.move(self.original_name, new_file_name)

  def move(self, oldFile, newFile):
    defineUtils = DefineUtils()
    fileUtils = FileUtils()

    oldFile = self.getModuleId(oldFile)
    newFile = self.getModuleId(newFile)

    print 'original_name: ' + oldFile
    print 'new_file_name: ' + newFile

    dir_name = 'D:/userdata/andrusie/htdocs/ckdb/src/Nsn/NetEng'
    extToFind = '.js'
    
    files = fileUtils.get_javascript_files(dir_name, extToFind)

    changedFiles = []
    for path in files:

      moduleId = self.getModuleId(path)
      content, defineObj = self.parse(path, moduleId);

      if oldFile in defineObj['imports']:
        index = defineObj['imports'].index(oldFile)
        defineObj['imports'][index] = newFile
        defineObj['args'][index] = newFile.split('/')[-1:][0]

        newContent = defineUtils.cleanUpDefine(content, defineObj)
        
        fileToBeEdited = open(path, 'w+')
        fileToBeEdited.write(newContent)
        fileToBeEdited.close()

        changedFiles.append(self.getModuleId(path))

    print str(len(changedFiles)) + ' files changed: ' + str(changedFiles)
    print str(len(self.exceptions)) + ' EXCEPTIONS: ' + str(self.exceptions)

  def empty(self, new_file_name):
    pass
