import os

class FileUtils:
  def get_javascript_files(self, dir_name, extToFind):
    files = []
    for file in os.listdir(dir_name):
      dirfile = os.path.join(dir_name, file).replace('/', '\\')
      if os.path.isfile(dirfile):
        if os.path.splitext(dirfile)[1] == extToFind:
          files.append(dirfile)
      elif os.path.isdir(dirfile):
        files2 = self.get_javascript_files(dirfile, extToFind)
        if len(files2) > 0:
          files.extend(files2)
    return files