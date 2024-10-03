#!/opt/anaconda/anaconda3/envs/qcmm/bin/python

#Import Modules                                                               
import sys
from pathlib import Path
import argparse
import subprocess
from qc_run.sub_job import molpro as sub_molpro

# Main script
def main():
    parser = argparse.ArgumentParser(description="Submit a Molpro job to the SLURM queue.")
    parser.add_argument("job_name", help="Name of the job")
    parser.add_argument("input_file", help="Input file for the calculation")
    parser.add_argument("-d", "--directory", help="Execution directory (default = current)", default=Path.cwd())
    parser.add_argument("-o", "--outputFile", help="Output file (default = out.dat)", default="out.dat")
    parser.add_argument("-c", "--procs", help="Number of cores to use (default = 8)", type=int, default=8)
    parser.add_argument("-q", "--queue", help="Destination queue (default = qcmm)", default="qcmm")
    parser.add_argument("-m", "--mem", help="Memory to reserve (default = read from input file)", default=None)
    parser.add_argument("-n", "--non", action="store_true", help="Only save the submit script? (default = False)")
    parser.add_argument("-v", "--version", help="Molpro version to use (default = 2020_1_2_linux_x86_64_openmp)", default="2020_1_2_linux_x86_64_openmp")

    args = parser.parse_args()

    run_dir = Path(args.directory)
    jname = args.job_name
    inputFile = args.input_file
    outputFile = args.outputFile
    mem = args.mem
    version = args.version
    queue = args.queue
    proc_num = args.procs
    no_sub = args.non

    # Read memory requirement from input file if not specified
    if mem is None:
        with open(run_dir / inputFile, 'r') as fid:
            for line in fid:
                if 'memory,' in line.lower():
                    mem_words = int(line.split(',')[1].split('m')[0].strip()) # Memory in megawords
                    mem = str(int(proc_num * 1.1 * mem_words * 8 / 1024)) + "GB"  # 1.1 scaling to have a little bit of buffer memory

    sbatch_string, jobName = sub_molpro(run_dir, nprocs=proc_num, mem=mem, partition=queue, inp=inputFile, out=outputFile, version=version, name=jname)
    jobName.write_text(sbatch_string)

    if not no_sub:
        process = subprocess.getoutput(f"sbatch {jobName}")
        infos = f"Job with the ID {process} was submitted in {run_dir}"
        print(infos)

if __name__ == "__main__":
    main()
