from pymatgen import Lattice, Structure
from ast import literal_eval
from shutil import copyfile
import pymatgen as mg
import pandas as pd
import numpy as np
import subprocess
import functions
import sys
import os

sys.argv[1:] = [literal_eval(i) for i in sys.argv[1:]]  # Convert types

# Input parameters
contcar = 'restart.txt'  # The CONTCAR file
potcar = 'ZrCu.lammps.eam'  # The VASP potential file
incar_name = '../../../run_creator/templates/incar/Zr50Cu50_step_down'  # The VASP input file
submit = '../../../run_creator/templates/submit/bardeen_morgan.q'  # The submit file
fits = '../../../run_creator/data_input/data.csv'  # Data for linear fits
time_step = 0.001  # Time step
hold_steps = 3000  # The number of hold steps
dT = sys.argv[1]  # Change in temperature
min_temp = sys.argv[2]  # The minimum allowable temperature hold

fits = pd.read_csv(fits)  # Load TV curves

cwd = os.getcwd()
temp = float(os.path.basename(cwd))-dT

if temp >= min_temp:

    # Random integer
    seed = np.random.randint(100000, 999999)

    dir_name = os.path.join('../', str(temp))
    functions.create_dir(dir_name)

    # Read composition from name
    composition = incar_name.split('/')[-1].split('_')[0]

    fit = fits.loc[fits['composition'] == composition].values[0]
    m = fit[1]
    b = fit[2]

    # Change volume
    length = m*temp+b

    # Open and read template
    incar = open(incar_name)
    incar_contents = incar.read()
    incar.close()

    # Write INCAR file
    contents = incar_contents.replace('$side$', str(length))
    contents = contents.replace('$time_step$', str(time_step))
    contents = contents.replace('$temp$', str(temp))
    contents = contents.replace('$steps$', str(hold_steps))
    contents = contents.replace('$seed$', str(seed))

    file_out = open(os.path.join(dir_name, 'INCAR'), 'w')
    file_out.write(contents)
    file_out.close()

    # Save input files
    copyfile(contcar, os.path.join(dir_name, contcar))
    copyfile(potcar, os.path.join(dir_name, potcar))
    copyfile(submit, os.path.join(dir_name, 'parallel.sh'))

    os.chdir(dir_name)  # Change working directory
