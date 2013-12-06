import sublime, sublime_plugin

from app.commands.clean_up_command import CleanUpCommand
from app.commands.use_import_command import UseImportCommand
from app.commands.move_command import MoveRequireJsModuleCommand

class CleanUpCommand(CleanUpCommand):
  def run(self, edit):
    self.perform(edit)

class UseImportCommand(UseImportCommand):
  def run(self, edit):
    self.perform(edit)

class MoveRequireJsModuleCommand(MoveRequireJsModuleCommand):
  def run(self, edit, cmd, file):
    self.perform(edit, cmd, file)
