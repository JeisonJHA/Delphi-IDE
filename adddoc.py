import datetime
import os
import sublime_plugin
import sublime

datetimeformat = "%d/%m/%Y"
methoddocXML = True


def readSetting():
    global datetimeformat, methoddocXML
    settings = sublime.load_settings('delphi-ide.sublime-settings')
    if not (settings.get("doctype", "XML") in ["XML", "JAVADOC"]):
        sublime.message_dialog('"doctype" not configured.')
        return
    datetimeformat = settings.get("datetimeformat", "%d/%m/%Y")
    methoddocXML = settings.get("doctype", "XML") == "XML"


def tag():
    return 'Owner: ' + \
        os.environ['USERNAME'].title() + ' Date: ' + \
        datetime.datetime.now().strftime(datetimeformat)


class AddDocCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        try:
            print("Add doc")
            readSetting()
            DocObjetct = self.GetDocObject()
            DocObjetct.run()
        except Exception as e:
            print(e)

    def GetDocObject(self):
        def isIn(word):
            return view.match_selector(cursor_pt, word)

        view = self.view
        cursor_pt = view.sel()[0].begin()
        if isIn('meta.function.delphi'):
            return MethodDoc(view)
        if isIn('meta.property.delphi'):
            return PropertyDoc(view)
        if isIn('entity.class.interface.delphi') or \
                isIn('entity.record.delphi'):
            return ClassDoc(view)
        if isIn('entity.interface.delphi'):
            return InterfaceDoc(view)
        raise Exception('No doc for this.')


class Parser(object):
    """docstring for Parser"""

    def __init__(self, methoddocXML):
        if methoddocXML:
            self.DocParser = self.XMLDoc()
        else:
            self.DocParser = self.JAVADOCDoc()

    def parseDoc(self, info):
        return self.DocParser.parse(info)

    class Doc(object):
        """docstring for Doc"""

        def __init__(self):
            self.num = 0

        def parse(self, info):

            result = ""
            print('num:%s' % self.num)
            if 'summary' in info:
                result += self.GetSummary()
            if 'value' in info:
                result += self.GetValue(info)
            if 'remarks' in info:
                result += self.GetRemarks(info)
            if 'param' in info:
                result += self.GetParams(info['param'])
            if 'return' in info:
                result += self.GetReturn()
            if 'example' in info:
                result += self.GetExample()
            if 'exception' in info:
                result += self.GetException()
            return self.GetResult(result)

        def GetResult(self, result):
            return result

    class XMLDoc(Doc):
        """docstring for XMLDoc"""

        def GetSummary(self):
            self.num += 1
            return ('/// <summary>\n' +
                    '/// ${' + str(self.num) + '}\n' +
                    '/// </summary>\n')

        def GetValue(self, info):
            return ('/// <value>\n' +
                    '/// ' + info['value'] + '\n' +
                    '/// </value>\n')

        def GetRemarks(self, info):
            return ('/// <remarks>\n' +
                    '/// ' + info['remarks'] + '\n' +
                    '/// </remarks>\n')

        def GetParams(self, params):
            param_return = ''
            for variable in params:
                param_return += ('/// <param name="' + variable + '">\n' +
                                 '/// </param>\n')
            return param_return

        def GetReturn(self):
            self.num += 1
            return ('/// <return>\n' +
                    '/// ${' + str(self.num) + '}\n' +
                    '/// </return>\n')

        def GetExample(self):
            self.num += 1
            return ('/// <example>\n' +
                    '/// ${' + str(self.num) + '}\n' +
                    '/// </example>\n')

        def GetException(self):
            self.num += 1
            return ('/// <exception>\n' +
                    '/// ${' + str(self.num) + '}\n' +
                    '/// </exception>\n')

    class JAVADOCDoc(Doc):
        """docstring for JAVADOCDoc"""

        def GetResult(self, result):
            return "{\n" + result + "}\n"

        def GetSummary(self):
            self.num += 1
            return '  @Summary: ${' + str(self.num) + '}\n'

        def GetValue(self, info):
            return '  @Value: ' + info['value'] + '\n'

        def GetRemarks(self, info):
            return '  @Remarks: ' + info['remarks'] + '\n'

        def GetParams(self, params):
            param_return = ''
            for variable in params:
                param_return += ('  @Param: ' + variable + '\n')
            return param_return

        def GetReturn(self):
            self.num += 1
            return '  @Return: ${' + str(self.num) + '}\n'

        def GetExample(self):
            self.num += 1
            return '  @Example: ${' + str(self.num) + '}\n'

        def GetException(self):
            self.num += 1
            return '  @Exception: ${' + str(self.num) + '}\n'


class MethodDoc(object):
    """Methods Summary, Remarks, Parameters, Returns and Exceptions"""

    def __init__(self, view):
        self.view = view

    def run(self):
        view = self.view
        selector = view.find_by_selector
        cursor_region = view.sel()[0]

        methodsdeclaration = selector('meta.function.delphi')
        methodsreturn = selector('return.delphi')
        storages = selector('storage.type.function.delphi')
        method_region = [
            s for s in methodsdeclaration if cursor_region.intersects(s)]
        method_return = [
            s for s in methodsreturn if s.intersects(method_region[0])]
        storage = [
            s for s in storages if s.intersects(method_region[0])]

        params = self.paramsFromRegion(method_region[0])

        info = {}
        info['summary'] = ""
        info['remarks'] = tag()
        info['param'] = params
        if method_return:
            info['return'] = ""
        info['exception'] = ""

        docParser = Parser(methoddocXML)
        doc = docParser.parseDoc(info)

        view.sel().clear()
        view.sel().add(sublime.Region(storage[0].a, storage[0].a))
        view.run_command("insert_snippet", {"contents": "%s" % doc})
        view.show_at_center(method_region[0])

    def paramsFromRegion(self, region):

        def params(region):
            params_region = view.find_by_selector(
                'meta.function.parameters.delphi')
            param_name_region = view.find_by_selector(
                'variable.parameter.function.delphi')
            params_region_filt = [
                s for s in params_region if region.contains(s)]
            params_region_filt = [
                s for s in param_name_region
                if params_region_filt[0].contains(s)]
            return params_region_filt

        try:
            view = self.view
            vsubstr = view.substr
            params_region_filt = params(region)
            x = [vsubstr(x) for x in params_region_filt]
            return x
        except:
            return []

        return params_region_filt


class ClassDoc(object):
    """Classes/Records Summary, Remarks , Examples and Thread Safety"""

    def __init__(self, view):
        self.view = view

    def run(self):
        view = self.view
        selector = view.find_by_selector
        cursor_region = view.sel()[0]
        cursor_pt = cursor_region.begin()

        sdefinition = 'entity.class.interface.delphi'
        sname = 'entity.name.section.delphi'
        if not view.match_selector(cursor_pt, 'entity.class.interface.delphi'):
            sdefinition = 'entity.record.delphi'
            sname = 'entity.record.definition.delphi'

        classdefinitions = selector(sdefinition)
        classnames = selector(sname)
        class_region = [
            s for s in classdefinitions if cursor_region.intersects(s)]
        classname = [
            s for s in classnames if s.intersects(class_region[0])]

        info = {}
        info['summary'] = ""
        info['remarks'] = tag()
        info['example'] = ""

        docParser = Parser(methoddocXML)
        doc = docParser.parseDoc(info)

        view.sel().clear()
        view.sel().add(sublime.Region(classname[0].a, classname[0].a))
        view.run_command("insert_snippet", {"contents": "%s" % doc})
        view.show_at_center(cursor_region[0])


class InterfaceDoc(object):
    """Interfaces Summary, Remarks, Examples"""

    def __init__(self, view):
        self.view = view

    def run(self):
        view = self.view
        selector = view.find_by_selector
        cursor_region = view.sel()[0]

        interfacedefinitions = selector('entity.interface.delphi')
        interfacenames = selector('entity.name.interface.definition.delphi')
        interface_region = [
            s for s in interfacedefinitions if cursor_region.intersects(s)]
        interfacename = [
            s for s in interfacenames if s.intersects(interface_region[0])]

        info = {}
        info['summary'] = ""
        info['remarks'] = tag()
        info['example'] = ""

        docParser = Parser(methoddocXML)
        doc = docParser.parseDoc(info)

        view.sel().clear()
        view.sel().add(sublime.Region(interfacename[0].a, interfacename[0].a))
        view.run_command("insert_snippet", {"contents": "%s" % doc})
        view.show_at_center(cursor_region[0])


class PropertyDoc(object):
    """Properties Summary, Value, Remarks and Exceptions"""

    def __init__(self, view):
        self.view = view

    def run(self):
        view = self.view
        selector = view.find_by_selector
        cursor_region = view.sel()[0]

        propertysdeclaration = selector('meta.property.delphi')
        propertystype = selector('propertytype.delphi')
        storages = selector('storage.type.property.delphi')
        property_region = [
            s for s in propertysdeclaration if cursor_region.intersects(s)]
        property_type = [
            s for s in propertystype if s.intersects(property_region[0])]
        storage = [
            s for s in storages if s.intersects(property_region[0])]

        info = {}
        info['summary'] = ""
        info['value'] = view.substr(property_type[0])
        info['remarks'] = tag()
        info['exception'] = ""

        docParser = Parser(methoddocXML)
        doc = docParser.parseDoc(info)

        view.sel().clear()
        view.sel().add(sublime.Region(storage[0].a, storage[0].a))
        view.run_command("insert_snippet", {"contents": "%s" % doc})
        view.show_at_center(propertysdeclaration[0])
