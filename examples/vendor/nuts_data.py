import pandas as pd
#import requests


def get_data():
    #DF = pd.read_csv(r"examples/vendor/datas/EU_Map_PREKall_17.02.csv", low_mwmory=False)
    DF = pd.read_csv(r"examples/vendor/datas/EU_Map_PREKall_17.02.csv",dtype={"NUTS_ID": str})

    return DF
