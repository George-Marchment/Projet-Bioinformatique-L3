#George Marchment + Clemence Sebe
#Script Figure deux
import os
import variables as v
import matplotlib.pyplot as plt
import numpy as np

#Function that return the string given as parameter but with quotation marks around if
#It is used to give R it's parameters
#G for 'guillemets' (quotation marks in french) 
def G(a):
	return ("\""+a+"\"")
		

#Function that creates all the graphs around the filters
def mainFigureDeux(nbDonnees,imageSansFiltreSNP, imageSansFiltreINDEL, imageSNP, imageINDEL, filtreSNP, filtreINDEL):
    
	#Function that takes the .vcf (in .txt format) and an adress and creates the corresponding graphs to the data at the adress for the SNPs
	def traceSNP(entree, adresse):
		if imageSNP:
			print("Figure SNP: ") 
			filtre = filtreSNP
		    
			#We recuperate the filters
			qd= filtre['QD'][1]
			mq= filtre['MQ'][1]
			mqRankSumInf= filtre['MQRankSumInf'][1]
			mqRankSumSup= filtre['MQRankSumSup'][1]
			readPosRankSumInf= filtre['ReadPosRankSumInf'][1]
			readPosRankSumSup= filtre['ReadPosRankSumSup'][1]
			sor= filtre['SOR'][1]
		 
		 	#We recuperate the comparaisons symbols for the filters 
			sym_qd= filtre['QD'][0]
			sym_mq= filtre['MQ'][0]
			sym_mqRankSumInf= filtre['MQRankSumInf'][0]
			sym_mqRankSumSup= filtre['MQRankSumSup'][0]
			sym_readPosRankSumInf= filtre['ReadPosRankSumInf'][0]
			sym_readPosRankSumSup= filtre['ReadPosRankSumSup'][0]
			sym_sor= filtre['SOR'][0]

			#We create the parameters to give to the R script (it's admittedly no very pretty)
			valeurs_filtre= str(qd)+" "+str(mq)+" "+str(mqRankSumInf)+" "+str(mqRankSumSup) + " "+ str(readPosRankSumInf)+" "+ str(readPosRankSumSup) + " "+str(sor)
			sym_filtre= G(str(sym_qd))+" "+G(str(sym_mq))+" "+G(str(sym_mqRankSumInf))+" "+G(str(sym_mqRankSumSup))+" "+G(str(sym_readPosRankSumInf))+" "+G(str(sym_readPosRankSumSup))+" "+G(str(sym_sor))

			#Calling the R script
			cmd = "Rscript figureSNP.R "+ entree+" "+adresse+ " "+valeurs_filtre+" "+sym_filtre
			os.system(cmd)
			#Deleting the DiagrammeVenn*.log file since it no longer serves a purpose
			cmd = "rm "+ adresse+"DiagrammeVenn*.log"
			os.system(cmd)

	#Function that takes the .vcf (in .txt format) and an adress and creates the corresponding graphs to the data at the adress for the INDELs
	def traceIndel(entree, adresse):
		if imageINDEL:
			print("Figure INDEL: ") 
			filtre = filtreINDEL

		    #We recuperate the filters
			qd= filtre['QD'][1]
			mq= filtre['MQ'][1]
			mqRankSumInf= filtre['MQRankSumInf'][1]
			mqRankSumSup= filtre['MQRankSumSup'][1]
			readPosRankSumInf= filtre['ReadPosRankSumInf'][1]
			readPosRankSumSup= filtre['ReadPosRankSumSup'][1]
			sor= filtre['SOR'][1]
		 
		 	#We recuperate the comparaisons symbols for the filters 
			sym_qd= filtre['QD'][0]
			sym_mq= filtre['MQ'][0]
			sym_mqRankSumInf= filtre['MQRankSumInf'][0]
			sym_mqRankSumSup= filtre['MQRankSumSup'][0]
			sym_readPosRankSumInf= filtre['ReadPosRankSumInf'][0]
			sym_readPosRankSumSup= filtre['ReadPosRankSumSup'][0]
			sym_sor= filtre['SOR'][0]

			#We create the parameters to give to the R script (it's admittedly no very pretty)
			valeurs_filtre= str(qd)+" "+str(mq)+" "+str(mqRankSumInf)+" "+str(mqRankSumSup) + " "+ str(readPosRankSumInf)+" "+ str(readPosRankSumSup) + " "+str(sor)
			sym_filtre= G(str(sym_qd))+" "+G(str(sym_mq))+" "+G(str(sym_mqRankSumInf))+" "+G(str(sym_mqRankSumSup))+" "+G(str(sym_readPosRankSumInf))+" "+G(str(sym_readPosRankSumSup))+" "+G(str(sym_sor))
			
			#Calling the R script
			cmd = "Rscript figureINDEL.R "+ entree+" "+adresse+ " "+valeurs_filtre+" "+sym_filtre
			os.system(cmd)
			#Deleting the DiagrammeVenn*.log file since it no longer serves a purpose
			cmd = "rm "+ adresse+"DiagrammeVenn*.log"
			os.system(cmd)

	#Beginning of the script
	print("DEBUT SCRIPT FIGURE DEUX")
	#REcuperate the current path
	current_path= os.getcwd()
	
	#Creating a .vcf(s) with only the PASS sequences  
	#Usefull for counting lignes and the graphs
	if nbDonnees or imageSNP or imageINDEL:
		cmd= "bcftools view -f PASS "+v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.vcf.gz > " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.vcf"
		os.system(cmd) 
		cmd= "bcftools view -f PASS "+v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.vcf.gz > " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.vcf"
		os.system(cmd)
	
	#Creating the stats doc (infoDonnees.txt)
	#Using bcftools to extarct the data we want
	if nbDonnees:
		print("Information sur les donnees")
		os.chdir(v.results+"General/")
		fichierFinal = open("infoDonnees.txt", "w")
		
		#Total Number of Sample
		cmd = "bcftools view -H " + v.vcf + "output.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Nombre total de Samples: " + line[0]
		fichierFinal.write(txt)
		inter.close()
		
		#Total number of SNPs before the filter
		cmd = "bcftools view -H " + v.vcf + "SNP/outputSNP.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Avant Filtres SNP: " + line[0]
		avantSNP= int(line[0])
		fichierFinal.write(txt)
		inter.close()

		#Number of SNPs after filter + percentage filtered 
		#Counting lignes without header
		cmd = "bcftools view -H " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.vcf |wc -l > nombre.txt"
		os.system(cmd)
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Apres Filtres SNP: " + line[0]
		apresSNP= int(line[0])
		fichierFinal.write(txt)
		txt = "Pourcentage Filtré SNP: {:.2f}%\n".format(abs(apresSNP-avantSNP)/avantSNP*100)
		fichierFinal.write(txt)
		inter.close()

		#Total number of INDELs before the filter
		cmd = "bcftools view -H " + v.vcf + "INDEL/outputINDEL.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Avant Filtres INDEL: " + line[0]
		avantINDEL= int(line[0])
		fichierFinal.write(txt)
		inter.close()

		#Number of INDELs after filter + percentage filtered 
		#Counting lignes without header
		cmd = "bcftools view -H " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.vcf |wc -l > nombre.txt"
		os.system(cmd)
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Apres Filtres INDEL: " + line[0]
		apresINDEL= int(line[0])
		fichierFinal.write(txt)
		txt = "Pourcentage Filtré INDEL: {:.2f}%\n".format(abs(apresINDEL-avantINDEL)/avantINDEL*100)
		fichierFinal.write(txt)
		inter.close()
		
		#END
		fichierFinal.close()
		#Removing nombre.txt cause no longer usefull
		os.remove("nombre.txt")
	#Returning to the original path	
	os.chdir(current_path)

	#Graphs without filters calling the R scripts
	#SNP
	if imageSansFiltreSNP: 
		print("Figure SNP no filtre") 
		cmd = "Rscript figureNoFilter.R " + v.vcf + "SNP/PRE_FILTRE/outputSnpNoFiltrer.txt" + " " + v.graphs+"SNP/NoFilter/"
		os.system(cmd)
	#INDEL
	if imageSansFiltreINDEL: 
		print("Figure INDEL no filtre") 
		cmd = "Rscript figureNoFilter.R " + v.vcf + "INDEL/PRE_FILTRE/outputIndelNoFiltrer.txt" + " " + v.graphs+"INDEL/NoFilter/"
		os.system(cmd)

	#Graphs after Filters
	#SNP
	if imageSNP:
		#Extracting only the usefull data
		cmd = "bcftools query " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.vcf -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.txt"
		os.system(cmd)	
		#Adding legend to the first ligne
		cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.txt"
		os.system(cmd)
		#Calling function definied at the beginning
		traceSNP(v.vcf + "SNP/POST_FILTRE/SNP_PASS.txt", v.graphs+"SNP/Filter/")
	#INDEL
	if imageINDEL:
		#Extracting only the usefull data
		cmd = "bcftools query " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.vcf -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.txt"
		os.system(cmd)	
		#Adding legend to the first ligne
		cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.txt"
		os.system(cmd)
		#Calling function definied at the beginning
		traceIndel(v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.txt", v.graphs+"INDEL/Filter/")


	print("FIN SCRIPT FIGURE DEUX")
