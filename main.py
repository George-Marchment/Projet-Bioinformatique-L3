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
telechargementFASTQ= True

#Variable if you want to create the .bam files
telechargementBAM= True

#Variable if you want to create the .g.vcf files
telechargementGVCF= True

#Variable if you want to create the database and .vcf files
createBbOutput = True

#Variable if you want to filtre the SNPs and/or INDELs
telechargementFiltreSNP = True
telechargementFiltreINDEL = True

#Variable if you want to the SNPs and/or INDELs with or without Filters
sansFiltre= True
avecFiltre= True

#Variable to create the different graphs
imageMapping = True
imageCouv = True

#Variable to create file including data informations
nbDonnees = True

#Variable to create venne graphs (filters)
imageSansFiltreSNP = True
imageSansFiltreINDEL = True

#Variable to create filter grahs
imageSNP = True
imageIndel = True

#Variable to do PCA and create trees and clustering
pcaSNP = True


#Definition of the different values of the filtre
#The name of the filter is always to the left of the comparaison, for ewample: "QD > 3"
#We have defined the filters as such: we 'put the values that we want to get rid off'
#For example: 'QD': ['<', 10.0] => we get rid of the SNP (or INDEL) with QD < 10
#SNP Filters
filtreSNP ={'QD': ['<', 10.0], 'MQ': ['<', 50.0], 'MQRankSumInf': ['<', -3.0],
	 'MQRankSumSup': ['>', 3.0], 'ReadPosRankSumInf': ['<', -2.0], 'ReadPosRankSumSup': ['>', 2.0], 'SOR': ['>', 2.0]}
#INDEL Filters
filtreINDEL ={'QD': ['<', 10.0], 'MQ': ['<', 50.0], 'MQRankSumInf': ['<', -3.0],
	 'MQRankSumSup': ['>', 3.0], 'ReadPosRankSumInf': ['<', -2.0], 'ReadPosRankSumSup': ['>', 2.0], 'SOR': ['>', 2.0]}

#Number of fastq files to download +  continue to 'work' in the pipeline
#IMPORTANT: If you want to select all the data, set numberFastq to -1
numberFastq= -1

if __name__ == "__main__":
 
    #Set the jdk to version 8.0
    os.system("sudo update-java-alternatives --set /usr/lib/jvm/java-1.8.0-openjdk-amd64")
    #Setting the different variables (adresses) depending on the user (George or Clemence) 
    v.initialize() 
    #1 - Downloading
    tabNomFastq, tabSampleAlias = download.mainDownload(telechargementFASTQ, numberFastq)

    #2 - BWA + SAM + BAM
    tabFichierNomNew, tabFichierBam = bwa.mainBWA(telechargementBAM, tabNomFastq)

    #3 - GVCF + VCF
    gvcf.mainGVCF(telechargementGVCF,createBbOutput, tabFichierNomNew, tabFichierBam, tabSampleAlias)

    #4 - Graphs Mapping anc Couverture
    figureUn.mainFigureUn(tabFichierNomNew, imageMapping, imageCouv)

    #5 - SNP Filters
    filtrationSNP.mainFiltrationSNP(telechargementFiltreSNP, sansFiltre, avecFiltre, filtreSNP)

    #6 - INDEL Filters
    filtrationINDEL.mainFiltrationINDEL(telechargementFiltreINDEL, sansFiltre, avecFiltre, filtreINDEL)

    #7 - Graphs Including Filters Information
    figureDeux.mainFigureDeux(nbDonnees,imageSansFiltreSNP, imageSansFiltreINDEL, imageSNP, imageIndel, filtreSNP, filtreINDEL)

    #8 - PCA SNP (Clustering + Trees)
    analyseSNP.mainAnalyseSNP(pcaSNP)

    #Set the jdk back to version 11.0
    #IMPORTANT: If the script stops during the execution (for whatever reason) make sure to set the jdk back to 11.0 manually with the same command line
    os.system("sudo update-java-alternatives --set /usr/lib/jvm/java-1.11.0-openjdk-amd64")
