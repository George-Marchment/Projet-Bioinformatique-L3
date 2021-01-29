import variables as v
import bwa
import download
 
telechargementFASTQ= False

 
if __name__ == "__main__": 
    v.initialize() 
    bwa.mainBWA(telechargementFASTQ)
    
