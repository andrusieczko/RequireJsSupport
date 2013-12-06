import sublime_plugin
import shutil
import re

from app.utils.file_utils import FileUtils
from app.core.settings import Settings

class MovePhpFileCommand(sublime_plugin.TextCommand):
  def perform(self, edit, cmd, file):

    window = self.view.window()
    fileName =  window.active_view().file_name()
    self.original_name = fileName

    # file to be changed
    window.show_input_panel("Move to", fileName, self.onDone, self.empty, self.empty)

  def onDone(self, new_file_name):
    shutil.move(self.original_name, new_file_name)
    self.move(self.original_name, new_file_name)

  def move(self, oldFile, newFile):
    fileUtils = FileUtils()
    settings = Settings(self.view.window())
    projectDir = settings.getPhpProjectDir()
    extToFind = '.php'
    files = fileUtils.get_files(projectDir, extToFind)

    oldNamespace, oldFilename = self.getModuleId(oldFile, projectDir)
    newNamespace, newFilename = self.getModuleId(newFile, projectDir)

    for file in files:
      content = fileUtils.getContent(file)

      newContent = self.replaceUses(content, oldNamespace, oldFilename, newNamespace, newFilename)

      if newContent != None:
        fileToBeEdited = open(file, 'w+')
        fileToBeEdited.write(newContent)
        fileToBeEdited.close()

    content = fileUtils.getContent(newFile)
    newContent = self.replaceNamespace(content, oldNamespace, newNamespace)
    fileToBeEdited = open(newFile, 'w+')
    fileToBeEdited.write(newContent)
    fileToBeEdited.close()

  def getModuleId(self, path, projectDir):
    path = path.replace('/', '\\')
    projectDir = projectDir.replace('/', '\\')

    fileWithNamespace = path.replace(projectDir, "")

    fileName = fileWithNamespace.split('\\')[-1].split(".")[-2]
    namespace = '\\'.join(fileWithNamespace.split('\\')[:-1])
    
    return (namespace, fileName)

  def replaceUses(self, content, oldNamespace, oldFilename, newNamespace, newFilename):
    oldUse = r"([\\]?)(" + oldNamespace.replace("\\", r"\\") + r"\\" + oldFilename + ")";
    newUse = r"\1" + newNamespace + "\\" + newFilename;
    if len(re.findall(oldUse, content, re.MULTILINE)) == 0:
      return None

    return re.sub(oldUse, newUse, content)

  def replaceNamespace(self, content, oldNamespace, newNamespace):
    oldUse = "namespace " + oldNamespace + ";";
    newUse = "namespace " + newNamespace + ";";

    content = content.replace(oldUse, newUse)
    return content

  def empty(self, new_file_name):
    pass