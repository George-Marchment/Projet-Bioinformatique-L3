#George Marchment + Clemence Sebe
#Script Main
import variables as v
import figureUn
import figureDeux
import bwa
import download 
import gvcf
import filtrationSNP
import filtrationINDEL
import analyseSNP
import os

#Variable if you want to download the original FASTQs
#If you want to download the FATSQs you can also remove the parameter from 'bwa.mainBWA' when it's called below
telechargementFASTQ= False

telechargementBAM= False

telechargementGVCF= False

createBbOutput = False

telechargementFiltreSNP = True
telechargementFiltreINDEL = True

sansFiltre= True
avecFiltre= True

#Variable pour les figures 
imageMapping = False

imageCouv = False

nbDonnees = True

imageSansFiltreSNP = True

imageSansFiltreINDEL = True

imageSNP = True

imageIndel = True

pcaSNP = True
#pcaINDEL = False

#Definition of the different values of the filtre
#The name of the filter is always to the left of the comparaison, for ewample: "QD > 3"
#On définit les filtres : on "met les valeurs qu'on ne veut pas garder"
filtreSNP ={'QD': ['>', 22.0], 'MQ': ['<', 50.0], 'MQRankSumInf': ['<', -3.0],
	 'MQRankSumSup': ['>', 3.0], 'ReadPosRankSumInf': ['<', -2.0], 'ReadPosRankSumSup': ['>', 2.0], 'SOR': ['>', 2.0]}

filtreINDEL ={'QD': ['>', 22.0], 'MQ': ['<', 50.0], 'MQRankSumInf': ['<', -3.0],
	 'MQRankSumSup': ['>', 3.0], 'ReadPosRankSumInf': ['<', -2.0], 'ReadPosRankSumSup': ['>', 2.0], 'SOR': ['>', 2.0]}

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
    
    #4 - Premiere Figures
    figureUn.mainFigureUn(tabFichierNomNew, imageMapping, imageCouv)
    
    #5 - Filtration SNP
    filtrationSNP.mainFiltrationSNP(telechargementFiltreSNP, sansFiltre, avecFiltre, filtreSNP)
    
    #6 - Filtration INDEL
    filtrationINDEL.mainFiltrationINDEL(telechargementFiltreINDEL, sansFiltre, avecFiltre, filtreINDEL)
        
    #7 - Seconde Figures 
    figureDeux.mainFigureDeux(nbDonnees,imageSansFiltreSNP, imageSansFiltreINDEL, imageSNP, imageIndel, filtreSNP, filtreINDEL)
    
    #8 - PCA SNP
    analyseSNP.mainAnalyseSNP(pcaSNP)
    
    #9 - PCA INDEL
    # A voir ...
    
    #Set the jdk back to version 11.0
    #IMPORTANT: If the script stops during the execution (for whatever reason) make sure to set the jdk back to 11.0 manually with the same command line
    os.system("sudo update-java-alternatives --set /usr/lib/jvm/java-1.11.0-openjdk-amd64")
