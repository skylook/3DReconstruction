#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# Python implementation of the bash script written by Romuald Perrot
#
# usage : python mvs.py sfm_data_dir output_dir
#
# sfm_data_path is the input sfm json file
# output_dir is where the project must be saved
#
# if output_dir is not present script will create it
#

# Indicate the I23DMVS binary directory
MVS_BIN = "/Users/leemeng/code/reconstruction/openMVS_build/bin/"
OPENMVG_SFM_BIN = "/Users/leemeng/code/reconstruction/openMVG_build/Darwin-x86_64-RELEASE/RELEASE"

import commands
import os
import subprocess
import sys
import time

print "\033[31m start time\033[00m " + time.asctime(time.localtime(time.time()))

if len(sys.argv) < 3:
    print ("Usage %s sfm_data_path output_dir" % sys.argv[0])
    sys.exit(1)

sfm_data_path = os.path.join(sys.argv[1], "sfm_data.json")
output_dir = sys.argv[2]
scene_path = os.path.join(output_dir, "scene.mvs")
working_dir = output_dir + "/intermediate"
use_poisson = False

print ("Using sfm data path  : ", sfm_data_path)
print ("      output_dir : ", output_dir)

if not os.path.exists(output_dir):
    os.mkdir(output_dir)
if not os.path.exists(working_dir):
    os.mkdir(working_dir)

file_path = output_dir + "/timerecord.txt"
f = open(file_path, "w")
f.write("start time \t\t\t\t" + time.asctime(time.localtime(time.time())) + '\n')

print "\033[31m start step 1\033[00m " + time.asctime(time.localtime(time.time()))
f.write("1. Import Scene from SFM \t\t" + time.asctime(time.localtime(time.time())) + '\n')
print ("1. Import Scene from SFM")
#pImport = subprocess.Popen( [os.path.join(MVS_BIN, "InterfaceVisualSFM"), "-i", sfm_data_path, "-o", output_dir+"/scene.mvs", "-w", working_dir] )
pImport = subprocess.Popen( [os.path.join(OPENMVG_SFM_BIN, "openMVG_main_openMVG2openMVS"), "-i", sfm_data_path, "-d", output_dir, "-o", output_dir+"/scene.mvs"] )
pImport.wait()

print "\033[31m start step 2\033[00m " + time.asctime(time.localtime(time.time()))
f.write("2. Dense Point-Cloud Reconstruction (optional) \t" + time.asctime(time.localtime(time.time())) + '\n')
print ("2. Dense Point-Cloud Reconstruction (optional)")
pPointRecon = subprocess.Popen( [os.path.join(MVS_BIN, "DensifyPointCloud"), "-i", output_dir+"/scene.mvs", "-w", working_dir, "--estimate-normals", "1"] )
pPointRecon.wait()

print "\033[31m start step 3\033[00m " + time.asctime(time.localtime(time.time()))
f.write("3. Rough Mesh Reconstruction \t\t" + time.asctime(time.localtime(time.time())) + '\n')
print ("3. Rough Mesh Reconstruction")
pMeshRecon = subprocess.Popen( [os.path.join(MVS_BIN, "ReconstructMesh"), "-i", output_dir+"/scene_dense.mvs", "-w", working_dir] )
pMeshRecon.wait()

print "\033[31m start step 4\033[00m " + time.asctime(time.localtime(time.time()))
f.write("4. Mesh Refinement (optional) \t\t" + time.asctime(time.localtime(time.time())) + '\n')
print ("4. Mesh Refinement (optional)")
pMeshRefine = subprocess.Popen( [os.path.join(MVS_BIN, "RefineMesh"), "-i", output_dir+"/scene_dense_mesh.mvs", "-w", working_dir, "--scales", "2", "--resolution-level", "2"] )
pMeshRefine.wait()

print "\033[31m start step 5\033[00m " + time.asctime(time.localtime(time.time()))
f.write("5. Mesh Texturing \t\t\t" + time.asctime(time.localtime(time.time())) + '\n')
print ("5. Mesh Texturing")
pTexture = subprocess.Popen( [os.path.join(MVS_BIN, "TextureMesh"), "-i", output_dir+"/scene_dense_mesh_refine.mvs", "-w", working_dir, "--resolution-level", "1"] )
pTexture.wait()

f.write("finish time \t\t\t\t" + time.asctime(time.localtime(time.time())) + '\n')
f.close()
print "\033[31m finish time\033[00m " + time.asctime(time.localtime(time.time()))

