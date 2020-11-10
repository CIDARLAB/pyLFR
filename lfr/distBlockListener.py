from typing import List, Tuple, Optional
from lfr.compiler.lfrerror import ErrorType, LFRError
from lfr.compiler.distribute.distributeblock import DistributeBlock
from lfr.antlrgen.lfrXParser import lfrXParser
from lfr.lfrbaseListener import LFRBaseListener, ListenerMode
from lfr.compiler.language.vectorrange import VectorRange
from lfr.compiler.distribute.BitVector import BitVector


class DistBlockListener(LFRBaseListener):

    def __init__(self) -> None:
        super().__init__()
        self._current_dist_block: Optional[DistributeBlock] = None
        self._current_sensitivity_list = None
        self._current_state: BitVector
        self._current_connectivities: List[Tuple[str, str]] = []
        # This particular variable is only used for
        # figuring out the else statement
        self._accumulated_states: List[BitVector] = []
        self._current_lhs = None

    def exitDistributeCondition(self, ctx: lfrXParser.DistributeConditionContext):
        rhs = self.stack.pop()
        lhs = self.stack.pop()

        relation_operator = ctx.binary_module_path_operator().getText()

        # TODO - Basically we need to know what the conditions are we need to set
        # the singals and the current state for the if statement

        # TODO - We only have a very limited range of validation right now
        # this needs to be extended to work with all kinds of conditions
        # not just 1 variable and the values of 0 or 1.
        assert(len(lhs) == 1)
        assert(rhs == 0 or rhs == 1)
        assert(relation_operator == '==')

        state_vector = self._current_dist_block.generate_state_vector([lhs], [rhs == 1])
        self._current_state = state_vector

    def enterDistributionBlock(self, ctx: lfrXParser.DistributionBlockContext):
        print("Entering the Distribution Block")
        # TODO - Instantiate the distribute graph or whatever class that encapsulates this
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
                        "Cannot find signal - {}".format(signal_name)
                    )
                )
                continue

            v = self.vectors[signal_name]

            if signal.vector() is not None:
                start_index = int(ctx.vector().start.text)
                end_index = int(ctx.vector().end.text)
            else:
                start_index = v.startindex
                end_index = v.endindex

            vrange = VectorRange(v, start_index, end_index)
            sentivity_list.append(vrange)

        self._current_dist_block.sensitivity_list = sentivity_list

    def exitDistributionBlock(self, ctx: lfrXParser.DistributionBlockContext):
        print("Exit the Distribution Block")
        # TODO - Generate the fig from the distribute block
        self._current_dist_block.generate_fig(self.currentModule.FIG)

    def enterDistributionassignstat(self, ctx: lfrXParser.DistributionassignstatContext):
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
                sourceid = source.id
                targetid = target.id

                self._current_connectivities.append((sourceid, targetid))

        elif len(lhs) != len(rhs):
            print("LHS not equal to RHS")
            for source in rhs:
                sourceid = source.id

                for target in lhs:
                    targetid = target.id
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
        self._accumulated_states.append(self._current_state)
        dist_block = self._current_dist_block
        for connectivity in self._current_connectivities:
            dist_block.set_connectivity(self._current_state, connectivity[0], connectivity[1])

    def exitElseIfBlock(self, ctx: lfrXParser.ElseIfBlockContext):
        # We need to go through all the current connectivities
        # and put them into the distribute block
        self._accumulated_states.append(self._current_state)
        dist_block = self._current_dist_block
        for connectivity in self._current_connectivities:
            dist_block.set_connectivity(self._current_state, connectivity[0], connectivity[1])

    def enterElseBlock(self, ctx: lfrXParser.ElseBlockContext):
        self._current_connectivities = []

    def exitElseBlock(self, ctx: lfrXParser.ElseBlockContext):
        remaining_states = self._current_dist_block.get_remaining_states(self._accumulated_states)
        for state in remaining_states:
            for connectivity in self._current_connectivities:
                self._current_dist_block.set_connectivity(state, connectivity[0], connectivity[1])

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
        assert(isinstance(rhs, BitVector))
        lhs = self._current_lhs
        dist_block = self._current_dist_block
        rhs_list = [rhs[i] == 1 for i in range(len(rhs))]
        state_vector = self._current_dist_block.generate_state_vector([lhs], rhs_list)
        self._current_state = state_vector

        for connectivity in self._current_connectivities:
            dist_block.set_connectivity(self._current_state, connectivity[0], connectivity[1])
