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

### A.2.2 Pressure Equilibration
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

#### A.3 Production MD
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
