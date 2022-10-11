from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
import sys, time, datetime
import pyttsx3

global pause, value, rvalue, lrvalue, rset_time, lrset_time, set_time, bwork, config
bwork = False
pause = True
value = 25
rvalue = 5
lrvalue = 15
set_time = value * 60
rset_time = rvalue * 60
lrset_time = lrvalue * 60
config = True


class MWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('ui/splash_screen.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.frameFinished.close()
        self.labelFinished.close()
        self.rsButton.close()

        global set_time, config
        self.thread = {}
        self.time_default = time.strftime('%M:%S', time.gmtime(set_time))

        self.labelPercentage.setText(self.time_default)

        self.stButton.clicked.connect(self.start_worker)
        self.psButton.clicked.connect(self.stop_worker)
        self.upButton.clicked.connect(self.upValue)
        self.downButton.clicked.connect(self.downValue)
        self.rsButton.clicked.connect(self.closeit)
        self.pushButton.clicked.connect(self.call)

        #self.upButton.clicked.connect(self.upValue)
        #self.downButton.clicked.connect(self.downValue)

    def start_worker(self):
        global pause, bwork
        if not bool(self.thread):
            self.thread[1] = ThreadClass(parent=None, index=1)
            self.thread[1].start()
            self.thread[1].any_signal.connect(self.my_function)
            self.thread[1].any_signal_2.connect(self.my_function_2)
            self.stButton.setIcon(QtGui.QIcon('img/pause.png'))
            print("changing icon")
            pause = False
        elif not pause:
            print("pausing")
            pause = True
            self.stButton.setIcon(QtGui.QIcon('img/play.png'))
        else:
            pause = False
            self.stButton.setIcon(QtGui.QIcon('img/pause.png'))
            self.psButton.setIcon(QtGui.QIcon('img/stop.png'))
            print("restarting")
            bwork = True


    def stop_worker(self):
        self.thread[1].stop()

    def my_function(self, counter):
        cnt = counter
        index = self.sender().index
        cnt = time.strftime('%M:%S', time.gmtime(cnt))
        self.labelPercentage.setText(str(cnt))

    def my_function_2(self, nws):
        newStylesheet = nws
        index = self.sender().index
        self.circularProgress.setStyleSheet(newStylesheet)

    def upValue(self):
        if config:
            global value, set_time
            value += 1
            if value > 59:
                value = 59
            set_time = value * 60
            print(set_time)
            self.frmt_time = time.strftime('%M:%S', time.gmtime(set_time))
            self.labelPercentage.setText(str(self.frmt_time))

    def downValue(self):
        if config:
            global value, set_time
            value -= 1
            if value < 0:
                value = 0
            set_time = value * 60
            print(set_time)
            self.frmt_time = time.strftime('%M:%S', time.gmtime(set_time))
            self.labelPercentage.setText(str(self.frmt_time))

    def closeit(self):
        self.frameFinished.close()
        self.labelFinished.close()
        self.rsButton.close()

    def call(self):
        if config:
            dialog = CustomDialog()
            dialog.show()
            mainWindow.close()


class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    any_signal_2 = QtCore.pyqtSignal(str)

    def __init__(self, parent=None, index=0):
        super(ThreadClass, self).__init__(parent)
        self.index = index
        self.is_running = True


    def run(self):

        def work():
            print("Starting thread...", self.index)
            global pause, set_time
            x = set_time
            stop_1 = 0
            stop_2 = 0 - 0.001
            for i in reversed(range(x)):
                while pause:
                    time.sleep(0.1)
                time.sleep(1)
                stop_1 = stop_1 + (1 / x)
                stop_2 = stop_2 + (1 / x)
                self.any_signal.emit(i)
                styleSheet = """
                            QFrame {
                                    border-radius: 150px;
                                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 130, 222, 0), stop:{STOP_2} rgba(97, 181, 255, 255))
                                    }
                            """
                newStylesheet = styleSheet.replace("{STOP_1}", str(stop_1)).replace("{STOP_2}", str(stop_2))
                self.any_signal_2.emit(newStylesheet)
                mainWindow.labelPercentage.setFont(QtGui.QFont('Roboto Thin', 40))

        def rest():
            print("Starting thread...", self.index)
            global pause, rset_time
            x = rset_time
            stop_1 = 0
            stop_2 = 0 - 0.001
            for i in reversed(range(x)):
                while pause:
                    time.sleep(0.1)
                time.sleep(1)
                stop_1 = stop_1 + (1 / x)
                stop_2 = stop_2 + (1 / x)
                self.any_signal.emit(i)
                styleSheet = """
                            QFrame {
                                    border-radius: 150px;
                                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 130, 222, 0), stop:{STOP_2} rgba(97, 181, 255, 255))
                                    }
                            """
                newStylesheet = styleSheet.replace("{STOP_1}", str(stop_1)).replace("{STOP_2}", str(stop_2))
                self.any_signal_2.emit(newStylesheet)

        def long_rest():
            print("Starting thread...", self.index)
            global pause, lrset_time
            x = lrset_time
            stop_1 = 0
            stop_2 = 0 - 0.001
            for i in reversed(range(x)):
                while pause:
                    time.sleep(0.1)
                time.sleep(1)
                stop_1 = stop_1 + (1 / x)
                stop_2 = stop_2 + (1 / x)
                self.any_signal.emit(i)
                styleSheet = """
                            QFrame {
                                    border-radius: 150px;
                                    background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 130, 222, 0), stop:{STOP_2} rgba(97, 181, 255, 255))
                                    }
                            """
                newStylesheet = styleSheet.replace("{STOP_1}", str(stop_1)).replace("{STOP_2}", str(stop_2))
                self.any_signal_2.emit(newStylesheet)

        def backtowork():
            global bwork, pause
            mainWindow.labelPercentage.setFont(QtGui.QFont('Roboto Thin', 12))
            mainWindow.labelPercentage.setText("Go back to work?")
            mainWindow.stButton.setIcon(QtGui.QIcon('img/v.png'))
            mainWindow.psButton.setIcon(QtGui.QIcon('img/x.png'))
            print("Debug")
            bwork = False
            pause = True

        def finished():
            mainWindow.frameFinished.show()
            mainWindow.labelFinished.show()
            mainWindow.rsButton.show()
            mainWindow.stButton.setIcon(QtGui.QIcon("img/start.png"))
            mainWindow.labelCredits.setText("by Stevan Carlon")
            mainWindow.pushButton.show()

        def voiceRest():
            engine = pyttsx3.init()
            engine.say("Descansar")
            engine.runAndWait()

        def voiceEndRest():
            engine = pyttsx3.init()
            engine.say("Fim do intervalo")
            engine.runAndWait()

        global config
        config = False
        if not config:
            mainWindow.pushButton.close()
        mainWindow.labelCredits.setText("[working...]")
        work()
        voiceRest()
        mainWindow.labelCredits.setText("[resting...]")
        mainWindow.labelLoadingInfo.setText("●⚬⚬⚬ ⚬⚬⚬⚬")
        rest()

        global bwork
        backtowork()
        while not bwork:
            mainWindow.labelPercentage.setText("Go back to work?")
            time.sleep(1)

        print("End of rest, going back to work.")
        mainWindow.labelCredits.setText("[working...]")
        work()
        voiceRest()
        mainWindow.labelCredits.setText("[resting...]")
        mainWindow.labelLoadingInfo.setText("●●⚬⚬ ⚬⚬⚬⚬")
        rest()
        voiceEndRest()

        backtowork()
        while not bwork:
            mainWindow.labelPercentage.setText("Go back to work?")
            time.sleep(1)

        print("End of rest, going back to work.")

        mainWindow.labelCredits.setText("[working...]")
        work()
        voiceRest()
        mainWindow.labelCredits.setText("[resting...]")
        mainWindow.labelLoadingInfo.setText("●●●⚬ ⚬⚬⚬⚬")
        rest()
        voiceEndRest()

        backtowork()
        while not bwork:
            mainWindow.labelPercentage.setText("Go back to work?")
            time.sleep(1)

        print("End of rest, going back to work.")

        mainWindow.labelCredits.setText("[working...]")
        work()
        voiceRest()
        mainWindow.labelCredits.setText("[resting...]")
        mainWindow.labelLoadingInfo.setText("●●●● ⚬⚬⚬⚬")
        long_rest()
        voiceEndRest()

        backtowork()
        while not bwork:
            mainWindow.labelPercentage.setText("Go back to work?")
            time.sleep(1)

        print("End of rest, going back to work.")

        mainWindow.labelCredits.setText("[working...]")
        work()
        voiceRest()
        mainWindow.labelCredits.setText("[resting...]")
        mainWindow.labelLoadingInfo.setText("●●●● ●⚬⚬⚬")
        rest()
        voiceEndRest()

        backtowork()
        while not bwork:
            mainWindow.labelPercentage.setText("Go back to work?")
            time.sleep(1)

        print("End of rest, going back to work.")

        mainWindow.labelCredits.setText("[working...]")
        work()
        voiceRest()
        mainWindow.labelCredits.setText("[resting...]")
        mainWindow.labelLoadingInfo.setText("●●●● ●●⚬⚬")
        rest()
        voiceEndRest()

        backtowork()
        while not bwork:
            mainWindow.labelPercentage.setText("Go back to work?")
            time.sleep(1)

        print("End of rest, going back to work.")

        mainWindow.labelCredits.setText("[working...]")
        work()
        voiceRest()
        mainWindow.labelCredits.setText("[resting...]")
        mainWindow.labelLoadingInfo.setText("●●●● ●●●⚬")
        rest()
        voiceEndRest()

        backtowork()
        while not bwork:
            mainWindow.labelPercentage.setText("Go back to work?")
            time.sleep(1)

        print("End of rest, going back to work.")

        mainWindow.labelCredits.setText("[working...]")
        work()
        mainWindow.labelCredits.setText("[finished session]")
        mainWindow.labelLoadingInfo.setText("●●●● ●●●●")
        config = True
        finished()
        print("End of session.")

    def stop(self):
        print("Stopping thread...", self.index)
        global pause, config, set_time
        pause = True
        config = True
        mainWindow.stButton.setIcon(QtGui.QIcon('img/play.png'))
        mainWindow.psButton.setIcon(QtGui.QIcon('img/stop.png'))
        mainWindow.pushButton.show()
        mainWindow.labelCredits.setText("by Stevan Carlon")
        self.frmt_time = time.strftime('%M:%S', time.gmtime(set_time))
        print(set_time)
        self.any_signal.emit(0)
        mainWindow.thread.clear()
        self.terminate()
        mainWindow.labelPercentage.setText(self.frmt_time)


class CustomDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('ui/dialog.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.move(520, 205)

        self.upButton_1.clicked.connect(self.upValue)
        self.downButton_1.clicked.connect(self.downValue)
        self.upButton_2.clicked.connect(self.upValue_2)
        self.downButton_2.clicked.connect(self.downValue_2)
        self.upButton_3.clicked.connect(self.upValue_3)
        self.downButton_3.clicked.connect(self.downValue_3)

        self.wtime_default = time.strftime('%M:%S', time.gmtime(set_time))
        self.labelWValue.setText(self.wtime_default)
        self.rtime_default = time.strftime('%M:%S', time.gmtime(rset_time))
        self.labelWValue_2.setText(self.rtime_default)
        self.lrtime_default = time.strftime('%M:%S', time.gmtime(lrset_time))
        self.labelWValue_3.setText(self.lrtime_default)
        self.saveButton.clicked.connect(self.save)
        self.discardButton.clicked.connect(self.discard)

    def save(self):
        mainWindow.show()
        self.close()

    def discard(self):

        global value, rvalue, lrvalue, set_time, rset_time, lrset_time
        value = 25
        rvalue = 5
        lrvalue = 15
        set_time = value * 60
        rset_time = rvalue * 60
        lrset_time = lrvalue * 60
        self.frmt_time = time.strftime('%M:%S', time.gmtime(set_time))
        self.labelWValue.setText(str(self.frmt_time))
        mainWindow.labelPercentage.setText(str(self.frmt_time))
        self.rfrmt_time = time.strftime('%M:%S', time.gmtime(rset_time))
        self.labelWValue.setText(str(self.rfrmt_time))
        self.lrfrmt_time = time.strftime('%M:%S', time.gmtime(lrset_time))
        self.labelWValue.setText(str(self.lrfrmt_time))
        mainWindow.show()
        self.close()

    def upValue(self):
        global value, set_time
        value += 1
        if value > 59:
            value = 59
        set_time = value * 60
        print(set_time)
        self.frmt_time = time.strftime('%M:%S', time.gmtime(set_time))
        self.labelWValue.setText(str(self.frmt_time))
        mainWindow.frmt_time = time.strftime('%M:%S', time.gmtime(set_time))
        mainWindow.labelPercentage.setText(str(mainWindow.frmt_time))

    def downValue(self):
        global value, set_time
        value -= 1
        if value < 0:
            value = 0
        set_time = value * 60
        print(set_time)
        self.frmt_time = time.strftime('%M:%S', time.gmtime(set_time))
        self.labelWValue.setText(str(self.frmt_time))
        mainWindow.frmt_time = time.strftime('%M:%S', time.gmtime(set_time))
        mainWindow.labelPercentage.setText(str(mainWindow.frmt_time))

    def upValue_2(self):
        global rvalue, rset_time
        rvalue += 1
        if rvalue > 59:
            rvalue = 59
        rset_time = rvalue * 60
        print(rset_time)
        self.frmt_time = time.strftime('%M:%S', time.gmtime(rset_time))
        self.labelWValue_2.setText(str(self.frmt_time))

    def downValue_2(self):
        global rvalue, rset_time
        rvalue -= 1
        if rvalue < 0:
            rvalue = 0
        rset_time = rvalue * 60
        print(rset_time)
        self.frmt_time = time.strftime('%M:%S', time.gmtime(rset_time))
        self.labelWValue_2.setText(str(self.frmt_time))

    def upValue_3(self):
        global lrvalue, lrset_time
        lrvalue += 1
        if lrvalue > 59:
            lrvalue = 59
        lrset_time = lrvalue * 60
        print(lrset_time)
        self.frmt_time = time.strftime('%M:%S', time.gmtime(lrset_time))
        self.labelWValue_3.setText(str(self.frmt_time))

    def downValue_3(self):
        global lrvalue, lrset_time
        lrvalue -= 1
        if lrvalue < 0:
            lrvalue = 0
        lrset_time = lrvalue * 60
        print(lrset_time)
        self.frmt_time = time.strftime('%M:%S', time.gmtime(lrset_time))
        self.labelWValue_3.setText(str(self.frmt_time))


app = QtWidgets.QApplication(sys.argv)
mainWindow = MWindow()
mainWindow.show()
sys.exit(app.exec_())
