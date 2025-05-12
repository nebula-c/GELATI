from gelati import core
import numpy as np

class Bridge:
    def __init__(self,):
        self.list_raw_time = []
        self.list_raw_amp = []
        self.list_model_time = []
        self.list_model_amp = []
        self.model_period = None
        self.time_for_1breath = None
        self.datarate = None
        self.interpolation_step = None
        self.index_range = None

        self.GM = core.guide_modeling()

    def set_raw_data(self,list_raw_time,list_raw_amp):
        self.list_raw_time = list_raw_time
        self.list_raw_amp = list_raw_amp

    def run_anzai(self,):
        self.setting_for_anzai()
        GM = self.GM

        GM.Set_interpolation_step(self.interpolation_step)
        GM.list_time = [float(x) for x in self.list_raw_time]
        GM.list_val = [float(x) for x in self.list_raw_amp]
        self.list_model_time = GM.list_time
        self.list_model_amp = GM.list_val

        GM.Peak_extract2(self.index_range)
        GM.Slicing_data()
        GM.Period_generate()
        GM.Guide_sample()

        self.list_model_amp = GM.list_guide
        self.model_period = GM.guide_period
        self.list_model_time = np.linspace(0, self.model_period, self.interpolation_step)

        return self.list_model_time, self.list_model_amp

    def setting_for_anzai(self,):
        self.time_for_1breath = 2
        self.datarate = 100
        self.interpolation_step = 100
        self.index_range = self.datarate * self.time_for_1breath




