#George Marchment + Clemence Sebe
#Figure
import os
import variables as v
import matplotlib.pyplot as plt
import numpy as np



#Fonction mettre entre guillement
def G(a):
	return ("\""+a+"\"")
		

def mainFigureDeux(nbDonnees,imageSansFiltreSNP, imageSansFiltreINDEL, imageSNP, imageINDEL, filtreSNP, filtreINDEL):
    
	def traceSNP(entree, adresse):
		if imageSNP:
			print("Figure SNP: ") 
			filtre = filtreSNP
		    	#On récupère les filtre
			qd= filtre['QD'][1]
			mq= filtre['MQ'][1]
			mqRankSumInf= filtre['MQRankSumInf'][1]
			mqRankSumSup= filtre['MQRankSumSup'][1]
			readPosRankSumInf= filtre['ReadPosRankSumInf'][1]
			readPosRankSumSup= filtre['ReadPosRankSumSup'][1]
			sor= filtre['SOR'][1]
		 
		 	#On récupère les synmboles de comparaison pour les filtres
			sym_qd= filtre['QD'][0]
			sym_mq= filtre['MQ'][0]
			sym_mqRankSumInf= filtre['MQRankSumInf'][0]
			sym_mqRankSumSup= filtre['MQRankSumSup'][0]
			sym_readPosRankSumInf= filtre['ReadPosRankSumInf'][0]
			sym_readPosRankSumSup= filtre['ReadPosRankSumSup'][0]
			sym_sor= filtre['SOR'][0]
   
			valeurs_filtre= str(qd)+" "+str(mq)+" "+str(mqRankSumInf)+" "+str(mqRankSumSup) + " "+ str(readPosRankSumInf)+" "+ str(readPosRankSumSup) + " "+str(sor)
			sym_filtre= G(str(sym_qd))+" "+G(str(sym_mq))+" "+G(str(sym_mqRankSumInf))+" "+G(str(sym_mqRankSumSup))+" "+G(str(sym_readPosRankSumInf))+" "+G(str(sym_readPosRankSumSup))+" "+G(str(sym_sor))
		
			cmd = "Rscript figureSNP.R "+ entree+" "+adresse+ " "+valeurs_filtre+" "+sym_filtre
			os.system(cmd)
			cmd = "rm "+ adresse+"DiagrammeVenn*.log"
			os.system(cmd)

	def traceIndel(entree, adresse):
		if imageINDEL:
			print("Figure INDEL: ") 
			filtre = filtreINDEL
		    	#On récupère les filtre
			qd= filtre['QD'][1]
			mq= filtre['MQ'][1]
			mqRankSumInf= filtre['MQRankSumInf'][1]
			mqRankSumSup= filtre['MQRankSumSup'][1]
			readPosRankSumInf= filtre['ReadPosRankSumInf'][1]
			readPosRankSumSup= filtre['ReadPosRankSumSup'][1]
			sor= filtre['SOR'][1]
		 
		 	#On récupère les synmboles de comparaison pour les filtres
			sym_qd= filtre['QD'][0]
			sym_mq= filtre['MQ'][0]
			sym_mqRankSumInf= filtre['MQRankSumInf'][0]
			sym_mqRankSumSup= filtre['MQRankSumSup'][0]
			sym_readPosRankSumInf= filtre['ReadPosRankSumInf'][0]
			sym_readPosRankSumSup= filtre['ReadPosRankSumSup'][0]
			sym_sor= filtre['SOR'][0]
   
			valeurs_filtre= str(qd)+" "+str(mq)+" "+str(mqRankSumInf)+" "+str(mqRankSumSup) + " "+ str(readPosRankSumInf)+" "+ str(readPosRankSumSup) + " "+str(sor)
			sym_filtre= G(str(sym_qd))+" "+G(str(sym_mq))+" "+G(str(sym_mqRankSumInf))+" "+G(str(sym_mqRankSumSup))+" "+G(str(sym_readPosRankSumInf))+" "+G(str(sym_readPosRankSumSup))+" "+G(str(sym_sor))
			cmd = "Rscript figureINDEL.R "+ entree+" "+adresse+ " "+valeurs_filtre+" "+sym_filtre
			os.system(cmd)
			cmd = "rm "+ adresse+"DiagrammeVenn*.log"
			os.system(cmd)

	print("DEBUT SCRIPT FIGURE DEUX")
	current_path= os.getcwd()
	
	#Creating vcf with only PASS  
	#Utile pour compter ligne + figure
	if nbDonnees or imageSNP or imageINDEL:
		cmd= "bcftools view -f PASS "+v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.vcf.gz > " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.vcf"
		os.system(cmd) 
		cmd= "bcftools view -f PASS "+v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.vcf.gz > " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.vcf"
		os.system(cmd)
	
	#Rajout stat
	if nbDonnees:
		print("Information sur les donnees")
		os.chdir(v.results+"General/")
		fichierFinal = open("infoDonnees.txt", "w")
		
		cmd = "bcftools view -H " + v.vcf + "output.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Nombre total de Samples: " + line[0]
		fichierFinal.write(txt)
		inter.close()
		
		cmd = "bcftools view -H " + v.vcf + "SNP/outputSNP.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Avant Filtres SNP: " + line[0]
		avantSNP= int(line[0])
		fichierFinal.write(txt)
		inter.close()

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

		cmd = "bcftools view -H " + v.vcf + "INDEL/outputINDEL.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Avant Filtres INDEL: " + line[0]
		avantINDEL= int(line[0])
		fichierFinal.write(txt)
		inter.close()


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
		
		#Fin
		fichierFinal.close()
		os.remove("nombre.txt")
		
	os.chdir(current_path)

	#Graphe donnees sans filtres
	if imageSansFiltreSNP: 
		print("Figure SNP no filtre") 
		cmd = "Rscript figureNoFilter.R " + v.vcf + "SNP/PRE_FILTRE/outputSnpNoFiltrer.txt" + " " + v.graphs+"SNP/NoFilter/"
		os.system(cmd)
		
	if imageSansFiltreINDEL: 
		print("Figure INDEL no filtre") 
		cmd = "Rscript figureNoFilter.R " + v.vcf + "INDEL/PRE_FILTRE/outputIndelNoFiltrer.txt" + " " + v.graphs+"INDEL/NoFilter/"
		os.system(cmd)


	#On trace les graphs des filtre pour SNP et INDEL
	if imageSNP:
	
		cmd = "bcftools query " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.vcf -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.txt"
		os.system(cmd)	
			
		#Rajout legende premiere ligne
		cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.vcf + "SNP/POST_FILTRE/SNP_PASS.txt"
		os.system(cmd)
	
		traceSNP(v.vcf + "SNP/POST_FILTRE/SNP_PASS.txt", v.graphs+"SNP/Filter/")
		
		
	if imageINDEL:
	
		cmd = "bcftools query " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.vcf -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.txt"
		os.system(cmd)	
		
		#Rajout legende premiere ligne
		cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.txt"
		os.system(cmd)
		
		traceIndel(v.vcf + "INDEL/POST_FILTRE/INDEL_PASS.txt", v.graphs+"INDEL/Filter/")
 
	print("FIN SCRIPT FIGURE DEUX")
