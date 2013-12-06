import re

class DefineUtils:

  def getJsVariablePattern(self, variableName):
    return '([^\.])(' + variableName + ')([^\w])'

  def cleanUpDefine(self, content, defineObj, toBeRenamedList = []):
    wrappedImports = map(self.wrap, defineObj['imports'])
    imports = ", ".join(wrappedImports)
    args = ", ".join(defineObj['args'])

    maxLineWidth = 140
    s = "define(["
    count = len(s)
    for imp in imports.split(' '):
      if len(s) + len(imp) < maxLineWidth:
        s = s + imp
        count = len(s)
      else:
        s = s + '\n' + imp
        count = 0

    define = s + "],\n\tfunction(" + args + ") {"    

    beggining = content[:defineObj['startIndex']]
    rest = content[defineObj['endIndex']:]

    if (len(toBeRenamedList) > 0):
      for toBeRenamed in toBeRenamedList:
        variableToBeRenamedPattern = self.getJsVariablePattern(toBeRenamed['oldName'])
        rest = re.sub(variableToBeRenamedPattern, r"\1" + toBeRenamed['newName'] + r"\3", rest)

    return beggining + define + rest

  def wrap(self, text, sep="'"):
    return sep + text + sep