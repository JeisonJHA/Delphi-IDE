class ClassDeclaration(object):
    """docstring for ClassDeclaration"""

    def __init__(self, view):
        self._view = view
        self._classname = None
        self._classregion = None
        self._privateregion = None
        self._privatemethods = None
        self._protectedregion = None
        self._protectedmethods = None
        self._publicregion = None
        self._publicmethods = None
        self._publishedregion = None
        self._publishedmethods = None

    @property
    def classname(self):
        return self._classname

    @classname.setter
    def classname(self, value):
        self._classname = value

    @property
    def classregion(self):
        return self._classregion

    @classregion.setter
    def classregion(self, value):
        self._classregion = value

    @property
    def privateregion(self):
        return self._privateregion

    @privateregion.setter
    def privateregion(self, value):
        self._privateregion = value

    @property
    def privatemethods(self):
        return self._privatemethods

    @privatemethods.setter
    def privatemethods(self, value):
        self._privatemethods = value

    @property
    def protectedregion(self):
        return self._protectedregion

    @protectedregion.setter
    def protectedregion(self, value):
        self._protectedregion = value

    @property
    def protectedmethods(self):
        return self._protectedmethods

    @protectedmethods.setter
    def protectedmethods(self, value):
        self._protectedmethods = value

    @property
    def publicregion(self):
        return self._publicregion

    @publicregion.setter
    def publicregion(self, value):
        self._publicregion = value

    @property
    def publicmethods(self):
        return self._publicmethods

    @publicmethods.setter
    def publicmethods(self, value):
        self._publicmethods = value

    @property
    def publishedregion(self):
        return self._publishedregion

    @publishedregion.setter
    def publishedregion(self, value):
        self._publishedregion = value

    @property
    def publishedmethods(self):
        return self._publishedmethods

    @publishedmethods.setter
    def publishedmethods(self, value):
        self._publishedmethods = value

    def getVisibilityRegion(self, visibility):
        visibility_region = self._view.find_by_selector(
            visibility + '.block.delphi')
        return [
            s for s in visibility_region if self.classregion[0].contains(s)]

    def getMethodsFromRegion(self, region):
        if not region:
            return []
        functions = self._view.find_by_selector('meta.function.delphi')
        return [
            s for s in functions if region[0].contains(s)]


class MethodDeclaration(object):
    """docstring for MethodDeclaration"""

    def __init__(self, view):
        self._view = view
        self._methodclass = None
        self._has_implementation = False
        self._implementationdef = None
        self._has_interface = False
        self._interfacedef = None
        self._visibility = None
        self._returntype = None
        self._returntypeimplregion = None
        self._returntypeinteregion = None
        self._fullreturntypeimplregion = None
        self._fullreturntypeinteregion = None
        self._paramdefimplreg = None
        self._paramdefimpl = None
        self._paramsimpl = None
        self._paramsnameimpl = None
        self._paramdefintreg = None
        self._paramdefint = None
        self._paramsint = None
        self._paramsnameint = None
        self._variabledef = None
        self._variables = None
        self._variablesname = None
        self._storagetype = None
        self._storagetyperegint = None
        self._storagetyperegimp = None

    def __str__(self):
        print('*' * 9 + 'delphimethodnav' + '*' * 9)
        print('storagetype:       %s' % self._storagetype)
        print('storagetyperegint: %s' % self._storagetyperegint)
        print('storagetyperegimp: %s' % self._storagetyperegimp)
        print('has_interface:     %s' % self._has_interface)
        print('interfacedef:      %s' % self._interfacedef)
        print('has_implementation:%s' % self._has_implementation)
        print('implementationdef: %s' % self._implementationdef)
        print('methodname:        %s' % self._methodname)
        print('methodregion:      %s' % self._methodregion)
        print('visibility:        %s' % self._visibility)
        print('returntype:        %s' % self._returntype)
        print('returntypeinte:    %s' % self._returntypeinteregion)
        print('returntypeimpl:    %s' % self._returntypeimplregion)
        print('fullreturntypeinte:%s' % self._fullreturntypeinteregion)
        print('fullreturntypeimpl:%s' % self._fullreturntypeimplregion)
        print('paramdefimplreg:   %s' % self._paramdefimplreg)
        print('paramdefimpl:      %s' % self._paramdefimpl)
        print('paramsimpl:        %s' % self._paramsimpl)
        print('paramsnameimpl:    %s' % self._paramsnameimpl)
        print('paramdefintreg:    %s' % self._paramdefintreg)
        print('paramdefint:       %s' % self._paramdefint)
        print('paramsint:         %s' % self._paramsint)
        print('paramsnameint:     %s' % self._paramsnameint)
        print('variabledef:       %s' % self._variabledef)
        print('variables:         %s' % self._variables)
        print('variablesname:     %s' % self._variablesname)

        print('methodclass:       %s' % self._methodclass)
        if self._methodclass:
            print('classname:         %s' % self._methodclass.classname)
            print('classregion:       %s' % self._methodclass.classregion)
            print('privateregion:     %s' % self._methodclass.privateregion)
            print('privateregion:     %s' % self._methodclass.privatemethods)
            print('protectedregion:   %s' % self._methodclass.protectedregion)
            print('protectedmethods:  %s' %
                  self._methodclass.protectedmethods)
            print('publicregion:      %s' % self._methodclass.publicregion)
            print('publicmethods:     %s' % self._methodclass.publicmethods)
            print('publishedregion:   %s' % self._methodclass.publishedregion)
            print('publishedmethods:  %s' %
                  self._methodclass.publishedmethods)
        print('-' * 99)

    def paramReg(self):
        try:
            if self._has_implementation:
                return self._paramsimpl
            elif self._has_interface:
                return self._paramsint
        except Exception:
            print('erro')

    def getNewMethodDef(self):
        _bparams = bool(self.paramReg())
        _params = ''
        if _bparams:
            _params = '; '.join(self.paramReg())
            _params = '(' + _params + ')'

        _classname = ''
        if not self._has_implementation and self._methodclass:
            _classname = self._methodclass.classname + '.'

        _returntype = ''
        if self._returntype:
            _returntype = ': ' + self._returntype
        return (self._storagetype + ' ' + _classname + self._methodname +
                _params + _returntype + ';')

    @property
    def has_implementation(self):
        return self._has_implementation

    @has_implementation.setter
    def has_implementation(self, value):
        self._has_implementation = value

    @property
    def implementationdef(self):
        return self._implementationdef

    @implementationdef.setter
    def implementationdef(self, value):
        self._implementationdef = value

    @property
    def has_interface(self):
        return self._has_interface

    @has_interface.setter
    def has_interface(self, value):
        self._has_interface = value

    @property
    def interfacedef(self):
        return self._interfacedef

    @interfacedef.setter
    def interfacedef(self, value):
        self._interfacedef = value

    @property
    def methodname(self):
        return self._methodname

    @methodname.setter
    def methodname(self, value):
        self._methodname = value

    @property
    def methodregion(self):
        return self._methodregion

    @methodregion.setter
    def methodregion(self, value):
        self._methodregion = value

    @property
    def visibility(self):
        return self._visibility

    @visibility.setter
    def visibility(self, value):
        self._visibility = value

    @property
    def returntypeimplregion(self):
        return self._returntypeimplregion

    @returntypeimplregion.setter
    def returntypeimplregion(self, value):
        self._returntypeimplregion = value

    @property
    def returntypeinteregion(self):
        return self._returntypeinteregion

    @returntypeinteregion.setter
    def returntypeinteregion(self, value):
        self._returntypeinteregion = value

    @property
    def fullreturntypeimplregion(self):
        return self._fullreturntypeimplregion

    @fullreturntypeimplregion.setter
    def fullreturntypeimplregion(self, value):
        self._fullreturntypeimplregion = value

    @property
    def fullreturntypeinteregion(self):
        return self._fullreturntypeinteregion

    @fullreturntypeinteregion.setter
    def fullreturntypeinteregion(self, value):
        self._fullreturntypeinteregion = value

    @property
    def returntype(self):
        return self._returntype

    @returntype.setter
    def returntype(self, value):
        self._returntype = value

    @property
    def paramdefimplreg(self):
        return self._paramdefimplreg

    @paramdefimplreg.setter
    def paramdefimplreg(self, value):
        self._paramdefimplreg = value

    @property
    def paramdefimpl(self):
        return self._paramdefimpl

    @paramdefimpl.setter
    def paramdefimpl(self, value):
        self._paramdefimpl = value

    @property
    def paramsimpl(self):
        return self._paramsimpl

    @paramsimpl.setter
    def paramsimpl(self, value):
        self._paramsimpl = value

    @property
    def paramsnameimpl(self):
        return self._paramsnameimpl

    @paramsnameimpl.setter
    def paramsnameimpl(self, value):
        self._paramsnameimpl = value

    @property
    def paramdefintreg(self):
        return self._paramdefintreg

    @paramdefintreg.setter
    def paramdefintreg(self, value):
        self._paramdefintreg = value

    @property
    def paramdefint(self):
        return self._paramdefint

    @paramdefint.setter
    def paramdefint(self, value):
        self._paramdefint = value

    @property
    def paramsint(self):
        return self._paramsint

    @paramsint.setter
    def paramsint(self, value):
        self._paramsint = value

    @property
    def paramsnameint(self):
        return self._paramsnameint

    @paramsnameint.setter
    def paramsnameint(self, value):
        self._paramsnameint = value

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    @property
    def variabledef(self):
        return self._variabledef

    @variabledef.setter
    def variabledef(self, value):
        self._variabledef = value

    @property
    def variablesname(self):
        return self._variablesname

    @variablesname.setter
    def variablesname(self, value):
        self._variablesname = value

    @property
    def methodclass(self):
        return self._methodclass

    @methodclass.setter
    def methodclass(self, value):
        self._methodclass = value

    @property
    def storagetype(self):
        return self._storagetype

    @storagetype.setter
    def storagetype(self, value):
        self._storagetype = value

    @property
    def storagetyperegint(self):
        return self._storagetyperegint

    @storagetyperegint.setter
    def storagetyperegint(self, value):
        self._storagetyperegint = value

    @property
    def storagetyperegimp(self):
        return self._storagetyperegimp

    @storagetyperegimp.setter
    def storagetyperegimp(self, value):
        self._storagetyperegimp = value

    def setstoragetype(self):
        v = self._view
        selector = v.find_by_selector
        storages = selector('storage.type.function.delphi')
        regstorageint = None
        regstorageimp = None
        if self._interfacedef:
            regstorageint = [
                n for n in storages if self._interfacedef[0].contains(n)]

        if self._implementationdef:
            regstorageimp = [
                n for n in storages if self._implementationdef[0].contains(n)]

        if regstorageint:
            _validregion = regstorageint[0]
        if regstorageimp:
            _validregion = regstorageimp[0]

        self._storagetype = v.substr(_validregion)
        self._storagetyperegint = regstorageint if not None else regstorageint[
            0]
        self._storagetyperegimp = regstorageimp if not None else regstorageimp[
            0]

    def paramsdefinition(self, region):
        v = self._view
        params_region = v.find_by_selector(
            'meta.function.parameters.delphi')
        param_name_region = v.find_by_selector(
            'variable.parameter.function.delphi')
        params = v.find_by_selector('param.delphi')
        params = [
            s for s in params if region.contains(s)]
        paramsdef = [
            s for s in params_region if region.contains(s)]
        paramsname = [
            s for s in param_name_region if
            paramsdef[0].contains(s)]

        return paramsname, paramsdef, params

    def paramsFromRegion(self, region):
        v = self._view
        try:
            _params_name_region, _paramsdefreg, _params = \
                self.paramsdefinition(region)
            _paramsdef = [v.substr(x) for x in _paramsdefreg]
            _paramsname = [v.substr(x) for x in _params_name_region]
            _params = [v.substr(x) for x in _params]
            return _paramsdefreg, _paramsdef, _params, _paramsname
        except:
            return [], [], [], []

    def getFunctionName(self):
        v = self._view
        functionname = v.find_by_selector('entity.name.function')
        functionnamefiltered = [
            n for n in functionname if self.methodregion[0].contains(n)]

        return v.substr(functionnamefiltered[0])

    def setFunctionReturn(self):
        v = self._view
        functionreturn = v.find_by_selector('return.type.delphi')
        functionreturnimplfiltered = None
        functionreturnintefiltered = None
        if self._interfacedef:
            functionreturnintefiltered = [
                n for n in functionreturn if self._interfacedef[0].contains(n)]

            if not functionreturnintefiltered:
                return

        if self._implementationdef:
            functionreturnimplfiltered = [
                n for n in functionreturn if self._implementationdef[0].contains(n)]

            if not functionreturnimplfiltered:
                return

        functionreturn = v.find_by_selector('return.delphi')

        fullfunctionreturnintefiltered = None
        if self._interfacedef:
            fullfunctionreturnintefiltered = [
                n for n in functionreturn if self._interfacedef[0].contains(n)]

        fullfunctionreturnimplfiltered = None
        if self._implementationdef:
            fullfunctionreturnimplfiltered = [
                n for n in functionreturn if self._implementationdef[0].contains(n)]

        if functionreturnimplfiltered:
            _validregion = functionreturnimplfiltered[0]
        if functionreturnintefiltered:
            _validregion = functionreturnintefiltered[0]

        self._returntype = v.substr(_validregion)
        self._returntypeimplregion = functionreturnimplfiltered if not None else functionreturnimplfiltered[
            0]
        self._returntypeinteregion = functionreturnintefiltered if not None else functionreturnintefiltered[
            0]
        self._fullreturntypeimplregion = fullfunctionreturnimplfiltered if not None else fullfunctionreturnimplfiltered[
            0]
        self._fullreturntypeinteregion = fullfunctionreturnintefiltered if not None else fullfunctionreturnintefiltered[
            0]

    def getVariablesMethod(self):
        v = self._view
        selector = v.find_by_selector
        method_region = self.methodregion
        _method = [
            s for s in selector('meta.function.delphi')
            if s.intersects(method_region[0])]
        end_block = v.find_by_selector('method.end.block.delphi')
        end_block = [
            s for s in end_block if s.intersects(method_region[0])]

        var_definitions = v.find_by_selector('var.block.delphi')
        var_definition = [
            s for s in var_definitions if s.intersects(method_region[0])]
        if not var_definition:
            return [], [], []

        if len(var_definition) > 1:
            if len(_method) > 1:
                if var_definition[0].begin() < _method[1].begin():
                    var_result = [var_definition[0]]
                elif (end_block[len(end_block) - 1].end() <
                      var_definition[len(var_definition) - 1].begin()):
                    var_result = [var_definition[len(var_definition) - 1]]
        else:
            var_result = [var_definition[0]]

        var_name = selector('variable_name.function.delphi')

        var_name = [
            s for s in var_name if s.intersects(var_result[0])]
        var_def = selector('var.delphi')
        var_def = [
            s for s in var_def if s.intersects(var_result[0])]

        return [v.substr(s) for s in var_result], \
            [v.substr(s) for s in var_def], [v.substr(s) for s in var_name]

    def setVisibility(self):
        if not self._methodclass:
            return

        if not self._has_interface:
            return

        for r in self._methodclass.privatemethods:
            if r.intersects(self._interfacedef[0]):
                self._visibility = 'private'
                pass

        for r in self._methodclass.protectedmethods:
            if r.intersects(self._interfacedef[0]):
                self._visibility = 'protected'
                pass

        for r in self._methodclass.publicmethods:
            if r.intersects(self._interfacedef[0]):
                self._visibility = 'public'
                pass

        for r in self._methodclass.publishedmethods:
            if r.intersects(self._interfacedef[0]):
                self._visibility = 'published'
                pass

    def setDefMethod(self):
        def validName(name, region):
            import re
            return re.search('(?i)(\\b)' + name + '(\\b)',
                             v.substr(region)) is not None

        def validateParamsFromRegion(region):
            _, _, _params, _ = self.paramsFromRegion(region)
            if self.has_implementation:
                return _params == self._paramsimpl
            else:
                return _params == self._paramsint

        v = self._view
        selector = v.find_by_selector
        if self._has_implementation:
            nameregion = 'meta.function.delphi'
            if self._methodclass:
                self._interfacedef = [
                    r for r in selector(nameregion)
                    if self._methodclass.classregion[0].contains(r)
                    and (validName(self._methodname, r))]                
            else:
                interfaceblock = selector('interface.block.delphi')
                typeblock = selector('type.block.delphi')
                self._interfacedef = [r for r in selector(nameregion)
                                      if interfaceblock[0].intersects(r) and
                                      (not typeblock[0].intersects(r))]

            if len(self._interfacedef) > 1:
                if not self.paramReg():
                    raise Exception(
                        'There is a duplicate statement on the interface for this method')
                    # mostrar mensagem mostrando que a
                    # declaração do método está
                    # duplicada.
                self._interfacedef = [
                    s for s in self._interfacedef
                    if validateParamsFromRegion(s)]
                if len(self._interfacedef) > 1:
                    raise Exception(
                        'There is a duplicate statement on the interface for this method')
            self._has_interface = bool(self._interfacedef)
        else:
            _implementationblock = selector('implementation.block.delphi')

            _implementationmethods = [
                s for s in selector('meta.function.delphi')
                if _implementationblock[0].contains(s)]
            _implementationmethods = [s for s in _implementationmethods
                                      if validName(self._methodname, s)]

            _functionimplementation = selector(
                'function.implementation.delphi')
            if self._methodclass:
                _classnamemethodfiltered = [
                    s for s in selector('entity.class.name.delphi')
                    if validName(self._methodclass.classname, s)]

                self._implementationdef = []
                for c in _classnamemethodfiltered:
                    for m in _implementationmethods:
                        if c.intersects(m):
                            self._implementationdef.append(m)
                            break

                _implementationdef2 = []
                for m in self._implementationdef:
                    for fr in _functionimplementation:
                        if m.intersects(fr):
                            _implementationdef2.append(fr)
                            break
                self._implementationdef = _implementationdef2
            else:
                self._implementationdef = []
                _r = [m for m in _implementationmethods
                      if not v.match_selector(
                          m.begin() + 11, 'entity.class.name.delphi')]
                self._implementationdef = _r                

            if len(self._implementationdef) > 1:
                self._implementationdef = [
                    s for s in self._implementationdef
                    if validateParamsFromRegion(s)]
                
                if len(self._implementationdef) > 1:
                    raise Exception(
                        'There is a duplicate statement on the implementarion for this method')
            self._has_implementation = bool(self._implementationdef)