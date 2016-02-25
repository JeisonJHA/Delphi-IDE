import datetime
import sublime
import sublime_plugin
import os


class AddTagCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.DefineComment()

    def DefineComment(self):
        print("AddTag")
        settings = sublime.load_settings('delphi-api.sublime-settings')
        datetimeformat = settings.get("datetimeformat", "%d/%m/%Y")

        line = os.environ['USERNAME'].title() + ' - ' + \
            datetime.datetime.now().strftime(datetimeformat)
        self.view.run_command(
            "insert_snippet", {"contents": "%s" % '// ' + line})
