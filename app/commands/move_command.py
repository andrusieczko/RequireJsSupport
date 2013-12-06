import sublime_plugin

from app.core.require_file_parser import RequireFileParser
from app.core.settings import Settings

from app.utils.define_utils import DefineUtils
from app.utils.file_utils import FileUtils

import shutil

class MoveRequireJsModuleCommand(RequireFileParser, sublime_plugin.TextCommand):
  def perform(self, edit, cmd, file):
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
    settings = Settings(self.view.window())

    oldFile = self.getModuleId(oldFile)
    newFile = self.getModuleId(newFile)

    print 'original_name: ' + oldFile
    print 'new_file_name: ' + newFile

    projectDir = settings.getProjectDir()
    extToFind = '.js'
    
    files = fileUtils.get_javascript_files(projectDir, extToFind)

    changedFiles = []
    for path in files:

      moduleId = self.getModuleId(path)
      content, defineObj = self.parse(path, moduleId);

      if oldFile in defineObj['imports']:
        index = defineObj['imports'].index(oldFile)

        oldName = defineObj['args'][index]
        newName = newFile.split('/')[-1:][0]
        
        toBeRenamed = [{
            'oldName': oldName,
            'newName': newName
        }]

        defineObj['imports'][index] = newFile
        defineObj['args'][index] = newName

        newContent = defineUtils.cleanUpDefine(content, defineObj, toBeRenamed)
        
        fileToBeEdited = open(path, 'w+')
        fileToBeEdited.write(newContent)
        fileToBeEdited.close()

        changedFiles.append(self.getModuleId(path))

    print str(len(changedFiles)) + ' files changed: ' + str(changedFiles)
    print str(len(self.exceptions)) + ' EXCEPTIONS: ' + str(self.exceptions)
    self.exceptions = []

  def empty(self, new_file_name):
    pass
