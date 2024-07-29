from inner_study.statistics.mean import calculate_mean_distance


# Function that calculates the standard deviation for each measurement
def calculate_std(distances: list[float]):
    mean = calculate_mean_distance(distances)
    std = (sum([(distance - mean) ** 2 for distance in distances])/len(distances))**0.5
    return std


