import os

## cleans up the curr directory of all the csv files
def clean():
    currDir = os.getcwd()

    filelist = [ f for f in os.listdir(currDir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(currDir, f))

clean()
