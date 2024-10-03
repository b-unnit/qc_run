#!/usr/bin/python  

import sys, os
from pathlib import Path
from optparse import OptionParser
import subprocess
from qc_run.sub_job import psi4_eb as sub_psi4

usage = "usage: %prog [options] <Nombre del proceso> <Archivo de input>"
parser = OptionParser(usage=usage)
parser.add_option("-d", dest="directory", help="Directorio destino de ejecución del calculo (default = "+str(Path.cwd()), default=Path.cwd())
parser.add_option("-o", dest="outputFile", help="Archivo de Output (default= out.dat)", default="out.dat")
parser.add_option("-c", dest="procs", help="Número de cores a usar (default= 4)", default=4)
parser.add_option("-q", dest="queue", help="Cola de destino (default = intel)", default="intel")
parser.add_option("-m", dest="mem", help="Memoria a reservar (default = 8GB)", default="8GB")
parser.add_option("-v", dest="version", help="Version de orca a usar (default = 1_0_2)", default="1.2.1")

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
queue = options.queue
proc_num = options.procs

sub_psi4(run_dir, nprocs = proc_num, mem = mem, partition = queue, inp = inputFile, out = outputFile, version =version, name=jname)

