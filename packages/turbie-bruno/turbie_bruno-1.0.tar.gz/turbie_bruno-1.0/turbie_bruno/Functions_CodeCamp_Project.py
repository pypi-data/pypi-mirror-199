# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 11:44:21 2023

@author: brofa
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from pathlib import Path
import glob
import os
import pkg_resources

# %% Assemble Matrices


def assemble_matrices_turbie():
    '''
    This function would assemble matrices(M, C, K) to build 2Dof system

    Parameters:
    ----------
    None
    Returns
    ---------
   M: array
   C: array
   K: array
   Area: int
   rho: int

    '''
    # importing turbie parameters
    stream = pkg_resources.resource_stream(__name__, "./Data_model/parameters.txt")
    para = np.genfromtxt(stream, skip_header=1)
    # only numerical
    para_turbie = para[:, 0]
    # rotor diamenter [m]
    d = para_turbie[12]
    Area = np.pi*(d/2)**2
    # air density [kg/m3]
    rho = para_turbie[13]
    ######################
    # Assemblying Masses
    ######################
    # Blade
    m1 = 3*para_turbie[0]
    # RNA/Tower
    m2 = np.sum(para_turbie[1:4])
    # Assemble
    M = np.zeros((2, 2))
    M[0, 0] = m1
    M[1, 1] = m2
    ######################
    # Assemblying Damping
    ######################
    # assemble C , zero matrix
    C = np.zeros((2, 2))
    # equivalent damping blades
    C[0, 0] = para_turbie[4]
    C[0, 1] = -para_turbie[4]
    C[1, 0] = -para_turbie[4]
    # equivalent damping blades + RNA/Tower
    C[1, 1] = para_turbie[4] + para_turbie[5]
    ######################
    # Assemblying Stiffness
    ######################
    # assemble K , zero matrix
    K = np.zeros((2, 2))
    # equivalent stiffness blades
    K[0, 0] = para_turbie[6]
    K[0, 1] = -para_turbie[6]
    K[1, 0] = -para_turbie[6]
    # equivalent stiffness RNA/Tower
    K[1, 1] = para_turbie[6] + para_turbie[7]
    # np.savetxt('Assembled_Matrices.txt',M)
    # Assembled_Matrix = np.stack((M, C, K))# M,C,K
    return M, C, K, Area, rho

# %% CT interpolating


def Ct_turbie_interpolated(wind):
    '''
    This function would interpolate CT with helping ct.txt file and wind mean
    Parameters
    ----------
    wind : arry
        wind speed array  [m/s].
    Returns
    -------
    Ct_mean : int
        CT for the wind speed mean.
    '''
    # load the CT file
    Ct_file = 'turbie_bruno/Data_model/Ct.txt'
    # Importing data from ct_file
    data = np.genfromtxt(Ct_file)
    Ct_turbie = data[:, 1]
    wind_Ct = data[:, 0]
    # Calculate the mean of wind array
    wind_mean = np.mean(wind)
    # inserting outliers
    # left side
    Ct_turbie[0] = 0.99
    wind_Ct[0] = 0
    # right side
    Ct_turbie = np.append(Ct_turbie, 0.03)
    wind_Ct = np.append(wind_Ct, 30)
    # interpolate CT mean
    Ct_mean = np.interp(wind_mean, wind_Ct, Ct_turbie)
    return Ct_mean

# %% find Response


def find_response(t_p, t_wind, u_wind):
    '''
    This function will find response closest to given time point.
    Parameters
    ----------
    t_p : int
        The idenfitied time.
    t_wind : array
        the time series array [s].
    u_wind : array
        the wind speed array [m/s].

    Returns
    -------
    u_wind[t_idx]: int
        the wind speed for t_p.
    '''
    # find index closest to time point
    t_idx = np.argmin(np.abs(t_wind - t_p))
    return u_wind[t_idx]

# %% Differential function with forcing


def dydt(t, y, M, C, K, rho, Area, Ct, t_wind, u_wind):
    '''
    Differential function for Turbie (with forcing)
    Parameters
    ----------
    t : array
        time series.
    y : array
        new force vector.
    M : array
        The 2DOF mass system.
    C : array
        The 2DOF spring system.
    K : array
        The 2DOF damper system .
    rho : int
        Air density [kg/m^3].
    Area : int
        Rotor area.
    Ct : int
        The thrust coefficient.
    t_wind : array
        time series for current wind [s].
    u_wind : array
        The current wind [m/s].

    Returns
    -------
    ydot : array
        time-marching response.

    '''
    # assemble an empty matrix for ydot
    ydot = np.empty(len(y))
    # assemble A matrix based on the M matrix shape
    A = np.empty([2*M.shape[0], 2*M.shape[0]])
    A = np.block([[np.zeros([2, 2]), np.identity(2)],
                  [-np.dot(np.linalg.inv(M), K),
                   -np.dot(np.linalg.inv(M), C)]])
    # finding the correspondent wind speed
    # at the time integration step
    wind_speed = find_response(t, t_wind, u_wind)
    # aerodynamic force
    faero = 0.5*rho*Area*Ct*(wind_speed - y[2])**2
    F = np.array([faero, 0])
    # B matrix sized (4,1)
    B = np.block([np.zeros([2, ]), np.dot(np.linalg.inv(M), F)])
    ydot = np.dot(A, y) + B
    return ydot

# %% open wind file for simulate


def open_wind(file):
    '''
    This function opens the file to be simulated
    Parameters
    ----------
    file : zip file

    Returns
    -------
    data_wind[:,0]: array
        The time series[s].
    data_wind[:,1]: array
        the wind speed [m/s].

    '''
    # input
    data_wind = np.genfromtxt(file, skip_header=1)
    return data_wind[:, 0], data_wind[:, 1]

# %% simulate Turbie


def simulate_turbie(t_wind, u_wind, args_cte):
    """
    Function that Simulates the Turbie model as a
    2Dof system of mass/dampers/springs

    Parameters
    ----------
    t_wind : time array [s].
    u_wind : wind speed array [m/s].
    args_cte : M,C,K,rho,Area

    Returns
    -------
    t : output time array [s]. (unless asked, equal to t_wind)
    xb : blade deflection [m].
    xt : tower deflection [m].
    """
    # Assemblying 2Dof matrices
    # M,C,K,d,rho = assemble_matrices_turbie()
    # Swept Area
    # Area = np.pi*(d/2)**2
    # Generating Ct mean for the wind profile
    Ct_mean = Ct_turbie_interpolated(u_wind)
    # Parameters used in the dydt function (args varies at each loop)
    M, C, K, rho, Area = args_cte
    args = (M, C, K, rho, Area, Ct_mean, t_wind, u_wind)
    # Setting Simulation Time and IC
    dt = t_wind[1]-t_wind[0]
    ti, tf = t_wind[0], t_wind[-1] + dt
    t_limits = [ti, tf]
    t_interval = np.arange(ti, tf, dt)
    y0 = [0, 0, 0, 0]
    # Running the integration routine
    res = solve_ivp(dydt, t_limits, y0, t_eval=t_interval, args=args)
    t, y = res.t, res.y
    # Extracting the Blade and Tower Deflection from the 2DOFs system
    xb = y[0, :]-y[1, :]
    xt = y[1, :]
    return t, xb, xt
# %% Save the Turbie simulation results


def turbie_for_TI_and_saving(TI_wanted):
    '''
    This function runs the turbie for different wind speed files, depending on
    the wanted TIs and their respective available time series recordings.

    The Turbie physical modelling is constant for all files (e.g. M,C,K...)

    The input files from each TI should be in a folder as the example below:
        Data_TI_0.1
    *for the case of a TI equal to 10%

    The function will save the response in a folder (created if not exists):
        Data_TI_0.1_out

    Parameters
    ----------
    TI_wanted : list (float)
                Values of Turbulence intensity to perform the turbie analysis

    Returns
    -------
    None.

    '''
    # Create a dictionary
    files_name = {}
    # TI needs to be a list! So thats the way
    if not isinstance(TI_wanted, list):
        Ti = [TI_wanted]
    else:
        Ti = TI_wanted
    # Constant parameters for all the loops - Assemblying 2dof matrices
    M, C, K, Area, rho = assemble_matrices_turbie()
    args_cte = (M, C, K, rho, Area)
    # Create a loop for the amount of TIs given
    for i in range(len(Ti)):
        # Looking for the Wind Input File for the given TI
        folder_path = 'turbie_bruno/Data_TI_' + str(Ti[i])
        # Load files into a dictionary files_name (only if the folder exists)
        if Path(folder_path).exists():
            files_name[Ti[i]] = glob.glob(folder_path + '/*.txt')
        else:
            # In case there is no input folder,
            # set files_name as empty and print message
            print('\nThere is no input data for TI = ' + str(Ti[i]) + '\n')
            files_name[Ti[i]] = []
        # Running the Turbie 2Dof model for each TI
        # Setting the arrays
        t_wind = []
        u_wind = []
        t = []
        xb = []
        xt = []
        label_mw = [None]*len(files_name[Ti[i]])
        # Create a loop for number of files in each TI folder
        for j in range(len(files_name[Ti[i]])):
            # Saving the label of mean wind speed
            # (could also be done by mean(u_wind))
            label_mw[j] = files_name[Ti[i]][j].split('_')[4]
            # Loading time and wind array form file
            t_wind, u_wind = open_wind(files_name[Ti[i]][j])
            # Running Turbie
            t, xb, xt = simulate_turbie(t_wind, u_wind, args_cte)
            # Merging Results into a 2D array (so to save it)
            # Define time step
            time_step = t_wind.size
            # Variables that should be save (time, wind speed, xb, xt)
            num_col = 4
            # Create an empty array to add the values
            final_output = np.empty((time_step, num_col))
            # Add values to the empty array
            final_output[:, 0] = t
            final_output[:, 1] = np.interp(t, t_wind, u_wind)
            final_output[:, 2] = xb
            final_output[:, 3] = xt
            # Creating a directory only for the first
            # loop of each TI to save results
            if j == 0:
                # Find the Parent folder of the file
                parent = Path(files_name[Ti[i]][j]).resolve().parents[0]
                # Create a twin folder but for the outputs
                output_folder = str(parent)+'_out'
                # Check whether the directory already exist,
                # avoiding error and message
                if not Path(output_folder).exists():
                    Path.mkdir(Path(output_folder))
                else:
                    print('\nWarning: The output folder for TI = ' + str(Ti[i])
                          + ' already existed and files inside '
                          'has been updated \n')
                # another way:  Path.mkdir(Path(output),exist_ok=True) -
                # but no message printed
            # Labeling output file with mean wind speed and TI
            output_file = 'Turbie_response_wind_' + label_mw[j] + '_ms_Ti_' + str(Ti[i]) + '.txt'
            # Setting the header of the output
            header = 'Time(s)\tV(m/s)\txb(m)\txt(m)'
            output = os.path.join(output_folder,output_file)
            #output = output_folder + '/' + output_file
            np.savetxt(output, final_output, fmt='%.3f', header=header,
                       delimiter='\t', comments='')
    return


# %% Plot Function


def plot_results_TI(Ti_wanted_2, sm, include_ref=False):
    '''
    This function plots 4 subplots:
        row - mean and standard deviation
        column - balde and tower deflection
    Each subplot will contain n lines (n being the # of Ti_wanted)

    If the include_ref is True, the reference will be plotted to check the
    results from the turbie_for_TI_and_saving function
    Parameters
    ----------
    Ti_wanted : list (float)
                Values of Turbulence intensity to perform the turbie analysis
    sm : dict
         Dictionary for each Ti, containing 2D array with statistics values.
    include_ref : TYPE, optional
        If user want to compare the turbie results (group4) with the reference
        given by CodeCamp
    Returns
    -------
    None.

    '''
    # Create a new list Ti with existing values
    Ti_wanted = []
    # Checking if the keys exist for sm for specific Ti
    for elem in Ti_wanted_2:
        allKeys = sm.keys()
        if elem in allKeys:
            Ti_wanted.append(elem)
        else:
            print("\nFor Plotting: \n \
                  - TI of " + str(elem) + ' does not have statistical values \
                  available')
    Ti_wanted.sort()
    # TI needs to be a list! So thats the way
    if not isinstance(Ti_wanted, list):
        Ti = [Ti_wanted]
    else:
        Ti = Ti_wanted

    # Check if Ti is empty (no available Ti)
    if not Ti:
        print('No TIs available to plot')
        return
    # Create one figure with two subplots (mean and std)
    fig, ax = plt.subplots(2, 2, clear=True, figsize=(10, 4))
    # Overall title
    # fig.suptitle('Turbie Response For Ti = '+ TI_wanted, fontsize =16)
    fig.suptitle('Turbie Response for TI = ' + str(Ti), fontsize=18)
    # Y label definition
    ax[0, 0].set_ylabel('Mean [m]', fontsize=12)
    ax[1, 0].set_ylabel('Standard Deviation [m]', fontsize=12)
    ax[0, 1].set_ylabel('Mean [m]', fontsize=12)
    ax[1, 1].set_ylabel('Standard Deviation [m]', fontsize=12)
    # X label definition
    ax[1, 0].set_xlabel('Wind Speed [m/s]', fontsize=12)
    ax[1, 1].set_xlabel('Wind Speed [m/s]', fontsize=12)
    # Setting headers
    ax[0, 0].set_title('Blade Deflection', fontsize=16)
    ax[0, 1].set_title('Tower Deflection', fontsize=16)
    # Color Vector in case of many TIs
    colors = ['#a4e700', '#2985ea', '#c423c4']
    # X limits for better visualization and grid
    ax[0, 0].set_xlim([4, 24])
    ax[0, 0].grid()
    ax[0, 1].set_xlim([4, 24])
    ax[0, 1].grid()
    ax[1, 0].set_xlim([4, 24])
    ax[1, 0].grid()
    ax[1, 1].set_xlim([4, 24])
    ax[1, 1].grid()
    if include_ref is True:
        # Include reference plot, maybe as dots
        sm_ref = calc_all_statistics(Ti, ref=True)
    # Create a loop to plot different TI curves
    for i in range(len(Ti)):
        try:
            # Plotting Mean Blade
            ax[0, 0].plot(sm[Ti[i]][:, 0], sm[Ti[i]][:, 1], color=colors[i],
                          label='TI = ' + str(Ti[i]))
            # Plotting Mean Tower
            ax[0, 1].plot(sm[Ti[i]][:, 0], sm[Ti[i]][:, 3], '--',
                          color=colors[i])
            # Plotting Std Blade
            ax[1, 0].plot(sm[Ti[i]][:, 0], sm[Ti[i]][:, 2],
                          color=colors[i])
            # Plotting Std Tower
            ax[1, 1].plot(sm[Ti[i]][:, 0], sm[Ti[i]][:, 4], '--',
                          color=colors[i])
            if include_ref is True:
                # Plotting Mean Blade - ref
                ax[0, 0].plot(sm_ref[Ti[i]][:, 0], sm_ref[Ti[i]][:, 1], '*',
                              color=colors[i],
                              label='ref - TI = ' + str(Ti[i]))
                # Plotting Mean Tower - ref
                ax[0, 1].plot(sm_ref[Ti[i]][:, 0], sm_ref[Ti[i]][:, 3], '*',
                              color=colors[i])
                # Plotting Std Blade - ref
                ax[1, 0].plot(sm_ref[Ti[i]][:, 0], sm_ref[Ti[i]][:, 2], '*',
                              color=colors[i])
                # Plotting Std Tower - ref
                ax[1, 1].plot(sm_ref[Ti[i]][:, 0], sm_ref[Ti[i]][:, 4], '*',
                              color=colors[i])
        # If there is not sm values for the wanted TI, plot error message
        except (KeyError):
            print("\nThere are no Statistical Values for TI = "
                  + str(Ti[i]) + '\n')
    # Include legend only on the top plot
    ax[0, 0].legend(ncol=len(Ti))
    return


# %% Calculation Statistical Matrix (SM) for multiple TI: import glob
def calc_sm(txt_files):
    """
    Function that calculates mean and standard deviation for multiple
    text files containing: Time, Wind speed, Blade and Tower deflection.

    Parameters
    ----------
    txt_files : list (str)
        List with paths for all the files we want to calculate statistics.

    Returns
    -------
    array
        array of dimensions ([number of files, 5]), where each column is:
            - Mean wind speed
            - Mean blade deflection
            - Standard deviation blade deflection
            - Mean tower deflection
            - Standard deviation tower deflection
    """
    # Initialize the matrix to store the values:
    Statistics_Matrix = np.empty([len(txt_files), 5])

    for i in range(len(txt_files)):
        # Reads values from text file, and store them as list
        t, u, xb, xt = np.loadtxt(txt_files[i], skiprows=1, unpack=True)

        # Calculation of statistics:
        u_mean = np.mean(u)
        xb_mean = np.mean(xb)
        xb_Std = np.std(xb)
        xt_mean = np.mean(xt)
        xt_Std = np.std(xt)

        # Saving values in the statistics matrix:
        Statistics_Matrix[i, :] = [u_mean, xb_mean, xb_Std, xt_mean, xt_Std]

        # Sorting values to show from lower to high wind speed:
        sorted_indices = Statistics_Matrix[:, 0].argsort()
        sm_sorted = Statistics_Matrix[sorted_indices]

    return sm_sorted
# %% Function to check if string can be converted to float


def is_valid_float(num):
    """Check if the input can be converted to float

    Parameters
    ----------
    num : str
        String value provided by the user

    Returns
    -------
    bool
    """
    try:
        float(num)
        return True
    except ValueError:
        return False


# %% Function that will ask if you want to run the code again


def code_run():
    """
    Inform the user the input values are not valid.
    Ask to the user if wants to try again:
    - If Yes, then it runs function ask_for_ti().
    - If No, stop code and display message 'Code has stop.'

    Returns
    -------
    None.

    """
    # Inform the user values are not valid
    print('\n Values input are not valid.')
    print('Ensure Ti values are float type. Example: 0.05, 0.1, 0.15')
    # Ask the user if it wants to continue
    cont = input('Do you want to try again (y/n): ')
    if cont in ('y', 'Y'):
        ask_for_ti()
    else:
        print('Code has stop.')
        return


# %% Function to request Ti values from the user:
def ask_for_ti():
    """
    Request from the user TI values to perform the analysis, and
    ensure values can be converted to float.

    Returns
    -------
    Ti : list (float)
        Values of Turbulence intensity to perform the statistical analysis.

    Example
    -------
    >>> Ti_test = ask_for_ti()
    >>> var_type = type(Ti_test)
    >>> print('The values provided were: ' + str(Ti_test))
    >>> print('The values are a type: ' + str(var_type))

    """
    Ti = []
    Ti_txt = input('Select the TI do you want to calculate the statistics.'
                   ' If is more than one, please separete them with a , :')
    Ti_sep = Ti_txt.split(',')
    for num in Ti_sep:
        if is_valid_float(num) is True:
            Ti.append(float(num))
        else:
            code_run()
    return Ti


# %% Function to calculate Turbie statistics for different Ti:


def calc_all_statistics(Ti, ref=False):
    """
    Calculate all statistics for all the files inside the output folder
    for Ti values.
    Parameters
    ----------
    Ti: list (float)
        Values of Turbulence intensity to perform the statistical analysis.
    ref: boolean
         in case the function is used for the reference response files

    Returns
    -------
    sm : dict
        Dictionary for each Ti, containing 2D array with statistics values.

    Example
    -------
    >>> Ti = [0.05, 0.1]
    >>> sm_test = cal_all_statistics(Ti)
    >>> print(sm_test)
    """
    sm = {}
    # Start loops for each TI, to go into the output folder:
    for i in range(len(Ti)):
        # Looking for the folder path for one Ti:
        if ref is False:
            folder_path = './Data_TI_' + str(Ti[i]) + '_out'
        else:
            folder_path = './Reference_Data/resp_TI_' + str(Ti[i])
        # Checks if the folder output exists:
        if os.path.exists(folder_path):
            txt_files = glob.glob(folder_path + '/*.txt')
            # Save information in Statistics matrix for each TI in each loop:
            sm[Ti[i]] = calc_sm(txt_files)
            # print(sm[Ti[i]])
        else:
            print("\nFor Statistics Matrix Calculation:\n \
                  - TI of " + str(Ti[i]) + " folder can not be found.")
            print("\n            This could be due to: \n \
                  - No information for this TI is available \n \
                  - TI output folder has not been generated.")
    return sm
