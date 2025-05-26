import pandas as pd


def read_abches(filepath):
    try:
        df = pd.read_csv(filepath)
        list_amp = df['TerminalExpirationLine'].values
        list_timestamp = df['MonitoringID'].values
        return list_timestamp, list_amp

    except:
        return None, None

def read_anzai(filepath):
    keyword = "***DataNo."
    mydatatime = 0
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
            for line in lines:
                if "Data Time(msec)" in line:
                    _, value_part = line.split(",", 1)
                    mydatatime = int(value_part.strip().split(",")[0])
                if keyword in line:
                    myheaders = line.strip().split(",")


            start_line = next(i for i, line in enumerate(lines) if "Data Start" in line) + 1
            df = pd.read_csv(filepath, skiprows=start_line,header=None,names=myheaders)
            
            # list_timestamp = float(df['"***DataNo.'].values * mydatatime)
            # list_amp = float(df['Physics-Value***"'].apply(lambda x: x.strip("mm ")).values)
            list_timestamp = (df['"***DataNo.'].values * mydatatime).astype(float)
            list_amp = df['Physics-Value***"'].apply(lambda x: float(x.strip("mm "))).values


            return list_timestamp, list_amp
    except:
        return None, None


def read_rgsc(filepath):
    try:
        keyword = "Data_layout"
        with open(filepath, "r") as file:
            lines = file.readlines()
            for line in lines:
                if keyword in line:
                    _, value_part = line.split("=", 1)
                    myheaders = value_part.strip().split(",")
            start_line = next(i for i, line in enumerate(lines) if "[Data]" in line)     + 1
            df = pd.read_csv(filepath, skiprows=start_line,header=None,names=myheaders)

            list_amp = df['amplitude'].values
            list_timestamp = df['timestamp'].values

        return list_timestamp, list_amp
        
    except:
        return None, None

def read_simrt(filepath):
    try:
        keyword = "Data_layout"
        with open(filepath, "r") as file:
            lines = file.readlines()
            for line in lines:
                if keyword in line:
                    _, value_part = line.split("=", 1)
                    myheaders = value_part.strip().split(",")
            start_line = next(i for i, line in enumerate(lines) if "[Data]" in line)     + 1
            df = pd.read_csv(filepath, skiprows=start_line,header=None,names=myheaders)

            list_amp = df['amplitude'].values
            list_timestamp = df['timestamp'].values

        return list_timestamp, list_amp
        
    except:
        return None, None