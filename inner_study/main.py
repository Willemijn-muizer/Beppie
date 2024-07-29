import pandas as pd

from inner_study.statistics.mean import calculate_mean_distance
from inner_study.statistics.std import calculate_std

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

def calculations_statistics():
    data_file_willemijn = 'data/Data_Willemijn.json'
    df = pd.read_json(data_file_willemijn)

    # take mean of each rows distances
    df['mean_distance'] = df['distances'].apply(calculate_mean_distance)
    df['std'] = df['distances'].apply(calculate_std)
    print(df)


if __name__ == '__main__':
    calculations_statistics()

