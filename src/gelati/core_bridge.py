from gelati import core
import numpy as np
import copy

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
        self.sigma_selA         = 2
        self.sigma_selB         = 5
        self.sigma_selC         = 2

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
            
    def set_dafault_setting(self,):
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
        

    def seeking_peak(self,):
        if self.list_sliced_time is None and self.list_sliced_amp is None and self.list_raw_time is None and self.list_raw_amp is None:
            self.print_terminal_colored("Please load raw file first")
            return

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
        # GM.Selection_A(sigma=self.sigma_selA)
        # GM.Selection_C(sigma=self.sigma_selC)
        
        before_list_sliced_time = copy.deepcopy(GM.list_sliced_time)
        before_list_sliced_val = copy.deepcopy(GM.list_sliced_val)

        GM.Selection_A(sigma=self.sigma_selA)
        if len(GM.list_sliced_time) == 0:
            self.print_terminal_colored("No data after selection A")
            GM.list_sliced_time = before_list_sliced_time
            GM.list_sliced_val = before_list_sliced_val
        else:
            self.print_terminal("Result of selection A: {} cycles -> {} cycles".format(len(before_list_sliced_time),len(GM.list_sliced_time)))
        
        before_list_sliced_time = copy.deepcopy(GM.list_sliced_time)
        before_list_sliced_val = copy.deepcopy(GM.list_sliced_val)

        GM.Selection_C(sigma=self.sigma_selC)
        if len(GM.list_sliced_time) == 0:
            self.print_terminal_colored("No data after selection C")
            GM.list_sliced_time = before_list_sliced_time
            GM.list_sliced_val = before_list_sliced_val
        else:
            self.print_terminal("Result of selection C: {} cycles -> {} cycles".format(len(before_list_sliced_time),len(GM.list_sliced_time)))

        
        self.list_sel_time = GM.list_sliced_time
        self.list_sel_amp  = GM.list_sliced_val

        return GM.list_sliced_time, GM.list_sliced_val

    def Run_selection_A(self):
        GM = self.GM
        before_list_sliced_time = copy.deepcopy(GM.list_sliced_time)
        before_list_sliced_val = copy.deepcopy(GM.list_sliced_val)

        GM.Selection_A(sigma=self.sigma_selA)
        if len(GM.list_sliced_time) == 0:
            self.print_terminal_colored("No data after selection A")
            GM.list_sliced_time = before_list_sliced_time
            GM.list_sliced_val = before_list_sliced_val
        else:
            self.print_terminal("Result of selection A: {} cycles -> {} cycles".format(len(before_list_sliced_time),len(GM.list_sliced_time)))

    def Run_selection_B(self):
        GM = self.GM
        before_list_sliced_time = copy.deepcopy(GM.list_sliced_time)
        before_list_sliced_val = copy.deepcopy(GM.list_sliced_val)

        GM.Selection_B(sigma=self.sigma_selB)
        if len(GM.list_sliced_time) == 0:
            self.print_terminal_colored("No data after selection B")
            GM.list_sliced_time = before_list_sliced_time
            GM.list_sliced_val = before_list_sliced_val
        else:
            self.print_terminal("Result of selection B: {} cycles -> {} cycles".format(len(before_list_sliced_time),len(GM.list_sliced_time)))

    
    def Run_selection_C(self):
        GM = self.GM
        before_list_sliced_time = copy.deepcopy(GM.list_sliced_time)
        before_list_sliced_val = copy.deepcopy(GM.list_sliced_val)

        GM.Selection_C(sigma=self.sigma_selC)
        if len(GM.list_sliced_time) == 0:
            self.print_terminal_colored("No data after selection C")
            GM.list_sliced_time = before_list_sliced_time
            GM.list_sliced_val = before_list_sliced_val
        else:
            self.print_terminal("Result of selection C: {} cycles -> {} cycles".format(len(before_list_sliced_time),len(GM.list_sliced_time)))



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

    def get_parameter(self,):
        return self.interpolation_step, self.time_for_1breath, self.datarate, self.sigma_selA, self.sigma_selB, self.sigma_selC
    
    def set_parameter(self,my_interpolation_step, my_time_for_1breath, my_datarate, mysigma_A, mysigma_B, mysigma_C):
        self.interpolation_step = int(my_interpolation_step)
        self.time_for_1breath = float(my_time_for_1breath)
        self.datarate = float(my_datarate)
        self.index_range = self.datarate * self.time_for_1breath
        self.sigma_selA = float(mysigma_A)
        self.sigma_selB = float(mysigma_B)
        self.sigma_selC = float(mysigma_C)