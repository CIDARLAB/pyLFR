
from typing import Dict
from lfr.compiler.lfrerror import ErrorType, LFRError
from lfr.antlrgen.lfrXParser import lfrXParser
from lfr.distBlockListener import DistBlockListener


class ModuleInstanceListener(DistBlockListener):

    def __init__(self) -> None:
        super().__init__()
        self._io_mapping: Dict[str, str] = None

    def enterModuleinstantiationstat(self, ctx: lfrXParser.ModuleinstantiationstatContext):
        # Check if the type exists in current compiler memory
        type_id = ctx.moduletype().getText()
        module_to_import = None
        for module_to_check in self.modules:
            if module_to_check.name == type_id:
                module_to_import = module_to_check
        if module_to_import is None:
            self.compilingErrors.append(LFRError(ErrorType.MODULE_NOT_FOUND))
            return
        self._io_mapping = dict()

        self.currentModule.add_new_import(module_to_import)

    def exitModuleinstantiationstat(self, ctx: lfrXParser.ModuleinstantiationstatContext):
        # Create new instance of the import the type
        type_id = ctx.moduletype().getText()
        io_mapping = self._io_mapping
        var_name = self.stack.pop()
        self.currentModule.instantiate_module(type_id, var_name, io_mapping)
