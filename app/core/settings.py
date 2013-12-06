import sublime

class Settings:
  def __init__(self, window):
    self.settings = sublime.load_settings('requireJsSupport.sublime-settings')
    self.window = window

  def getProjectDir(self):
    return self.window.folders()[0] + self.settings.get('project-dir')
