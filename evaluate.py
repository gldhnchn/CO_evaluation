#!/usr/bin/python3

import pandas, matplotlib.pyplot as plt

if __name__ == '__main__':
    # import data set
    with open('CO_sensor.csv', 'r', encoding='ISO-8859-1') as csvfile:
        data = pandas.read_csv(csvfile, sep=", ")

        ### tidy up data
        df = pandas.DataFrame(data)

    raw_data_points=len(df)

    df.columns = ['timestamp', 'analog_read', 'digital_read']
    df['timestamp'] = pandas.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna()
    df['analog_read'] = pandas.to_numeric(df['analog_read'], downcast='unsigned', errors='coerce')

    digital_anomalies = df.loc[df['digital_read'] != 1]
    if(digital_anomalies.empty):
        print('There are no lines where digital_read is not 1.')
    else:
        print('There are lines where digital_read is not 1: ')
        print(digital_anomalies)
    df = df.drop(columns = 'digital_read')
    data_points = len(df)
    print("Data points in raw data: ", raw_data_points)
    print("Dropped data points: ", raw_data_points-data_points)
    print("Data points: ", data_points)
    df.plot(x="timestamp", y="analog_read")
    plt.show()