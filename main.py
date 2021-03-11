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

telechargementFiltreSNP = True
telechargementFiltreINDEL = False

sansFiltre= True
avecFiltre= True

#Variable pour les figures 
imageMapping = False

imageCouv = False

nbDonnees = True

imageSansFiltreSNP = False

imageSansFiltreINDEL = False

imageSNP = False

imageIndel = False

#Definition of the different values of the filtre
#The name of the filter is always to the left of the comparaison, for ewample: "QD > 3"
filtre={'QD': ['>', 90.0], 'FS': ['<', 1.0], 'MQ': ['<', 1.0],
	 'MQRankSum': ['<', 1.0], 'ReadPosRankSum': ['>=', 0.0], 'SOR': ['<', 1.0]}

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
             
    #4 - Filtration 
    filtration.mainFiltration(telechargementFiltreSNP, telechargementFiltreINDEL, sansFiltre, avecFiltre, filtre)
  
    #Figure 
    figure.mainFigure(tabFichierNomNew, imageMapping, imageCouv, nbDonnees,imageSansFiltreSNP, imageSansFiltreINDEL, imageSNP, imageIndel, filtre)
    
    #Set the jdk back to version 11.0
    #IMPORTANT: If the script stops during the execution (for whatever reason) make sure to set the jdk back to 11.0 manually with the same command line
    os.system("sudo update-java-alternatives --set /usr/lib/jvm/java-1.11.0-openjdk-amd64")
