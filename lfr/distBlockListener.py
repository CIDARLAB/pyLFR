from typing import List, Tuple
from lfr.compiler.lfrerror import ErrorType, LFRError
from lfr.compiler.distribute.distributeblock import DistributeBlock
from lfr.antlrgen.lfrXParser import lfrXParser
from lfr.lfrCompiler import LFRCompiler, ListenerMode
from lfr.compiler.language.vectorrange import VectorRange
from BitVector import BitVector


class DistBlockListener(LFRCompiler):

    def __init__(self) -> None:
        super().__init__()
        self._current_dist_block: DistributeBlock = None
        self._current_sensitivity_list = None
        self._current_state: BitVector = None
        self._current_connectivities: Tuple[str, str] = None
        # This particular variable is only used for
        # figuring out the else statement
        self._accumulated_states: List[BitVector] = None

    def enterDistributionBlock(self, ctx: lfrXParser.DistributionBlockContext):
        print("Entering the Distribution Block")
        # TODO - Instantiate the distribute graph or whatever class that encapsulates this
        self._current_dist_block = DistributeBlock()

    def enterSensitivitylist(self, ctx: lfrXParser.SensitivitylistContext):
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

        self._current_dist_block.sentivity_list = sentivity_list

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
        pass

    def enterIfElseBlock(self, ctx: lfrXParser.IfElseBlockContext):
        # TODO - Setup the class level variables necessary to capture
        # the various states necessary for distribute blocks
        pass

    def enterIfBlock(self, ctx: lfrXParser.IfBlockContext):
        self._current_connectivities = []
        self._accumulated_states = []

    def exitIfBlock(self, ctx: lfrXParser.IfBlockContext):
        # TODO - Get the condition(s) and store in the current state option
        # We need to figure out what kind of conditions would work or only
        # a single signal would work
        states = []
        # TODO - Modify this line to extract and parse the logic condition
        condition = "Logic Expresstion"
        states = self._current_dist_block.generate_states(condition)
        for state in states:
            for connectivity in self._current_connectivities:
                self._current_dist_block.set_connectivity(state, connectivity[0], connectivity[1])

    def enterElseIfBlock(self, ctx: lfrXParser.ElseIfBlockContext):
        self._current_connectivities = []

    def exitElseIfBlock(self, ctx: lfrXParser.ElseIfBlockContext):
        # TODO - Get the condition(s) and store in the current state option
        # This would have very much the identical code as the ifBlock
        states = []
        # TODO - Modify this line to extract and parse the logic condition
        condition = "Logic Expresstion"
        states = self._current_dist_block.generate_states(condition)
        for state in states:
            for connectivity in self._current_connectivities:
                self._current_dist_block.set_connectivity(state, connectivity[0], connectivity[1])

    def enterElseBlock(self, ctx: lfrXParser.ElseBlockContext):
        self._current_connectivities = []

    def exitElseBlock(self, ctx: lfrXParser.ElseBlockContext):
        states = self._current_dist_block.get_remaining_states(self._accumulated_states)
        for state in states:
            for connectivity in self._current_connectivities:
                self._current_dist_block.set_connectivity(state, connectivity[0], connectivity[1])
