from PyQt6 import QtWidgets
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtCore import Qt, QMargins, QPointF


class modelingchart_handler:
    def __init__(self):
        self.chart_modeling = QChart()
        # self.is_phase_changed = False
        self.list_guide_time = None
        self.list_guide_amp = None
        self.list_guide_amp_shown = None

    def set_callback(self, name, func):
        setattr(self, name, func)

    def set_modeling_yaix_range_new(self):
        new_ymin, new_ymax = self.get_new_yrange()
        self.axis_y_modeling.setRange(new_ymin,new_ymax)

    def set_modeling_yaix_range_raw(self):
        new_ymin, new_ymax = self.get_raw_yrange()
        self.axis_y_modeling.setRange(new_ymin,new_ymax)

    def set_giude_data(self,):
        self.list_guide_time, self.list_guide_amp = self.get_guide_data()

    def chart_modeling_view(self):
        self.chart_modeling.setMargins(QMargins(0, 0, 0, 0))
        self.chart_modeling.setTitle("Modeling")


        self.axis_x_modeling = QValueAxis()
        self.axis_x_modeling.setTitleText("Time")
        self.chart_modeling.addAxis(self.axis_x_modeling, Qt.AlignmentFlag.AlignBottom)

        self.axis_y_modeling = QValueAxis()
        self.axis_y_modeling.setTitleText("Value")
        self.chart_modeling.addAxis(self.axis_y_modeling, Qt.AlignmentFlag.AlignLeft)
        
        series_empty = QLineSeries()
        self.chart_modeling.addSeries(series_empty)
        series_empty.attachAxis(self.axis_x_modeling)
        series_empty.attachAxis(self.axis_y_modeling)

        legend = self.chart_modeling.legend()
        legend.setVisible(False)
        
        
        self.chart_modeling_view = QChartView(self.chart_modeling)
        self.chart_modeling_view.setContentsMargins(0, 0, 0, 0)
        
        self.chart_modeling_view.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        return self.chart_modeling_view


    def Show_modeling_chart(self,):
        try:
            self.series_modeling = QLineSeries()
            self.set_giude_data()
            for x, y in zip(self.list_guide_time, self.list_guide_amp):
                self.series_modeling.append(QPointF(float(x), float(y)))
            for series in self.chart_modeling.series():
                self.chart_modeling.removeSeries(series)
                
            self.chart_modeling.addSeries(self.series_modeling)
            self.series_modeling.attachAxis(self.axis_x_modeling)
            self.series_modeling.attachAxis(self.axis_y_modeling)
            self.axis_x_modeling.setRange(min(self.list_guide_time),max(self.list_guide_time))
            raw_chart_time_min,raw_chart_time_max,raw_chart_val_min,raw_chart_val_max = self.get_raw_chart_range()
            self.axis_y_modeling.setRange(raw_chart_val_min,raw_chart_val_max)
            self.list_guide_amp_shown = self.list_guide_amp

            self.chart_modeling.setTitle("Modeling(range: {}-{})".format(raw_chart_time_min, raw_chart_time_max)) 
            self.print_terminal("Successed to generate guide-signal")

        except:
            self.print_terminal("Failed to show guide-signal")

    def Change_phase(self,):
        if self.list_guide_time is None:
            self.print_terminal_colored("Please load raw data first.")
            return
        
        self.chart_modeling.removeAllSeries()
        len_data = len(self.list_guide_time)

        

        
        self.series_modeling = QLineSeries()
        list_temp_amp = []
        list_changed_amp = []

        for i in range(len_data):
            y_temp = self.list_guide_amp_shown[i]
            if i < len_data/4:
                list_temp_amp.append(y_temp)
            else:
                list_changed_amp.append(y_temp)
            
        for temp_y in list_temp_amp:
            list_changed_amp.append(temp_y)
        self.list_guide_amp_shown = list_changed_amp

        for x, y in zip(self.list_guide_time, list_changed_amp):
            self.series_modeling.append(QPointF(float(x), float(y)))

        self.chart_modeling.addSeries(self.series_modeling)
        self.series_modeling.attachAxis(self.axis_x_modeling)
        self.series_modeling.attachAxis(self.axis_y_modeling)
                    


        