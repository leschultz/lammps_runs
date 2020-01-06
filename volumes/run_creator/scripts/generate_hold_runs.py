from ast import literal_eval
from shutil import copyfile

import numpy as np
import functions
import sys
import os

sys.argv[1:] = [literal_eval(i) for i in sys.argv[1:]]  # Convert types

# Input paramters
elements = sys.argv[1]  # Elements
numbers = sys.argv[2]  # Number corresponding to each element
save = sys.argv[3]  # Location to save POSCAR
runs = sys.argv[4]  # List of cubic lattice constants
incar = sys.argv[5]  # The VASP input file
potcar = sys.argv[6]  # The VASP potential file
submit = sys.argv[7]  # The cluster submit file

# Open submit template
incar = open(incar)
incar_contents = incar.read()
incar.close()

# Generate runs
count = 1
total = str(len(runs))
for number in runs:
    run = os.path.join(save, str(number))

    # Write run
    functions.create_dir(run)

    # Write input files
    contents = incar_contents.replace('$side$', str(number))
    contents = contents.replace('$lattice$', str(number/5))
    incar_out = open(os.path.join(run, 'INCAR'), 'w')
    incar_out.write(contents)
    incar_out.close()

    copyfile(potcar, os.path.join(run, potcar.split('/')[-1]))
    copyfile(submit, os.path.join(run, 'parallel.sh'))

    # Status update
    print('Generated ('+str(count)+'/'+total+')'+run)

    count += 1
