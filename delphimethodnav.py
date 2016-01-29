import sublime_plugin
import re


class delphimethodnavCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print("Delphi method navigated")
        global classdefinition
        global class_name_region
        global methoddeclaration
        global classnamemethod
        global method_regions
        global cursor_pt
        global cursor_region
        global vsubstr
        global view
        global research
        global params

        research = re.search
        view = self.view
        cursor_pt = view.sel()[0].begin()
        cursor_region = view.sel()[0]
        vsubstr = view.substr

        selector = view.find_by_selector
        classdefinition = selector('entity.class.interface.delphi')
        class_name_region = selector('entity.name.section.delphi')
        methoddeclaration = selector('meta.function.delphi')
        classnamemethod = selector('entity.class.name.delphi')
        method_regions = selector('function.implementation.delphi')

        if view.match_selector(cursor_pt, 'interface.block.delphi'):
            self.findMethodInterface()
        else:
            self.findMethodImplementation()

    def params(self, region):
        params_region = view.find_by_selector(
            'meta.function.parameters.delphi')
        param_name_region = view.find_by_selector(
            'variable.parameter.function.delphi')
        params_region_filt = [s for s in params_region if region.contains(s)]
        params_region_filt = [
            s for s in param_name_region if params_region_filt[0].contains(s)]

        return params_region_filt

    def paramsFromRegion(self, region):
        try:
            params_region_filt = self.params(region)
            x = [vsubstr(x) for x in params_region_filt]
            return x
        except:
            return []

    def validateParamsFromRegion(self, region):
        try:
            params_region_filt = self.params(region)
            x = [vsubstr(x) for x in params_region_filt]
            return x == params
        except:
            return False

    def go(self, region):
        if len(region) > 1:
            region = [
                s for s in region if self.validateParamsFromRegion(s)]

        self.view.sel().clear()
        self.view.sel().add(region[0])
        self.view.show(region[0])

    def findMethodInterface(self):
        global params

        def name():
            vsymbols = view.symbols
            for method_name_region in methoddeclaration:
                if method_name_region.contains(cursor_pt):
                    return [s for s in vsymbols()
                            if method_name_region.contains(s[0])][0][1]
                else:
                    continue
                break

        if not view.match_selector(cursor_pt, 'meta.function.delphi'):
                # exit because it is not in a method
            return

        method_region = [
            s for s in methoddeclaration if cursor_region.intersects(s)]

        params = self.paramsFromRegion(method_region[0])
        try:
            class_region = [
                s for s in classdefinition if cursor_region.intersects(s)][0]

            class_name = vsubstr(
                [s for s in class_name_region
                 if s.intersects(class_region)][0]).strip()

            methoddecfiltered = [s for s in methoddeclaration
                                 if research('(\\b)' + class_name +
                                             '(\\b)', vsubstr(s)) is not None]
            name = name()
            methoddecfiltered = [s for s in methoddecfiltered
                                 if research('(\\b)' + name +
                                             '(\\b)', vsubstr(s)) is not None]

        except IndexError:
            implementation = view.find_by_selector(
                'implementation.block.delphi')

            methoddecfiltered = [
                s for s in methoddeclaration if implementation[0].contains(s)]

            name = name()
            methoddecfiltered = [s for s in methoddecfiltered
                                 if research('(\\b)' + name +
                                             '(\\b)', vsubstr(s)) is not None]

            methoddecfiltered2 = list(methoddecfiltered)

            for s in methoddecfiltered:
                for x in classnamemethod:
                    if s.contains(x):
                        methoddecfiltered2.remove(s)

            methoddecfiltered3 = list(methoddecfiltered2)

            for x in method_regions:
                for s in methoddecfiltered:
                    if x.contains(s) and x.begin() != s.begin():
                        methoddecfiltered3.remove(s)
            methoddecfiltered = methoddecfiltered3

        self.go(methoddecfiltered)

    def findMethodImplementation(self):
        global params
        if not view.match_selector(cursor_pt,
                                   'function.implementation.delphi'):
            # exit because it is not in a method
            return

        method_region = [
            s for s in method_regions if cursor_region.intersects(s)]

        params = self.paramsFromRegion(method_region[0])

        functionname = self.view.find_by_selector('entity.name.function')

        functionnamefiltered = [
            s for s in functionname if method_region[0].contains(s)]

        method_name = vsubstr(functionnamefiltered[0])

        classnamemethodfiltered = [
            s for s in classnamemethod if method_region[0].contains(s)]

        if classnamemethodfiltered != []:
            class_name = vsubstr(classnamemethodfiltered[0])

            classnamefiltered = [s for s in class_name_region
                                 if research('(\\b)' + class_name +
                                             '(\\b)', vsubstr(s)) is not None]

            classdefinitionfiltered = classdefinition

            classdefinitionfiltered2 = list(classdefinitionfiltered)
            for s in classdefinitionfiltered:
                for x in classnamefiltered:
                    if not s.contains(x):
                        classdefinitionfiltered2.remove(s)

            classdefinitionfiltered = classdefinitionfiltered2

            methoddecfiltered = [
                s for s in methoddeclaration if classdefinitionfiltered[0].contains(s)]

            methoddecfiltered = [s for s in methoddecfiltered
                                 if research('(\\b)' + method_name +
                                             '(\\b)', vsubstr(s)) is not None]

        else:
            interface = view.find_by_selector('interface.block.delphi')
            methoddecfiltered = [
                s for s in functionname if interface[0].contains(s)]

            methoddecfiltered = [s for s in methoddecfiltered
                                 if research('(\\b)' + method_name +
                                             '(\\b)', vsubstr(s)) is not None]

            for s in classdefinition:
                methoddecfiltered = [
                    x for x in methoddecfiltered if not s.contains(x)]

            methoddecfiltered = [
                s for s in methoddeclaration
                if s.contains(methoddecfiltered[0])]

        self.go(methoddecfiltered)
