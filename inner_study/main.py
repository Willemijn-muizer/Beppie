import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)


# Function that reads the data using pandas and returns a dataframe
def read_data(filename: str) -> pd.DataFrame:
    folder = "data"
    df = pd.read_csv(folder + "/" + filename + ".csv", delimiter=";")

    return df


# Function that eliminates the difference of measurement between the observer and the script.
# The script measures the distance to the center of the pixel, while the observer measures to the edge of the pixel.
def fix_pixel_distance(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    for col in cols:
        df[col] = df[col] + 0.71

    return df


# Function that calculates the intra-observator variability from the data of Willemijn
def intra_observer_willemijn(df: pd.DataFrame, n=3) -> pd.DataFrame:
    df['mean_intra'] = (df['Meting 1'] + df['Meting 2'] + df['Meting 3']) / n
    df['std'] = ((
                         (df["Meting 1"] - df["mean_intra"]) ** 2 +
                         (df["Meting 2"] - df["mean_intra"]) ** 2 +
                         (df["Meting 3"] - df["mean_intra"]) ** 2
                 ) / (n - 1)) ** 0.5

    df['cv'] = df['std'] / df['mean_intra']

    return df


# Function that calculates the difference in measurement between the data of col1 and col2
def inter_observer(df: pd.DataFrame, col1="mean_intra", col2="Script", name="delta") -> pd.DataFrame:
    df[name] = df[col1] - df[col2]
    return df


def calculate_std_differences(delta_col: pd.Series, print_name: str) -> float:
    mean_difference = sum(delta_col) / len(delta_col)
    difference_squared = sum((delta_col - mean_difference) ** 2)

    std_difference = (difference_squared / (len(delta_col) - 1)) ** 0.5

    print("> STD DIFFERENCES " + print_name + ": ", std_difference)
    return std_difference


def plot_bland_altman_willemijn_script(df: pd.DataFrame):
    x = (df['mean_intra'] + df['Script']) / 2
    y = df['delta']

    std_difference = calculate_std_differences(df["delta"], "Willemijn & script")

    mean_difference = sum(df['delta']) / len(df)
    upper_limit = mean_difference + 1.96 * std_difference
    lower_limit = mean_difference - 1.96 * std_difference

    plt.title("Bland Altman plot with data Willemijn and Script")
    plt.xlabel("Average between observer and script")
    plt.ylabel("Difference between observer and script")
    plt.scatter(x, y)

    # Draw a line at  mean_difference, upper_limit, lower_limit
    plt.axhline(mean_difference, color='b')
    plt.text(30, mean_difference - 0.25, "Mean=" + str(mean_difference)[:5], color="b")

    plt.axhline(upper_limit, color='r', linestyle="--")
    plt.text(2, upper_limit + 0.1, "+1.96 SD; " + str(upper_limit)[:5], color="r")

    plt.axhline(lower_limit, color='r', linestyle="--")
    plt.text(2, lower_limit + 0.1, "-1.96 SD; " + str(lower_limit)[:5], color="r")

    plt.text(28, 2.70, "Participant 10, \n RB, Sessie 2")

    plt.savefig('bland_altman_willemijn_script.png')
    plt.close()
    plt.clf()


def plot_bland_altman_irma_script(df: pd.DataFrame):
    x = (df['Meting 1'] + df['Script']) / 2
    y = df['delta']

    std_difference = calculate_std_differences(df["delta"], "Irma & script")

    mean_difference = sum(df['delta']) / len(df)
    upper_limit = mean_difference + 1.96 * std_difference
    lower_limit = mean_difference - 1.96 * std_difference

    plt.title("Bland Altman plot with data Irma and Script")
    plt.xlabel("Average between observer and script")
    plt.ylabel("Difference between observer and script")
    plt.scatter(x, y)

    # Draw a line at  mean_difference, upper_limit, lower_limit
    plt.axhline(mean_difference, color='b')
    plt.text(30, mean_difference - 0.25, "Mean=" + str(mean_difference)[:5], color="b")

    plt.axhline(upper_limit, color='r', linestyle="--")
    plt.text(2, upper_limit + 0.1, "+1.96 SD; " + str(upper_limit)[:5], color="r")

    plt.axhline(lower_limit, color='r', linestyle="--")
    plt.text(2, lower_limit + 0.1, "-1.96 SD; " + str(lower_limit)[:5], color="r")

    plt.savefig('bland_altman_irma_script.png')
    plt.close()
    plt.clf()

# Function that
def plot_bland_altman_observators(df_will: pd.DataFrame, df_irma: pd.DataFrame):
    assert len(df_will) == len(df_irma)

    x = (df_will['mean_intra'] + df_irma['Meting 1']) / 2
    y = df_will['mean_intra'] - df_irma['Meting 1']

    std_difference = calculate_std_differences(y, "Willemijn & Irma")

    mean_difference = sum(y) / len(df_will)
    upper_limit = mean_difference + 1.96 * std_difference
    lower_limit = mean_difference - 1.96 * std_difference

    plt.title("Bland Altman plot with data Willemijn and Irma")
    plt.xlabel("Average between two observers")
    plt.ylabel("Difference between two observers")
    plt.scatter(x, y)

    # Draw a line at  mean_difference, upper_limit, lower_limit
    plt.axhline(mean_difference, color='b')
    plt.text(30, mean_difference - 0.25, "Mean=" + str(mean_difference)[:5], color="b")

    plt.axhline(upper_limit, color='r', linestyle="--")
    plt.text(2, upper_limit + 0.1, "+1.96 SD; " + str(upper_limit)[:5], color="r")

    plt.axhline(lower_limit, color='r', linestyle="--")
    plt.text(2, lower_limit + 0.1, "-1.96 SD; " + str(lower_limit)[:5], color="r")

    plt.savefig('bland_altman_observers.png')
    plt.close()
    plt.clf()

def plot_bland_altman_scripts(df_will: pd.DataFrame, df_irma: pd.DataFrame):
    assert len(df_will) == len(df_irma)

    x = (df_will['Script'] + df_irma['Script']) / 2
    y = df_will['Script'] - df_irma['Script']

    std_difference = calculate_std_differences(y, "Script_Will & Script_Irma")

    mean_difference = sum(y) / len(df_will)
    upper_limit = mean_difference + 1.96 * std_difference
    lower_limit = mean_difference - 1.96 * std_difference

    plt.title("Bland Altman plot with data scripts")
    plt.xlabel("Average between two scripts")
    plt.ylabel("Difference between two scripts")
    plt.scatter(x, y)

    # Draw a line at  mean_difference, upper_limit, lower_limit
    plt.axhline(mean_difference, color='b')
    plt.text(30, mean_difference - 0.25, "Mean=" + str(mean_difference)[:5], color="b")

    plt.axhline(upper_limit, color='r', linestyle="--")
    plt.text(2, upper_limit + 0.1, "+1.96 SD; " + str(upper_limit)[:5], color="r")

    plt.axhline(lower_limit, color='r', linestyle="--")
    plt.text(2, lower_limit + 0.1, "-1.96 SD; " + str(lower_limit)[:5], color="r")

    plt.savefig('bland_altman_scripts.png')
    plt.close()
    plt.clf()

if __name__ == '__main__':
    willemijn_data = read_data('data_willemijn_script')
    irma_data = read_data('data_irma_script')

    # Correct the distance between heart and stomach
    willemijn_data = fix_pixel_distance(willemijn_data, ["Meting 1", "Meting 2", "Meting 3"])
    irma_data = fix_pixel_distance(irma_data, ["Meting 1"])

    willemijn_data = intra_observer_willemijn(willemijn_data) # Adds a mean_intra, std and cv column to the dataset

    willemijn_data = inter_observer(willemijn_data, "mean_intra", "Script") # Adds a delta column to the dataset
    irma_data = inter_observer(irma_data, "Meting 1", "Script") # Adds a delta column to the dataset

    # Make a bland altman plot for willemijn data (mean) and script data
    plot_bland_altman_willemijn_script(willemijn_data)
    plot_bland_altman_irma_script(irma_data)
    plot_bland_altman_observators(willemijn_data, irma_data)
    plot_bland_altman_scripts(willemijn_data, irma_data)

    print(willemijn_data.head())
