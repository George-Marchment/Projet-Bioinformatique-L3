#George Marchment + Clemence Sebe
#Script Main
import variables as v
import figure 
import bwa
import download 
import gvcf
import filtration
import os

#Variable if you want to download the original FASTQs
#If you want to download the FATSQs you can also remove the parameter from 'bwa.mainBWA' when it's called below
telechargementFASTQ= False

telechargementBAM= False

telechargementGVCF= False

createBbOutput = False

telechargementFiltreSNP = False

telechargementFiltreINDEL = False

#Variable pour les figures 
imageMapping = True

imageCouv = True

imageSNP = True

imageIndel = True

#Number of fastq files to download +  continue to 'work' in the pipeline
#IMPORTANT: - the corresponding number of files will only download if 'telechargementFASTQ=True'
#           - To download all the .fastq files set 'numberFastq=-1' or remove it when 'bwa.mainBWA' is called below
numberFastq= -1


if __name__ == "__main__":
    
    #Set the jdk to version 8.0
    os.system("sudo update-java-alternatives --set /usr/lib/jvm/java-1.8.0-openjdk-amd64")
    
    #Setting the different variables (adresses) depending on the user (George or Clemence) 
    v.initialize() 
    
    #Calling the "main" script
    
    #1 - Downloading
    tabNomFastq, tabSampleAlias = download.mainDownload(telechargementFASTQ, numberFastq)
   
    #2 - BWA
    tabFichierNomNew, tabFichierBam = bwa.mainBWA(telechargementBAM, tabNomFastq)
       
    #3 - GVCF
    gvcf.mainGVCF(telechargementGVCF,createBbOutput, tabFichierNomNew, tabFichierBam, tabSampleAlias)
           
    #info rajouter CM3 page 13 - bcftools => a ecrire ds un fichier de sortie
    
    #4 - Filtration 
    filtration.mainFiltration(telechargementFiltreSNP, telechargementFiltreINDEL)
  
    #Figure 
    figure.mainFigure(tabFichierNomNew, imageMapping, imageCouv, imageSNP, imageIndel)
    
    #Set the jdk back to version 11.0
    #IMPORTANT: If the script stops during the execution (for whatever reason) make sure to set the jdk back to 11.0 manually with the same command line
    os.system("sudo update-java-alternatives --set /usr/lib/jvm/java-1.11.0-openjdk-amd64")
