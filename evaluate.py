#!/usr/bin/python3

import pandas as pd, matplotlib.pyplot as plt

if __name__ == '__main__':
    # import data set
    print("Importing data...")
    with open('CO_sensor.csv', 'r', encoding='ISO-8859-1') as csvfile:
        df = pd.read_csv(csvfile, skipinitialspace=True, error_bad_lines=False)

    raw_data_points=len(df)
    df.columns = ['timestamp', 'analog_read', 'digital_read']
    print("Converting timestamps...")
    df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True, errors='coerce')
    print("Converting sensor data...")
    df['analog_read'] = pd.to_numeric(df['analog_read'], downcast='unsigned', errors='coerce')
    print("Dropping unreadable data...")
    df = df.dropna()
    print("Evaluating digital read...")
    digital_anomalies = df.loc[df['digital_read'] != 1]
    if(digital_anomalies.empty):
        print('There are no lines where digital_read is not 1.')
    else:
        print('There are lines where digital_read is not 1: ')
        print(digital_anomalies)
    df = df.drop(columns = 'digital_read')
    print("Dropping duplicate timestamps...")
    df = df.drop_duplicates(subset="timestamp")
    df = df.set_index('timestamp')
    data_points = len(df)
    print("Lines in raw data: ", raw_data_points)
    print("Dropped lines: ", raw_data_points-data_points)
    print("Data points: ", data_points)
    print("Plotting data...")
    ax = df.plot()
    ax = df.rolling('60s').mean().plot(ax=ax)
    ax = df.rolling('1h').mean().plot(ax=ax)
    ax = df.rolling('1d').mean().plot(ax=ax)
    plt.show()