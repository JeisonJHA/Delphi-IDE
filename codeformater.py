import sublime
import sublime_plugin
import subprocess
import os
import threading
import stat
import locale
from winreg import *


def plugin_loaded():
    def changeRegistry():
        keyVal = r'Software\CodeGear\BDS\6.0\Jedi\JCF\General'
        try:
            key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
        except:
            key = CreateKey(HKEY_CURRENT_USER, keyVal)
        SetValueEx(key, "FormatConfigFileName", 0, REG_SZ,
                   sublime.packages_path() + "\Delphi-API\JCFSettings.cfg")
        CloseKey(key)

    changeRegistry()

default_formatter = sublime.packages_path() + "\Delphi-API\JCF.exe"
default_param = ' -F -inplace -clarify '


class TFormatter(object):
    """docstring for TFormatter"""

    def formatCode(self, view):
        print('formatCode')
        view.erase_regions('codeerror')
        path = view.file_name()

        if (path is None):
            return

        s = sublime.load_settings("delphi-api.sublime-settings")
        auto_format = s.get("auto_format", False)

        if not auto_format:
            return

        filename, file_extension = os.path.splitext(path)
        if not file_extension in ['.pas', '.dpr', '.pp']:
            return

        validate_encode = s.get("validate_encode", False)
        if validate_encode:
            encode = s.get("encode", 'Western (Windows 1252)')
            if not (view.encoding() == encode):
                sublime.message_dialog('Encode: ' + view.encoding())
                return

        vssyntax = view.settings().get('syntax')
        if not (((vssyntax.find('Pascal.tmLanguage') > 0) or
                 (vssyntax.find('Pascal.sublime-syntax') > 0)) or
                ((vssyntax.find('delphi.tmLanguage') > 0) or
                 (vssyntax.find('delphi.sublime-syntax') > 0)
                 )):
            return

        if isReadonly(path):
            return

        path_formatter = s.get("path_formatter", default_formatter)
        use_default_formatter = default_formatter == path_formatter
        ThreadFormatter = TFormatterThread(
            view, path_formatter, path, use_default_formatter)
        ThreadFormatter.start()


def isReadonly(p_path):
    try:
        fileAttrs = os.stat(p_path)
        fileAtt = fileAttrs[0]
        return not fileAtt & stat.S_IWRITE
    except WindowsError:
        pass


class TFormatterThread(threading.Thread):

    def __init__(self, view, exe, param, default):
        super(TFormatterThread, self).__init__()
        self.view = view
        self.exe = exe
        self.param = param
        self.formatter = self.getFormatterObject(default)

    def run(self):
        self.view.set_status('formatter', 'Formatter: Formatting...')
        self.formatter.run_command(self.exe, self.param)
        self.view.erase_status('formatter')

    def getFormatterObject(self, default):
        if default:
            return self.DefaultFormatter(self.view)
        else:
            return self.OtherFormatter(self.view)

    class OtherFormatter(object):
        """docstring for OtherFormatter"""

        def __init__(self, view):
            self.view = view

        def run_command(self, exe, param):
            command = ('"' + exe + '" "' + param + '"')

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            p = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo
            )
            (out, err) = p.communicate()

            out = (out.decode(locale.getpreferredencoding())
                   if not out is None else None)
            err = (err.decode(locale.getpreferredencoding())
                   if not err is None else None)

            msglist = []
            msg = out.split('\r\n')
            for s in msg:
                if s.find(param) == 0:
                    msglist.append(s[len(param):].lstrip())
                else:
                    msglist.append(s.lstrip())
            else:
                out_msg = '\n'.join(msglist)

            if out_msg:
                sublime.message_dialog(out_msg)

    class DefaultFormatter(object):
        """docstring for DefaultFormatter"""

        def __init__(self, view):
            self.view = view

        def run_command(self, exe, param):
            command = ('"' + exe + '"' + default_param + '"' + param + '"')

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            p = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                startupinfo=startupinfo
            )
            (out, err) = p.communicate()

            out = (out.decode(locale.getpreferredencoding())
                   if not out is None else None)

            msglist = []
            if p.returncode == 0:
                msg = out.split('\r\n')
                for s in msg:
                    if s.find(param) == 0:
                        msglist.append(s[len(param):].lstrip())
                    else:
                        msglist.append(s.lstrip())
                else:
                    out_msg = '\n'.join(msglist)

            elif p.returncode == 1:
                err = (err.decode(locale.getpreferredencoding())
                       if not err is None else None)
                err = err.split('\r\n')
                out_msg = '\n'.join(err)

            elif p.returncode == 7:
                msg = out.split('\r\n')
                for s in msg:
                    if s.find('(') >= 0:
                        region = s[s.find('(') + 1:s.find(')')]
                        region = region.split(',')

                    if s.find(param) == 0:
                        msglist.append(s[len(param):].lstrip())
                    else:
                        msglist.append(s.lstrip())
                else:
                    out_msg = '\n'.join(msglist)

                style = (sublime.DRAW_NO_FILL | sublime.DRAW_NO_OUTLINE |
                         sublime.DRAW_SQUIGGLY_UNDERLINE)
                sview = self.view

                pt = sview.text_point(int(region[0]) - 1, int(region[1]))
                word = sview.word(pt)
                print('teste')
                sview.add_regions('codeerror', [word], 'invalid',
                                  'Packages/Delphi-API/warning.png', style)
                sview.show(word)

            else:
                msg = out.split('\r\n')
                for s in msg:
                    if s.find(param) == 0:
                        msglist.append(s[len(param):].lstrip())
                    else:
                        msglist.append(s.lstrip())
                else:
                    out_msg = '\n'.join(msglist)

            if out_msg:
                sublime.message_dialog(out_msg)


class TEventListener(sublime_plugin.EventListener):

    def on_post_save(self, view):
        Formatter = TFormatter()
        Formatter.formatCode(view)
