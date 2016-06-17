import re
import sublime
import sublime_plugin


class declaremethod(sublime_plugin.TextCommand):

    def run(self, edit):
        print('Declare Method')
        global classdefinition
        global class_name_region
        global methoddeclaration
        global classnamemethod
        global method_regions
        global cursor_pt
        global cursor_region
        global methodnames
        global vsubstr
        global research
        global view
        global methodstype
        global functionsreturn
        global settings
        global propertysregion

        view = self.view
        research = re.search
        vsubstr = view.substr
        cursor_pt = view.sel()[0].begin()
        cursor_region = view.sel()[0]

        selector = view.find_by_selector
        classdefinition = selector('entity.class.interface.delphi')
        class_name_region = selector('entity.name.section.delphi')
        methoddeclaration = selector('meta.function.delphi')
        classnamemethod = selector('entity.class.name.delphi')
        method_regions = selector('function.implementation.delphi')
        methodnames = selector('entity.name.function')
        methodstype = selector('storage.type.function.delphi')
        functionsreturn = selector('return.type.delphi')
        propertysregion = selector('meta.property.delphi')

        settings = sublime.load_settings(
            'delphi-ide.sublime-settings')

        if(view.match_selector(cursor_pt, 'interface.block.delphi') or
            (view.match_selector(cursor_pt, 'program.delphi') and
             view.match_selector(cursor_pt, 'entity.class.interface.delphi'))):
            self.MethodInterface(edit)
        else:
            self.MethodImplementarion(edit)

    def MethodInterface(self, edit):
        view = self.view

        def getValidLine():
            if view.match_selector(cursor_pt, 'unit.block.delphi'):
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

        if not view.match_selector(cursor_pt, 'meta.function.delphi'):
                # exit because it is not in a method
            return

        methoddeclarationfiltered = [
            s for s in methoddeclaration if cursor_region.intersects(s)]

        classdefinitionfiltered = [
            s for s in classdefinition if s.contains(cursor_region)]

        if classdefinitionfiltered:

            class_name = vsubstr([s for s in class_name_region
                                  if s.intersects(classdefinitionfiltered[0])]
                                 [0]).strip()

        line = getValidLine()
        line, _ = view.rowcol(line)
        line -= 1
        tab_size = 0

        methodname = [
            s for s in methodnames if methoddeclarationfiltered[0].contains(s)]

        methodtype = [
            s for s in methodstype if methoddeclarationfiltered[0].contains(s)]

        functionreturn = [
            s for s in functionsreturn if methoddeclarationfiltered[0].contains(s)]

        params = self.params(methoddeclarationfiltered[0])
        method = ''
        method += vsubstr(methodtype[0]) + ' '

        if 'class_name' in vars():
            method += class_name + '.'

        method += vsubstr(methodname[0])

        if params:
            method += '(' + vsubstr(params[0]) + ')'

        if functionreturn:
            method += vsubstr(functionreturn[0])

        method += ';'
        pt = view.text_point(line, tab_size)
        pt = view.line(pt).end()

        method += '\n' + 'begin' + ' \n\n' + 'end;' + '\n'

        view.insert(edit, pt, '\n' + method)

    def MethodImplementarion(self, edit):
        view = self.view

        def validClass(s):
            r1, _ = view.rowcol(s.begin())
            r2, _ = view.rowcol(s.end())
            if (r1 == r2) or (r1 == (r2 - 1)):
                return False
            return True

        if not view.match_selector(cursor_pt,
                                   'function.implementation.delphi'):
            # exit because it is not in a method
            return

        method_region = [
            s for s in method_regions if cursor_region.intersects(s)]
        methoddeclarationfiltered = [
            s for s in methoddeclaration if method_region[0].intersects(s)]

        methodname = [
            s for s in methodnames if methoddeclarationfiltered[0].contains(s)]

        methodtype = [
            s for s in methodstype if methoddeclarationfiltered[0].contains(s)]

        functionreturn = [
            s for s in functionsreturn if method_region[0].contains(s)]

        params = self.params(methoddeclarationfiltered[0])
        method = ''
        method += vsubstr(methodtype[0]) + ' '

        method += vsubstr(methodname[0])

        if params:
            method += '(' + vsubstr(params[0]) + ')'

        if functionreturn:
            method += vsubstr(functionreturn[0])

        method += ';'

        classnamemethodfiltered = [
            s for s in classnamemethod if methoddeclarationfiltered[0].intersects(s)]

        if classnamemethodfiltered:
            classname = vsubstr(classnamemethodfiltered[0])
            classnamefiltered = [s for s in class_name_region
                                 if research('(\\b)' + classname +
                                             '(\\b)', vsubstr(s)) is not None]

            if not classnamefiltered:
                print("Class don't exists.")
                return

            classdefinitionfiltered = [
                s for s in classdefinition if validClass(s)]

            classdefinitionfiltered2 = list(classdefinitionfiltered)
            for s in classdefinitionfiltered:
                for x in classnamefiltered:
                    if not s.contains(x):
                        classdefinitionfiltered2.remove(s)

            classdefinitionfiltered = classdefinitionfiltered2

            visibility_regionfiltered = self. \
                getVisibilityRegion(edit,
                                    classdefinitionfiltered[0])

            propertysregionfiltered = [
                s for s in propertysregion if visibility_regionfiltered[0].
                contains(s)]

            if propertysregionfiltered:
                line = propertysregionfiltered[0].begin()
            else:
                line = visibility_regionfiltered[0].end()

            line, _ = view.rowcol(line)
            line -= 1
            tab_size = view.settings().get("tab_size") * 2
        else:
            if view.match_selector(cursor_pt, 'program.delphi'):
                return
            interface = view.find_by_selector('interface.block.delphi')

            line = interface[0].end()
            line, _ = view.rowcol(line)
            line -= 2
            tab_size = 0

        pt = view.text_point(line, 0)
        pt = view.line(pt).end()
        view.insert(edit, pt, '\n' + (' ' * tab_size) +
                    method)

    def getVisibilityRegion(self, edit, classdefinitionfiltered):
        visibility = settings.get("visibility", "private")
        createblock = settings.get("create_visibility_block", False)

        visibility_region = view.find_by_selector(
            visibility + '.block.delphi')
        visibility_regionfiltered = [
            s for s in visibility_region if classdefinitionfiltered.contains(s)]

        if not visibility_regionfiltered:
            if not createblock:
                print('Visibility ' + visibility + ' do not exists.')
                return
            elif createblock:
                line = classdefinitionfiltered.end()
                line, _ = view.rowcol(line)
                line -= 1
                pt = view.text_point(line, 0)
                pt = view.line(pt).end()
                tab_size = view.settings().get("tab_size")
                view.insert(edit, pt, '\n' + (' ' * tab_size) +
                            visibility)
                pt = pt + tab_size + len(visibility) + 2
                visibility_regionfiltered = [sublime.Region(
                    pt, pt + (tab_size * 2))]
        return visibility_regionfiltered

    def params(self, region):
        params_region = view.find_by_selector(
            'meta.function.parameters.delphi')

        return [s for s in params_region if region.contains(s)]
