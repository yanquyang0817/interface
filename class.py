import sys
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtChart import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

global count
global stop
stop= True
def toggle_timer():
    global stop
    stop=not stop
class Window1(QChartView,QChart):
    def __init__(self, *args, **kwargs):
        super(Window1, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setWindowOpacity(0.1)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.chart_init()
        self.timer_init()



    def timer_init(self):  # 使用QTimer，2秒触发一次，更新数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.drawLine)
        self.timer.start(2000)

    def chart_init(self):
        self.chart = QChart()
        self.series = QSplineSeries()
        self.series2 = QSplineSeries()
        #设置曲线名称
        self.series.setName("模拟实时数据")
        self.series2.setName("实时数据")
        #把曲线添加到QChart的实例中
        self.chart.addSeries(self.series)
        self.chart.addSeries(self.series2)
        #声明并初始化X轴，Y轴
        self.dtaxisX = QDateTimeAxis()
        self.vlaxisY = QValueAxis()
        # 设置X轴的刻度线数量为5
        self.dtaxisX.setTickCount(5)
        # 设置Y轴的刻度线数量为6
        self.vlaxisY.setTickCount(6)
        #设置坐标轴显示范围
        self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-30*1))
        self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
        self.vlaxisY.setMin(0)
        self.vlaxisY.setMax(1500)
        #设置X轴时间样式
        self.dtaxisX.setFormat("hh")
        #设置坐标轴上的格点
        self.dtaxisX.setTickCount(5)
        self.vlaxisY.setTickCount(11)
        #设置坐标轴名称
        self.dtaxisX.setTitleText("时间")
        self.vlaxisY.setTitleText("预测光伏发电量")
        #设置网格不显示
        self.vlaxisY.setGridLineVisible(False)
        #把坐标轴添加到chart中
        self.chart.addAxis(self.dtaxisX,Qt.AlignBottom)
        self.chart.addAxis(self.vlaxisY,Qt.AlignLeft)
        #把曲线关联到坐标轴
        self.series.attachAxis(self.dtaxisX)
        self.series.attachAxis(self.vlaxisY)
        self.series2.attachAxis(self.dtaxisX)
        self.series2.attachAxis(self.vlaxisY)

        self.setChart(self.chart)
    def drawLine(self):
        global stop
        if stop:
            bjtime = QDateTime.currentDateTime()
            # 更新X轴坐标
            self.dtaxisX.setMin(QDateTime.currentDateTime().addSecs(-30 * 1))
            self.dtaxisX.setMax(QDateTime.currentDateTime().addSecs(0))
            # 当曲线上的点超出X轴的范围时，移除最早的点
            if (self.series.count() > 15):
                self.series.removePoints(0, self.series.count() - 15)
            if (self.series2.count() > 15):
                self.series2.removePoints(0, self.series2.count() - 15)

            # 产生随即数
            yint = random.randint(0, 1500)
            xint = random.randint(0, 1500)
            # 添加数据到曲线末端
            global count
            count = abs(yint - xint)
            self.series.append(bjtime.toMSecsSinceEpoch(), yint)
            self.series2.append(bjtime.toMSecsSinceEpoch(), xint)
class Window4(QMainWindow):
    def __init__(self):
        super().__init__()
        # 设置主窗口标题和大小
        self.setWindowTitle("可随时间变化的条形图")
        # 创建绘图部件、布局和添加到窗口中
        plot_widget = PlotWidget(self)
        main_layout = QVBoxLayout()
        main_layout.addWidget(plot_widget)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
class PlotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建画布和绘图区域对象
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # 设置画布的大小策略
        self.canvas.setSizePolicy(QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        self.canvas.updateGeometry()

        # 创建随时间变化的条形图
        self.max_x_data = 15
        self.x_data = list(range(1, self.max_x_data+1))
        self.y_data = [0 for _ in range(self.max_x_data)]
        self.ax.bar(self.x_data, self.y_data)
        self.ax.set_xlabel("时间")
        self.ax.set_ylabel("数值")
        self.ax.set_xlim(0, self.max_x_data+1)
        self.ax.set_ylim(0, max(self.y_data)+10)

        # 创建计时器，随时间变化
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(2000)

        # 布局该部件
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)

    def update_plot(self):
        """计时器事件，在该函数中实现动态效果"""
        # 让x和y坐标的数据随时间变化
        global stop
        global count
        if stop:
            new_y_data = count
            self.y_data.append(new_y_data)
            if len(self.y_data) > self.max_x_data:
                self.y_data.pop(0)
                self.x_data = list(range(1, self.max_x_data + 1))

            # 更新绘图区域
            self.ax.clear()
            if count>100:
                self.ax.bar(self.x_data, self.y_data,color='r')
            else:
                self.ax.bar(self.x_data, self.y_data)
            self.ax.set_xlabel("时间")
            self.ax.set_ylabel("数值")
            self.ax.set_xlim(0, self.max_x_data + 1)
            self.ax.set_ylim(0, max(self.y_data) + 10)
            self.canvas.draw()
class BeautifulLabel(QWidget):
    def __init__(self, text):
        super().__init__()

        # 初始化UI
        self.initUI(text)

    def initUI(self, text):
        # 创建QLabel对象
        self.label = QLabel(text, self)
        # 设置字体大小和样式
        self.label.setStyleSheet('''
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #FFFFFF;
                background-color: rgba(255, 255, 255, 0);
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 20px;
                }
        ''')
        # 居中显示
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        # 将文本框添加为窗口的子控件
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
class InputWidget(QWidget):
    def __init__(self,text):
        super().__init__()

        self.init_ui(text)

    def init_ui(self,text):
        # 创建输入框
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText(text)

        # 使用样式表设置输入框样式
        self.input_box.setStyleSheet("""
            border-radius: 10px;
            border: 2px solid gray;
            padding: 8px;
        """)

        # 创建一个垂直布局器，并将输入框添加到布局器中
        layout = QVBoxLayout()
        layout.addWidget(self.input_box)

        # 将布局器设置为 QWidget 的布局器
        self.setLayout(layout)
class Window_reason(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("光伏发电量影响因素")
        self.create_piechart()
        self.show()

    def create_piechart(self):
        # 创建QPieSeries对象，它用来存放饼图的数据
        series = QPieSeries()

        # append方法中的数字，代表的是权重，完成可以改成其它，如80,70,60等等
        series.append("温度", 8)
        series.append("湿度", 7)
        series.append("光照强度", 6)

        # 创建QChart实例，它是PyQt5中的类
        chart = QChart()
        # QLegend类是显示图表的图例，先隐藏掉
        chart.legend().hide()
        chart.addSeries(series)
        chart.createDefaultAxes()

        # 设置动画效果
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # 设置标题
        chart.setTitle("光伏发电影响因素")

        chart.legend().setVisible(True)

        # 对齐方式
        chart.legend().setAlignment(Qt.AlignBottom)
        # color = QColor(0, 10, 100)
        # color.setAlpha(200)
        # chart.setBackgroundBrush(color)
        # 创建ChartView，它是显示图表的控件
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(chartview)
class LineChart(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化UI
        self.initUI()
    def initUI(self):
        # 创建QChart对象
        chart = QChart()
        # 创建折线图数据
        lineseries = QLineSeries()
        # 添加折线图数据，这里X轴以月份为标签
        lineseries.append(1, 30)
        lineseries.append(2, 35)
        lineseries.append(3, 40)
        lineseries.append(4, 42)
        lineseries.append(5, 48)
        lineseries.append(6, 50)
        lineseries.append(7, 55)
        lineseries.append(8, 60)
        lineseries.append(9, 65)
        lineseries.append(10, 70)
        lineseries.append(11, 75)
        lineseries.append(12, 80)
        # 将折线图数据添加到QChart对象中
        chart.addSeries(lineseries)
        # 创建X轴标签
        axisX = QValueAxis()
        axisX.setRange(1, 12)
        axisX.setTitleText("Month")
        # 创建Y轴标签
        axisY = QValueAxis()
        axisY.setTitleText("Value")
        # 将X轴和Y轴添加到QChart对象中
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        # 将折线图数据绑定到X轴和Y轴上
        lineseries.attachAxis(axisX)
        lineseries.attachAxis(axisY)
        # 创建QChartView对象，将QChart对象传入
        chartview = QChartView(chart)
        # 在主窗口中添加QChartView控件
        self.setCentralWidget(chartview)
        # 设置窗口大小和标题
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('PyQt5 Line Chart Example')
class MyWindow(QWidget):
    def __init__(self):
        super().__init__() #调用父类的__init__方法，因为父类里面有许多初始化的操作
        self.resize(1700,1000)           #在类里面为self
        contain = QHBoxLayout()    #水平布局
        #最左侧布局
        box_right = QGroupBox("光伏发电信息")
        box_right.setStyleSheet("color: white;font-size: 20px;")
        layout_right = QVBoxLayout()
        w2=Window_reason()
        w_right1=BeautifulLabel("昨日发电量:")
        w_right2 = BeautifulLabel("今日预测发电量:")
        w_right3 = BeautifulLabel("发电功率:")
        layout_right.addWidget(w_right1)
        layout_right.addWidget(w_right2)
        layout_right.addWidget(w_right3)
        w_exampl=LineChart()
        layout_right.addWidget(w_exampl)
        box_right.setLayout(layout_right)
        contain.addWidget(box_right)
        #中间布局
        box_middle = QGroupBox("实时光伏发电量预测")
        box_middle.setStyleSheet("color: white;font-size: 20px;")
        layout_middle = QVBoxLayout()
        w1 = Window1()
        w1.setStyleSheet("background-color: transparent;")
        btn_middle1 = QPushButton("停止")
        btn_middle1.clicked.connect(toggle_timer)
        btn_middle1.setObjectName('halfTransparentButton')
        btn_middle1.setStyleSheet('font-size: 28px;font-weight: bold;color: #FFFFFF;background-color: rgba(255, 255, 255, 0);border: 1px solid #ccc;border-radius: 5px;padding: 20px;')
        w4=Window4()
        # 显示
        layout_middle.addWidget(w1)
        layout_middle.addWidget(w4)
        layout_middle.addWidget(btn_middle1)
        box_middle.setLayout(layout_middle)

        contain.addWidget(box_middle)

        #右侧布局
        layout_left = QVBoxLayout()
        #两个按钮水平布局
        layout_btn=QHBoxLayout()
        close = QtWidgets.QPushButton("")  # 关闭按钮
        mini = QtWidgets.QPushButton("")  # 最小化按钮
        close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        close.clicked.connect(self.close)
        mini.clicked.connect(self.showMinimized)
        layout_btn.addWidget(mini)
        layout_btn.addWidget(close)
        layout_left.addLayout(layout_btn)
        w_reason = Window_reason()
        input1=InputWidget("当前时间")
        input2=InputWidget('当前发电信息')
        layout_left.addWidget(input1)
        layout_left.addWidget(input2)

        layout_left.addWidget(w_reason)

        contain.addLayout(layout_left)


        self.setLayout(contain)

        # 设置背景图片
        palette = QPalette()
        pix = QPixmap("./img/OIP-C.jpg")
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)



if __name__ == '__main__':
    app=QApplication(sys.argv)
    w=MyWindow()
    w.show()
    app.exec()