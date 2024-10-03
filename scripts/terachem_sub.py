#!/usr/bin/python  

import sys, os
from pathlib import Path
from optparse import OptionParser
import subprocess
from qc_run.sub_job import terachem as sub_terachem

usage = "usage: %prog [options] <Nombre del proceso> <Archivo de input>"
parser = OptionParser(usage=usage)
parser.add_option("-d", dest="directory", help="Directorio destino de ejecucion del calculo (default = "+str(Path.cwd()), default=Path.cwd())
parser.add_option("-o", dest="outputFile", help="Archivo de Output (default= out.dat)", default="out.dat")
parser.add_option("-g", dest="gpus", help="Numero de GPUS a usar (Defualt: 1)')", default=1)
parser.add_option("-q", dest="queue", help="Particion de destino (default = terachem)", default="terachem")
parser.add_option("-m", dest="mem", help="Memoria a reservar (default = 8GB)", default="8GB")
parser.add_option("-n", dest="non", action="store_true", help="Solo guardar el submit script? (Defualt = False)")
parser.add_option("-v", dest="version", help="Version de terachem (default = 1.9)", default="1.9.lua")

(options, args) = parser.parse_args()

if (len(args)!=2):
  print(usage)
  sys.exit(1)

run_dir =  Path(options.directory)
jname = args[0]
inputFile = args[1]
outputFile = options.outputFile
mem = options.mem
queue = options.queue
gpu = options.gpus
no_sub = options.non
version = options.version

sbatch_string, jobName = sub_terachem(run_dir, nprocs = gpu, mem = mem, partition = queue, inp = inputFile, out = outputFile,version=version, name=jname)
jobName.write_text(sbatch_string)
if not no_sub:
    process = subprocess.getoutput("sbatch "+str(jobName))
    infos = " Job with the ID {} was submitted in {}".format(process, run_dir)
    print(infos)

