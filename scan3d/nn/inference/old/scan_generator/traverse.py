import os
from pathlib import Path

def traverse_serie(intree, outtree, function):
    # traverse a input tree and execude function(indir, outdir) on every set
    print("Traverse_serie folder " + str(intree) + " to " + str(outtree))
    os.makedirs(outtree) 
    no = 0
    while True:
        indir = intree / str(no)
        #print (indir)
        if Path.exists(indir):
            outdir = Path(outtree) / str(no)
            os.makedirs(outdir)
            function(indir, outdir, no)
        else:
            break
        no += 1
        if no % 10 == 0:
            print(".", end='')
    print("")
    return

def gen_serie(infolder, outtree, function, number=20 ):
       # traverse a input tree and execude function(indir, outdir) on every set
    print("Generate_serie infolder " + str(infolder) + " to " + str(outtree))
    os.makedirs(outtree) 
    no = 0
    indir = infolder
    for no in range(number):
        outdir = Path(outtree) / str(no)
        os.makedirs(outdir)
        function(infolder, outdir, no)
        print(".", end='')
    print("")
    return