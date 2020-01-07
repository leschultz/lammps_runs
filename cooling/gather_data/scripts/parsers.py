import pandas as pd
import numpy as np


def output(path):
    '''
    Parse the VASP print to screen file.

    inputs:
        path = The file path.

    outputs:
        error = Whether or not there was an error.
    '''

    # Check if the run has any errors
    error = False
    with open(path) as f:
        for line in f:
            if 'ERROR' in line:
                error = True

    return error


def incar(path):
    '''
    Parse INCAR file.

    inputs:
        path = The file path.

    outputs:
        param = The input parameters.
    '''

    param = {}
    with open(path) as f:
        for line in f:
            line = line.strip().split(' ')

            if 'eqtemp' in line:
                param['TEBEG'] = float(line[-1])
                param['TEEND'] = float(line[-1])

            if 'mytimestep' in line:
                param['POTIM'] = float(line[-1])

            if 'pair_coeff' in line:
                elements = line[4:]
                number = list(range(1, len(elements)+1))
                param['elements'] = dict(zip(number, elements))

    return param


def poscar(path):
    '''
    Parse POSCAR file.

    inputs:
        path = The file path.

    outputs:
        lattice = The lattice parameters.
        coords = The atom coordinates.
    '''

    df = []

    count = 0
    with open(path) as f:
        for line in f:
            if 'ITEM' in line:
                count += 1

            if count == 4:
                line = line.strip().split(' ')
                if 'ITEM:' in line:
                    headers = line[2:]

                else:
                    df.append(line)

            if count > 4:
                break

    df = pd.DataFrame(df, columns=headers)

    elements = df['type'].values
    elements = list(map(lambda x: int(x), elements))
    elements, numbers = np.unique(elements, return_counts=True)

    return elements, numbers


def outcar(path):
    '''
    Parse OUTCAR file.

    inputs:
        path = The file path.

    outputs:
        volumes = The volume data.
        pressures =  The pressure data.
        temperatures = The temperature data.
    '''

    df = []  # Avoid unusual printing occasionally seen

    count = 0
    with open(path) as f:
        for line in f:
            line = line.strip().split(' ')

            if count == 1:
                headers = line[1:]

            if count > 1:
                line = list(map(lambda x: float(x), line))
                df.append(line)

            count += 1

    # Create dataframe
    df = pd.DataFrame(df, columns=headers)

    # Prepare values for export
    volumes = df['v_vol'].values
    pressures = df['c_pressure'].values
    temperatures = df['c_temp'].values
    total_energy = df['c_pe']+df['c_ke']
    total_energy = total_energy.values

    return volumes, pressures, temperatures, total_energy
