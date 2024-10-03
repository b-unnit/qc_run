from pathlib import Path
import subprocess

def orca(run_dir, nprocs = 8, mem = "4GB", partition = "qcmm", inp = "inp.dat", out = "out.dat", version = "4.2.1-gompi-2019a", name="job"):
    jobName = run_dir / Path("ORCA_" + name + ".sh")
    sbatch_string = '''#!/bin/bash
#SBATCH --job-name  {0}
#SBATCH --error={0}.e%A
#SBATCH --output={0}.o%A
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --chdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}

# Setting the variables
ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

# Create scratch dir and copy the inputfile to scratch
cd $WORKDIR
mkdir $SCRDIR
cp {6} $SCRDIR
cd $SCRDIR

# Loading the Orca environment
ulimit -n 4096
export MODULEPATH=/opt/easybuild/modules/all
module load ORCA/{5}

echo "Using the following orca version:"
which orca

# Setting the NBO variables
export NBOBIN=/opt/shared/nbo7/bin
export NBOEXE=/opt/shared/nbo7/bin/nbo7.i4.exe
export GENEXE=/opt/shared/nbo7/bin/gennbo.i4.exe

# Run calculation (Output appears in WORKDIR)
echo "Running orca..."
ORCA_EXE=$(which orca)
$ORCA_EXE {6} > $WORKDIR/{7} 2>&1

# Copy the relevant files to WORKDIR and removing the SCDIR
shopt -s extglob
cp !(*.tmp) $WORKDIR/
shopt -u extglob
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs), str(run_dir), mem, partition, version, str(inp), str(out))
    return sbatch_string, jobName



def orca_amd(run_dir, nprocs = 8, mem = "4GB", partition = "qcmm", inp = "inp.dat", out = "out.dat", version = "orca_4_2_1_linux_x86-64_openmpi314", name="job"):
    jobName = run_dir / Path("ORCA_" + name + ".sh")
    sbatch_string = '''#!/bin/bash
#SBATCH --job-name  {0}
#SBATCH --error={0}.e%A
#SBATCH --output={0}.o%A
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --chdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}

# Setting the variables
ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

# Create scratch dir and copy the inputfile to scratch
cd $WORKDIR
mkdir $SCRDIR
cp {6} $SCRDIR
cd $SCRDIR

# Loading the Orca environment
ulimit -n 4096

export PATH="$PATH:/opt/shared/openmpi-3.1.4/bin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/opt/shared/openmpi-3.1.4/lib/"
export PATH="$PATH:/opt/shared/{5}"
#BINDIR=/opt/shared/{5}


echo "Using the following orca version:"
which orca

# Setting the NBO variables
export NBOBIN=/opt/shared/nbo7/bin
export NBOEXE=/opt/shared/nbo7/bin/nbo7.i4.exe
export GENEXE=/opt/shared/nbo7/bin/gennbo.i4.exe

# Run calculation (Output appears in WORKDIR)
echo "Running orca..."
ORCA_EXE=$(which orca)
$ORCA_EXE {6} > $WORKDIR/{7} 2>&1

# Copy the relevant files to WORKDIR and removing the SCDIR
shopt -s extglob
cp !(*.tmp) $WORKDIR/
shopt -u extglob
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs), str(run_dir), mem, partition, version, str(inp), str(out))
    return sbatch_string, jobName


def psi4(run_dir, nprocs = 6, mem = "8GB", partition = "qcmm", inp = "inp.dat", out = "out.dat", version ="1.2.1", name="job"):
    jobName = run_dir / Path("Psi4_" + name + ".sh")
    sbatch_string = '''#!/bin/bash
#SBATCH --job-name  {0}
#SBATCH --error={0}.e%A
#SBATCH --output={0}.o%A
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --chdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}

echo "Loading Psi4 environment..."
ID=$SLURM_JOB_ID
source /opt/anaconda/anaconda3/etc/profile.d/conda.sh
conda activate psi4-{5}

export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}
export PSI_SCRATCH=$SCRDIR/data

cd $WORKDIR
mkdir -p $PSI_SCRATCH
cp {6} $SCRDIR/
cd $SCRDIR

echo "Created Scratch data dir in " ${{PSI_SCRATCH}}

echo "Using the following psi4 version:"
which psi4

echo "Calling psi4..."
psi4 -i {6} -o $WORKDIR/{7} -n {1} 2>&1

shopt -s extglob
cp !(*.clean) $WORKDIR/
shopt -u extglob

cd $WORKDIR/
echo "Removing scratch dir: " $SCRDIR
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs),str(run_dir),mem, partition, version, str(inp), str(out))
    return (sbatch_string, jobName)

def terachem(run_dir, nprocs = '1', mem = "1GB", partition = "terachem", inp = "inp.dat", out = "out.dat", version ="1.9.lua", name="job"):
    jobName = run_dir / Path("Terachem_" + name + ".sh")
    sbatch_string = '''#!/bin/bash

#SBATCH --job-name  {0}
#SBATCH --error={0}.e%A
#SBATCH --output={0}.o%A
#SBATCH --nodes=1
#SBATCH --gres=gpu:{1}
#SBATCH --tasks-per-node=1
#SBATCH --workdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}

ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

cd $WORKDIR
mkdir $SCRDIR
cp -rp {6} $SCRDIR/
cd $SCRDIR

export MODULEPATH=/opt/easybuild/modules/all
module load Terachem/{5}

$TeraChem/bin/terachem {6} > $WORKDIR/{7} 2>&1

cp -rp * $WORKDIR/
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs),str(run_dir),mem, partition, version, str(inp), str(out))
    return (sbatch_string, jobName)

def gaussian(run_dir, nprocs = 8, mem = "4GB", partition = "qcmm", inp = "inp.dat", out = "out.dat", version = "16-AVX.lua", name="job"):
    jobName = run_dir / Path("G16_" + name + ".sh")
    sbatch_string = '''#!/bin/bash
#SBATCH --job-name  {0}
#SBATCH --error={0}.e%A
#SBATCH --output={0}.o%A
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --chdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}

# Setting the variables
ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

# Create scratch dir and copy the inputfile to scratch
cd $WORKDIR
mkdir $SCRDIR
cp {6} $SCRDIR
cd $SCRDIR

# Loading the Gaussian environment
ulimit -n 4096
export MODULEPATH=/opt/easybuild/modules/all
module load Gaussian/{5}

echo "Using the following gaussian version:"
which g16

# Run calculation (Output appears in WORKDIR)
echo "Running gaussian..."
GAUSSIAN_EXE=$(which g16)
$GAUSSIAN_EXE < {6} > $WORKDIR/{7} 2>&1

# Copy the relevant files to WORKDIR and removing the SCDIR
shopt -s extglob
cp !(*.tmp) $WORKDIR/
shopt -u extglob
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs), str(run_dir), mem, partition, version, str(inp), str(out))
    return sbatch_string, jobName


def molpro(run_dir, nprocs = 8, mem = "4GB", partition = "qcmm", inp = "inp.dat", out = "out.dat", version = "2020_1_2_linux_x86_64_openmp", name="job"):
    jobName = run_dir / Path("MOLPRO_" + name + ".sh")
    sbatch_string = '''#!/bin/bash
# SLURM script parameters
#SBATCH -J {0}
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --mem={2}
#SBATCH --partition={3}

ID=$SLURM_JOB_ID
export WORKDIR=$SLURM_SUBMIT_DIR
export SCRDIR=/scratch/${{ID}}

# Create scratch dir and copy the inputfile to scratch
cd $WORKDIR
mkdir $SCRDIR
cp {4} $SCRDIR
cd $SCRDIR

# Loading the Molpro environment
export MODULEPATH=/opt/easybuild/modules/all
module load Molpro/{5}

# Run calculation (Output appears in WORKDIR)
MOLPRO_EXE=$(which molpro)
$MOLPRO_EXE -t {1} -d $SCRDIR {4} > $WORKDIR/{6} 2>&1
echo $MOLPRO_EXE -t {1} -d $SCRDIR {4} > $WORKDIR/{6}

# Copy the relevant files to WORKDIR and removing the SCDIR
shopt -s extglob
cp !(*.tmp) $WORKDIR/
shopt -u extglob
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs),  mem, partition,  str(inp), version, str(out))
    return sbatch_string, jobName
