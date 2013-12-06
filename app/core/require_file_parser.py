import re

from app.utils.file_utils import FileUtils

class RequireFileParser:
  moduleNamePattern = 'a-zA-Z@/-_#$!\+#0-9\-\.'
  defineSeparators = ' \t\r\n,'

  exceptions = []

  def parse(self, path, moduleId):
    fileUtils = FileUtils()
    content = fileUtils.getContent(path)
    defineStartIndex, defineEndIndex = self.getDefineRegion(content)

    defineContent = content[defineStartIndex:defineEndIndex]

    defineObj = self.createDefineObject(defineContent, moduleId, defineStartIndex, defineEndIndex)

    return (content, defineObj)

  def createDefineObject(self, defineContent, moduleId, defineStartIndex, defineEndIndex):
    imports = []
    args = []
    try:
      imports = self.getDefineImports(defineContent)
      args = self.getDefineArgs(defineContent)
    except Exception:
      self.exceptions.append(moduleId)

    return {
      "imports": imports,
      "args": args,
      "startIndex": defineStartIndex,
      "endIndex": defineEndIndex
    }

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

  def getDefineRegion(self, content):
    startIndex = content.find("define(")
    endIndex = content.find("{", startIndex) + 1
    return (startIndex, endIndex)

  def getDefineImports(self, content):
    m = re.search('define\(\[([' + self.moduleNamePattern + '\'' + self.defineSeparators + ']*)\]', content, re.MULTILINE)
    defines = m.group(1)
    imports = re.findall('\'([' + self.moduleNamePattern + ']*)\'[' + self.defineSeparators + ']*', defines, re.MULTILINE)
    return imports

  def getDefineArgs(self, content):
    m = re.search('function[ a-zA-Z]*\(([^\)]*)\)', content, re.MULTILINE)
    defines = m.group(1)
    definesList = re.split('[' + self.defineSeparators + ']*', defines, re.MULTILINE)
    return filter(None, definesList)

  def createDefineObj(self, defineImports, defineArgs):
    return {
      "imports": defineImports,
      "args": defineArgs
    }
