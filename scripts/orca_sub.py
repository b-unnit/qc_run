#!/opt/anaconda/anaconda3/envs/qcmm/bin/python

#Import Modules                                                               
import sys, os
from pathlib import Path
from optparse import OptionParser
import subprocess
from qc_run.sub_job import orca as sub_orca

usage = "usage: %prog [options] <Nombre del proceso> <Archivo de input>"
parser = OptionParser(usage=usage)
parser.add_option("-d", dest="directory", help="Directorio destino de ejecucion del calculo (default = "+str(Path.cwd()), default=Path.cwd())
parser.add_option("-o", dest="outputFile", help="Archivo de output (default= out.dat)", default="out.dat")
parser.add_option("-c", dest="procs", help="Número de cores a usar (default= 4)", default=4)
parser.add_option("-q", dest="queue", help="Cola de destino (default = intel)", default="intel")
parser.add_option("-m", dest="mem", help="Memoria a reservar (default = 4GB)", default="4GB")
parser.add_option("-n", dest="non", action="store_true", help="Solo guardar el submit script? (Defualt = False)")
parser.add_option("-v", dest="version", help="Version de Orca a usar (default = 4.2.1)", default="4.2.1-gompi-2019a")
#parser.add_option("--parametros", dest="parametros", help="Parametros adicionales de gromax (Se ingresan entre comillas)", default="")

(options, args) = parser.parse_args()

if (len(args)!=2):
  print(usage)
  sys.exit(1)

run_dir =  Path(options.directory)
jname = args[0]
inputFile = args[1]
outputFile = options.outputFile
mem = options.mem
version = options.version
#parametros = options.parametros
queue = options.queue
proc_num = 1
no_sub = options.non
proc_num = options.procs

#with open(run_dir / inputFile, mode='r') as fid:
#    for line in fid:
#        if line.startswith('%pal'):
#            proc_num = line.split()[2]

sbatch_string, jobName = sub_orca(run_dir, nprocs = proc_num, mem = mem, partition = queue, inp = inputFile, out = outputFile, version=version,  name = jname)
jobName.write_text(sbatch_string)
if not no_sub:
    process = subprocess.getoutput("sbatch "+str(jobName))
    infos = " Job with the ID {} was submitted in {}".format(process, run_dir)
    print(infos)

