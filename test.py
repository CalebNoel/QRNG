import os
import sys
import itertools
import matplotlib.pyplot as plt
from textwrap import wrap

#----------------------------------------------------------------------
#Imports bits from .lvm file. Returns a bitstring
#----------------------------------------------------------------------
def importFromLVM(filename):
    with open(filename) as file:
        rawfile = file.readlines()
        bits=""
        for line in rawfile[22:]:
            bits += bin(int(float(line.replace('\t','').replace('\n', ''))))[2:]
    return bits

#----------------------------------------------------------------------
#Uses von Nuemann algorithm to debiass bits. Returns them as 0-255 decimal
#----------------------------------------------------------------------
def vonNuemann(filename, byteSize):
    bits = importFromLVM(filename)
    pairs = wrap(bits, 2)
    biased=""
    for pair in pairs:
        if(len(pair)==2):
            if(pair[0]!=pair[1]):
                biased += pair[0]
    bytes = wrap(biased, int(byteSize)) #Change this to change the byte size
    nums=[]
    for byte in bytes:
        dec = int(byte, 2)
        nums.append(dec)
    return nums,bytes,bits

#------------------------------------------------------------------------
#Plot decimal values for a given file
#------------------------------------------------------------------------
def individualPlot(filename, byteSize):
    test1=vonNuemann(filename, byteSize)
    nums = test1[0]
    nums.sort()
    xAxis=[g[0] for g in itertools.groupby(nums)]
    yAxis=[len(list(g[1])) for g in itertools.groupby(nums)]
    plt.bar(xAxis, yAxis)
    plt.show()

#------------------------------------------------------------------------
#Plot decimal values for a given file
#------------------------------------------------------------------------
def combinedPlot(directory, byteSize):
    allnums=[]
    for dataset in os.listdir(directory):
        f = os.path.join(directory, dataset)
        allnums += vonNuemann(f, byteSize)[2]
    allnums.sort()
    #print([(g[0], len(list(g[1]))) for g in itertools.groupby(allnums)])
    xAxis=[g[0] for g in itertools.groupby(allnums)]
    yAxis=[len(list(g[1])) for g in itertools.groupby(allnums)]
    plt.bar(xAxis, yAxis)
    plt.xlabel("Value", fontsize=30)
    plt.ylabel("Count", fontsize=30)
    plt.title("Histogram of Generated Numbers", fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.show()

#------------------------------------------------------------------------
#2dPlot
#------------------------------------------------------------------------
def noisePlot(directory, byteSize):
    allnums=[]
    for dataset in os.listdir(directory):
        f = os.path.join(directory, dataset)
        allnums += vonNuemann(f, byteSize)[0]
    #print([(g[0], len(list(g[1]))) for g in itertools.groupby(allnums)])
    xPoints=[]
    for point in allnums:
        xPoints.append(point)
    yPoints=[]
    for point in allnums:
        yPoints.append(point)
        yPoints.append(yPoints.pop(0))

    plt.scatter(xPoints, yPoints, color='black', marker='s')
    #plt.title("2d Correlation Plot", fontsize = 35)
    #plt.title("")
    plt.xlabel("$X_{k}$", fontsize=30)
    plt.ylabel("$X_{k-1}$", fontsize=30)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.show()

#------------------------------------------------------------------------
#Serial Test
#------------------------------------------------------------------------
def serialTest(directory, byteSize):
    allnums=[]
    for dataset in os.listdir(directory):
        f = os.path.join(directory, dataset)
        allnums += vonNuemann(f, byteSize)[0]

    pairs = [tuple(allnums[i:i+2]) for i in range(0,len(allnums), 2)]

    xAxis=[g[0] for g in itertools.groupby(pairs)]
    yAxis=[len(list(g[1])) for g in itertools.groupby(pairs)]

    plt.bar(xAxis, yAxis)
    plt.xlabel("Value", fontsize=30)
    plt.ylabel("Count", fontsize=30)
    plt.title("Histogram of Generated Numbers", fontsize=35)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    plt.show()
#------------------------------------------------------------------------
#Main
#------------------------------------------------------------------------
if __name__ == "__main__":
    args = sys.argv
    globals()[args[1]](*args[2:])
