import sublime_plugin
from Plugins_Development import objectdef, adddoc


class DelphiIdeCommand(sublime_plugin.TextCommand):

    def run(self, edit, methodname, args=[]):
        print(methodname)
        self.edit = edit
        pluginCall = None
        try:
            pluginCall = getattr(self, methodname)
        except AttributeError:
            raise NotImplementedError("Class `{}` does not implement `{}`".
                                      format(self.__class__.__name__,
                                             methodname))
        try:
            pluginCall(args)
        except Exception as e:
            raise print(e)

    def adddoc(self, args):
        edit = self.edit
        _adddoc = adddoc.AddDocCommand(self.view)
        _adddoc.run(edit)
        pass

    def addtag(self, args):
        import os
        import datetime
        import sublime
        print("AddTag")
        settings = sublime.load_settings('delphi-ide.sublime-settings')
        datetimeformat = settings.get("datetimeformat", "%d/%m/%Y")

        line = os.environ['USERNAME'].title() + ' - ' + \
            datetime.datetime.now().strftime(datetimeformat)
        self.view.run_command(
            "insert_snippet", {"contents": "%s" % '// ' + line})

    def changefunctionreturn(self, args):
        prompt = True
        return_type = ''
        if args:
            prompt = args[0]
            return_type = args[1]

        def on_done(return_type):
            view.run_command(
                "delphi_ide", {"methodname": "changefunctionreturn",
                               "args": [False, return_type]})

        def AskReturn(return_type):
            view.window().show_input_panel(
                "Function return:",
                str(return_type),
                lambda f: on_done(f),
                None, None)

        print("Change method return")
        view = self.view
        cursor_pt = view.sel()[0].begin()

        if ((view.match_selector(cursor_pt, 'function.implementation.delphi')
             ) or (view.match_selector(cursor_pt, 'meta.function.delphi'))) \
                and prompt:
            print("Change method return")
            AskReturn(return_type)
            return

        method = self.getMethodInformation()
        edit = self.edit
        if return_type:
            print('method.returntypeimplregion:%s' %
                  method.returntypeimplregion)
            view.replace(edit, method.returntypeimplregion[0], return_type)
            view.replace(edit, method.storagetyperegimp[0], 'function')
            view.replace(edit, method.returntypeinteregion[0], return_type)
            view.replace(edit, method.storagetyperegint[0], 'function')
        else:
            view.replace(edit, method.fullreturntypeimplregion[0], return_type)
            view.replace(edit, method.storagetyperegimp[0], 'procedure')
            view.replace(edit, method.fullreturntypeinteregion[0], return_type)
            view.replace(edit, method.storagetyperegint[0], 'procedure')

    def declaremethod(self, args):
        def getValidLine():
            if view.match_selector(view.sel()[0].begin(), 'unit.block.delphi'):
                implementation = view.find_by_selector(
                    'implementation.block.delphi')
                line = implementation[0].end()

                initia = view.find_by_selector('initialization.block.delphi')
                if initia:
                    if line > initia[0].begin():
                        line = initia[0].begin()

                finali = view.find_by_selector('finalization.block.delphi')
                if finali:
                    if line > finali[0].begin():
                        line = finali[0].begin()
            else:
                program = view.find_by_selector(
                    'program.block.delphi')
                line = program[0].begin()

            return line

        import sublime
        method = self.getMethodInformation()
        if method.has_interface and method.has_implementation:
            return
        edit = self.edit
        view = self.view
        settings = sublime.load_settings(
            'delphi-ide.sublime-settings')
        _visibility = settings.get("visibility", "private")

        _createblock = settings.get("create_visibility_block", False)
        tab_size = view.settings().get("tab_size")

        if method.methodclass:
            _visibregion = getattr(method.methodclass, _visibility + 'region')
            if not _visibregion:
                if not _createblock:
                    print('Visibility ' + _visibility + ' do not exists.')
                    return
                elif _createblock:
                    line = method.methodclass.classregion[0].end()
                    line, _ = view.rowcol(line)
                    line -= 1
                    pt = view.text_point(line, 0)
                    pt = view.line(pt).end()
                    view.insert(edit, pt, '\n' + (' ' * tab_size) +
                                _visibility)
                    method.methodclass = self.getClassInformation(method)

            _newdecmethod = method.getNewMethodDef()
            if method.has_implementation:
                line = getattr(method.methodclass, _visibility + 'region')
                line, _ = view.rowcol(line[0].end())
                line -= 1
                pt = view.text_point(line, 0)
                pt = view.line(pt).end()
                view.insert(edit, pt, '\n' +
                            (' ' * (tab_size * 2)) + _newdecmethod)
            elif method.has_interface:
                line = getValidLine()
                line, _ = view.rowcol(line)
                line -= 1
                pt = view.text_point(line, 0)
                pt = view.line(pt).end()

                view.insert(edit, pt, '\n' + _newdecmethod + '\n' +
                            'begin' + '\n\n' + 'end;' + '\n')
        else:
            _newdecmethod = method.getNewMethodDef()
            if method.has_implementation:
                pt, _ = self.getSelectorPTEnd('interface')
                view.insert(edit, pt, '\n' + _newdecmethod + '\n')
            elif method.has_interface:
                pt, _ = self.getSelectorPTEnd('implementation')

                view.insert(edit, pt, '\n' + _newdecmethod + '\n' +
                            'begin' + '\n\n' + 'end;' + '\n')

    def extractmethod(self, args):
        from re import search

        def isSubInText(sub, text):
            return search('(?i)(\\b)' + sub + '(\\b)', text) is not None

        def getClass():
            if not method.methodclass:
                return ''
            return method.methodclass.classname + '.'

        def params(paramsIn, varsIn):
            if (not paramsIn) and (not varsIn):
                return ''
            result = []
            if paramsIn:
                for param in method.paramsimpl:
                    for para in paramsIn:
                        if isSubInText(para, param):
                            result.append(param)

            if varsIn:
                for var in method.variables:
                    for va in varsIn:
                        if isSubInText(va, var):
                            result.append(var)
            if result:
                return '(' + '; '.join(result) + ')'
            else:
                return ''

        method = self.getMethodInformation()
        v = self.view
        vsubstr = v.substr
        self.cursor_region = v.sel()[0]
        cursor_region = self.cursor_region
        word_region = v.word(cursor_region)
        word = vsubstr(word_region).strip()

        selection_text = vsubstr(word_region).splitlines()
        _varsIn = []
        _paramsIn = []

        for line in selection_text:
            _bfind = False
            for param in method.paramsnameimpl:
                if isSubInText(param, line):
                    _paramsIn.append(param)
                    _bfind = True
                    break

            if _bfind:
                continue

            for var in method.variablesname:
                if isSubInText(var, line):
                    _varsIn.append(var)
                    break

        if _paramsIn:
            _paramsIn = list(set(_paramsIn))
        if _varsIn:
            _varsIn = list(set(_varsIn))

        _method = 'procedure ' + getClass() + 'ExtractedMethod' + \
            params(_paramsIn, _varsIn) + ';' + '\n'

        edit = self.edit
        ptinicio, line = self.getSelectorPTEnd('implementation')
        _method = '\n' + _method + 'begin' + '\n  ' + word + '\n' + \
            'end;' + '\n'
        v.insert(edit, ptinicio, _method)

        params_declare = ''
        params_declare = ', '.join(_paramsIn)
        if params_declare and _varsIn:
            params_declare += ', ' + ', '.join(_varsIn)
        elif _varsIn:
            params_declare = ', '.join(_varsIn)

        if params_declare:
            params_declare = '(' + params_declare + ')'
        v.replace(
            edit, word_region, '\n  ExtractedMethod' + params_declare + '; \n')

        v.sel().clear()
        v.sel().add(v.line(ptinicio))
        v.run_command("delphi_ide", {"methodname": "declaremethod"})
        v.sel().clear()

        import sublime
        region = sublime.Region(0, v.size())
        lines = v.split_by_newlines(region)

        for line in lines:
            if 'ExtractedMethod' in v.substr(line):
                regiao_do_metodo = v.find(
                    'ExtractedMethod', line.begin())
                v.sel().add(regiao_do_metodo)
        v.show(regiao_do_metodo)

    def syncronizemethoddeclaration(self, args):
        edit = self.edit
        view = self.view
        cursor_pt = view.sel()[0].begin()

        method = self.getMethodInformation()
        _isImpl = view.match_selector(cursor_pt, 'implementation.block.delphi')

        if _isImpl:
            view.replace(edit, method.paramdefintreg[
                         0], method.paramdefimpl[0])
        else:
            view.replace(edit, method.paramdefimplreg[
                         0], method.paramdefint[0])

    def delphimethodnav(self, args):
        method = self.getMethodInformation()
        if not method.has_interface:
            return

        cursor_pt = self.view.sel()[0].begin()
        self.view.sel().clear()
        if self.view.match_selector(cursor_pt, 'implementation.block.delphi'):
            self.view.sel().add(method.interfacedef[0])
            self.view.show(method.interfacedef[0])
        else:
            if not method.has_implementation:
                raise Exception('Method has no implementation')

            self.view.sel().add(method.implementationdef[0])
            self.view.show(method.implementationdef[0].a)

    def getMethodInformation(self):
        view = self.view
        cursor_region = view.sel()[0]
        cursor_pt = view.sel()[0].begin()

        if (not view.match_selector(
                cursor_pt, 'function.implementation.delphi')) \
            and (not view.match_selector(
                cursor_pt, 'meta.function.delphi')):

                # exit because it is not in a method
            return None

        method = objectdef.MethodDeclaration(self.view)

        selector = view.find_by_selector
        nameregion = 'function.implementation.delphi'
        if view.match_selector(cursor_pt, 'interface.block.delphi'):
            nameregion = 'meta.function.delphi'

        method.has_implementation = view.match_selector(
            cursor_pt, 'implementation.block.delphi')
        method.has_interface = view.match_selector(
            cursor_pt, 'interface.block.delphi')
        _isImpl = method.has_implementation
        if method.has_implementation:
            method.implementationdef = [r for r in selector(nameregion)
                                        if cursor_region.intersects(r)]

            method.paramdefimplreg, method.paramdefimpl, method.paramsimpl, \
                method.paramsnameimpl = method.paramsFromRegion(
                    method.implementationdef[0])
        else:
            method.interfacedef = [r for r in selector(nameregion)
                                   if cursor_region.intersects(r)]

            method.paramdefintreg, method.paramdefint, method.paramsint, \
                method.paramsnameint = method.paramsFromRegion(
                    method.interfacedef[0])

        method.methodregion = [r for r in selector(nameregion)
                               if cursor_region.intersects(r)]
        method.methodname = method.getFunctionName()

        method.variabledef, method.variables, \
            method.variablesname = method.getVariablesMethod()

        method.methodclass = self.getClassInformation(method)

        method.setDefMethod()

        if _isImpl:
            if method.interfacedef:
                method.paramdefintreg, method.paramdefint, method.paramsint, \
                    method.paramsnameint = method.paramsFromRegion(
                        method.interfacedef[0])
        else:
            if method.implementationdef:
                method.paramdefimplreg, method.paramdefimpl, \
                    method.paramsimpl, \
                    method.paramsnameimpl = method.paramsFromRegion(
                        method.implementationdef[0])
        method.setstoragetype()

        method.setVisibility()

        method.setFunctionReturn()

        return method

    def getClassInformation(self, method):

        def filterValidClasses():
            v = self.view
            selector = v.find_by_selector
            _classdefinition = selector('entity.class.interface.delphi')
            _class_name_region = selector('entity.name.section.delphi')
            exclude_list = []
            for s in _classdefinition:
                rowa, _ = v.rowcol(s.a)
                rowb, _ = v.rowcol(s.b)
                rowbb = rowb - 1
                if (rowa == rowb) or (rowa == rowbb):
                    exclude_list.append(s)

            for r in exclude_list:
                _classdefinition.remove(r)

            exclude_name_list = []
            for r in exclude_list:
                for s in _class_name_region:
                    if r.contains(s):
                        exclude_name_list.append(s)

            for r in exclude_name_list:
                _class_name_region.remove(r)
            return _classdefinition, _class_name_region

        _classdefinition, _class_name_region = filterValidClasses()

        classInfo = objectdef.ClassDeclaration(self.view)
        method_region = method.methodregion[0]

        v = self.view
        selector = v.find_by_selector
        cursor_region = v.sel()[0]
        cursor_pt = v.sel()[0].begin()

        if v.match_selector(cursor_pt, 'type.block.delphi'):
            classInfo.classregion = [
                s for s in _classdefinition
                # s for s in selector('entity.class.interface.delphi')
                if cursor_region.intersects(s)]

            classInfo.classname = v.substr([
                s for s in _class_name_region
                # s for s in selector('entity.name.section.delphi')
                if classInfo.classregion[0].intersects(s)][0])

            classInfo.privateregion = \
                classInfo.getVisibilityRegion('private')
            classInfo.privatemethods = \
                classInfo.getMethodsFromRegion(classInfo.privateregion)

            classInfo.protectedregion = \
                classInfo.getVisibilityRegion('protected')
            classInfo.protectedmethods = \
                classInfo.getMethodsFromRegion(classInfo.protectedregion)

            classInfo.publicregion = \
                classInfo.getVisibilityRegion('public')
            classInfo.publicmethods = \
                classInfo.getMethodsFromRegion(classInfo.publicregion)

            classInfo.publishedregion = \
                classInfo.getVisibilityRegion('published')
            classInfo.publishedmethods = \
                classInfo.getMethodsFromRegion(classInfo.publishedregion)
        else:
            classnamemethodfiltered = [
                s for s in selector('entity.class.name.delphi')
                if method_region.contains(s)]

            if classnamemethodfiltered != []:
                classInfo.classname = v.substr(
                    classnamemethodfiltered[0])

                classInfo.classregion = [
                    s for s in _classdefinition
                    # s for s in selector('entity.class.interface.delphi')
                    if self.validName(classInfo.classname, s)]

                classInfo.privateregion = \
                    classInfo.getVisibilityRegion('private')
                classInfo.privatemethods = \
                    classInfo.getMethodsFromRegion(classInfo.privateregion)

                classInfo.protectedregion = \
                    classInfo.getVisibilityRegion('protected')
                classInfo.protectedmethods = \
                    classInfo.getMethodsFromRegion(classInfo.protectedregion)

                classInfo.publicregion = \
                    classInfo.getVisibilityRegion('public')
                classInfo.publicmethods = \
                    classInfo.getMethodsFromRegion(classInfo.publicregion)

                classInfo.publishedregion = \
                    classInfo.getVisibilityRegion('published')
                classInfo.publishedmethods = \
                    classInfo.getMethodsFromRegion(classInfo.publishedregion)
            else:
                return None

        return classInfo

    def validName(self, name, region):
        import re
        return re.search('(?i)(\\b)' + name + '(\\b)',
                         self.view.substr(region)) is not None

    def getSelectorPTEnd(self, selector):
        view = self.view
        interface = view.find_by_selector(selector + '.block.delphi')
        line = interface[0].end()
        line, _ = view.rowcol(line)
        line -= 1
        pt = view.text_point(line, 0)
        return view.line(pt).end(), line


import sys
from time import time


def plugin_loaded():
    import sublime
    global Pref

    class Pref:

        def load(self):
            Pref.display_file = settings.get('display_file', False)
            Pref.display_class = settings.get('display_class', True)
            Pref.display_function = settings.get('display_function', True)
            Pref.display_arguments = settings.get('display_arguments', False)
            Pref.display_visibility = settings.get('display_visibility', True)
            Pref.wait_time = 0.12
            Pref.time = time()

    settings = sublime.load_settings('plugins-development.sublime-settings')
    # settings = sublime.load_settings('Method Name Display.sublime-settings')
    Pref = Pref()
    Pref.load()
    settings.add_on_change('reload', lambda: Pref.load())

if sys.version_info[0] == 2:
    plugin_loaded()


class FunctionNameStatusEventHandler(sublime_plugin.EventListener):

    def on_activated(self, view):
        import sublime
        Pref.time = time()
        sublime.set_timeout(
            lambda: self.display_current_class_and_function(view,
                                                            'activated'), 0)

    # could be async, but ST2 does not support that
    def on_selection_modified_async(self, view):
        import sublime
        now = time()
        if now - Pref.time > Pref.wait_time:
            sublime.set_timeout(lambda:
                                self.display_current_class_and_function(
                                    view, 'selection_modified'), 0)
        Pref.time = now

    # display the current class and function name
    def display_current_class_and_function(self, view, where):
        view_settings = view.settings()
        if view_settings.get('is_widget'):
            return

        if view.sel().__len__() < 1:
            return

        region = view.sel()[0]
        region_row, region_col = view.rowcol(region.begin())

        if region_row != view_settings.get('function_name_status_row', -1):
            view_settings.set('function_name_status_row', region_row)
        else:
            return

        delphi = DelphiIdeCommand(view)
        method = delphi.getMethodInformation()
        if not bool(method):
            return

        s = ""
        fname = view.file_name()
        if Pref.display_file and fname:
            s = fname + ' '

        if Pref.display_visibility and method.visibility:
            s += method.visibility + ' '

        # Look for any classes
        if Pref.display_class and method.methodclass:
            s += method.methodclass.classname + '.'

        # Look for any functions
        if Pref.display_function:
            s += method.methodname

        view.set_status('function', s)
