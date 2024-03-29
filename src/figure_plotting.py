import pandas as pd
import csv
from file_handling import find_csv_files, select_csv_file, ask_for_enzyme_concentration
import seaborn as sns
import matplotlib.pyplot as plt
from data_calculations import v_to_tn


def plotting_handler(csv_file_path,path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        files_list = next(reader)  # Assuming the first row contains filenames
        return files_list
    plotting_menu(files_list,path)





def plotting_menu(path):


    while True:
        print("\nSmoothing Methods:")
        print("1) Plot data")
        print("2) Plot smoothed data")
        print("3) Plot smoothed data over raw data")
        print("4) Plot intital rates")
        print("5) Return to Main Menu")

        method_choice = input("Enter your choice: ")

        if method_choice == "5":
            break
        elif method_choice == '1':
            raw_csv_file = find_csv_files(path)
            print('Select raw data file')
            raw_data_path = select_csv_file(raw_csv_file, path)
            plot_raw_data(raw_data_path)

        elif method_choice == '2':

            smoothed_csv_file = find_csv_files(path)
            print('Select smoothed data file')
            smoothed_data_path = select_csv_file(smoothed_csv_file, path)
            plot_smoothed_data(smoothed_data_path)

        elif method_choice == '3':

            raw_csv_file = find_csv_files(path)
            print('Select raw data file')
            raw_data_path = select_csv_file(raw_csv_file,path)
            smoothed_csv_file = find_csv_files(path)
            print('Select smoothed data file')
            smoothed_data_path = select_csv_file(smoothed_csv_file, path)
            plot_smoothed_over_raw(raw_data_path, smoothed_data_path)

        elif method_choice == '4':

            files = find_csv_files(path)
            initial_rate_path = select_csv_file(files,path)
            enzyme_concentration = ask_for_enzyme_concentration()
            grouped_replicates = group_replicates(initial_rate_path)
            turnover_df = v_to_tn(grouped_replicates,enzyme_concentration)
            plot_replicate_coefficients(turnover_df)
        else:
            print('Invalid choice, please select a number from the menu.')

def plot_smoothed_over_raw(raw_data_path, smoothed_data_path):
    # Read the data
    raw_data_df = pd.read_csv(raw_data_path)
    smoothed_data_df = pd.read_csv(smoothed_data_path)

    # Combine both datasets for plotting
    combined_data = pd.merge(raw_data_df, smoothed_data_df, on=['Filename', 'Time (s)'], suffixes=('_raw', '_smoothed'), how='inner')

    # Initialize and plot the FacetGrid
    g = sns.FacetGrid(combined_data, col="Filename", col_wrap=3, height=4, sharex=False, sharey=False)
    g = g.map(plt.plot, 'Time (s)', '[H2O2]_raw', marker=".", label="Raw Data", alpha=0.5)
    g = g.map(plt.plot, 'Time (s)', '[H2O2]_smoothed', marker="", color='red', label="Smoothed Data", linewidth=2)

    # Add a legend to each subplot
    for ax in g.axes.flatten():
        ax.legend()

    # Adjust the plot titles
    plt.subplots_adjust(top=0.92)
    g.fig.suptitle('Comparison of Raw and Smoothed [H2O2] Data Across Different Experiments')

    # Show plot
    plt.show()


def plot_raw_data(raw_data_path):
    # Read the raw data
    raw_data_df = pd.read_csv(raw_data_path)

    # Plot the raw data using FacetGrid
    g = sns.FacetGrid(raw_data_df, col="Filename", col_wrap=3, height=4, sharex=False, sharey=False)
    g = g.map(plt.plot, 'Time (s)', '[H2O2]', marker=".", label="Raw Data", alpha=0.5)
    g.add_legend()
    plt.subplots_adjust(top=0.92)
    g.fig.suptitle('Raw [H2O2] Data Across Different Experiments')
    plt.show()

def plot_smoothed_data(smoothed_data_path):
    # Read the smoothed data
    smoothed_data_df = pd.read_csv(smoothed_data_path)

    # Plot the smoothed data using FacetGrid
    g = sns.FacetGrid(smoothed_data_df, col="Filename", col_wrap=3, height=4, sharex=False, sharey=False)
    g = g.map(plt.plot, 'Time (s)', '[H2O2]', marker="", color='red', label="Smoothed Data", linewidth=2)
    g.add_legend()
    plt.subplots_adjust(top=0.92)
    g.fig.suptitle('Smoothed [H2O2] Data Across Different Experiments')
    plt.show()


def group_replicates(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)
    df['Replicate'] = None  # Initialize the Replicate column

    # Display the filenames and their corresponding index
    for index, row in df.iterrows():
        print(f"{index}: {row['Filename']}")

    replicate_number = 1
    while True:
        # Prompt the user to select replicates or quit
        replicate_input = input("Select replicates (e.g., '1,2') or 'q' to quit: ")

        # Check if the user wants to quit
        if replicate_input.lower() == 'q':
            break

        # Process the user input
        replicate_indices = [int(x.strip()) for x in replicate_input.split(',')]

        # Assigning the replicate number to the selected rows
        for index in replicate_indices:
            df.at[index, 'Replicate'] = replicate_number

        print(f"Replicate Group {replicate_number}:")
        print(df.iloc[replicate_indices])
        replicate_number += 1



    return df

def plot_replicate_coefficients(df):
    # Ensure 'Replicate' is a categorical type
    df['Replicate'] = df['Replicate'].astype('category')

    # Calculating mean and standard deviation for each replicate group
    stats_df = df.groupby('Replicate')['Turnover_Number'].agg(['mean', 'std']).reset_index()
    stats_df['Replicate'] = stats_df['Replicate'].apply(lambda x: f'Sample {x}')

    # Ensure 'std' is numeric
    stats_df['std'] = pd.to_numeric(stats_df['std'], errors='coerce')

    # Plotting
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Replicate', y='mean', yerr=stats_df['std'], data=stats_df, capsize=.2)
    plt.title('Mean Coefficient with Standard Deviation for Each Replicate Group')
    plt.xlabel('Replicate Group')
    plt.ylabel('Mean Coefficient')
    plt.show()

