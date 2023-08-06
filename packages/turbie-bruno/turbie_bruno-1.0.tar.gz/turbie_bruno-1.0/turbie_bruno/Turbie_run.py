"""
Created on Tue Mar  7 20:54:30 2023

@author: espa

Main Script for Turbie Project
"""

# Testing Script
from Functions_CodeCamp_Project import (ask_for_ti,
                                        calc_all_statistics,
                                        plot_results_TI,
                                        turbie_for_TI_and_saving)

# Load which TIs (or TI) will be analyzed
Ti_wanted = ask_for_ti()

# Test Ti instead of ask_for_ti() every time
# Ti_wanted = [0.05, 0.1, 0.15, 0.2]

# Run turbie for the given Ti_wanted and save outputs
turbie_for_TI_and_saving(Ti_wanted)

# Load outputs and calculate Statistical Matrix (sm)
sm = calc_all_statistics(Ti_wanted)

# Plot Results
plot_results_TI(Ti_wanted, sm, include_ref=True)
