import sklearn as sk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def get_usable_data(Dataset, Subset):
    return Dataset[Subset].copy()

#Checking the Data
def check_data(Dataset):
    print(Dataset.head())
    print(Dataset.describe())
    print(Dataset.info())

"""
This dataset cannot be normalized or have outliers removed in a similar way to other datasets. 
"""
#visulization
def Visualise_hist(Dataset):
    Dataset.hist(bins=50, figsize=(20, 15))
    plt.show()



packet_streams = pd.read_csv("Data/Datasets/Dataset.csv")
packet_streams_2 = pd.read_csv("Data/Datasets/Dataset2.csv")

#dropping any columns that cant be used for analysis of a single packet.
usable_data_stream_1 = ["Source.IP", "Source.Port", "Destination.IP", "Destination.Port", "Protocol", "Timestamp", "Label", "L7Protocol", "ProtocolName"]
packet_data_1 = get_usable_data(packet_streams,usable_data_stream_1)

usable_data_stream_2 = ["srcaddr","dstaddr", "srcport", "dstport", "prot", "tos", "tcp_flags", "Label"]
packet_data_2 = get_usable_data(packet_streams_2, usable_data_stream_2)

check_data(packet_data_2)

