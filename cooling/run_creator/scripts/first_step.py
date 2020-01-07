from shutil import copyfile
from os.path import join
from math import ceil
import pandas as pd
import numpy as np
import functions
import re

# Input paramters
save = '../../runs'  # Location to save POSCAR
incar = '../templates/incar/Zr50Cu50'  # The VASP input file
potcar = '../templates/potential/ZrCu.lammps.eam'  # The VASP potential file
submit = '../templates/submit/bardeen_morgan.q'  # The cluster submit file
fits = '../data_input/data.csv'  # Data for linear fits
start_temp = 2000.0  # The starting temperature
time_step = 0.001  # Time step
hold_steps = 3000  # The number of hold steps

start_temp_str = str(start_temp)

# Load the linear fits
fits = pd.read_csv(fits)

# Open and read template
incar = open(incar)
incar_contents = incar.read()
incar.close()

groups = fits.groupby(['composition'])

count = 1
total = str(fits.shape[0])
for group, values in groups:

    # Random integer
    seed = np.random.randint(100000, 999999)

    i = re.split('(\d+)', group)
    i = [j for j in i if j != '']

    for j in range(len(i)):
        try:
            i[j] = int(i[j])
        except Exception:
            pass

    numbers = [j for j in i if isinstance(j, int)]
    elements = [j for j in i if isinstance(j, str)]

    atom_count = sum(numbers)  # Total atoms
    atom_count_plus = atom_count+1  # Used in loop
    l = ceil(atom_count**(1/3))

    # Element ID based on order defined
    elements_id = list(range(1, len(elements)+1))

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

    m = values['slope'].values[0]
    b = values['intercept'].values[0]

    length = m*start_temp+b

    run = join(*[save, group, start_temp_str])

    # Write run
    functions.create_dir(run)

    # Write input files for cubic
    contents = incar_contents.replace('$side$', str(length))
    contents = contents.replace('$lattice$', str(length/l))
    contents = contents.replace('$time_step$', str(time_step))
    contents = contents.replace('$seed$', str(seed))
    contents = contents.replace('$temp$', str(start_temp))
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

    contents = contents.replace('$remove$', remove)

    print(join(run, 'INCAR'))
    file_out = open(join(run, 'INCAR'), 'w')
    file_out.write(contents)
    file_out.close()

    copyfile(potcar, join(run, potcar.split('/')[-1]))
    copyfile(submit, join(run, 'parallel.sh'))  # Save KPOINTS

    # Status update
    print('Generated ('+str(count)+'/'+total+')'+run)

    count += 1
