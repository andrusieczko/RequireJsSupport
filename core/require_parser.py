import sublime, re

class RequireParser:
  moduleNamePattern = 'a-zA-Z@/-_#$'
  defineSeparators = ' \t\r\n,'

  def getContent(self):
    return self.view.substr(sublime.Region(0, self.view.size()))

  def getDefineRegion(self, content):
    startIndex = content.find("define(")
    endIndex = content.find("{", startIndex) + 1
    return sublime.Region(startIndex, endIndex)

  def getDefineImports(self, content):
    m = re.search('define\(\[([' + self.moduleNamePattern + '\'' + self.defineSeparators + ']*)\]', content, re.MULTILINE)
    defines = m.group(1)
    imports = re.findall('\'([' + self.moduleNamePattern + ']*)\'[' + self.defineSeparators + ']*', defines, re.MULTILINE)
    return imports

  def getDefineArgs(self, content):
    m = re.search('function\(([^\)]*)\)', content, re.MULTILINE)
    defines = m.group(1)
    definesList = re.split('[' + self.defineSeparators + ']*', defines, re.MULTILINE)
    return filter(None, definesList)

  def createDefineObj(self, defineImports, defineArgs):
    return {
      "imports": defineImports,
      "args": defineArgs
    }

  def wrap(self, text, sep="'"):
    return sep + text + sep