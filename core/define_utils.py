class DefineUtils:

  def cleanUpDefine(self, content, defineObj):
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

    return (beggining + define + rest, define)

  def wrap(self, text, sep="'"):
    return sep + text + sep