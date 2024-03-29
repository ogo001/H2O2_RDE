

from data_analysis import analyze, intial_rate_analysis, plot_precomputed_rolling_regression_facet_grid, intial_rate_manual
from data_smoothing import smoothing_handler
from file_handling import select_csv_file, find_csv_files
from figure_plotting import plotting_menu
import argparse

def comma_separated_numbers(string):
    return string.split(',')

def main():
    parser = argparse.ArgumentParser(description="Data Processing CLI")
    parser.add_argument("-p", "--path", required=True, help="Path to the data file")
    parser.add_argument("-c", type=comma_separated_numbers, help="Comma-separated list of numbers")

    args = parser.parse_args()

    path = args.path
    concentration_values = args.c

    print("""
    
                             
                              
         Credits:                                                ..                
            -Methodology: Lorenz Schwaiger                       ..               
            -Software: Ole Golten                               :++.               
                                                               .+=+=               
                                                               ==..+.             
                                                              -+. .:=             
                                                             .+:  ..+              
                                                             +-     ::           
                                                           .==.     .+.          
                                                          .-=.       .:          
                                                         .-:.         =:           
                                                        .=.            =-.        
                                                      .==.              :+:       
                                                   .:+-.                  :+-.      
                                              ..=++:.                       ..+=.  
                                   ...::-=+==-.                                  :=-:.   
                    ....-=+++++=:......                                                ...:=++-:..... 
            .--:.                                       RDE ANALYZER                   .:--::::-----::.. 
            .-:::-----=++++++++++=-:.                                            .+=..      
                                      ...:-=+=-.                           .-=:.       
                                               .=+..                    .=-.             
                                                  .:=.                 -=.                
                                                    .=.              ==.                  
                                                     -=            .=- 
                                                      +-        .=-  
                                                      -+.      ==.  
                                                      .+-    .+:    
                                                       ==:  .+.     
                                                       :+=..=:      
                                                        ++=:=
                                                        -+++        
                                                         =+        
                                     
                
    """)
    

    while True:
        print("\nMenu:")
        print("1) Analysis")
        print("2) Smoothing")
        print("3) Determine Initial Rate")
        print("4) Plot Data")
        print("5) Exit")

        choice = input("\nSelect an option: ")

        if choice == "1":
            analyze(path, concentration_values)
        elif choice == "2":


            csv_files = find_csv_files(path)
            file_name = select_csv_file(csv_files, path)
            smoothing_handler(file_name,path)

        elif choice == "3":

            csv_files = find_csv_files(path)
            file_name = select_csv_file(csv_files, path)
            intial_rate_manual(file_name, path)

            #data, results = intial_rate_analysis(input_filename=file_name)
            #plot_precomputed_rolling_regression_facet_grid(data, results)
        elif choice == "4":

            plotting_menu(path)



        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")




if __name__ == '__main__':
    main()

    #data_path = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\Experiments\Sensor\b\Selection'
