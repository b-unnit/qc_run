#!/usr/bin/python  

#Import Modules                                                               
import sys, os
from pathlib import Path
from optparse import OptionParser
import subprocess
from qc_run.sub_job import orca_eb as sub_orca

usage = "usage: %prog [options] <Nombre del proceso> <Archivo de input>"
parser = OptionParser(usage=usage)
parser.add_option("-d", dest="directory", help="Directorio destino de ejecución del calculo (default = "+str(Path.cwd()), default=Path.cwd())
parser.add_option("-o", dest="outputFile", help="Archivo de Output (default= out.dat)", default="out.dat")
parser.add_option("-q", dest="queue", help="Cola de destino (default = intel)", default="intel")
parser.add_option("-m", dest="mem", help="Memoria a reservar (default = 4GB)", default="4GB")
parser.add_option("-v", dest="version", help="Version de orca a usar (default= 4.0.0.2)", default="_4_0_0_2_linux_x86-64")
parser.add_option("-w", dest="wf", action="store_true",  help="conserve the wavefunction file? (Default= False)", default = False)
parser.add_option("--parametros", dest="parametros", help="Parametros adicionales de gromax (Se ingresan entre comillas)", default="")

(options, args) = parser.parse_args()

if (len(args)!=2):
  print(usage)
  sys.exit(1)

run_dir =  Path(options.directory)
jname = args[0]
inputFile = args[1]
outputFile = options.outputFile
mem = options.mem
parametros = options.parametros
version = options.version
queue = options.queue
wf = options.wf
proc_num = 1

with open(run_dir / inputFile, mode='r') as fid:
    for line in fid:
        if line.startswith('%pal'):
            proc_num = line.split()[2]

sub_orca(run_dir, nprocs = proc_num, mem = mem, partition = queue, inp = inputFile, out = outputFile, version =version, name=jname, wf = wf)

