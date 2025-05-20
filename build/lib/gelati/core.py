#!/usr/bin/env python3

### - - - - - - - - - - - - - - -
### free_guide_python_v5
### - - - - - - - - - - - - - - -
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
import argparse
import math
from scipy.signal import find_peaks
import ast


total_start_time = time.time()    ### Just to check run time


# temp_list_interpol_time = []
# temp_list_interpol_val = []




class guide_modeling:
    def __init__(self,):
        self.list_time = []
        self.list_val = []
        self.list_time_peak = []
        self.list_val_peak = []
        self.list_sliced_time = []
        self.list_sliced_val = []
        self.list_guide = []
        self.list_guide_time = []
        self.list_guide_val = []
        self.guide_period = None
        self.interpolation_step = 30
        
        # self.list_selected_sliced_time = []
        # self.list_selected_sliced_val  = []


    def Set_interpolation_step(self,value):
        self.interpolation_step = value

    def Reset_selection(self,):
        self.Slicing_data()


    ### --------------------------------------------------------
    ### Function for File reading. Output type : (list_time,list_cm)
    ### --------------------------------------------------------    
    def File_reading2(self, target_data_file):
        file_content = []
        list_x = []
        list_y = []
        list_z = []
        list_vec = []
        list_time = []

        list_target = []
        list_cm = []

        ### --------------------------------------------------------
        ### File Reading
        ### --------------------------------------------------------
        prev_time = None
        accum_time = 0
        with open(target_data_file, 'r') as file:
            for line in file:
                parts = line.split()
                temp_x = int(parts[2])
                temp_y = int(parts[4])
                temp_z = int(parts[6])
                temp_rms = float(parts[8])
                temp_time = parts[10]
                
                list_x.append(temp_x)
                list_y.append(temp_y)
                list_z.append(temp_z)
                list_vec.append(temp_rms)

                ### --------------------------------------------------------
                ### Saving time info in a microseconds unit
                ### --------------------------------------------------------
                current_time = datetime.strptime(temp_time.strip(), "%H:%M:%S.%f")
                if prev_time is None:
                    list_time.append(0)
                else:
                    time_diff = (current_time - prev_time).total_seconds()
                    accum_time += time_diff
                    list_time.append(accum_time)
                prev_time = current_time
                ### --------------------------------------------------------
        ### --------------------------------------------------------

        ### --------------------------------------------------------
        ### Finding main axis
        ### : Target axis is sometime confused
        ### --------------------------------------------------------
        x_mean = sum(list_x) / len(list_x)
        y_mean = sum(list_y) / len(list_y)
        z_mean = sum(list_z) / len(list_z)

        if x_mean >= y_mean and x_mean >= z_mean:
            list_target = list_x
        elif y_mean >= x_mean and y_mean >= z_mean:
            list_target = list_y
        else:
            list_target = list_z
        
        self.list_time = list_time
        self.list_val = list_target


    def File_reading(self,target_data_file):
        file_content = []
        list_time = []
        list_target = []

        ### --------------------------------------------------------
        ### File Reading
        ### --------------------------------------------------------
        prev_time = None
        accum_time = 0
        with open(target_data_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    data_dict = ast.literal_eval(line)
                    list_time.append(data_dict['x'])
                    list_target.append(data_dict['y'])

        ### --------------------------------------------------------
        
        self.list_time = list_time
        self.list_val = list_target


    def Data_Input_time(self,mytimelist):
        self.list_time = mytimelist

    def Data_Input_val(self,myvallist):
        self.list_val = myvallist

    ### --------------------------------------------------------
    ### Function for peak extraction. Output type : (list_time_peak, list_cm_peak)
    ### --------------------------------------------------------    
    def Peak_extract(self,):
        list_time = self.list_time
        list_cm = self.list_val
        ### Tunable parameters
        trial_period = 2.5
        # trial_period = 5.0
        temp_min = 7777777;  temp_min_time = 0
        temp_max = -7777777; temp_max_time = 0
        # seeking_ratio = 0.8; compare_margin = 30
        
        seeking_ratio = 0.8; compare_margin = 3

        ### Variables declaration
        is_max_first = True; is_first = True
        iter_peak=0; prev_time = 0

        list_time_peak = []
        list_cm_peak = []
        list_temp_period = []


        iter_list =0
        while iter_list < len(list_cm):
            temp_time = list_time[iter_list]
            val = list_cm[iter_list]


            ### ------------------------------------------------------------------------
            ### IF time is in the trial period
            ### ------------------------------------------------------------------------
            if(temp_time < prev_time + trial_period):
                if(is_first):    # Finding max
                    if(val>temp_max):
                        ### ------------------------------------------------------------------------
                        ### Using margin check system
                        ### ------------------------------------------------------------------------
                        is_real_max = True
                        for i_temp in range(0,compare_margin):
                            if(iter_list+i_temp > len(list_cm)-1):
                                break
                            if val < list_cm[iter_list+i_temp]:
                                is_real_max = False
                        if(is_real_max):
                            temp_max = val
                            temp_max_time = temp_time
                            iter_peak = iter_list
                        ### ------------------------------------------------------------------------


                        # ### ------------------------------------------------------------------------
                        # ### Not using margin check system
                        # ### ------------------------------------------------------------------------
                        # temp_max = val
                        # temp_max_time = temp_time
                        # iter_peak = iter_list
                        # ### ------------------------------------------------------------------------
                
                
                else:
                    if(val<temp_min):
                        ### ------------------------------------------------------------------------
                        ### Margin check system
                        ### ------------------------------------------------------------------------
                        is_real_min = True
                        for i_temp in range(0,compare_margin):
                            if(iter_list+i_temp > len(list_cm)-1):
                                break
                            if(val > list_cm[iter_list+i_temp]):
                                is_real_min = False

                        if(is_real_min):
                            temp_min = val
                            temp_min_time = temp_time
                        ### ------------------------------------------------------------------------
                        
                        # ### ------------------------------------------------------------------------
                        # ### No margin check system
                        # ### ------------------------------------------------------------------------
                        # temp_min = val
                        # temp_min_time = temp_time


            ### ------------------------------------------------------------------------
            ### IF time is out of the trial period
            ### ------------------------------------------------------------------------
            else:
                if(is_first):
                    is_first = False
                    iter_list = iter_peak
                    prev_time = temp_max_time
                else: 
                    break
            iter_list+=1
        ### ------------------------------------------------------------------------
        ### End of finding first period
        ### ------------------------------------------------------------------------
        
        
        
        ### Parameters set based on first period as estimated period
        estimated_period = 2 * abs(temp_max_time-temp_min_time)
        prev_time = 0; iter_peak=0
        is_first = True
        temp_max = -7777777; temp_min = 7777777
        


        ### ------------------------------------------------------------------------
        ### Finding peaks
        ### ------------------------------------------------------------------------
        iter_list = 0
        while iter_list < len(list_cm):
            temp_time = list_time[iter_list]
            val = list_cm[iter_list]
            seeking_range = prev_time + estimated_period * seeking_ratio
            ### ------------------------------------------------------------------------
            ### IF time is in the seeking range
            ### ------------------------------------------------------------------------
            if(temp_time < seeking_range) :
                ### Finding max                 
                if(is_first): 
                    if(val>temp_max):
                        # ### ------------------------------------------------------------------------
                        # ### Margin check system
                        # ### ------------------------------------------------------------------------
                        is_real_max = True
                        for i_temp in range(1,compare_margin):
                            if(iter_list+i_temp > len(list_cm)-1):
                                break
                            if(val < list_cm[iter_list+i_temp]):
                                is_real_max = False
                        if(is_real_max):
                            temp_max = val
                            temp_max_time = temp_time
                            iter_peak = iter_list
                        # ### ------------------------------------------------------------------------
                        

                        ### ------------------------------------------------------------------------
                        ### No margin check system
                        ### ------------------------------------------------------------------------
                        
                        # temp_max = val
                        # temp_max_time = temp_time
                        # iter_peak=iter_list
                        ### ------------------------------------------------------------------------
                

                ### Finding min
                else:        
                    if(val<temp_min):
                        # ### ------------------------------------------------------------------------
                        # ### Margin check system
                        # ### ------------------------------------------------------------------------
                        is_real_min = True
                        for i_temp in range(compare_margin):
                            if(iter_list+i_temp > len(list_cm)-1):
                                break
                            if(val > list_cm[iter_list+i_temp]):
                                is_real_min = False
                        if(is_real_min):
                            temp_min = val
                            temp_min_time = temp_time
                            iter_peak=iter_list
                        # ### ------------------------------------------------------------------------

                        
                        ### ------------------------------------------------------------------------
                        ### No margin check system
                        ### ------------------------------------------------------------------------
                        # temp_min = val
                        # temp_min_time = temp_time
                        # iter_peak=iter_list
                        ### ------------------------------------------------------------------------


            ### ------------------------------------------------------------------------
            ### IF time is out of the seeking range
            ### ------------------------------------------------------------------------
            if(temp_time >= prev_time + estimated_period * seeking_ratio):
                if(iter_peak==0):        ###  If there is no data in range
                    temp_max = -7777777; temp_min = 7777777
                    iter_peak = 0; prev_time = temp_time
                    iter_list-=1
                    continue
                if(is_first==True):      ### after finding max
                    is_first = False
                    prev_time = temp_max_time
                    list_cm_peak.append(temp_max)
                    list_time_peak.append(temp_max_time)
                else:                    ### after finding min
                    is_first = True
                    # list_cm_peak.append(temp_min)
                    # list_time_peak.append(temp_min_time)
                    prev_time = temp_min_time

                
                iter_list = iter_peak; iter_peak=0
                temp_max = -7777777; temp_min = 7777777
            iter_list+=1

        # print("Peak-extraction is done")   
        self.list_time_peak = list_time_peak
        self.list_val_peak = list_cm_peak
    ### --------------------------------------------------------    

    ### --------------------------------------------------------
    ### Function for peak extraction using scipy. Output type : (list_time_peak, list_cm_peak)
    ### --------------------------------------------------------    
    def Peak_extract2(self,range=200):
        list_time = self.list_time
        list_cm = self.list_val
        up_peaks, _ = find_peaks(np.array(list_cm),distance=range)
        down_peaks, _ = find_peaks(-1*np.array(list_cm),distance=range)
        # all_peaks = np.sort(np.concatenate((up_peaks, down_peaks)))
        all_peaks = up_peaks

        list_time_peak=[]; list_cm_peak=[]
        for ipeak in all_peaks:
            list_time_peak.append(list_time[ipeak])
            list_cm_peak.append(list_cm[ipeak])


        # print("Peak-extraction is done")    
        self.list_time_peak = list_time_peak
        self.list_val_peak = list_cm_peak
    ### --------------------------------------------------------

    ### --------------------------------------------------------
    ### Function for converting to signal->cm. Output type : list_cm
    ### --------------------------------------------------------    
    def Convert_signal_to_cm(self,):
        list_target = self.list_val
        list_cm=[]
        # Magnet dependent parameters
        Br = 6.75997e+13    # Br
        Vol = 6.25e-06      # Volume of magnet
        offset = 2632       # offset
        
        for i in range(len(list_target)):
            myval = list_target[i]
            # my_cm = math.cbrt((Br * Vol) / (2 * math.pi * (myval - offset)))
            my_cm = np.cbrt((Br * Vol) / (2 * math.pi * (myval - offset)))
            list_cm.append(my_cm)

        self.list_val = list_cm
    ### --------------------------------------------------------

    ### --------------------------------------------------------
    ### Function for the interpolation. Output type : list_
    ### --------------------------------------------------------
    def Interpolation(self, list_temp_1cycle_time, list_temp_1cycle_cm):
        list_res = []

        start_time = list_temp_1cycle_time[0]
        end_time = list_temp_1cycle_time[len(list_temp_1cycle_time)-1]
        temp_period = end_time - start_time
        step_ratio = 1 / self.interpolation_step




        iter_sample = 0
        iter = 0
        
        # while iter < len(list_temp_1cycle_cm):

        #     temp_time = list_temp_1cycle_time[iter]
        #     step_ratio = 1 / interpolation_step
            
        #     target_time = temp_period * step_ratio * iter_sample + start_time   
        #     if(temp_time > target_time):
        #         iter_sample += 1
        #         val1 = list_temp_1cycle_cm[iter-1]
        #         val2 = list_temp_1cycle_cm[iter]
        #         time1 = list_temp_1cycle_time[iter-1]
        #         time2 = list_temp_1cycle_time[iter]
        #         next_tartget_time = temp_period * step_ratio * iter_sample + start_time

        #         while(time2 > next_tartget_time):
        #             print("iter_sample : {}  ----".format(iter_sample))
        #             iter-=1
        #             val1 = list_temp_1cycle_cm[iter-1]
        #             val2 = list_temp_1cycle_cm[iter]
        #             time1 = list_temp_1cycle_time[iter-1]
        #             time2 = list_temp_1cycle_time[iter]
                    
        #         iter-=1

        #         interpolated_value = val1 + (val2 - val1) * (target_time - time1) / (time2 - time1)
        #         list_res.append(interpolated_value)
                
        #         # if(interpolated_value>23.5 or interpolated_value<21.5):
        #             # print("iter_sample : {}  ----".format(iter_sample))
        #             # print("(iter:{}) time1 : {} / target_time : {} / time2 : {}".format(iter,time1, target_time, time2))

        #         temp_list_interpol_val.append(interpolated_value)
        #         temp_list_interpol_time.append(target_time)
        #     iter+=1
        # print("--------------------------------------------------------")


        list_targeted_time = []
        for iter_sample in range(0,self.interpolation_step):
            temp_target_time =  temp_period * step_ratio * iter_sample + start_time
            list_targeted_time.append(temp_target_time)

        iter_target=0
        # while iter < len(list_temp_1cycle_cm):
        for iter in range(0,len(list_temp_1cycle_cm)):
            temp_time = list_temp_1cycle_time[iter]
            if(iter_target >= len(list_targeted_time)):
                break
            now_target = list_targeted_time[iter_target]
            while(now_target<=temp_time):
                if(now_target==temp_time):
                    interpolated_value = list_temp_1cycle_cm[iter]
                else:
                    val1 = list_temp_1cycle_cm[iter-1]
                    val2 = list_temp_1cycle_cm[iter]
                    time1 = list_temp_1cycle_time[iter-1]
                    time2 = list_temp_1cycle_time[iter]
                    interpolated_value = val1 + (val2 - val1) * (now_target - time1) / (time2 - time1)

                # if(interpolated_value<20):
                #     print("now_target : {} / now_time : {} / interpolated_value : {}".format(now_target,temp_time,interpolated_value))
                #     print("time1 : {} / time2 : {} / val1 : {} / val2 : {}".format(time1,time2,val1,val2))
                #     print("({} - {}) * ({} - {}) / ({} - {})".format(val2,val1,now_target,time1,time2,time1))
                #     print('-----------------------------------------------------------------------------')
                
                list_res.append(interpolated_value)
                iter_target+=1
                if(iter_target >= len(list_targeted_time)):
                    break
                now_target = list_targeted_time[iter_target]
        return list_res
    ### --------------------------------------------------------    

    # ### --------------------------------------------------------
    # ### Function for the period generation. Output type : mean_period
    # ### --------------------------------------------------------
    # def Period_generate(list_peak_time):
    #     list_period_candi = []
    #     # for i in range(2,len(list_peak_time),2):
    #     for i in range(1,len(list_peak_time)):
    #         list_period_candi.append(list_peak_time[i] - list_peak_time[i-1])
    #     mean_period = float(np.mean(list_period_candi))
    #     return mean_period
    # ### --------------------------------------------------------    

    def Slicing_data(self,):
        list_time = self.list_time
        list_cm = self.list_val
        list_peak_time = self.list_time_peak
        list_peak_cm = self.list_val_peak
        

        iter_peak_list = 0
        list_sliced_cm = []
        list_sliced_time = []
        list_temp_cm = []
        list_temp_time = []
        
        for time_val,cm_val in zip(list_time,list_cm):
            if time_val < list_peak_time[0]:
                continue
            mypeaktime = list_peak_time[iter_peak_list]
            mypeakcm = list_peak_cm[iter_peak_list]
            if cm_val==mypeakcm and time_val==mypeaktime:
                if time_val!=list_peak_time[0] :
                    list_sliced_cm.append(list_temp_cm)
                    list_sliced_time.append(list_temp_time)
                list_temp_cm = []
                list_temp_time = []
                # iter_peak_list += 2
                iter_peak_list += 1
                if iter_peak_list > len(list_peak_cm)-1:
                    break
            
            list_temp_time.append(time_val)
            list_temp_cm.append(cm_val)

        self.list_sliced_time = list_sliced_time
        self.list_sliced_val = list_sliced_cm

    ### --------------------------------------------------------
    ### Function for the interpolation. Output type : list_guide
    ### --------------------------------------------------------    
    def Guide_sample(self,):
        sliced_list_time = self.list_sliced_time
        sliced_list_cm = self.list_sliced_val

        iter_up_peak = 1
        guide_period = 0
        list_temp = [0] * self.interpolation_step
        list_temp_1cycle_cm = []
        list_temp_1cycle_time = []
        list_samples = []
        list_guide = []
            
        for i in range(0,len(sliced_list_cm)):
            each_cm_sliced = sliced_list_cm[i]
            each_time_sliced = sliced_list_time[i]
            list_temp_guide = self.Interpolation(each_time_sliced,each_cm_sliced)
            for j in range(0,len(list_temp_guide)):
                list_temp[j] += list_temp_guide[j]

        num_period = len(sliced_list_cm)
        list_samples = [x / num_period for x in list_temp]
        for i in range(0,len(list_samples)):
            list_guide.append(float(np.mean(list_samples[i])))

        self.list_guide = list_guide
        # self.Guide_signal_time()
    ### --------------------------------------------------------    


    def Guide_sample_sel(self,):
        sliced_list_time = self.list_sliced_time
        sliced_list_cm = self.list_sliced_val
        # sliced_list_time = self.list_selected_sliced_time
        # sliced_list_cm = self.list_selected_sliced_val

        iter_up_peak = 1
        guide_period = 0
        list_temp = [0] * self.interpolation_step
        list_temp_1cycle_cm = []
        list_temp_1cycle_time = []
        list_samples = []
        list_guide = []
            
        for i in range(0,len(sliced_list_cm)):
            each_cm_sliced = sliced_list_cm[i]
            each_time_sliced = sliced_list_time[i]
            list_temp_guide = self.Interpolation(each_time_sliced,each_cm_sliced)
            for j in range(0,len(list_temp_guide)):
                list_temp[j] += list_temp_guide[j]

        num_period = len(sliced_list_cm)
        list_samples = [x / num_period for x in list_temp]
        for i in range(0,len(list_samples)):
            list_guide.append(float(np.mean(list_samples[i])))

        # print("Guide sample is generated")
        self.list_guide = list_guide



    def Guide_signal_time(self,times,phase=0):
        mean_period = self.guide_period
        list_guide = self.list_guide
        iter = 0
        list_guide_time = []; list_guide_cm = []
        step_ratio = 1/self.interpolation_step

        while(iter < times):
            for iter_10 in range(0,len(list_guide)):
                list_guide_time.append(iter*mean_period + mean_period*step_ratio*iter_10 + phase)
                # print(iter*mean_period + mean_period*step_ratio*iter_10 + phase)
                # list_guide_time.append(iter*mean_period + mean_period*step_ratio*iter_10 + phase + iter * mean_period*step_ratio)
                # print(mean_period*step_ratio*iter)
                list_guide_cm.append(list_guide[iter_10])
            iter+=1
        self.list_guide_time = list_guide_time
        self.list_guide_val = list_guide_cm
        return self.list_guide_time, self.list_guide_val

    def Sel_sliced_data(self,):
        list_sliced_time = self.list_sliced_time
        list_sliced_cm = self.list_sliced_val 
        
        ### For the period
        list_selected_cm = []
        list_selected_time = []
        list_period = []
        
        total_size = len(list_selected_cm)

        for each_cycle_cm, each_cycle_time in zip(list_sliced_cm, list_sliced_time):
            each_size = len(each_cycle_time)
            temp_period = each_cycle_time[each_size-1] - each_cycle_time[0]
            list_period.append(temp_period)
            
        std_period = np.std(list_period)
        mean_period = np.mean(list_period)

        filtered_periods = [x for x in list_period if (mean_period - std_period) <= x <= (mean_period + std_period)]
        mean_filtered_period = np.mean(filtered_periods)

        
        for each_cycle_cm, each_cycle_time in zip(list_sliced_cm, list_sliced_time):
            each_size = len(each_cycle_time)
            temp_period = each_cycle_time[each_size-1] - each_cycle_time[0]
            if(abs(temp_period-mean_period) < std_period):
                list_selected_cm.append(each_cycle_cm)
                list_selected_time.append(each_cycle_time)

        ### For the baseline
        list_temp_cm = list_selected_cm
        list_temp_time = list_selected_time
        list_selected_cm = []
        list_selected_time = []
        list_baseline = []

        for each_cycle_cm, each_cycle_time in zip(list_temp_cm, list_temp_time):
            lowest_5 = sorted(each_cycle_cm)[:5]
            mean_lowest_5 = np.mean(lowest_5)
            list_baseline.append(mean_lowest_5)

        mean_base = np.mean(list_baseline)
        std_base = np.std(list_baseline)

        i_base = 0
        for each_cycle_cm, each_cycle_time in zip(list_temp_cm, list_temp_time):
            mybase = list_baseline[i_base]
            if abs(mybase-mean_base) < std_base:
                list_selected_cm.append(each_cycle_cm)
                list_selected_time.append(each_cycle_time)
            i_base+=1

        
        # self.list_selected_sliced_time = list_selected_time
        # self.list_selected_sliced_val = list_selected_cm
        self.list_sliced_time = list_selected_time
        self.list_sliced_val = list_selected_cm
        # self.guide_period = mean_filtered_period


    ### For the period    
    def Selection_A(self,sigma=1):
        list_sliced_time = self.list_sliced_time
        list_sliced_cm = self.list_sliced_val 
        
        list_selected_cm = []
        list_selected_time = []
        list_period = []

        for each_cycle_cm, each_cycle_time in zip(list_sliced_cm, list_sliced_time):
            each_size = len(each_cycle_time)
            temp_period = each_cycle_time[each_size-1] - each_cycle_time[0]
            list_period.append(temp_period)
            
        std_period = np.std(list_period)
        mean_period = np.mean(list_period)

        filtered_periods = [x for x in list_period if (mean_period - std_period) <= x <= (mean_period + std_period)]
        mean_filtered_period = np.mean(filtered_periods)

        
        for each_cycle_cm, each_cycle_time in zip(list_sliced_cm, list_sliced_time):
            each_size = len(each_cycle_time)
            temp_period = each_cycle_time[each_size-1] - each_cycle_time[0]
            if(abs(temp_period-mean_period) < std_period*sigma):
                list_selected_cm.append(each_cycle_cm)
                list_selected_time.append(each_cycle_time)
        
        if(len(list_selected_cm)==0):
            print("!!! There is no selelcted from Selection_A !!!")
        self.list_sliced_time = list_selected_time
        self.list_sliced_val = list_selected_cm
        # self.guide_period = mean_filtered_period
        
    ### For the baseline
    def Selection_B(self,sigma=1):
        list_sliced_time = self.list_sliced_time
        list_sliced_cm = self.list_sliced_val 
        
        list_temp_cm = list_sliced_cm
        list_temp_time = list_sliced_time
        list_selected_cm = []
        list_selected_time = []
        list_baseline = []

        for each_cycle_cm, each_cycle_time in zip(list_temp_cm, list_temp_time):
            lowest_5 = sorted(each_cycle_cm)[:5]
            mean_lowest_5 = np.mean(lowest_5)
            list_baseline.append(mean_lowest_5)

        mean_base = np.mean(list_baseline)
        std_base = np.std(list_baseline)

        i_base = 0
        for each_cycle_cm, each_cycle_time in zip(list_temp_cm, list_temp_time):
            mybase = list_baseline[i_base]
            if abs(mybase-mean_base) < std_base * sigma:
                list_selected_cm.append(each_cycle_cm)
                list_selected_time.append(each_cycle_time)
            i_base+=1

        if(len(list_selected_cm)==0):
            print("!!! There is no selelcted from Selection_B !!!")
        self.list_sliced_time = list_selected_time
        self.list_sliced_val = list_selected_cm
        # self.guide_period = mean_filtered_period


    ### For the peak high
    def Selection_C(self,sigma=1):
        list_sliced_time = self.list_sliced_time
        list_sliced_cm = self.list_sliced_val 
        
        list_temp_cm = list_sliced_cm
        list_temp_time = list_sliced_time
        list_selected_cm = []
        list_selected_time = []
        list_baseline = []

        mean_peak = np.mean(self.list_val_peak)
        std_peak= np.std(self.list_val_peak)

        for each_cycle_cm, each_cycle_time in zip(list_sliced_cm, list_sliced_time):
            if(abs(each_cycle_cm[0]-mean_peak) < std_peak*sigma):
                list_selected_cm.append(each_cycle_cm)
                list_selected_time.append(each_cycle_time)
        
        if(len(list_selected_cm)==0):
            print("!!! There is no selelcted from Selection_C !!!")
        self.list_sliced_time = list_selected_time
        self.list_sliced_val = list_selected_cm



    # def Show_sliced(self,):
    #     # list_sliced_time_sel = self.list_selected_sliced_time
    #     # list_sliced_cm_sel = self.list_selected_sliced_val
    #     list_sliced_time_sel = self.list_sliced_time
    #     list_sliced_cm_sel = self.list_sliced_val
    #     stitched_time_list = []; stitched_cm_list =[]
    #     for temp_time_list,temp_cm_list in zip(list_sliced_time_sel,list_sliced_cm_sel):
    #         stitched_time_list.extend(temp_time_list)
    #         stitched_cm_list.extend(temp_cm_list)

    #     return stitched_time_list,stitched_cm_list


    ### --------------------------------------------------------
    ### Function for the period generation. Output type : mean_period
    ### --------------------------------------------------------
    def Period_generate(self,):
        list_sliced_time = self.list_sliced_time
        list_period_candi = []
        for i in range(0,len(list_sliced_time)):
            mycycle = list_sliced_time[i]
            cycle_start_time = mycycle[0]
            cycle_end_time = mycycle[len(mycycle)-1]
            list_period_candi.append(cycle_end_time-cycle_start_time)
        mean_period = float(np.mean(list_period_candi))
        self.guide_period = mean_period
    ### --------------------------------------------------------    

    def Guide_input(self, list_input_guide):
        self.list_guide = list_input_guide

    def Period_input(self, input_period):
        self.guide_period = input_period

    # ### --------------------------------------------------------    
    # def Evaluation(self,):
    #     list_time = self.list_time
    #     list_val = self.list_val
    #     list_guide = self.list_guide
    #     i_guide = 0
    #     i_peak = 0
    #     step_ratio = 1 / self.interpolation_step
    #     myperiod = self.guide_period
    #     first_peak_time = self.list_time_peak[0]

    #     list_cal = []

    #     for mytime,myval in zip(list_time,list_val):
    #         if mytime < first_peak_time:
    #             continue
    #         time_guide = first_peak_time + myperiod * step_ratio * i_guide
    #         val_guide = list_guide[i_guide%30]

    #         if mytime == time_guide:
    #             x_target = time_guide
    #             y_target = val_guide
    #         if mytime > time_guide:
    #             x1 = first_peak_time + myperiod * step_ratio * (i_guide-1)
    #             y1 = list_guide[(i_guide-1)%30]
    #             x2 = time_guide
    #             y2 = val_guide
                
    #             y_target = y1+(y2-y1)/(x2-x1)*(mytime-x1)
                
    #         if mytime < time_guide:
    #             continue
    #         print(abs((y_target - myval)))
    #         score = abs((y_target - myval)/myval)
    #         # score = math.sqrt((y_target - myval)*(y_target - myval))
    #         list_cal.append(score)

    #         i_guide+=1
    #     average = sum(list_cal) / len(list_cal)
    #     print("--------------------------")
    #     return average

    def Evaluation(self,):
        list_sliced_time = self.list_sliced_time
        list_sliced_val = self.list_sliced_val
        list_guide = self.list_guide
        i_guide = 0
        i_peak = 0
        interpolation_step = self.interpolation_step
        step_ratio = 1 / self.interpolation_step
        myperiod = self.guide_period
        # first_peak_time = self.list_time_peak[0]

        list_cal = []

        for mysinglepeak_time, mysinglepeak_val in zip(list_sliced_time,list_sliced_val):
            first_peak_time = self.list_time_peak[i_peak]
            # print("!!!!!!!!!!!!!!!!!")
            # print(i_peak)
            # print(mysinglepeak_time)
            # print("!!!!!!!!!!!!!!!!!")
            for mytime,myval in zip(mysinglepeak_time,mysinglepeak_val):
                # time_guide = first_peak_time + myperiod * step_ratio * (i_guide%30)
                time_guide = first_peak_time + myperiod * step_ratio * (i_guide)
                val_guide = list_guide[i_guide%interpolation_step]
                # print("mytime:{} / time_guide:{}".format(mytime,time_guide))
                if mytime == time_guide:
                    x_target = time_guide
                    y_target = val_guide
                if mytime > time_guide:
                    x1 = first_peak_time + myperiod * step_ratio * (i_guide-1)
                    y1 = list_guide[(i_guide-1)%interpolation_step]
                    x2 = time_guide
                    y2 = val_guide
                    
                    y_target = y1+(y2-y1)/(x2-x1)*(mytime-x1)
                    
                if mytime < time_guide:
                    continue
                # print("x1:{}, x2:{}, y1:{}, y2:{}, mytime:{}".format(x1,x2,y1,y2,mytime))
                # print(first_peak_time)
                # if(y_target > 50):
                    # print("x1:{}, x2:{}, y1:{}, y2:{}, mytime:{}".format(x1,x2,y1,y2,mytime))
                # print("hello")


                score = abs((y_target - myval)/myval)
                # score = math.sqrt((y_target - myval)*(y_target - myval))
                list_cal.append(score)

                i_guide+=1
            i_peak += 1
        # print("- - - - - - - - - - - - - - - -")
        

        # for mytime,myval in zip(list_sliced_time,list_sliced_val):
        #     if mytime < first_peak_time:
        #         continue
        #     time_guide = first_peak_time + myperiod * step_ratio * i_guide
        #     val_guide = list_guide[i_guide%30]

        #     if mytime == time_guide:
        #         x_target = time_guidex
        #         y_target = val_guide
        #     if mytime > time_guide:
        #         x1 = first_peak_time + myperiod * step_ratio * (i_guide-1)
        #         y1 = list_guide[(i_guide-1)%30]
        #         x2 = time_guide
        #         y2 = val_guide
                
        #         y_target = y1+(y2-y1)/(x2-x1)*(mytime-x1)
                
        #     if mytime < time_guide:
        #         continue
        #     print(abs((y_target - myval)))
        #     score = abs((y_target - myval)/myval)
        #     # score = math.sqrt((y_target - myval)*(y_target - myval))
        #     list_cal.append(score)

        #     i_guide+=1
        average = sum(list_cal) / len(list_cal)
        # print(self.list_time_peak)
        return average

            
            







