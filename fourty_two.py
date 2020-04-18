import sys
import PyQt5
from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class LoggingState(QtCore.QState):
    def __init__(self, name, childMode=QtCore.QState.ExclusiveStates, parent=None):
        super(LoggingState, self).__init__(childMode, parent)
        self.setObjectName(name)
        self.finished.connect(self.on_finished)

    def onEntry(self, event):
        print(self.objectName() + " entered")

    def onExit(self, event):
        print(self.objectName() + " exited")

    def on_finished(self):
        print(self.objectName() + " finished")


class LoggingFinalState(QtCore.QFinalState):
    def __init__(self, name, parent=None):
        super(LoggingFinalState, self).__init__(parent)
        self.setObjectName(name)

    def onEntry(self, event):
        print(self.objectName() + " entered")

    def onExit(self, event):
        print(self.objectName() + " exited")


class LoggingHistoryState(QtCore.QHistoryState):
    def __init__(self, name, historyType=QtCore.QHistoryState.ShallowHistory, parent=None):
        super(LoggingHistoryState, self).__init__(historyType, parent)
        self.setObjectName(name)

    def onEntry(self, event):
        print(self.objectName() + " entered")

    def onExit(self, event):
        print(self.objectName() + " exited")


class EasyKeyTransition(QtWidgets.QKeyEventTransition):
    def __init__(self, eventSource, sourceState, targetState, key):
        super(EasyKeyTransition, self).__init__(eventSource, QtCore.QEvent.KeyPress, key)
        self.setTargetState(targetState)
        sourceState.addTransition(self)


class CompareITransition(QtCore.QAbstractTransition):
    def __init__(self, fourty_two, sourceState, targetState):
        super(CompareITransition, self).__init__(sourceState)
        self.setTargetState(targetState)
        self.fourty_two = fourty_two

    def eventTest(self, e):
        if   self.fourty_two.i%2 == 0 and self.targetState() == self.fourty_two.s19:
            print("source: " + self.sourceState().objectName() + " target: " + self.targetState().objectName() + " i = " + str(self.fourty_two.i))
            return True
        elif self.fourty_two.i%3 == 0 and self.targetState() == self.fourty_two.s20:
            print("source: " + self.sourceState().objectName() + " target: " + self.targetState().objectName() + " i = " + str(self.fourty_two.i))
            return True
        elif self.fourty_two.i%5 == 0 and self.targetState() == self.fourty_two.s21:
            print("source: " + self.sourceState().objectName() + " target: " + self.targetState().objectName() + " i = " + str(self.fourty_two.i))
            return True
        elif self.targetState() == self.fourty_two.s22:
            print("source: " + self.sourceState().objectName() + " target: " + self.targetState().objectName() + " i = " + str(self.fourty_two.i))
            return True
        else:
            print("source: " + self.sourceState().objectName() + " target: " + self.targetState().objectName() + " i = " + str(self.fourty_two.i) + " NO TRANSITION")
            return False

    def onTransition(self, event):
        pass    # NotImplementedError: QAbstractTransition.onTransition() is abstract and must be overridden


class MaxITransition(QtCore.QAbstractTransition):
    def __init__(self, max, sourceState, targetState):
        super(MaxITransition, self).__init__(sourceState)
        self.max = max
        self.setTargetState(targetState)

    def eventTest(self, e):
        if (e.type() != QtCore.QEvent.Type(QtCore.QEvent.User+1)):
            return False

        fourty_two = self.object()
        print("i = " + str(fourty_two.i))
        return (fourty_two.i > self.max)

    def onTransition(self, event):
        pass    # NotImplementedError: QAbstractTransition.onTransition() is abstract and must be overridden


class S1(LoggingState):
    def __init__(self, name, childMode, parent):
        super(S1, self).__init__(name, childMode, parent)
        self.fourty_two = parent

    def onEntry(self, event):
        self.fourty_two.i += 1
        print("FourtyTwo.i= " + str(self.fourty_two.i))


class S3(LoggingState):
    def __init__(self, key_source, name, childMode, parent):
        super(S3, self).__init__(name, childMode, parent)
        s3_1 = LoggingState("s3_1", QtCore.QState.ExclusiveStates, self)
        s3_1_final = LoggingFinalState("s3_1_final", s3_1)
        s3_1_1 = LoggingState("s3_1_1", QtCore.QState.ExclusiveStates, s3_1)
        s3_1.setInitialState(s3_1_1)
        s3_1_1.addTransition(s3_1_final)    # unconditional transition

        s3_2 = LoggingState("s3_2", QtCore.QState.ExclusiveStates, self)
        s3_2_final = LoggingFinalState("s3_2_final", s3_2)
        s3_2_1 = LoggingState("s3_2_1", QtCore.QState.ExclusiveStates, s3_2)
        s3_2_1_1_1 = LoggingState("s3_2_1_1_1", QtCore.QState.ExclusiveStates, s3_2_1)
        s3_2_1_1_1_1_1 = LoggingState("s3_2_1_1_1_1_1", QtCore.QState.ExclusiveStates, s3_2_1_1_1)
        s3_2.setInitialState(s3_2_1)
        s3_2_1.setInitialState(s3_2_1_1_1)
        s3_2_1_1_1.setInitialState(s3_2_1_1_1_1_1)
        s3_2_1_1_1_1_1.addTransition(EasyKeyTransition(key_source, s3_2_1_1_1_1_1, s3_2_final, QtCore.Qt.Key_D))

        s3_3 = LoggingState("s3_3", QtCore.QState.ExclusiveStates, self)
        s3_3_final = LoggingFinalState("s3_3_final", s3_3)
        s3_3_1 = LoggingState("s3_3_1", QtCore.QState.ExclusiveStates, s3_3)
        s3_3.setInitialState(s3_3_1)
        s3_3_1.addTransition(EasyKeyTransition(key_source, s3_3_1, s3_3_final, QtCore.Qt.Key_C))


class S5(LoggingState):
    def __init__(self, key_source, name, childMode, parent):
        super(S5, self).__init__(name, childMode, parent)
        s5 = self
        s5_final = LoggingFinalState("s5_final", s5)
        s5_1_1 = LoggingState("s5_1_1", QtCore.QState.ExclusiveStates, s5)
        s5_1_1_1_1 = LoggingState("s5_1_1_1_1", QtCore.QState.ExclusiveStates, s5_1_1)
        s5_1_1_1_1 = LoggingState("s5_1_1_1_1", QtCore.QState.ExclusiveStates, s5_1_1)
        s5_1_1_1_1_1_1 = LoggingState("s5_1_1_1_1_1_1", QtCore.QState.ExclusiveStates, s5_1_1_1_1)
        s5_1_1_1_1_1_2 = LoggingState("s5_1_1_1_1_1_2", QtCore.QState.ExclusiveStates, s5_1_1_1_1)
        s5.setInitialState(s5_1_1)
        s5_1_1.setInitialState(s5_1_1_1_1)
        s5_1_1_1_1.setInitialState(s5_1_1_1_1_1_1)
        s5_1_1_1_1_1_1.addTransition(EasyKeyTransition(key_source, s5_1_1_1_1_1_1, s5_1_1_1_1_1_2, QtCore.Qt.Key_A))
        s5_1_1_1_1_1_1.addTransition(EasyKeyTransition(key_source, s5_1_1_1_1_1_1, s5_final, QtCore.Qt.Key_E))


class S7(LoggingState):
    def __init__(self, key_source, name, childMode, parent):
        super(S7, self).__init__(name, childMode, parent)
        s7 = self

        self.s7_1_1 = LoggingState("s7_1_1", QtCore.QState.ExclusiveStates, s7)
        s7_1_1_1_1 = LoggingState("s7_1_1_1_1", QtCore.QState.ExclusiveStates, self.s7_1_1)
        s7_1_1_1_1_1_1 = LoggingState("s7_1_1_1_1_1_1", QtCore.QState.ExclusiveStates, s7_1_1_1_1)
        self.s7_1_1_1_1_1_1_1_1 = LoggingState("s7_1_1_1_1_1_1_1_1", QtCore.QState.ExclusiveStates, s7_1_1_1_1_1_1)
        s7.setInitialState(self.s7_1_1)
        self.s7_1_1.setInitialState(s7_1_1_1_1)
        s7_1_1_1_1.setInitialState(s7_1_1_1_1_1_1)
        s7_1_1_1_1_1_1.setInitialState(self.s7_1_1_1_1_1_1_1_1)


class FourtyTwo(QtCore.QStateMachine):
    def __init__(self, parent=None):
        super(FourtyTwo, self).__init__(parent)
        self.i = 0
        key_source = self.parent()
        machine_final = LoggingFinalState("machine_final", self)
        s1 = S1("s1", QtCore.QState.ExclusiveStates, self)
        s2 = LoggingState("s2", QtCore.QState.ExclusiveStates, self)
        s3 = S3(key_source, "s3", QtCore.QState.ParallelStates, self)
        s4 = LoggingState("s4", QtCore.QState.ExclusiveStates, self)
        s5 = S5(key_source, "s5", QtCore.QState.ExclusiveStates, self)
        s6 = LoggingState("s6", QtCore.QState.ExclusiveStates, self)
        s7 = S7(key_source, "s7", QtCore.QState.ExclusiveStates, self)
        s8 = LoggingState("s8", QtCore.QState.ExclusiveStates, self)
        s9 = LoggingState("s9", QtCore.QState.ExclusiveStates, self)

        s10 = LoggingState("s10", QtCore.QState.ExclusiveStates, self)
        s10_history = LoggingHistoryState("s10_history", QtCore.QHistoryState.ShallowHistory, s10)
        s10_1_1 = LoggingState("s10_1_1", QtCore.QState.ExclusiveStates, s10)
        s10_1_1_1_1 = LoggingState("s10_1_1_1_1", QtCore.QState.ExclusiveStates, s10_1_1)
        s10_1_1_1_2 = LoggingState("s10_1_1_1_2", QtCore.QState.ExclusiveStates, s10_1_1)
        s10_1_1_1_2_1_1 = LoggingState("s10_1_1_1_2_1_1", QtCore.QState.ExclusiveStates, s10_1_1_1_2)
        s10_1_2 = LoggingState("s10_1_2", QtCore.QState.ExclusiveStates, s10)
        s10_1_3 = LoggingState("s10_1_3", QtCore.QState.ExclusiveStates, s10)
        s10.setInitialState(s10_history)
        s10_history.setDefaultState(s10_1_2)
        s10_1_1.setInitialState(s10_1_1_1_1)
        s10_1_1_1_2.setInitialState(s10_1_1_1_2_1_1)
        s10_1_1.addTransition(EasyKeyTransition(key_source, s10_1_1, s10_1_1_1_2, QtCore.Qt.Key_H))
        s10_1_1.addTransition(EasyKeyTransition(key_source, s10_1_1, s10_1_3, QtCore.Qt.Key_A))
        s10_1_2.addTransition(EasyKeyTransition(key_source, s10_1_2, s10_1_1, QtCore.Qt.Key_G))
        s10_1_2.addTransition(EasyKeyTransition(key_source, s10_1_2, s10_1_3, QtCore.Qt.Key_A))

        s11 = LoggingState("s11", QtCore.QState.ExclusiveStates, self)
        s12 = LoggingState("s12", QtCore.QState.ExclusiveStates, self)

        s13 = LoggingState("s13", QtCore.QState.ExclusiveStates, self)
        s13_deep_history = LoggingHistoryState("s13_deep_history", QtCore.QHistoryState.DeepHistory, s13)
        s13_1_1 = LoggingState("s13_1_1", QtCore.QState.ExclusiveStates, s13)
        s13_1_1_1_1 = LoggingState("s13_1_1_1_1", QtCore.QState.ExclusiveStates, s13_1_1)
        s13_1_1_1_2 = LoggingState("s13_1_1_1_2", QtCore.QState.ExclusiveStates, s13_1_1)
        s13_1_1_1_2_1_1 = LoggingState("s13_1_1_1_2_1_1", QtCore.QState.ExclusiveStates, s13_1_1_1_2)
        s13_1_2 = LoggingState("s13_1_2", QtCore.QState.ExclusiveStates, s13)
        s13_1_3 = LoggingState("s13_1_3", QtCore.QState.ExclusiveStates, s13)
        s13.setInitialState(s13_deep_history)
        s13_deep_history.setDefaultState(s13_1_2)
        s13_1_1.setInitialState(s13_1_1_1_1)
        s13_1_1_1_2.setInitialState(s13_1_1_1_2_1_1)
        s13_1_1_1_1.addTransition(EasyKeyTransition(key_source, s13_1_1_1_1, s13_1_1_1_2, QtCore.Qt.Key_L))
        s13_1_1.addTransition(EasyKeyTransition(key_source, s13_1_1, s13_1_3, QtCore.Qt.Key_A))
        s13_1_2.addTransition(EasyKeyTransition(key_source, s13_1_2, s13_1_1, QtCore.Qt.Key_G))     # 42.png misses character "G" like for s10
        s13_1_2.addTransition(EasyKeyTransition(key_source, s13_1_2, s13_1_3, QtCore.Qt.Key_A))

        s14 = LoggingState("s14", QtCore.QState.ExclusiveStates, self)
        s15 = LoggingState("s15", QtCore.QState.ExclusiveStates, self)

        s16 = LoggingState("s16", QtCore.QState.ParallelStates, self)
        s16_1 = LoggingState("s16_1", QtCore.QState.ExclusiveStates, s16)
        s16_1_final = LoggingFinalState("s16_1_final", s16_1)
        s16_1_1 = LoggingState("s16_1_1", QtCore.QState.ExclusiveStates, s16_1)
        s16_1_2 = LoggingState("s16_1_2", QtCore.QState.ExclusiveStates, s16_1)
        s16_1_3 = LoggingState("s16_1_3", QtCore.QState.ExclusiveStates, s16_1)
        s16_1.setInitialState(s16_1_1)
        s16_1_2.addTransition(s16_1_final)  # uncoditional transition when finished
        s16_1_1.addTransition(EasyKeyTransition(key_source, s16_1_1, s16_1_2, QtCore.Qt.Key_Q))
        s16_1_1.addTransition(EasyKeyTransition(key_source, s16_1_1, s16_1_3, QtCore.Qt.Key_A))

        s16_2 = LoggingState("s16_2", QtCore.QState.ExclusiveStates, s16)
        s16_2_final = LoggingFinalState("s16_2_final", s16_2)
        s16_2_1 = LoggingState("s16_2_1", QtCore.QState.ExclusiveStates, s16_2)
        s16_2_2 = LoggingState("s16_2_2", QtCore.QState.ExclusiveStates, s16_2)
        s16_2_3 = LoggingState("s16_2_3", QtCore.QState.ExclusiveStates, s16_2)
        s16_2.setInitialState(s16_2_1)
        s16_2_2.addTransition(s16_2_final)  # uncoditional transition when finished
        s16_2_1.addTransition(EasyKeyTransition(key_source, s16_2_1, s16_2_2, QtCore.Qt.Key_P))
        s16_2_1.addTransition(EasyKeyTransition(key_source, s16_2_1, s16_2_3, QtCore.Qt.Key_A))

        s16_3 = LoggingState("s16_3", QtCore.QState.ExclusiveStates, s16)
        s16_3_final = LoggingFinalState("s16_3_final", s16_3)
        s16_3_1 = LoggingState("s16_3_1", QtCore.QState.ExclusiveStates, s16_3)
        s16_3_2 = LoggingState("s16_3_2", QtCore.QState.ExclusiveStates, s16_3)
        s16_3.setInitialState(s16_3_1)
        s16_3_2.addTransition(s16_3_final)  # uncoditional transition when finished
        s16_3_1.addTransition(EasyKeyTransition(key_source, s16_3_1, s16_3_2, QtCore.Qt.Key_Q))

        s16_4 = LoggingState("s16_4", QtCore.QState.ExclusiveStates, s16)
        s16_4_final = LoggingFinalState("s16_4_final", s16_4)
        s16_4_1 = LoggingState("s16_4_1", QtCore.QState.ExclusiveStates, s16_4)
        s16_4_2 = LoggingState("s16_4_2", QtCore.QState.ExclusiveStates, s16_4)
        s16_4_3 = LoggingState("s16_4_3", QtCore.QState.ExclusiveStates, s16_4)
        s16_4.setInitialState(s16_4_1)
        s16_4_2.addTransition(s16_4_final)  # uncoditional transition when finished
        s16_4_1.addTransition(EasyKeyTransition(key_source, s16_4_1, s16_4_2, QtCore.Qt.Key_Q))
        s16_4_1.addTransition(EasyKeyTransition(key_source, s16_4_1, s16_4_3, QtCore.Qt.Key_A))

        s17 = LoggingState("s17", QtCore.QState.ExclusiveStates, self)
        s18 = LoggingState("s18", QtCore.QState.ExclusiveStates, self)
        s18_with_R = LoggingState("s18_with_R", QtCore.QState.ExclusiveStates, self)
        # these states as members, because these states must be referenced by transitions
        self.s19 = LoggingState("s19", QtCore.QState.ExclusiveStates, self)
        self.s20 = LoggingState("s20", QtCore.QState.ExclusiveStates, self)
        self.s21 = LoggingState("s21", QtCore.QState.ExclusiveStates, self)
        self.s22 = LoggingState("s22", QtCore.QState.ExclusiveStates, self)
        self.s23 = LoggingState("s23", QtCore.QState.ExclusiveStates, self)
        self.s24 = LoggingState("s24", QtCore.QState.ExclusiveStates, self)

        self.setInitialState(s1)
        s1.addTransition(EasyKeyTransition(key_source, s1, s2, QtCore.Qt.Key_B))
        s1.addTransition(EasyKeyTransition(key_source, s1, s3, QtCore.Qt.Key_A))
        s3.addTransition(EasyKeyTransition(key_source, s3, s2, QtCore.Qt.Key_C))
        s3.addTransition(EasyKeyTransition(key_source, s3, s4, QtCore.Qt.Key_A))
        s3.addTransition(s3.finished, s5)   # unconditional transition after finished
        s5.addTransition(s5.finished, s7)   # unconditional transition after finished
        s5.addTransition(EasyKeyTransition(key_source, s5, s6, QtCore.Qt.Key_E))    # will be overwritten when in state s5_1_1_1_1_1_1
        s7.addTransition(EasyKeyTransition(key_source, s7, s8, QtCore.Qt.Key_F))
        s7.s7_1_1.addTransition(EasyKeyTransition(key_source, s7.s7_1_1, s9, QtCore.Qt.Key_A))
        s7.s7_1_1_1_1_1_1_1_1.addTransition(EasyKeyTransition(key_source, s7.s7_1_1_1_1_1_1_1_1, s10, QtCore.Qt.Key_F))
        s10_1_1.addTransition(EasyKeyTransition(key_source, s10_1_1, s11, QtCore.Qt.Key_I))
        s10.addTransition(EasyKeyTransition(key_source, s10, s13, QtCore.Qt.Key_K))
        s11.addTransition(EasyKeyTransition(key_source, s11, s10_history, QtCore.Qt.Key_J))
        s11.addTransition(EasyKeyTransition(key_source, s11, s12, QtCore.Qt.Key_A))

        s13.addTransition(EasyKeyTransition(key_source, s13, s16, QtCore.Qt.Key_O))
        s13_1_1.addTransition(EasyKeyTransition(key_source, s13_1_1, s14, QtCore.Qt.Key_M))
        s14.addTransition(EasyKeyTransition(key_source, s14, s15, QtCore.Qt.Key_A))
        s14.addTransition(EasyKeyTransition(key_source, s14, s13_deep_history, QtCore.Qt.Key_N))

        s16.addTransition(EasyKeyTransition(key_source, s16, s17, QtCore.Qt.Key_B))
        s16.addTransition(s16.finished, s18)

        s18.addTransition(CompareITransition(self, s18, self.s19))
        s18.addTransition(EasyKeyTransition(key_source, s18, s18_with_R, QtCore.Qt.Key_R))
        s18_with_R.addTransition(CompareITransition(self, s18_with_R, self.s20))
        s18_with_R.addTransition(CompareITransition(self, s18_with_R, self.s21))
        s18_with_R.addTransition(CompareITransition(self, s18_with_R, self.s22))
        self.s19.addTransition(self.s23)
        self.s20.addTransition(self.s23)
        self.s21.addTransition(self.s23)
        self.s22.addTransition(self.s23)
        self.s23.addTransition(EasyKeyTransition(key_source, self.s23, self.s24, QtCore.Qt.Key_T))
        self.s24.addTransition(MaxITransition(42-1, self.s24, machine_final))
        self.s24.addTransition(s1)
        self.start()


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.fourty_two = FourtyTwo(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.resize(110, 300)
    widget.show()
    sys.exit(app.exec())
