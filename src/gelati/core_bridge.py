from gelati import core
import numpy as np

class Bridge:
    def __init__(self,):
        self.list_raw_time      = None
        self.list_raw_amp       = None
        self.list_raw_time_peak = None
        self.list_raw_amp_peak  = None
        self.list_sel_time      = None
        self.list_sel_amp       = None
        self.list_model_time    = None
        self.list_model_amp     = None
        self.list_sliced_time   = None
        self.list_sliced_amp    = None
        self.model_period       = None
        self.time_for_1breath   = None
        self.datarate           = None
        self.interpolation_step = None
        self.index_range        = None
        self.filetype = None

        self.GM = core.guide_modeling()

    def set_raw_data(self,):
        self.list_raw_time, self.list_raw_amp = self.get_raw_data_from_file()
        self.list_raw_time_peak = None
        self.list_raw_amp_peak  = None
        self.list_sel_time      = None
        self.list_sel_amp       = None
        self.list_model_time    = None
        self.list_model_amp     = None
        self.list_sliced_time   = None
        self.list_sliced_amp    = None
        self.model_period       = None

    def set_callback(self, name, func):
        setattr(self, name, func)

    def guide_modeling_run(self,):
        if self.list_raw_time is None:
            self.print_terminal_colored("Please load raw data first.")
            return
        
        try:
            self.list_model_time, self.list_model_amp = self.run_modeling()
            if self.list_model_time is None or self.list_model_amp is None:
                self.print_terminal_colored("Please load raw data first.")
                return
            else:
                self.get_guide_data()
                self.Show_modeling_chart()
        except:
            self.print_terminal_colored("Modeling is not working")    
            
    def seeking_peak(self,):
        self.filetype = self.get_filetype()
        if self.filetype=="Abches":
            self.setting_for_abches()
        elif self.filetype=="Anzai":
            self.setting_for_anzai()
        elif self.filetype=="RGSC":
            self.setting_for_rgsc()
        elif self.filetype=="SimRT":
            self.setting_for_simrt()
        else:
            self.print_terminal_colored("Please check the type of file.")

        GM = self.GM

        if self.list_sliced_time is not None and self.list_sliced_amp is not None:
            list_target_time = self.list_sliced_time
            list_target_amp = self.list_sliced_amp
        elif self.list_sliced_time is None and self.list_sliced_amp is None:
            list_target_time = self.list_raw_time
            list_target_amp = self.list_raw_amp
        else:
            self.print_terminal_colored("Failed to seek peaks")
            return

        GM.Set_interpolation_step(self.interpolation_step)
        GM.list_time = [float(x) for x in list_target_time]
        GM.list_val = [float(x) for x in list_target_amp]
        self.list_model_time = GM.list_time
        self.list_model_amp = GM.list_val

        try:
            GM.Peak_extract2(self.index_range)
            self.list_raw_time_peak = GM.list_time_peak
            self.list_raw_amp_peak = GM.list_val_peak
            self.show_peaks()
        except:
            self.print_terminal_colored("Failed to seek peaks")


    def get_selected_data(self,):
        GM = self.GM
        if self.list_raw_amp_peak is None or self.list_raw_time_peak is None:
            self.print_terminal_colored("Please ckeck peaks by pressing the peaks button")

        GM.Slicing_data()
        GM.Selection_A(sigma=2)
        GM.Selection_C(sigma=2)
        
        self.list_sel_time = GM.list_sliced_time
        self.list_sel_amp  = GM.list_sliced_val

        return GM.list_sliced_time, GM.list_sliced_val

    
    def run_modeling(self,):
        
        GM = self.GM
        if self.list_raw_amp_peak is None or self.list_raw_time_peak is None:
            self.print_terminal_colored("Please ckeck peaks by pressing the peaks button")
        
        if self.list_sel_time is None or self.list_sel_amp is None:
            self.print_terminal_colored("Please check selected data by pressing the select button")

        try:
            GM.Period_generate()
            GM.Guide_sample()
            
            self.list_model_amp = GM.list_guide
            self.model_period = GM.guide_period
            self.list_model_time = np.linspace(0, self.model_period, self.interpolation_step)

            return self.list_model_time, self.list_model_amp
        
        except:
            return None, None

    def setting_for_abches(self,):
        self.time_for_1breath = 2
        self.datarate = 35
        self.interpolation_step = 100
        self.index_range = self.datarate * self.time_for_1breath
    
    def setting_for_anzai(self,):
        self.time_for_1breath = 2
        self.datarate = 100
        self.interpolation_step = 100
        self.index_range = self.datarate * self.time_for_1breath

    def setting_for_rgsc(self,):
        self.time_for_1breath = 2.5
        self.datarate = 25
        self.interpolation_step = 100
        self.index_range = self.datarate * self.time_for_1breath

    def setting_for_simrt(self,):
        self.time_for_1breath = 2.5
        self.datarate = 35
        self.interpolation_step = 100
        self.index_range = self.datarate * self.time_for_1breath

        
    def range_slicing(self,new_xmin, new_xmax):
        list_temp_time  = []
        list_temp_amp   = []
        for iter in range(len(self.list_raw_time)):
            eachtime = self.list_raw_time[iter]
            if eachtime < new_xmin :
                continue
            if eachtime >= new_xmin :
                eachval = self.list_raw_amp[iter]
                list_temp_time.append(eachtime)
                list_temp_amp.append(eachval)
            if eachtime > new_xmax :
                break
        
        self.list_sliced_time = list_temp_time
        self.list_sliced_amp  = list_temp_amp

    def reset_slicing(self,):
        self.list_sliced_time = None
        self.list_sliced_amp  = None

    def get_guide_data(self,):
        return self.list_model_time, self.list_model_amp
    
    def get_raw_peaks(self,):
        return self.list_raw_time_peak, self.list_raw_amp_peak

    def get_raw_yrange(self):
        return min(self.list_raw_amp),max(self.list_raw_amp)
    
    def get_raw_xyrange(self):
        return min(self.list_raw_time),max(self.list_raw_time),min(self.list_raw_amp),max(self.list_raw_amp)
