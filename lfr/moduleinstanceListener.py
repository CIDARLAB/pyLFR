from lfr.netlistgenerator import explicitmapping
from lfr.fig.fignode import FIGNode
from lfr.compiler.module import Module
from typing import Dict, Optional
from lfr.compiler.lfrerror import ErrorType, LFRError
from lfr.antlrgen.lfrXParser import lfrXParser
from lfr.distBlockListener import DistBlockListener


class ModuleInstanceListener(DistBlockListener):

    def __init__(self) -> None:
        super().__init__()
        self._module_to_import: Optional[Module] = None
        # There Ref -> Here Ref
        self._io_mapping: Dict[str, str] = dict()

    def enterModuleinstantiationstat(self, ctx: lfrXParser.ModuleinstantiationstatContext):
        # Check if the type exists in current compiler memory
        type_id = ctx.moduletype().getText()
        module_to_import = None
        for module_to_check in self.modules:
            if module_to_check.name == type_id:
                module_to_import = module_to_check
        if module_to_import is None:
            self.compilingErrors.append(LFRError(ErrorType.MODULE_NOT_FOUND, "Could find type {}".format(type_id)))
            return
        self._io_mapping = dict()
        self.currentModule.add_new_import(module_to_import)

        # Save the reference in the class
        self._module_to_import = module_to_import

    def exitModuleinstantiationstat(self, ctx: lfrXParser.ModuleinstantiationstatContext):
        # Create new instance of the import the type
        type_id = ctx.moduletype().getText()
        io_mapping = self._io_mapping
        var_name = ctx.instancename().getText()
        self.currentModule.instantiate_module(type_id, var_name, io_mapping)

    def exitOrderedioblock(self, ctx: lfrXParser.OrderedioblockContext):
        num_variables = len(ctx.vectorvar())
        # look at last num_variables in the stack and put them into the mapping
        variables = []
        for i in range(num_variables):
            variables.insert(0, self.stack.pop())

        # now go through the different connections in the module to import
        module_io = self._module_to_import.io
        assert(len(module_io) == num_variables)

        for i in range(num_variables):
            assert(len(module_io[i].vector_ref) == len(variables[i]))
            # Since both the lengths are the same, just make 1-1 connections here
            # REDO - Use this if we need to vector range level mapping
            # self._io_mapping[module_io[i].id] = variables[i].id
            there_vector_ref = module_io[i].vector_ref
            here_vector_ref = variables[i]
            for i in range(len(there_vector_ref)):
                self._io_mapping[there_vector_ref[i].id] = here_vector_ref[i].id

    # def exitUnorderedioblock(self, ctx: lfrXParser.UnorderedioblockContext):
    #     num_variables = len(ctx.explicitinstanceiomapping())
    #     variables = []
    #     for i in range(num_variables):
    #         variables.insert(0, self.stack.pop())

    #     module_io_labels = []
    #     for explicitmapping in ctx.explicitinstanceiomapping():
    #         module_io_labels.append(explicitmapping.ID().getText())


    def exitExplicitinstanceiomapping(self, ctx: lfrXParser.ExplicitinstanceiomappingContext):
        variable = self.stack.pop()
        label = ctx.ID().getText()

        # Check if label exists in module_to_import
        if label not in self._module_to_import.get_all_io():
            self.compilingErrors.append(LFRError(
                ErrorType.MODULE_IO_NOT_FOUND, 
                "Could not find io `{}` in module `{}`".format(
                    label,
                    self._module_to_import.name
                )))
            return

        io = self._module_to_import.get_io(label)
        assert(len(io.vector_ref) == len(variable))
        for i in range(len(variable)):
            self._io_mapping[io.vector_ref[i].id] = variable[i].id
