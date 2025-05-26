from PyQt6 import QtWidgets
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QScatterSeries
from PyQt6.QtCore import Qt, QMargins, QPointF
from PyQt6.QtGui import QColor


class rawchart_handler:
    chart_raw = None
    axis_x_raw = None
    axis_y_raw = None
    list_raw_time = None
    list_raw_amp = None
    list_raw_time_peak = None
    list_raw_amp_peak  = None
    list_sel_time = None
    list_sel_amp = None
    sliced_min_time = None
    sliced_max_time = None
    min_raw_val = None
    max_raw_val = None
    

    def __init__(self):
        self.chart_raw = QChart()
        self.chart_peaks = QChart()

    def set_callback(self, name, func):
        setattr(self, name, func)

    def set_raw_data(self,):
        self.list_raw_time, self.list_raw_amp = self.get_raw_data_from_file()

    def chart_raw_view(self,):
        self.chart_raw.setMargins(QMargins(0, 0, 0, 0))
        self.chart_raw.setTitle("BLANK")
        self.axis_x_raw = QValueAxis()
        self.axis_x_raw.setTitleText("Time")
        self.chart_raw.addAxis(self.axis_x_raw, Qt.AlignmentFlag.AlignBottom)
        self.axis_y_raw = QValueAxis()
        self.axis_y_raw.setTitleText("Value")
        self.chart_raw.addAxis(self.axis_y_raw, Qt.AlignmentFlag.AlignLeft)
        
        series_empty = QLineSeries()
        self.chart_raw.addSeries(series_empty)
        series_empty.attachAxis(self.axis_x_raw)
        series_empty.attachAxis(self.axis_y_raw)
        legend = self.chart_raw.legend()
        legend.setVisible(False)
        QChartView_raw = QChartView(self.chart_raw)
        QChartView_raw.setContentsMargins(100, 100, 100, 100)
        QChartView_raw.setStyleSheet("padding:0px; margin:0px; border:0px;")
        
        QChartView_raw.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        return QChartView_raw

    def set_raw_chart_title(self,):
        mytitle = "File : {}".format(self.get_filename())
        self.chart_raw.setTitle(mytitle)

    def Show_raw_chart(self,):    
        try:
            series_file = QLineSeries()
            for x, y in zip(self.list_raw_time, self.list_raw_amp):
                series_file.append(QPointF(float(x), float(y)))
            
            for series in self.chart_raw.series():
                self.chart_raw.removeSeries(series)
            
            series_file.setColor(QColor("#0000FF"))
            self.chart_raw.addSeries(series_file)
            series_file.attachAxis(self.axis_x_raw)
            series_file.attachAxis(self.axis_y_raw)
            
            xmin = min(self.list_raw_time)
            xmax = max(self.list_raw_time)
            ymin = min(self.list_raw_amp)
            ymax = max(self.list_raw_amp)
            
            self.axis_x_raw.setRange(xmin,xmax)
            self.axis_y_raw.setRange(ymin,ymax)
            
            self.sliced_min_time = xmin
            self.sliced_max_time = xmax
            self.min_raw_val = ymin
            self.max_raw_val = ymax

            self.set_lineedit_raw_range()

            self.print_terminal("Successed to load data from the file")

        except:
            self.print_terminal("Failed to show data from the file")


    def get_raw_chart_range(self):
        return self.sliced_min_time, self.sliced_max_time, self.min_raw_val, self.max_raw_val

    def set_axis_range(self,):
        xmin,xmax,ymin,ymax = self.get_sliced_range()
        self.sliced_min_time = xmin
        self.sliced_max_time = xmax
        self.min_raw_val = ymin
        self.max_raw_val = ymax


        self.axis_x_raw.setRange(xmin,xmax)
        self.axis_y_raw.setRange(ymin,ymax)


    def show_peaks(self,):
        self.list_raw_time_peak, self.list_raw_amp_peak = self.get_raw_peaks()
        series_peaks = QScatterSeries()
        for x, y in zip(self.list_raw_time_peak, self.list_raw_amp_peak):
            series_peaks.append(QPointF(float(x), float(y)))
        self.chart_raw.addSeries(series_peaks)
        series_peaks.setMarkerSize(10)
        series_peaks.attachAxis(self.axis_x_raw)
        series_peaks.attachAxis(self.axis_y_raw)

    def show_sel(self,):
        try:
            self.list_sel_time, self.list_sel_amp =  self.get_selected_data()
        except:
            self.print_terminal_colored("Failed to load selected data")

        for i in range(len(self.list_sel_time)):
            each_list_selected_sliced_time = self.list_sel_time[i]
            each_list_selected_sliced_val = self.list_sel_amp[i]
            series_each = QLineSeries()

            for x, y in zip(each_list_selected_sliced_time, each_list_selected_sliced_val):
                series_each.append(QPointF(float(x), float(y)))
                
            series_each.setColor(QColor("#22AA00"))
            self.chart_raw.addSeries(series_each)
            series_each.attachAxis(self.axis_x_raw)
            series_each.attachAxis(self.axis_y_raw)
        
    def reset_raw_chart(self,):
        self.chart_raw.removeAllSeries()