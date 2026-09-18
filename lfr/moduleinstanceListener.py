from typing import Dict, Optional, Set

from lfr.antlrgen.lfr.lfrXParser import lfrXParser
from lfr.compiler.lfrerror import ErrorType, LFRError
from lfr.compiler.module import DROPLET_GENERATOR_PORTS, DIY_SIDES, Module
from lfr.distBlockListener import DistBlockListener


class ModuleInstanceListener(DistBlockListener):
    def __init__(self) -> None:
        super().__init__()
        self._module_to_import: Optional[Module] = None
        # There Ref -> Here Ref
        self._io_mapping: Dict[str, str] = {}
        # Optional Verilog-style #(length=…, width=…) instance parameters
        self._instance_params: Dict[str, float] = {}
        # DIYcomponent: up/right/down/left → here net id or None
        self._diy_side_bindings: Optional[Dict[str, Optional[str]]] = None
        self._diy_sides_seen: Set[str] = set()

    def enterModuleinstantiationstat(
        self, ctx: lfrXParser.ModuleinstantiationstatContext
    ):
        if self.currentModule is None:
            raise ValueError("currentModule set to None")

        # Check if the type exists in current compiler memory
        type_id = ctx.moduletype().getText()
        module_to_import = None
        for module_to_check in self.modules:
            if module_to_check.name == type_id:
                module_to_import = module_to_check
        if module_to_import is None:
            self.compilingErrors.append(
                LFRError(
                    ErrorType.MODULE_NOT_FOUND, "Could find type {}".format(type_id)
                )
            )
            self._module_to_import = None
            self._diy_side_bindings = None
            return
        self._io_mapping = {}
        self._instance_params = {}
        self._diy_sides_seen = set()
        if module_to_import.name == "DIYcomponent":
            self._diy_side_bindings = {side: None for side in DIY_SIDES}
        else:
            self._diy_side_bindings = None
        self.currentModule.add_new_import(module_to_import)

        # Save the reference in the class
        self._module_to_import = module_to_import

    def exitModuleinstantiationstat(
        self, ctx: lfrXParser.ModuleinstantiationstatContext
    ):
        if self.currentModule is None:
            raise ValueError("currentModule set to None")

        # Create new instance of the import the type
        type_id = ctx.moduletype().getText()
        io_mapping = self._io_mapping
        var_name = ctx.instancename().getText()

        # Parse optional #(length=10000, width=8000, height=2000, componentSpacing=2000)
        instance_params: Dict[str, float] = {}
        param_list = ctx.moduleparamlist()
        if param_list is not None:
            for param_ctx in param_list.moduleparam():
                key = param_ctx.ID().getText()
                value = float(param_ctx.number().getText())
                instance_params[key] = value

        if (
            type_id == "DIYcomponent"
            and self._diy_side_bindings is not None
            and self._module_to_import is not None
        ):
            missing = [s for s in DIY_SIDES if s not in self._diy_sides_seen]
            if missing:
                self.compilingErrors.append(
                    LFRError(
                        ErrorType.MODULE_IO_NOT_FOUND,
                        "DIYcomponent `{}` must list all sides up/right/down/left "
                        "(use None for unused); missing: {}".format(
                            var_name, ", ".join(missing)
                        ),
                    )
                )
                return
            self.currentModule.instantiate_diy_component(
                var_name,
                self._diy_side_bindings,
                self._module_to_import,
                instance_params=instance_params or None,
            )
            return

        if type_id == "droplet_generator" and self._module_to_import is not None:
            missing = [p for p in DROPLET_GENERATOR_PORTS if p not in io_mapping]
            if missing:
                self.compilingErrors.append(
                    LFRError(
                        ErrorType.MODULE_IO_NOT_FOUND,
                        "droplet_generator `{}` requires oil_left, oil_right, "
                        "aqueous, droplets; missing: {}".format(
                            var_name, ", ".join(missing)
                        ),
                    )
                )
                return
            self.currentModule.instantiate_droplet_generator(
                var_name,
                io_mapping,
                self._module_to_import,
                instance_params=instance_params or None,
            )
            return

        self.currentModule.instantiate_module(
            type_id, var_name, io_mapping, instance_params=instance_params or None
        )

    def exitOrderedioblock(self, ctx: lfrXParser.OrderedioblockContext):
        num_variables = len(ctx.vectorvar())
        # look at last num_variables in the stack and put them into the mapping
        variables = []
        for i in range(num_variables):
            variables.insert(0, self.stack.pop())

        # now go through the different connections in the module to import
        if self._module_to_import is None:
            raise ValueError("No module to import here")
        module_io = self._module_to_import.io
        assert len(module_io) == num_variables

        for k in range(num_variables):
            assert len(module_io[k].vector_ref) == len(variables[k])
            # Since both the lengths are the same, just make 1-1 connections here
            # REDO - Use this if we need to vector range level mapping
            # self._io_mapping[module_io[i].id] = variables[i].id
            there_vector_ref = module_io[k].vector_ref
            here_vector_ref = variables[k]
            for j in range(len(there_vector_ref)):
                self._io_mapping[there_vector_ref[j].ID] = here_vector_ref[j].ID

    def exitExplicitinstanceiomapping(
        self, ctx: lfrXParser.ExplicitinstanceiomappingContext
    ):
        # enterModuleinstantiationstat may have failed (MODULE_NOT_FOUND);
        # skip IO binding rather than crashing the walk.
        if self._module_to_import is None:
            return

        label = ctx.ID().getText()

        # DIYcomponent directional ports: .up(net) / .right(None) / …
        if self._diy_side_bindings is not None:
            if label not in DIY_SIDES:
                self.compilingErrors.append(
                    LFRError(
                        ErrorType.MODULE_IO_NOT_FOUND,
                        "DIYcomponent ports are up/right/down/left, not `{}`".format(
                            label
                        ),
                    )
                )
                return
            self._diy_sides_seen.add(label)
            if ctx.variables() is None:
                self._diy_side_bindings[label] = None
                return
            variable = self.stack.pop()
            if len(variable) != 1:
                self.compilingErrors.append(
                    LFRError(
                        ErrorType.MODULE_SIGNAL_BINDING_MISMATCH,
                        "DIYcomponent side `{}` expects a single net".format(label),
                    )
                )
                return
            self._diy_side_bindings[label] = variable[0].ID
            return

        variable = self.stack.pop()

        # Check if label exists in module_to_import
        if label not in [item.id for item in self._module_to_import.get_all_io()]:
            self.compilingErrors.append(
                LFRError(
                    ErrorType.MODULE_IO_NOT_FOUND,
                    "Could not find io `{}` in module `{}`".format(
                        label, self._module_to_import.name
                    ),
                )
            )
            return

        io = self._module_to_import.get_io(label)
        if len(io.vector_ref) != len(variable):
            self.compilingErrors.append(
                LFRError(
                    ErrorType.MODULE_SIGNAL_BINDING_MISMATCH,
                    "Number of module instance signals and variables don't match",
                )
            )
            return
        for i in range(len(variable)):
            self._io_mapping[io.vector_ref[i].ID] = variable[i].ID
