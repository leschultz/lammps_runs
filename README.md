# MD Run Creator and Analyzer

This tool aids in the production of standard LAMMPS NVT isothermal runs.

## Running

Under each main working directory, there are general directories containing the following: executables containing bash files that provide input arguments to python scripts when applicable, scripts containing analysis scripts that may have some input parameters within, data where data is saved, templates where file templates are used to create runs, and figures where figures are saved. The structure is as follows:

```
./vasp_runs
├── cooling
│   └── run_creator
│       ├── data_input
│       ├── executables
│       ├── scripts
│       └── templates
│           ├── incar
│           ├── kpoints
│           ├── poscar
│           └── submit
├── dmax
│   ├── data
│   ├── figures
│   └── scripts
├── README.md
└── volumes
    ├── gather_data
    │   ├── data
    │   ├── figures
    │   └── scripts
    ├── lv_curves
    │   ├── data
    │   ├── figures
    │   └── scripts
    ├── run_creator
    │   ├── executables
    │   │   ├── cluster_submit
    │   │   ├── generate_runs
    │   │   └── run_types
    │   ├── scripts
    │   └── templates
    │       ├── incar
    │       ├── kpoints
    │       ├── poscar
    │       └── submit
    ├── tv_curves
    │   ├── data
    │   ├── figures
    │   └── scripts
    └── volume_guesser
```

## Coding Style

Python scripts follow PEP 8 guidelines. A usefull tool to use to check a coding style is pycodestyle.

```
pycodestyle <script>
```

## Authors

* **Lane Schultz** - *Data Creation and Analysis* - [leschultz](https://github.com/leschultz)

## Acknowledgments

* The Computational Materials Group (CMG) at the University of Wisconsin - Madison
* Dr. Dane Morgan for computational material science guidence
* Dr. Izabela Szlufarska for computational material science guidence
