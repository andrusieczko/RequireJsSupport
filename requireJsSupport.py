from app.commands.clean_up_command import CleanUpCommand
from app.commands.use_import_command import UseImportCommand
from app.commands.move_command import MoveRequireJsModuleCommand
from app.commands.move_php_file_command import MovePhpFileCommand

class CleanUpCommand(CleanUpCommand):
  def run(self, edit):
    self.perform(edit)

class UseImportCommand(UseImportCommand):
  def run(self, edit):
    self.perform(edit)

class MoveRequireJsModuleCommand(MoveRequireJsModuleCommand):
  def run(self, edit, cmd, file):
    self.perform(edit, cmd, file)

class MovePhpFileCommand(MovePhpFileCommand):
  def run(self, edit, cmd, file):
    self.perform(edit, cmd, file)

import sublime_plugin

from app.core.require_file_parser import RequireFileParser
from app.core.settings import Settings

from app.utils.define_utils import DefineUtils
from app.utils.file_utils import FileUtils
from app.core.settings import Settings

class GoToJsClassCommand(RequireFileParser, sublime_plugin.TextCommand):
  def run(self, edit):
    moduleName = self.getModuleName()

    window = self.view.window()
    path =  window.active_view().file_name()

    moduleId = "my-module"
    content, defineObj = self.parse(path, moduleId);

    if (moduleName in defineObj['args']):
      index = defineObj['args'].index(moduleName)
      moduleNameToBeOpened = defineObj['imports'][index]

      fileName = self.getFileNameFromModule(moduleNameToBeOpened)
      window.open_file(fileName)

  def getFileNameFromModule(self, moduleName):
    # @AuditsBundle/containers/model/distributions/distributionsFilteringStorage

    settings = Settings(self.view.window())
    bundleName = moduleName.split('/')[0][1:]
    filePath = '/'.join(moduleName.split('/')[1:]) + ".js"
    fileName = settings.getProjectDir() + "/" + bundleName + "/Resources/public/js/" + filePath
    return fileName.replace('\\', '/')

  def getModuleId(self, fileName):
    # TODO: Big Fat Todo
    netEngPattern = 'Nsn\\NetEng\\'
    netEngIndex = fileName.index(netEngPattern) + len(netEngPattern)
    resourcesPattern = 'Resources\\public\\js\\'
    resourcesIndexStart = fileName.index(resourcesPattern)
    resourcesIndexEnd = fileName.index(resourcesPattern) + len(resourcesPattern)
    extIndex = fileName.index('.js')
    newPath = '@' + fileName[netEngIndex:resourcesIndexStart] + fileName[resourcesIndexEnd:extIndex]
    newPath = newPath.replace('\\', '/')
    return newPath

  def getModuleName(self):
    return self.getSelectedText()

  def getSelectedText(self):
    return self.view.substr(self.getSelection())

  def getSelection(self):
    return self.view.sel()[0]