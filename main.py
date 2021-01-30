import variables as v
import bwa
import download
 
telechargementFASTQ= False
numberDownloads=2


conserveMemory=False
 
if __name__ == "__main__": 
    v.initialize() 
    bwa.mainBWA(telechargementFASTQ, numberDownloads)
    
