#George Marchment + Clemence Sebe
#Script Main
import variables as v
import bwa
import download
import gvcf
import os

#Variable if you want to download the original FASTQs
#If you want to download the FATSQs you can also remove the parameter from 'bwa.mainBWA' when it's called below
telechargementFASTQ= False

telechargementBAM= True

telechargementGVCF=True

#Number of fastq files to download +  continue to 'work' in the pipeline
#IMPORTANT: - the corresponding number of files will only download if 'telechargementFASTQ=True'
#           - To download all the .fastq files set 'numberFastq=-1' or remove it when 'bwa.mainBWA' is called below
numberFastq= 2


if __name__ == "__main__":
    
    #Set the jdk to version 8.0
    os.system("sudo update-java-alternatives --set /usr/lib/jvm/java-1.8.0-openjdk-amd64")
    
    #Setting the different variables (adresses) depending on the user (George or Clemence) 
    v.initialize() 
    
    #Calling the "main" script
    #bwa.mainBWA(telechargementFASTQ, numberFastq)
    
    
    gvcf.mainGVCF(telechargementFASTQ, telechargementBAM,telechargementGVCF, numberFastq)
    
    #Set the jdk back to version 11.0
    #IMPORTANT: If the script stops during the execution (for whatever reason) make sure to set the jdk back to 11.0 manually with the same command line
    os.system("sudo update-java-alternatives --set /usr/lib/jvm/java-1.11.0-openjdk-amd64")
