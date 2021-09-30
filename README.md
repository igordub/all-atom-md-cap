# All-atom Molecular Dynamics Simulation of CAP

Scritps for AMBER simulations are take from [David Burnell's PhD thesis](http://etheses.dur.ac.uk/11055/), Appendix A. Normal Mode Analysis has been performed in GROMACS, Appendix B.

## All-atom MD
### A.1 Energy Minimisation
#### A.1.1 Minimising Solvent
```
CAP_2cAMP: initial minimisation solvent + ions
&cntrl
imin = 1, maxcyc = 10000,
ncyc = 5000, ntb = 1,
ntr = 1, cut = 10.0,
ntwx = 100
/
Hold the Protein fixed
500.0
RES 1 403
END
END
```

#### A.1.2 Minimising Solute
```
CAP_2cAMP: initial minimisation whole system
&cntrl
imin = 1, maxcyc = 50000,
ncyc = 25000, ntb = 1,
ntr = 0, cut = 10.0
/
```

### A.2 Equilibration
#### A.2.1 Temperature Equilibration
```
CAP_2cAMP: heat equilibration
&cntrl
imin=0, irest=0,
nstlim=100000, dt=0.002,
ntc=2, ntf=2,
cut=10.0, ntb=1,
ntpr=500, ntwx=5000,
ntt=3, gamma_ln=1.0,
ntx=1, ig=-1,
tempi=0.0, temp0=300.0,
ntr=1, ioutfm=1
/
Keep CAP fixed with weak restraints
2.5
RES 1 403
END
END
```

#### A.2.2 Pressure Equilibration
```
CAP_2cAMP: density equilibration
&cntrl
imin=0, irest=1,
nstlim=25000, dt=0.002,
ntc=2, ntf=2,
ntx=5, taup=1.0,
cut=8.0, ntb=2,
ntpr=500, ntwx=500,
ntt=3, gamma_ln=2.0,
temp0=300.0, ig=-1,
ntr=1, ioutfm=1,
ntp=1
/
Keep CAP fixed with weak restraints
10.0
RES 1 403
END
END
```

### A.3 Production MD
```
CAP_2cAMP: 4000ps of production MD
&cntrl
imin = 0, irest = 1,
ntb = 2, pres0 = 1.0,
taup = 2.0, iwrap=1,
cut = 10.0, ntr = 0,
ntc = 2, ntf = 2,
temp0 = 300.0, ntx = 5,
ntt = 3, gamma_ln = 1.0,
ntp = 1, ig=-1,
nstlim = 2000000, dt = 0.002,
ntpr = 5000, ntwx = 5000,
ntwr = 10000, ioutfm=1
/
```

### A.4 Sample Script for MD
```bash
module purge
module load dot
module load amber/cuda/SPDP/gcc/12.0
PROTEIN=cap
VAR=2CAMP
#Execute Commands
pmemd.cuda -O -i ../../wat_min1.in -o ${PROTEIN}_${VAR}_min1.out -p ${PROTEIN}_${VAR}.prmtop -c
${PROTEIN}_${VAR}.inpcrd -r ${PROTEIN}_${VAR}_min1.rst -ref ${PROTEIN}_${VAR}.inpcrd
#
pmemd.cuda -O -i ../../wat_min2.in -o ${PROTEIN}_${VAR}_min2.out -p ${PROTEIN}_${VAR}.prmtop -c
${PROTEIN}_${VAR}_min1.rst -r ${PROTEIN}_${VAR}_min2.rst
#
pmemd.cuda -O -i ../../heat_nc.in -o ${PROTEIN}_${VAR}_heat.out -p ${PROTEIN}_${VAR}.prmtop -c
${PROTEIN}_${VAR}_min2.rst -r ${PROTEIN}_${VAR}_heat.rst -ref ${PROTEIN}_${VAR}_min2.rst -x
${PROTEIN}_${VAR}_heat.nc
#
pmemd.cuda -O -i ../../density_nc.in -o ${PROTEIN}_${VAR}_density.out -p
${PROTEIN}_${VAR}.prmtop -c ${PROTEIN}_${VAR}_heat.rst -r ${PROTEIN}_${VAR}_density.rst -ref
${PROTEIN}_${VAR}_heat.rst -x ${PROTEIN}_${VAR}_density.nc
#
pmemd.cuda -O -i ../../md-prod_nc.in -o ${PROTEIN}_${VAR}_mdprod1.out -p
${PROTEIN}_${VAR}.prmtop -c ${PROTEIN}_${VAR}_density.rst -r ${PROTEIN}_${VAR}_mdprod1.rst -x
${PROTEIN}_${VAR}_mdprod1.nc
```

## NMA
### B.1 Energy Minimisation
```
; STANDARD MD INPUT OPTIONS NMA MINIMISATION
; for use with GROMACS
define = -DFLEXIBLE
constraints = none
integrator = l-bfgs
tinit = 0
nsteps = 100000
nbfgscorr = 50
emtol = .0005
emstep = 0.1
gen_vel = yes
gen-temp = 300
nstcomm = 1
; NEIGHBORSEARCHING PARAMETERS
; nblist update frequency
nstlist = 0
; ns algorithm (simple or grid)
ns-type = simple
; Periodic boundary conditions:
pbc = no
; nblist cut-off
rlist = 0
domain-decomposition = no
; OPTIONS FOR ELECTROSTATICS AND VDW
; Method for doing electrostatics
coulombtype = Cut-Off
rcoulomb-switch = 0
rcoulomb = 0
; Dielectric constant (DC) for cut-off or DC of reaction field
epsilon-r = 1
; Method for doing Van der Waals
vdw-type = Cut-off
; cut-off lengths
rvdw-switch = 0
rvdw = 0
```

### B.2 Normal Mode Analysis
```
; STANDARD MD INPUT OPTIONS NMA
; for use with GROMACS
define = -DFLEXIBLE
constraints = none
integrator = nm
tinit = 0
nsteps = 100000
nbfgscorr = 50
emtol = .0005
emstep = 0.1
gen_vel = yes
gen-temp = 300
nstcomm = 1
; NEIGHBORSEARCHING PARAMETERS
; nblist update frequency
nstlist = 0
; ns algorithm (simple or grid)
ns-type = simple
; Periodic boundary conditions: xyz (default), no (vacuum)
; or full (infinite systems only)
pbc = no
; nblist cut-off
rlist = 0
domain-decomposition = no
; OPTIONS FOR ELECTROSTATICS AND VDW
; Method for doing electrostatics
coulombtype = Cut-Off
rcoulomb-switch = 0
rcoulomb = 0
; Dielectric constant (DC) for cut-off or DC of reaction field
epsilon-r = 1
; Method for doing Van der Waals
vdw-type = Cut-off
; cut-off lengths
rvdw-switch = 0
rvdw = 0
```
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

# All-atom Molecular Dynamics of the SARS-CoV-2 PLpro

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

We perform all-atom MD simualtion of the SCoV2-PLpro to inform construction of the Elastic Network Model (ENM) for the same protein.

PDB ID: [6WX4](https://www.rcsb.org/structure/6WX4)
### Built With

* [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/)


<!-- GETTING STARTED -->
## Getting Started

Simply, clone the repo to your machine.
Clone the repo:
```bash
git clone https://github.com/igordub/md-scov2-plpro.git
```

### Prerequisites

If you have Conda installed on your machine simply create a separate Conda environment and intall AmberTools from the `conda-forge` channel. Alternatively, download and install form the [source](https://ambermd.org/GetAmber.php).
* AmberTools21
  ```bash
  conda create --name AmberTools21
  conda activate AmberTools21
  conda install -c conda-forge ambertools=21 compilers
  ```

Grant execution permissions to a shell script that you want to run
```bash
chmod u+x src/structurre/prepare_pdb.sh
```
or give the permission to all scritps at once()
```bash
chmod u+x src/*/*.sh
```
### Installation

No istallation is needed.

<!-- USAGE EXAMPLES -->
## Usage
1. Download the strucutre file and configure it for AMBER
    ```bash
    ./src/structure/prepare_pdb.sh
    ```

2. Create parameter and coordinate files for the ligand
    ```bash
    ./src/structure/prepare_ligand_ff.sh
    ```    
    
**Note** The shell scripts are configured to be run on the [Viking](https://www.york.ac.uk/it-services/services/viking-computing-cluster/) (research computing clsuter at the University of York). However, computationally easy jobs, like structure configuration and minimisation, can be done on a desktop or laptop in a reasonable amount of time.

## Miscellaneous

- AMBER input files **must** end with an empty line. Otherwise, Fortran executable produe segmentation error:
  ```
  At line 639 of file mdin_ctrl_dat.F90 (unit = 5, file = 'src/production/prod.in')
  Fortran runtime error: End of file

  Error termination. Backtrace:
  #0  0x7f4a90f4dedb in next_record_r
    at ../../../libgfortran/io/transfer.c:3144
  #1  0x7f4a90f50327 in finalize_transfer
    at ../../../libgfortran/io/transfer.c:3629
  #2  0x418e42 in ???
  #3  0x4ae5d0 in ???
  #4  0x495ace in ???
  #5  0x4060bc in ???
  #6  0x7f4a907bf554 in ???
  #7  0x40a2c6 in ???
  #8  0xffffffffffffffff in ???
  ```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/igordub/md-scov2-plpro/issues) for a list of proposed features (and known issues).
Currently, the main and only issue is in creating a force field modification for the ligand.


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Igors Dubanevics - [@IgorsDubanevics](https://twitter.com/IgorsDubanevics)

Project Link: [https://github.com/igordub/md-scov2-plpro](https://github.com/igordub/md-scov2-plpro)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png

<!-- APENDIX -->
## Apendix
### Original README
```
#####                          Resubmission Scripts                      ######

To treat the ligand seperately to the main protein, a forcefield mod file needs
to be created. Antechamber.job does this and uses the 6wx4_lig.pdb file for 
its input. After the forcefield mod file is created, tleap is run using the
leapscript. (This is where errors are occuring as tleap doesn't recognise
the ligand atoms). After the crd and top files are created, the minimisation
can occur. Run min_solu.in and min_solv.in to minimise solute and solvent 
structure respectively. Heat.in anneals the system and stabalises at 300K. 
Pres.in carries out pressure equilibration. 

Prod.in runs the amber simulation for 20 ns. To run from prm top files to the 
final simulatuion use Simulate.job. To just equilibrate the system use 
Equilibration.job

Cpptraj can be used to interpret the results.
```
<!-- REFERENCES -->
## References

- [Running Minimization and MD (in explicit solvent)](https://ambermd.org/tutorials/basic/tutorial1/section5.htm)
- [Simulating a pharmaceutical compound using antechamber and the Generalized Amber Force Field](https://ambermd.org/tutorials/basic/tutorial4b/index.php)