from pathlib import Path
import subprocess

def orca(run_dir, nprocs = 8, mem = "4GB", partition = "intel", inp = "inp.dat", out = "out.dat", version ="_4_0_0_2_linux_x86-64", name="job"):
    jobName = run_dir / Path("ORCA_" + name + ".sh")
    sbatch_string = '''#!/bin/bash

#SBATCH -J {0}
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --workdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}
#SBATCH --cpu-bind=ldoms

# Setting the variables
ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

cd $WORKDIR
mkdir $SCRDIR
cp {6} $SCRDIR/
cd $SCRDIR

export ORCA_PATH=/opt/shared/orca{5}
source /opt/shared/openmpi-2.0.1/environment.sh
ulimit -n 4096
BINDIR=/opt/shared/orca{5}

MY_PROG="${{BINDIR}}/orca {6} "
$MY_PROG > $WORKDIR/{7} 2>&1

shopt -s extglob
cp !(*.tmp) $WORKDIR/
shopt -u extglob

cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs),str(run_dir),mem,partition,version, str(inp), str(out))
    jobName.write_text(sbatch_string)
    process = subprocess.getoutput("qsub "+str(jobName))
    infos = " Job with the ID {} was submitted in {}".format(process, run_dir)
    print(infos)

def orca_eb(run_dir, nprocs = 8, mem = "4GB", partition = "intel", inp = "inp.dat", out = "out.dat", name="job", wf=False):
    jobName = run_dir / Path("ORCA_" + name + ".sh")
    sbatch_string = '''#!/bin/bash

#SBATCH -J {0}
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --workdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}
#SBATCH --cpu-bind=ldoms

# Setting the variables
ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

# Create scratch dir and copy the inputfile to scratch
cd $WORKDIR
mkdir $SCRDIR
cp {5} $SCRDIR
cd $SCRDIR

# Loading the Orca environment
ulimit -n 4096
export MODULEPATH=/opt/easybuild/modules/all
module load ORCA/4.1.0-OpenMPI-3.1.3


# Run calculation (Output appears in WORKDIR)
ORCA_EXE=$(which orca)
$ORCA_EXE {5} > $WORKDIR/{6} 2>&1

# Copy the relevant files to WORKDIR and removing the SCDIR
shopt -s extglob
cp !(*.tmp) $WORKDIR/
shopt -u extglob
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs), str(run_dir),mem, partition, str(inp), str(out))
    return (sbatch_string, jobName)

def psi4(run_dir, nprocs = 8, mem = "8GB", partition = "intel", inp = "inp.dat", out = "out.dat", version ="1.2.1", name="job"):
    jobName = run_dir / Path("Psi4_" + name + ".sh")
    sbatch_string = '''#!/bin/bash

#SBATCH -J {0}
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --workdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}
#SBATCH --cpu-bind=ldoms

ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

cd $WORKDIR
mkdir $SCRDIR
cp -rp {6} $SCRDIR/
cd $SCRDIR

source /opt/shared/psi4conda-{5}/environment.sh
#export PATH=/opt/shared/psi4conda-20190717/bin:/opt/shared/mrcc:$PATH

psi4 -i {6} -o $WORKDIR/{7} -n {1}

cp -rp * $WORKDIR/
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs),str(run_dir),mem, partition, version, str(inp), str(out))
    jobName.write_text(sbatch_string)
    process = subprocess.getoutput("qsub "+str(jobName))
    infos = " Job with the ID {} was submitted in {}".format(process, run_dir)
    print(infos)

def psi4_eb(run_dir, nprocs = 8, mem = "8GB", partition = "intel", inp = "inp.dat", out = "out.dat", version ="1.2.1", name="job"):
    jobName = run_dir / Path("Psi4_" + name + ".sh")
    sbatch_string = '''#!/bin/bash

#SBATCH -J {0}
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --workdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}
#SBATCH --cpu-bind=ldoms

ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

cd $WORKDIR
mkdir $SCRDIR
cp -rp {6} $SCRDIR/
cd $SCRDIR

source /opt/anaconda/anaconda3/etc/profile.d/conda.sh
conda activate psi4

psi4 -i {6} -o $WORKDIR/{7} -n {1}

cp -rp * $WORKDIR/
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs),str(run_dir),mem, partition, version, str(inp), str(out))
    jobName.write_text(sbatch_string)
    process = subprocess.getoutput("qsub "+str(jobName))
    infos = " Job with the ID {} was submitted in {}".format(process, run_dir)
    print(infos)

def terachem(run_dir, nprocs = '4', mem = "8GB", partition = "terachem", inp = "inp.dat", out = "out.dat", version ="", name="job"):
    jobName = run_dir / Path("Terachem_" + name + ".sh")
    #gpu_num = len(gpus.split(','))
    sbatch_string = '''#!/bin/bash

#SBATCH -J {0}
#SBATCH --nodes=1
#SBATCH --gres=gpu:{1}
#SBATCH --tasks-per-node=1
#SBATCH --workdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}
#SBATCH --cpu-bind=ldoms

ID=$SLURM_JOB_ID
export WORKDIR={2}
export SCRDIR=/scratch/${{ID}}

cd $WORKDIR
mkdir $SCRDIR
cp -rp {6} $SCRDIR/
cd $SCRDIR

source /opt/shared/Terachem/SetTCVars.sh
export MagmaNGPUs={1}

$TeraChem/bin/terachem {6} > $WORKDIR/{7} 2>&1

cp -rp * $WORKDIR/
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs),str(run_dir),mem, partition, version, str(inp), str(out))
    jobName.write_text(sbatch_string)
    process = subprocess.getoutput("qsub "+str(jobName))
    infos = " Job with the ID {} was submitted in {}".format(process, run_dir)
    print(infos)

def gaussian(run_dir, nprocs = 8, mem = "8GB", partition = "intel", inp = "inp.dat", out = "out.dat", version ="", name="job"):
    jobName = run_dir / Path("G16_" + name + ".sh")
    inputfile = run_dir / inp
    sbatch_string = '''#!/bin/bash

#SBATCH -J {0}
#SBATCH --nodes=1
#SBATCH --tasks-per-node={1}
#SBATCH --workdir={2}
#SBATCH --mem={3}
#SBATCH --partition={4}
#SBATCH --cpu-bind=ldoms

ID=$SLURM_JOB_ID
WORKDIR={2}

cd $WORKDIR
export SCRDIR=/scratch/${{ID}}

export g16root=/opt/shared
export GAUSS_SCRDIR=/scratch/${{ID}}
. $g16root/g16/bsd/g16.profile

mkdir $SCRDIR
cp -rp * $SCRDIR/
cd $SCRDIR
g16 -p={1} -m={3} < {6} > $WORKDIR/{7}
cp -rp * $WORKDIR/
cd $WORKDIR/
rm -rf $SCRDIR
    '''.format(jobName.stem, str(nprocs),str(run_dir),mem, partition, version, str(inputfile), str(outputfile))
    jobName.write_text(sbatch_string)
    process = subprocess.getoutput("qsub "+str(jobName))
    infos = " Job with the ID {} was submitted in {}".format(process, run_dir)
    print(infos)
