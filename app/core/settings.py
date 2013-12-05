import sublime

class Settings:
  def __init__(self):
    self.settings = sublime.load_settings('requireJsSupport.sublime-settings')

  def getProjectDir(self):
    return self.settings.get('project-dir')
