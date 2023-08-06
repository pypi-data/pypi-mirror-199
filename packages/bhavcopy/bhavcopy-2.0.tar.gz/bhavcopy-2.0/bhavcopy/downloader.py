# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:01:18 2023

@author: ajayd
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:48:43 2023

@author: ajayd
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 08:57:46 2023

@author: ajayd
"""

import pandas as pd
import urllib.request
import os
import datetime
import zipfile
import random
import time
import numpy as np
import requests
import io



class bhavcopy:
    
    def __init__(self, instr ,start_date, end_date, data_storage, wait_time):
        self.start_date = start_date
        self.end_date = end_date
        self.data_storage = data_storage
        self.wait_time = wait_time
        self.instr = instr
    
    def wait(self):
        wait_time = self.wait_time
        time.sleep(random.randint(wait_time[0],wait_time[1]))
    
    def clear_junc(self):
        
        os.chdir(self.data_storage)
        
        for filename in os.listdir():
            if "cm" in filename:
                try:
                    os.remove(filename)
                except OSError as e:
                    print(f"Error: {e.strerror} - {filename}")
        
        for filename in os.listdir():
            if "fo" in filename:
                try:
                    os.remove(filename)
                except OSError as e:
                    print(f"Error: {e.strerror} - {filename}")
                 
    def extraction_engine(self,myDate):
        
        instr = self.instr
        wait_time = self.wait_time
        data_storage = self.data_storage
        
        with requests.Session() as s:
        
            if (instr == "equities"):
                downloadfilename = "cm" + str(myDate.strftime("%d%b%Y")).upper() + "bhav.csv"
                temp = ""
                myURL = "http://www1.nseindia.com/content/historical/EQUITIES/" + str(myDate.strftime("%Y")) + "/" + str(myDate.strftime("%b")).upper() + "/" + downloadfilename + ".zip"
                self.wait()
                try:
                
                    # download file
                    s.headers.update({'User-Agent': 'Mozilla/5.0'})
                    response = s.get(myURL)
                    response.raise_for_status()
                
                    # Download Zipped File
                    zippedFile = os.path.join(data_storage, downloadfilename + ".zip")
                    with open(zippedFile, "wb") as f:
                        f.write(response.content)
                
                    # Unzip file and save it in temp
                    with zipfile.ZipFile(zippedFile, 'r') as zip_ref:
                        zip_ref.extractall(data_storage)
                    
                    temp = pd.read_csv(os.path.join(data_storage, downloadfilename), sep=",")
                    temp["TIMESTAMP"] = pd.to_datetime(temp["TIMESTAMP"])
                
                    print(myDate)
                
                except requests.exceptions.HTTPError as errh:
                    print("HTTP Error:", errh)
                
                except requests.exceptions.ConnectionError as errc:
                    print("Error Connecting:", errc)
            
                except requests.exceptions.Timeout as errt:
                    print("Timeout Error:", errt)
            
                except requests.exceptions.RequestException as err:
                    print("Something went wrong:", err)
                
                    pass
             
            if(instr == "indices"):
                
                
                index_link = f"http://www1.nseindia.com/content/indices/ind_close_all_{myDate.strftime('%d%m%Y').upper()}.csv"
                self.wait()
                
                try:
                #with requests.Session() as s:
                    s.headers.update({'User-Agent': 'Mozilla/5.0'})
                    response = s.get(index_link)
                    response.raise_for_status()
                    
                    temp = pd.read_csv(io.StringIO(response.text))
                    temp["TIMESTAMP"] = pd.to_datetime(temp["Index Date"],format='%d-%m-%Y')
                    temp.drop("Index Date", axis=1, inplace=True)
                    
                    print(myDate)
                    
                except requests.exceptions.HTTPError as errh:
                    print("HTTP Error:", errh)
                except requests.exceptions.ConnectionError as errc:
                    print("Error Connecting:", errc)
                except requests.exceptions.Timeout as errt:
                    print("Timeout Error:", errt)
                except requests.exceptions.RequestException as err:
                    print("Something went wrong:", err)
                    pass
                
            if(instr == "derivatives"):
                index_link = f"http://www1.nseindia.com/content/historical/DERIVATIVES/{myDate.strftime('%Y')}/{myDate.strftime('%b').upper()}/fo{myDate.strftime('%d%b%Y').upper()}bhav.csv.zip"
                self.wait()
            
                try:
                    s.headers.update({'User-Agent': 'Mozilla/5.0'})
                    response = s.get(index_link)
                    response.raise_for_status()
                
                    # Unzip file and save it in temp
                    temp_file = io.BytesIO(response.content)
                    with zipfile.ZipFile(temp_file, 'r') as zip_ref:
                        zip_ref.extractall(data_storage)
                    
                    ## Read the csv file and add the data to main_file
                    headers = "INSTRUMENT,SYMBOL,EXPIRY_DT,STRIKE_PR,OPTION_TYP,OPEN,HIGH,LOW,CLOSE,SETTLE_PR,CONTRACTS,VAL_INLAKH,OPEN_INT,CHG_IN_OI,TIMESTAMP"
                    headers = headers.split(",")
                
                    temp = pd.read_csv(os.path.join(data_storage, f"fo{myDate.strftime('%d%b%Y').upper()}bhav.csv"), usecols=headers)
                    temp['TIMESTAMP'] = pd.to_datetime(myDate)
                    #temp.to_csv(os.path.join(data_storage, main_file), mode='a', header=False, index=False)
                
                    print(myDate)
                
                except requests.exceptions.HTTPError as errh:
                    print("HTTP Error:", errh)
                    
                except requests.exceptions.ConnectionError as errc:
                    print("Error Connecting:", errc)
            
                except requests.exceptions.Timeout as errt:
                    print("Timeout Error:", errt)
            
                except requests.exceptions.RequestException as err:
                    print("Something went wrong:", err)
                    
                    pass
            
            
            self.clear_junc()
            self.temp = temp
               
    def file_checks(self):
    
        print("Running File Check")
        data_storage = self.data_storage
        instr = self.instr
        file_path = data_storage + "\\" + instr + ".csv"

        if os.path.exists(file_path):
            print("The file exists.")

        else:
            print("The file does not exist. Creating File")
            
            if instr == "equities":
                headers = ["SYMBOL", "SERIES", "OPEN", "HIGH", "LOW", "CLOSE", "LAST", "PREVCLOSE", "TOTTRDQTY", "TOTTRDVAL", "TIMESTAMP", "TOTALTRADES", "ISIN", "X"]
                df = pd.DataFrame(columns=headers)
                df.to_csv(file_path, index=False)
            
            if instr == "indices":
                headers = "Index Name,Open Index Value,High Index Value,Low Index Value,Closing Index Value,Points Change,Change(%),Volume,Turnover (Rs. Cr.),P/E,P/B,Div Yield,TIMESTAMP"
                headers = headers.split(",")
                df = pd.DataFrame(columns=headers)
                df.to_csv(file_path, index=False)
            
            
            if instr == "derivatives":
                headers = "INSTRUMENT,SYMBOL,EXPIRY_DT,STRIKE_PR,OPTION_TYP,OPEN,HIGH,LOW,CLOSE,SETTLE_PR,CONTRACTS,VAL_INLAKH,OPEN_INT,CHG_IN_OI,TIMESTAMP"
                headers = headers.split(",")
                df = pd.DataFrame(columns=headers)
                df.to_csv(file_path, index=False)
            
        
        
        self.file_path = file_path
    
    def get_missing_dates(self, unique_dates):
    
        start_date = self.start_date
        end_date = self.end_date
        
    # Get a range of dates between start_date and end_date
        date_range = pd.date_range(start=start_date, end=end_date)
    
    # Convert unique_dates to a NumPy array
        unique_dates = np.array(unique_dates)
    
    # Get the missing dates that are not in unique_dates
        missing_dates = set(date_range) - set(pd.to_datetime(unique_dates))
    
    # Filter out Sundays and Saturdays
        filtered_dates = []
        for date in missing_dates:
            if date.weekday() != 6 and date.weekday() != 5:
                filtered_dates.append(date)
        
        filtered_dates.sort()
        
        return filtered_dates  
    
    def date_check(self):
        
        path = self.file_path
        start_date = self.start_date
        end_date = self.end_date
        
        DF = pd.read_csv(path)
        unique_dates = DF["TIMESTAMP"].unique()
        
        filtered_dates = self.get_missing_dates(unique_dates)
        
        print("Downloading Data for {}".format(filtered_dates))
        self.filtered_dates = filtered_dates
    
    def update_database(self):
        dates = self.filtered_dates
        if len(dates) > 0:
            for d in dates:
                myDate = d
                try:
                    self.extraction_engine(myDate)
                    self.temp.to_csv(self.file_path, mode='a', header=False, index=False)
                    print("{}:done".format(myDate))
                except:
                    print("{}:failed".format(myDate))
        else:
            print("Data the for period already exists")
    
    def get_data(self):
        self.file_checks()
        self.date_check()
        self.update_database()
        


 