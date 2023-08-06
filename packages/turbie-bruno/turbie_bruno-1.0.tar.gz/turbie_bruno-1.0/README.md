# TURBIE BY BRUNO FARIA

## Welcome young padawan!

This package was created to share the functions generated and to be used in 2Dof representation of a Wind Turbine, modelling the blades flapwise and tower fore-aft motions when a wind series (steady flow) is given with specific TI. 

## And thats all for now! See you next time 


## or maybe not

In case you want to run the whole Turbie model, you should copy paste the following code:


### Testing Script
from Functions_CodeCamp_Project import (ask_for_ti,
                                        calc_all_statistics,
                                        plot_results_TI,
                                        turbie_for_TI_and_saving)

### Load which TIs (or TI) will be analyzed
Ti_wanted = ask_for_ti()

### Run turbie for the given Ti_wanted and save outputs
turbie_for_TI_and_saving(Ti_wanted)

### Load outputs and calculate Statistical Matrix (sm)
sm = calc_all_statistics(Ti_wanted)

### Plot Results
plot_results_TI(Ti_wanted, sm, include_ref=True)




- obs: the input wind series should be given in the right format as the example file wind_4_ms_TI_0.1.txt inside the folder Data/Data_TI_0.1

# The instructions for how to use the above lines is written below 

# :handshake: CodeCamp Project: Turbie :handshake:

The CodeCamp project Turbie was organized as follow: 
- One module that contains all functions for the project - [Function Module code](https://gitlab.windenergy.dtu.dk/python-at-risoe/spp-2023/group_4_shaking_hands/-/blob/main/CodeCamp/Functions_CodeCamp_Project.py)
- One file that executes the require functions to complete the task requested for the project. - [Main Turbie file](https://gitlab.windenergy.dtu.dk/python-at-risoe/spp-2023/group_4_shaking_hands/-/blob/main/CodeCamp/Turbie_run.py)

The "main" branch was merged/pushed/updated when we were working together. Aditionally, each group member push on main, when working separetly on assigned tasks. 

## Improvements performed from first submission to final submission

- The code was made more robust, adding safety features to avoid the code did not run due to mistakes or missunderstandings. For this, some functions were created to avoid errors and ensure the code run as expected. 
- The reference values were added as optional in the plot section, to ensure if the values we obtained are correct. 
- The code was check with pycodestyle, to ensure was properly with the recommended standards. 
- PEP 257 information added to each function

## Getting started - How it works

The file Turbie_run.py is the file from where the whole project can be executed. 

Each main function will be explained below. For more detailed information about each function, please check the informaiton available inside each function in the [Function Module code](https://gitlab.windenergy.dtu.dk/python-at-risoe/spp-2023/group_4_shaking_hands/-/blob/main/CodeCamp/Functions_CodeCamp_Project.py)

### Step 1: Function: ask_for_ti()

Function will display a message on the console asking the user to submit TI values for which the evaluation wants to be performed.
The format of the TI needs to be as float and separeted by a ',' (*Example: 0.05, 0.1, 0.15*). 
If the values are not a float, empty or not found, an message error will be display. 

Values submitted by the user will be stored as a list of floats. 

***Note: To avoid to run the function is time, also a Ti_wanted = [0.1, 0.05, 0.2, 0.15, 0.3] has been added as a comment. To use, comment line 16 and uncomment line 19.***

#### Inputs: 
- No inputs are required. 

#### Outputs:
- Ti_wanted (list, floats)

### Step 2: Function: turbie_for_TI_and_saving(Ti_wanted)

Function that calculates the response for the TI provided, for all the files contained inside the folder under that specific TI value. 
This can be done for multiple Ti, and the values will be stored in a text file for each wind speed, and all saved under an output foldler for each TI (for which data is available). 

***Note: It takes around 4-6 minutes per Ti. If you want to avoid this function, you can comment line 22, since values can be already found on output folders:  Data_TI_0.05_out, Data_TI_0.1_out and Data_TI_0.15_out***

#### Inputs: 
- Ti_wanted (list, float)

#### Outputs:
- Creates text_files for each wind speed on a folder for each Ti (Example: Data_TI_0.05_out)

### Step 3: Function: calc_all_statistics(Ti_wanted)

With data available on the output folder, we can proceed to calculate the Statistic Matrices for each TI. 
This function calculates the statistics for each file for the selected Tis (float list), and saving it in an array of dimensions 1 x 5 for each file, where each columm represents:

- Mean wind speed
- Mean blade deflection
- Standard deviation blade deflection
- Mean tower deflection
- Standard deviation tower deflection

It returns a 2D array for each TI, with shape [Number of files x 5]. In the example, it is store as '**sm**'.
Finally, the Statistic Matrix '**sm**' is stored inside a dictionary, where the keys(float) are each TI. 

#### Inputs: 
- Ti_wanted (list, float)

#### Outputs:
- Dictionary, where keys are each TI as floats. Each key contain an array float 64, with size [Number of files x 5]. 

### Step 4: Function plots_results(Ti_wanted, sm, include_ref=True)

The final function is for plotting the results. 
It has three inputs, which are the Ti selected, sm being the dictionary with the 2D arrays saved from the previous function: ***'calc_all_statistics(Ti)'***, and an *optional parameters*, where if include_ref=True, it will plot the selected values plus the reference values added for this project, allowing to compare the results.

#### Inputs: 
- Ti_wanted (list, float)
- sm (Dictionary, with array float 22x5 for each key. Created from Step 3. 
- Optional paramenter: include_ref=True will add to the plot the reference values provided for this project, for comparison. 

#### Outputs:
- Figure with Mean and Standard deviation for Blade and Tower deflection for each Ti specify by the user in Step 1. 


## Git Group flow

For the last stage of Turbie, all work from the main branch, just communicating with each other where someone will push into main, to avoid merge conflicts. 
We meet and work together on multiple ocassions, and we also divided the workload, and each of us contribute on different sections, performing changing and ensuring the code runs as intended.

 