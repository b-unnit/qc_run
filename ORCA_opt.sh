#!/bin/bash
#SBATCH --job-name  ORCA_opt
#SBATCH --error=ORCA_opt.e%A
#SBATCH --output=ORCA_opt.o%A
#SBATCH --nodes=1
#SBATCH --cores-per-socket=8
#SBATCH --chdir=/home/svogt/repos/qc_run
#SBATCH --mem=12GB
#SBATCH --partition=intel

# Setting the variables
ID=$SLURM_JOB_ID
export WORKDIR=/home/svogt/repos/qc_run
export SCRDIR=/scratch/${ID}

# Create scratch dir and copy the inputfile to scratch
cd $WORKDIR
mkdir $SCRDIR
cp inp.dat $SCRDIR
cd $SCRDIR

# Loading the Orca environment
ulimit -n 4096
export MODULEPATH=/opt/easybuild/modules/all
module load ORCA/4.2.1-gompi-2019a

echo "Using the following psi4 version:"
which orca

# Run calculation (Output appears in WORKDIR)
echo "Running orca..."
ORCA_EXE=$(which orca)
$ORCA_EXE inp.dat > $WORKDIR/out.dat 2>&1

# Copy the relevant files to WORKDIR and removing the SCDIR
shopt -s extglob
cp !(*.tmp) $WORKDIR/
shopt -u extglob
cd $WORKDIR/
rm -rf $SCRDIR
    