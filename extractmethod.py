import sublime
import sublime_plugin
import re


class ExtractMethodCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print("Extract Method")
        self.filterValidClasses()

        self.addMethod(edit)

    def filterValidClasses(self):
        view = self.view
        selector = view.find_by_selector
        self.settings = sublime.load_settings(
            'plugins-development.sublime-settings')
        self.method_regions = selector('function.implementation.delphi')
        self.methoddeclaration = selector('meta.function.delphi')
        self.classdefinition = selector('entity.class.interface.delphi')
        self.class_name_region = selector('entity.name.section.delphi')
        exclude_list = []
        for s in self.classdefinition:
            rowa, _ = self.view.rowcol(s.a)
            rowb, _ = self.view.rowcol(s.b)
            rowbb = rowb - 1
            if (rowa == rowb) or (rowa == rowbb):
                exclude_list.append(s)

        for r in exclude_list:
            self.classdefinition.remove(r)

        exclude_name_list = []
        for r in exclude_list:
            for s in self.class_name_region:
                if r.contains(s):
                    exclude_name_list.append(s)

        for r in exclude_name_list:
            self.class_name_region.remove(r)

    def addMethod(self, edit):
        view = self.view
        research = re.search
        vsubstr = view.substr
        self.cursor_region = view.sel()[0]
        cursor_region = self.cursor_region
        word_region = view.word(cursor_region)
        word = view.substr(word_region).strip()
        amount_selected_row = word.count('\n') + 1

        # Line and position to the new method
        line, ptinicio = self.getValidPosition()

        method_region = [
            s for s in self.method_regions if cursor_region.intersects(s)]

        methoddeclarationfiltered = [
            s for s in self.methoddeclaration if s.intersects(method_region[0])]

        class_name = self.getClassName()
        classnamefiltered = [s for s in self.class_name_region
                             if research('(?i)(\\b)' + class_name + '(\\b)',
                                         vsubstr(s)) is not None]
        # Class where the method will be included
        classdefinitionfiltered = list(self.classdefinition)
        for s in classdefinitionfiltered:
            for x in classnamefiltered:
                if not s.contains(x):
                    classdefinitionfiltered.remove(s)

        self.classdefinition = classdefinitionfiltered

        selection_text = view.substr(word_region).splitlines()
        params = self.getParametersName(methoddeclarationfiltered[0])
        params_def = self.getParametersName(
            methoddeclarationfiltered[0], False)
        variables, vars_def, vars_name = self.getVariablesMethod(
            self.getViewSel(cursor_region))

        vars_on_text = []
        if ((vars_name != []) and not (vars_name is None)):
            for text in selection_text:
                for name in vars_name:
                    if len(name) == 1:
                        continue

                    if research('(?i)(\\b)' + name + '(\\b)',
                                text) is not None:
                        if not (name in vars_on_text):
                            vars_on_text.append(name)
        params_on_text = []
        if ((params != []) and not (params is None)):
            for text in selection_text:
                for name in params:
                    if len(name) == 1:
                        continue

                    if research('(?i)(\\b)' + name + '(\\b)',
                                text) is not None:
                        if not (name in params_on_text):
                            params_on_text.append(name)

        param_tothe_method = []
        if vars_on_text:
            for v in vars_on_text:
                param_tothe_method += [s for s in vars_def if research(
                    '(?i)(\\b)' + v + '(\\b)', s) is not None]
        if params_on_text:
            for v in params_on_text:
                param_tothe_method += [s for s in params_def if research(
                    '(?i)(\\b)' + v + '(\\b)', s) is not None]

        parametros = ''
        if param_tothe_method != [] and not (param_tothe_method is None):
            parametros = '('
            for var in param_tothe_method:
                parametros += var + ';'
            parametros = self.removeLastStr(parametros, ';')
            parametros += ')'
        method = 'procedure ' + class_name + '.ExtractedMethod' + parametros + ';' + '\n'

        view.insert(edit, ptinicio, method)

        line_begin = line + 1
        pt = view.text_point(line_begin, 0)
        view.insert(edit, pt, 'begin' + ' \n')

        line_text = line_begin + 1
        pt = view.text_point(line_text, 0)
        word_region = self.getViewSel(view.sel()[0])

        method_body = ''
        for text in selection_text:
            method_body += text + '\n'
        view.insert(edit, pt, '  ' + method_body + ' \n')

        linha_end = line_text + 0 + amount_selected_row
        pt = view.text_point(linha_end, 0)
        view.insert(edit, pt, 'end;' + ' \n')

        params_declare = ''
        # divisor = ''

        if vars_on_text:
            for v in vars_on_text:
                params_declare += v + ', '
        if params_on_text:
            for v in params_on_text:
                params_declare += v + ', '

        params_declare = self.removeLastStr(params_declare, ', ')

        if params_declare:
            params_declare = '(' + params_declare + ')'

        view.replace(
            edit, word_region, '\n  ExtractedMethod' + params_declare + '; \n')

        linha, _ = view.rowcol(word_region.begin())

        ptnovo = view.text_point(linha, 2)

        selection_region = view.sel()[0]
        word_region = view.word(selection_region)
        view.sel().subtract(word_region)
        view.sel().add(ptnovo)

        self.addHeadMethod(edit, parametros)

        self.filter(edit, '')

    def removeLastStr(self, stri, sbstr):
        lenstr = len(stri)
        lensbstr = len(sbstr)
        if stri[lenstr - lensbstr:lenstr] == sbstr:
            return stri[0:lenstr - lensbstr]
        else:
            return stri

    # def adjustByPattern(self, variables, variable_on_text):
        # v = self.view
        # research = re.search
        # result = []
        # prefix_param = self.settings.get("prefix_param", {})

        # if not variables:
        #     return variables

        # for new_var in variable_on_text:
        #     for new_param in variables:
        #         if research('(\\b)' + new_var + '(\\b)', new_param) is None:
        #             continue

        #         if (new_param.find(';') > -1):
        #             end_pos = new_param.find(';')
        #         else:
        #             end_pos = len(new_param)
        #         type_p = new_param[new_param.find(
        #             ':') + 1:end_pos].strip()
        #         type_param = type_p.upper()

        #         param_prefix = ''
        #         if type_param in prefix_param:
        #             key = type_param
        #         else:
        #             key = 'ELSE'

        #         key_in = prefix_param[key]
        #         if (new_var[0: len(key_in)].upper() != key_in):
        #             if new_var[0:len(key_in) - 1].upper() == key_in[1:len(key_in)]:
        #                 param_prefix = key_in[0]
        #             else:
        #                 param_prefix = key_in

        #         result.append(
        #             param_prefix.lower() + new_var + ': ' + type_p + ';')
        # return result

    def getValidPosition(self):
        v = self.view

        def DisregardingCommentStartingBlock(line):

            line_decreases = True
            comment_previous_line = False
            while line_decreases:
                ptinicio = v.text_point(line, 0)
                comment_block_regions = v.find_by_selector(
                    'comment.block')

                if comment_block_regions:
                    for r in comment_block_regions:
                        ptinicio = v.text_point(line, 0)
                        if (((r.begin() < ptinicio) and (r.end() > ptinicio)) or
                                (r.begin() == ptinicio)):
                            ptinicio, line = self.lineDecreases(r, line)
                            comment_previous_line = True
                        else:
                            line_decreases = False

                comment_line_regions = v.find_by_selector(
                    'comment.line.double-slash')
                if comment_line_regions:
                    for r in comment_line_regions:
                        linha, _ = v.rowcol(r.begin())
                        ptinicio = v.text_point(line, 0)
                        if (((r.begin() < ptinicio) and (r.end() > ptinicio)) or
                                (r.begin() == ptinicio)):
                            ptinicio, line = self.lineDecreases(r, line)
                            comment_previous_line = True
                        else:
                            line_decreases = False
                else:
                    break

            if not comment_previous_line:
                line += 1
                ptinicio = v.text_point(line, 0)
            return line, ptinicio

        method_regions = self.method_regions
        next_method_region = [
            s for s in method_regions if self.cursor_region.end() < s.begin()]

        if next_method_region:
            line, _ = v.rowcol(next_method_region[0].begin())
            line -= 1
        else:
            next_method_region = v.find_by_selector(
                'implementation.block.delphi')
            line, _ = v.rowcol(next_method_region[0].end())
            line += -1

        return DisregardingCommentStartingBlock(line)

    def getParametersName(self, region_method, name=True):
        v = self.view

        def params(region):
            params_region = v.find_by_selector(
                'meta.function.parameters.delphi')
            param_name_region = v.find_by_selector(
                'variable.parameter.function.delphi')
            params_region_filt = [
                s for s in params_region if region.contains(s)]
            if name:
                params_region_filt = [
                    s for s in param_name_region if
                    params_region_filt[0].contains(s)]
            else:
                param_def = v.find_by_selector('param.delphi')
                params_region_filt = [
                    s for s in param_def if
                    params_region_filt[0].contains(s)]

            return params_region_filt

        def paramsFromRegion(region):
            try:
                params_region_filt = params(region)
                return [v.substr(x) for x in params_region_filt]
            except:
                return []
        return paramsFromRegion(region_method)

    def getVariablesMethod(self, word_region):
        v = self.view
        method_region = [
            s for s in self.method_regions if self.cursor_region.intersects(s)]
        method = [
            s for s in self.methoddeclaration if s.intersects(method_region[0])]
        end_block = v.find_by_selector('method.end.block.delphi')
        end_block = [
            s for s in end_block if s.intersects(method_region[0])]

        var_definitions = v.find_by_selector('var.block.delphi')
        var_definition = [
            s for s in var_definitions if s.intersects(method_region[0])]
        if not var_definition:
            return [], [], []

        if len(var_definition) > 1:
            if len(method) > 1:
                if var_definition[0].begin() < method[1].begin():
                    var_result = [var_definition[0]]
                elif end_block[len(end_block) - 1].end() < var_definition[len(var_definition) - 1].begin():
                    var_result = [var_definition[len(var_definition) - 1]]
        else:
            var_result = [var_definition[0]]

        var_name = v.find_by_selector('variable_name.function.delphi')
        var_name = [
            s for s in var_name if s.intersects(var_result[0])]
        var_def = v.find_by_selector('var.delphi')
        var_def = [
            s for s in var_def if s.intersects(var_result[0])]

        return [v.substr(s) for s in var_result], [v.substr(s) for s in var_def], [v.substr(s) for s in var_name]

    def getClassName(self):
        class_name = ''
        view = self.view
        vsubstr = view.substr
        selector = view.find_by_selector
        classnamemethod = selector('entity.class.name.delphi')
        method_regions = selector('function.implementation.delphi')

        self.method_region = [
            s for s in method_regions if self.cursor_region.intersects(s)]
        method_region = self.method_region
        classnamemethodfiltered = [
            s for s in classnamemethod if method_region[0].contains(s)]

        if classnamemethodfiltered:
            class_name = vsubstr(classnamemethodfiltered[0])

        return class_name

    def getViewSel(self, cursor_region):
        v = self.view
        selection_region = cursor_region
        word_region = v.word(selection_region)
        return word_region

    def addHeadMethod(self, edit, parametros):
        v = self.view
        head_region = self.getVisibilityRegion(edit)
        linha, _ = v.rowcol(head_region[0].begin())

        linha += 1
        pt = v.text_point(linha, 0)
        v.insert(
            edit, pt, '    procedure ExtractedMethod' +
            parametros + ';' + '\n')

    def getVisibilityRegion(self, edit):
        v = self.view
        extract_visibility = self.settings.get("extract_visibility", "private")
        createblock = self.settings.get("create_visibility_block", False)

        visibility_region = v.find_by_selector(
            extract_visibility + '.block.delphi')
        visibility_regionfiltered = [
            s for s in visibility_region if self.classdefinition[0].contains(s)]

        if not visibility_regionfiltered:
            if not createblock:
                print('Visibility ' + extract_visibility + ' do not exists.')
                return
            else:
                line = self.classdefinition[0].end()
                line, _ = v.rowcol(line)
                line -= 1
                pt = v.text_point(line, 0)
                pt = v.line(pt).end()
                tab_size = self.settings.get("tab_size")
                v.insert(edit, pt, '\n' + (' ' * tab_size) +
                         extract_visibility)
                pt = pt + tab_size + len(extract_visibility) + 2
                visibility_regionfiltered = [sublime.Region(
                    pt, pt + (tab_size * 2) - 5)]
        return visibility_regionfiltered

    def lineDecreases(self, region, line):
        line -= 1
        ptinicio = self.view.text_point(line, 0)
        if ((region.begin() < ptinicio) and (region.end() > ptinicio)):
            return self.lineDecreases(region, line)
        return ptinicio, line

    def filter(self, edit, needle):
        v = self.view
        regions = [s for s in v.sel() if not s.empty()]

        if len(regions) == 0:
            regions = [sublime.Region(0, v.size())]

        regiao_metodo_novo = 0

        v.sel().clear

        selection_region = v.sel()[0]
        word_region = v.word(selection_region)

        view_sel = v.sel()
        view_sel.subtract(word_region)

        for region in reversed(regions):
            lines = v.split_by_newlines(region)

            for line in reversed(lines):
                if 'ExtractedMethod' in v.substr(line):
                    # word_region = v.word(line)
                    # word = v.substr(word_region).strip()
                    regiao_do_metodo = v.find(
                        'ExtractedMethod', line.begin())
                    v.sel().add(regiao_do_metodo)

        v.show(regiao_do_metodo)
        return regiao_metodo_novo
