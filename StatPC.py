import sys
import os
import time
import psutil
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PerformanceMonitor(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(PerformanceMonitor, self).__init__(fig)
        self.setParent(parent)
        self.x = []
        self.y_cpu = []
        self.y_mem = []

    def update_plot(self, cpu_percent, mem_percent):
        self.x.append(time.time())
        self.y_cpu.append(cpu_percent)
        self.y_mem.append(mem_percent)
        self.axes.clear()
        self.axes.plot(self.x, self.y_cpu, 'r', label='CPU')
        self.axes.plot(self.x, self.y_mem, 'b', label='RAM')
        self.axes.set_title('Performance Monitor')
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Usage (%)')
        self.axes.legend()
        self.draw()

class App(QtWidgets.QMainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.setWindowTitle('Performance Monitor')
        self.setGeometry(200, 200, 800, 600)
        self.monitor = PerformanceMonitor(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.monitor)
        self.show()

    def update_data(self):
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        self.monitor.update_plot(cpu_percent, mem_percent)
        #if (cpu_percent==100 or mem_percent==100):
        #self.saveGeometry("C:\\Users\\Account2\\Desktop\\Progettini\\ciao.png")

    def start_monitoring(self, interval=1):
        self.timer = self.startTimer(interval * 1000)
        self.last_update_time = time.time()

    def timerEvent(self, event):
        if event.timerId() == self.timer:
            now = time.time()
            if now - self.last_update_time >= 1:
                self.update_data()
                self.last_update_time = now
                 
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.start_monitoring()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
