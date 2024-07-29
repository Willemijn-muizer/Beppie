import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

# Function that calculates the mean for each measurement
def calculate_mean_distance(distances: list[float]):
    return sum(distances)/len(distances)

# Function that calculates the standard deviation for each measurement
def calculate_std(distances: list[float]):
    mean = calculate_mean_distance(distances)
    std = (sum([(distance - mean) ** 2 for distance in distances])/len(distances))**0.5
    return std


def calculations_statistics():
    data_file_willemijn = 'data/Data_Willemijn.json'
    df = pd.read_json(data_file_willemijn)

    # take mean of each rows distances
    df['mean_distance'] = df['distances'].apply(calculate_mean_distance)
    df['std'] = df['distances'].apply(calculate_std)
    print(df)


if __name__ == '__main__':
    calculations_statistics()

