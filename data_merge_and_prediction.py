# code from: https://github.com/jbrowell/HEFTcom24/blob/main/Getting%20Started.ipynb

import pandas as pd
import xarray as xr
import numpy as np
import tkinter as tk
from tkinter import ttk
import statsmodels.api as sm # https://www.statsmodels.org/stable/index.html
import statsmodels.formula.api as smf
from statsmodels.iolib.smpickle import load_pickle
from sklearn.linear_model import LogisticRegression

# import comp_utils

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pickle as pkl
import time

def main():
    # solar
    start = time.time()
    dwd_solar = xr.open_dataset("Documents/data_science_data/dwd_icon_eu_pes10_20200920_20231027.nc")

    solar_radiation = dwd_solar["SolarDownwardRadiation"].mean(dim="point").to_dataframe().reset_index()
    temperature = dwd_solar["Temperature"].mean(dim="point").to_dataframe().reset_index()
    cloud_cover = dwd_solar["CloudCover"].mean(dim="point").to_dataframe().reset_index()

    dwd_solar_features = pd.merge(solar_radiation, temperature, on=["ref_datetime", "valid_datetime"])
    dwd_solar_features = pd.merge(dwd_solar_features, cloud_cover, on=["ref_datetime", "valid_datetime"])
    dwd_solar_features["ref_datetime"] = dwd_solar_features["ref_datetime"].dt.tz_localize("UTC")
    dwd_solar_features["valid_datetime"] = dwd_solar_features["ref_datetime"] + pd.TimedeltaIndex(dwd_solar_features["valid_datetime"],unit="hours")

    # energy data
    energy_data = pd.read_csv("Documents/data_science_data/Energy_Data_20200920_20231027.csv")
    energy_data["dtm"] = pd.to_datetime(energy_data["dtm"])
    energy_data["Wind_MWh_credit"] = 0.5*energy_data["Wind_MW"] - energy_data["boa_MWh"]
    energy_data["Solar_MWh_credit"] = 0.5*energy_data["Solar_MW"]

    modelling_table = dwd_solar_features
    modelling_table = modelling_table.set_index("valid_datetime").groupby("ref_datetime").resample("30T").interpolate("linear")
    modelling_table = modelling_table.drop(columns="ref_datetime",axis=1).reset_index()
    modelling_table = modelling_table.merge(energy_data,how="inner",left_on="valid_datetime",right_on="dtm")
    modelling_table = modelling_table[modelling_table["valid_datetime"] - modelling_table["ref_datetime"] < np.timedelta64(50,"h")]
    end = time.time()
    print("duration of data loading and merging: ", end-start)
    print("table shape before cleaning: ", modelling_table.shape)
    # modelling_table.to_csv('Documents/data_science_data/solar_table.csv')
    # plotRadiationGeneration()
    
    # data cleaning
    start = time.time()
    #modelling_table = cleanData(modelling_table)
    print("duration of data cleansing: ", time.time()-start)
    print("table shape after cleaning: ", modelling_table.shape)
    # plotRadiationGeneration()
    # displayCorrelation(modelling_table)

    """
    MODELLING
    There are three datetime columns.
    1) ref_datetime - time of prediction
    2) valid_datetime - time that is being predicted
    3) dtm - time of energy generation
    Important: valid_datetime = dtm

    Dependent var.: Solar_MW
    Indep. var.: SolarDownwardRadiation, Temperature, CloudCover
    """

    start = time.time()
    forecast_model = smf.ols('Solar_MW ~ SolarDownwardRadiation + Temperature + CloudCover', data=modelling_table).fit()
    #print(forecast_model.summary())
    modelling_table["prediction"] = forecast_model.predict(modelling_table)
    print("duration of modelling: ", time.time()-start)
    # modelling_table.to_csv('Documents/data_science_data/solar_table.csv')
    plotPrediction(modelling_table, 10)

    
def plotPrediction(table, time_stamp):
    ref_time = table["ref_datetime"]== table["ref_datetime"][time_stamp]
    plt.figure(figsize=(10,6))
    sns.set_style("darkgrid", {"grid.color": ".6", "grid.linestyle": ":"})
    ax1 = sns.lineplot(data=table[ref_time], 
                       x="valid_datetime",
                       y="Solar_MW",
                       label='real production')
    sns.lineplot(data=table,
                 x=table[ref_time]["valid_datetime"],
                 y=table[ref_time]["prediction"],
                 color='gray',
                 label='prediction')
    plt.ylim(0, 1600)
    plt.xlim(table[ref_time]['valid_datetime'].min())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M \n %D"))
    plt.xlabel('Date/Time [30-minute period]')
    plt.ylabel('Solar [MW]')
    plt.title(f"Forecast reference time: {table[ref_time]['ref_datetime'][0]}",
            fontsize=14)
    plt.tight_layout()
    plt.show()

def plotRadiationGeneration(table):
    plt.figure(figsize=(9,5))
    sns.scatterplot(data=table, x="SolarDownwardRadiation", 
                    y="Solar_MWh_credit", color='darkorange',s=5)
    plt.xlabel('Solar Radiation Downwards [w/m^2]')
    plt.ylabel('Generation [MWh]')
    plt.show()

def cleanData(raw_table):
    # throwing away missing data
    raw_table = raw_table[raw_table["SolarDownwardRadiation"].notnull()]
    # derivation 0,04 < y/x < 100
    raw_table['y_x'] = raw_table["Solar_MWh_credit"] / raw_table["SolarDownwardRadiation"]
    raw_table = raw_table.drop(raw_table[(raw_table["y_x"]<0.04) | (raw_table["y_x"]>15)].index)
    del raw_table['y_x']
    raw_table = raw_table.reset_index(drop=True)
    #if modelling too time intensive, we can limit the dataset size: raw_table = raw_table.head(10000) 
    return raw_table

def displayCorrelation(table):
    root = tk.Tk()
    root.title("Correlation Table")
    table_correlation = table.corr()
    tree = ttk.Treeview(root, columns=list(table_correlation.columns), show="headings")
    for col in table_correlation.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for index, row in table_correlation.iterrows():
        tree.insert("", "end", values=list(row))
    tree.pack(padx=10, pady=10)
    root.mainloop()

if __name__ == '__main__':
    main()