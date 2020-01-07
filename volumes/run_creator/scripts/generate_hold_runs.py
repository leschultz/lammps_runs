from ast import literal_eval
from shutil import copyfile
from math import ceil

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
temp = sys.argv[8]  # Hold temperature
time_step = sys.argv[9]  # Time step
hold_steps = sys.argv[10]  # The number of hold steps

# Open submit template
incar = open(incar)
incar_contents = incar.read()
incar.close()

atom_count = sum(numbers)  # Total atoms
atom_count_plus = atom_count+1  # Used in loop

l = ceil(atom_count**(1/3))

# Element ID based on order defined
elements_id = list(range(1, len(elements)+1))

# Generate runs
count = 1
total = str(len(runs))
for number in runs:
    run = os.path.join(save, str(number))

    # Random integer
    seed = np.random.randint(100000, 999999)

    # Assign atom types
    atoms = []
    for i in range(1, atom_count_plus):
        atoms.append('set atom '+str(i)+' type ')

    types = []
    for i, j in zip(elements_id, numbers):
        types += [str(i)]*j

    # Shuffle order
    types = np.array(types)
    np.random.shuffle(types)

    atom_setting = ''
    for i, j in zip(atoms, types):
        atom_setting += i+j+'\n'

    # Write run
    functions.create_dir(run)

    # Write input files for cubic
    contents = incar_contents.replace('$side$', str(number))
    contents = contents.replace('$lattice$', str(number/l))
    contents = contents.replace('$time_step$', str(time_step))
    contents = contents.replace('$seed$', str(seed))
    contents = contents.replace('$temp$', str(temp))
    contents = contents.replace('$steps$', str(hold_steps))
    contents = contents.replace('$l$', str(l))
    contents = contents.replace('$atom_setting$', atom_setting)

    remove = ''
    l_cubed = l**3
    if atom_count < l_cubed:

        remove += '# Remove extra atoms \n'
        remove += 'group remove id '
        remove += str(atom_count_plus)+':'+str(l_cubed)
        remove += '\n'
        remove += 'delete_atoms group remove'

        print(remove)

    contents = contents.replace('$remove$', remove)

    incar_out = open(os.path.join(run, 'INCAR'), 'w')
    incar_out.write(contents)
    incar_out.close()

    copyfile(potcar, os.path.join(run, potcar.split('/')[-1]))
    copyfile(submit, os.path.join(run, 'parallel.sh'))

    # Status update
    print('Generated ('+str(count)+'/'+total+')'+run)

    count += 1
