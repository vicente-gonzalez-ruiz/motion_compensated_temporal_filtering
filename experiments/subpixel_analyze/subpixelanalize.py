#!/usr/bin/env python
import numpy as np
from numpy import matrix
import os
import os.path as path
from scipy.stats import entropy
import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Analyze subpixel impact')
parser.add_argument('-p',type=str, default="", help='Path video to analyze',required=True)
parser.add_argument('-s',type=str, default="0", help='Subpixel Order')

args = parser.parse_args()
file_path = args.p
subpixel = args.s
folder = 'subpixelanalyze'
pathroot = os.getcwd()

os.system('mkdir '+pathroot+'/'+folder)


if path.exists(pathroot+'/'+folder+'/subpixel.yuv'):
        os.system('rm '+pathroot+'/'+folder+'/subpixel.yuv')

os.system('ffmpeg -i ' +file_path+' '+pathroot+'/'+folder+'/subpixel.yuv')

if path.exists(pathroot+'/'+folder+'/low_0'):
        os.system('rm ' +pathroot+'/'+folder+'/'+'low_0')

os.chdir(pathroot+'/'+folder)
os.system('rm motion_*')
os.system('ln -s '+pathroot+'/'+folder+'/subpixel.yuv low_0')

os.system('mctf analyze --subpixel_accuracy '+subpixel)

motionEnt = np.array([])
highEnt = np.array([])

for i in range(1,4):
	f = open(pathroot+'/'+folder+'/motion_'+str(i))
	data = np.fromfile(f,dtype=np.int8)
	hist = np.histogram(data)[0]
	ent = entropy(hist,base=2)
	motionEnt = np.append(motionEnt,ent)
	print("Entropy motion_"+str(i)+"= "+str(ent))

for i in range(1,4):
	f = open(pathroot+'/'+folder+'/high_'+str(i))
	data = np.fromfile(f,dtype=np.int8)
	hist = np.histogram(data)[0]
	ent = entropy(hist,base=2)
	highEnt = np.append(highEnt,ent)
	print("Entropy high_"+str(i)+"= "+str(ent))

plt.figure("Motion")
plt.plot(motionEnt,marker='x')
plt.xlabel("Resolution Level")
plt.ylabel("Motion Entropy")
plt.savefig(pathroot+'/'+folder+'/motionentropy_subpixel_'+subpixel+'.png',dpi=100)

plt.figure("High")
plt.plot(highEnt,marker='x')
plt.xlabel("Resolution Level")
plt.ylabel("High Entropy")
plt.savefig(pathroot+'/'+folder+'/highentropy_subpixel_'+subpixel+'.png',dpi=100)
print(motionEnt)
print(highEnt)

matriz = matrix([[1,2,3],motionEnt,highEnt])
mT = matriz.transpose()
print(mT)

np.savetxt(pathroot+'/'+folder+'/motionhigh_entropy_'+subpixel+'.txt',mT,fmt='%1.8f',header="Resolution Level,Motion Entropy,High Entropy")