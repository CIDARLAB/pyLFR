from typing import List, Optional, Tuple

from lfr.antlrgen.lfr.lfrXParser import lfrXParser
from lfr.compiler.distribute.BitVector import BitVector
from lfr.compiler.distribute.distributeblock import DistributeBlock
from lfr.compiler.language.vectorrange import VectorRange
from lfr.compiler.lfrerror import ErrorType, LFRError
from lfr.lfrbaseListener import LFRBaseListener, ListenerMode


class DistBlockListener(LFRBaseListener):
    def __init__(self) -> None:
        super().__init__()
        self._current_dist_block: Optional[DistributeBlock] = None
        self._current_sensitivity_list = None
        self._current_state: Optional[BitVector]
        self._current_connectivities: List[Tuple[str, str]] = []
        # This particular variable is only used for
        # figuring out the else statement
        self._accumulated_states: List[BitVector] = []
        self._current_lhs = None

    def exitDistributeCondition(self, ctx: lfrXParser.DistributeConditionContext):
        rhs = self.stack.pop()
        lhs = self.stack.pop()

        if isinstance(rhs, BitVector):
            rhs = rhs.intValue()

        relation_operator = ctx.binary_module_path_operator().getText()

        # TODO - Basically we need to know what the conditions are we need to set
        # the singals and the current state for the if statement

        # TODO - We only have a very limited range of validation right now
        # this needs to be extended to work with all kinds of conditions
        # not just 1 variable and the values of 0 or 1.
        assert len(lhs) == 1
        if relation_operator != "==":
            raise NotImplementedError(
                'Did not implement distribute condition beyond "=="'
            )

        if type(rhs) == float or type(rhs) == int:
            if (rhs == 0 or rhs == 1) is False:
                raise NotImplementedError(
                    "Did not implement distribute condition to be beyond simple 1 or 0"
                    " conditions"
                )

        if self._current_dist_block is None:
            raise ValueError('"_current_dist_block" is set to None')

        state_vector = self._current_dist_block.generate_state_vector([lhs], [rhs == 1])
        self._current_state = state_vector

    def enterDistributionBlock(self, ctx: lfrXParser.DistributionBlockContext):
        print("Entering the Distribution Block")
        self._current_dist_block = DistributeBlock()

    def exitSensitivitylist(self, ctx: lfrXParser.SensitivitylistContext):
        sentivity_list = []

        # TODO - Go through the signals and then add then to the sentivity list
        for signal in ctx.signal():
            start_index = 0
            end_index = 0
            signal_name = signal.ID().getText()

            if signal_name not in self.vectors.keys():
                self.compilingErrors.append(
                    LFRError(
                        ErrorType.SIGNAL_NOT_FOUND,
                        "Cannot find signal - {}".format(signal_name),
                    )
                )
                continue

            v = self.vectors[signal_name]

            if signal.vector() is not None:
                start_index = int(signal.vector().start.text)
                if signal.vector().end is not None:
                    end_index = int(signal.vector().end.text)
                else:
                    end_index = start_index
            else:
                start_index = v.startindex
                end_index = v.endindex

            vrange = VectorRange(v, start_index, end_index)
            sentivity_list.append(vrange)

        if self._current_dist_block is None:
            raise ValueError('"_current_dist_block" is set to None')

        self._current_dist_block.sensitivity_list = sentivity_list

    def exitDistributionBlock(self, ctx: lfrXParser.DistributionBlockContext):
        print("Exit the Distribution Block")
        # TODO - Generate the fig from the distribute block
        if self._current_dist_block is None:
            raise ValueError('"_current_dist_block" is set to None')

        if self.currentModule is None:
            raise ValueError("Current module set to none")
        self._current_dist_block.generate_fig(self.currentModule.FIG)

    def enterDistributionassignstat(
        self, ctx: lfrXParser.DistributionassignstatContext
    ):
        print("Entering the dis assign stat")
        self.listermode = ListenerMode.DISTRIBUTE_ASSIGN_STAT_MODE
        pass

    def exitDistributionassignstat(self, ctx: lfrXParser.DistributionassignstatContext):
        print("Exiting the dist assign stat")
        rhs = self.stack.pop()
        lhs = self.stack.pop()

        # Do the same connectivity as we would do this in the normal assign
        # stat and save it for current state in the distblock object
        if len(lhs) == len(rhs):
            print("LHS, RHS sizes are equal")
            for source, target in zip(rhs, lhs):
                print(source, target)
                sourceid = source.ID
                targetid = target.ID

                self._current_connectivities.append((sourceid, targetid))

        elif len(lhs) != len(rhs):
            print("LHS not equal to RHS")
            for source in rhs:
                sourceid = source.ID

                for target in lhs:
                    targetid = target.ID
                    self._current_connectivities.append((sourceid, targetid))

    def enterIfElseBlock(self, ctx: lfrXParser.IfElseBlockContext):
        # TODO - Setup the class level variables necessary to capture
        # the various states necessary for distribute blocks
        self._accumulated_states = []

    def enterIfBlock(self, ctx: lfrXParser.IfBlockContext):
        self._current_connectivities = []
        self._accumulated_states = []

    def enterElseIfBlock(self, ctx: lfrXParser.ElseIfBlockContext):
        self._current_connectivities = []

    def exitIfBlock(self, ctx: lfrXParser.IfBlockContext):
        # We need to go through all the current connectivities
        # and put them into the distribute block
        if self._current_state is None:
            raise ValueError("No state set for if block")
        self._accumulated_states.append(self._current_state)
        if self._current_dist_block is None:
            raise ValueError('"_current_dist_block" is set to None')

        dist_block = self._current_dist_block
        for connectivity in self._current_connectivities:
            dist_block.set_connectivity(
                self._current_state, connectivity[0], connectivity[1]
            )

    def exitElseIfBlock(self, ctx: lfrXParser.ElseIfBlockContext):
        # We need to go through all the current connectivities
        # and put them into the distribute block
        if self._current_state is None:
            raise ValueError("No state set for if block")
        self._accumulated_states.append(self._current_state)

        if self._current_dist_block is None:
            raise ValueError('"_current_dist_block" is set to None')

        dist_block = self._current_dist_block
        for connectivity in self._current_connectivities:
            dist_block.set_connectivity(
                self._current_state, connectivity[0], connectivity[1]
            )

    def enterElseBlock(self, ctx: lfrXParser.ElseBlockContext):
        self._current_connectivities = []

    def exitElseBlock(self, ctx: lfrXParser.ElseBlockContext):
        if self._current_dist_block is None:
            raise ValueError('"_current_dist_block" is set to None')

        remaining_states = self._current_dist_block.get_remaining_states(
            self._accumulated_states
        )
        for state in remaining_states:
            for connectivity in self._current_connectivities:
                self._current_dist_block.set_connectivity(
                    state, connectivity[0], connectivity[1]
                )

    def enterCaseBlock(self, ctx: lfrXParser.CaseBlockContext):
        self._accumulated_states = []
        self._current_state = None

    def exitCaseBlockHeader(self, ctx: lfrXParser.CaseBlockHeaderContext):
        lhs = self.stack.pop()
        self._current_lhs = lhs

    def enterCasestat(self, ctx: lfrXParser.CasestatContext):
        self._current_connectivities = []

    def exitCasestat(self, ctx: lfrXParser.CasestatContext):
        rhs = self.stack.pop()
        assert isinstance(rhs, BitVector)
        lhs = self._current_lhs

        if self._current_dist_block is None:
            raise ValueError('"_current_dist_block" is set to None')

        dist_block = self._current_dist_block
        rhs_list = [rhs[i] == 1 for i in range(len(rhs))]
        if lhs is None:
            raise ValueError("LHS set to none in case stat")
        state_vector = self._current_dist_block.generate_state_vector([lhs], rhs_list)
        self._current_state = state_vector

        for connectivity in self._current_connectivities:
            dist_block.set_connectivity(
                self._current_state, connectivity[0], connectivity[1]
            )
