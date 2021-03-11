#George Marchment + Clemence Sebe
#Figure
import os
import variables as v
import matplotlib.pyplot as plt
import numpy as np





def mainFigure(tabFichier, imageMapping, imageCouv, nbDonnees,imageSansFiltreSNP, imageSansFiltreINDEL, imageSNP, imageIndel, filtre):
    
    #On récupère les filtre
	qd= filtre['QD'][1]
	fs= filtre['FS'][1]
	mq= filtre['MQ'][1]
	mqRankSum= filtre['MQRankSum'][1]
	readPosRankSum= filtre['ReadPosRankSum'][1]
	sor= filtre['SOR'][1]
 
 	#On récupère les synmboles de comparaison pour les filtres
	sym_qd= filtre['QD'][0]
	sym_fs= filtre['FS'][0]
	sym_mq= filtre['MQ'][0]
	sym_mqRankSum= filtre['MQRankSum'][0]
	sym_readPosRankSum= filtre['ReadPosRankSum'][0]
	sym_sor= filtre['SOR'][0]
    
    #Fonction mettre entre guillement
	def G(a):
		return ("\""+a+"\"")

	valeurs_filtre= str(qd)+" "+str(fs)+" "+str(mq)+" "+str(mqRankSum)+" "+str(readPosRankSum)+" "+str(sor)
	sym_filtre= G(str(sym_qd))+" "+G(str(sym_fs))+" "+G(str(sym_mq))+" "+G(str(sym_mqRankSum))+" "+G(str(sym_readPosRankSum))+" "+G(str(sym_sor))
	
	def traceSNP(entree, adresse):
		if imageSNP:
				print("Figure SNP: ") 
				cmd = "Rscript figureSNP.R "+ entree+" "+adresse+ " "+valeurs_filtre+" "+sym_filtre
				os.system(cmd)
				cmd = "rm "+ adresse+"DiagrammeVenn*.log"
				os.system(cmd)

	def traceIndel(entree, adresse):
		if imageIndel:
			print("Figure INDEL: ") 
			cmd = "Rscript figureINDEL.R "+ entree+" "+adresse+ " "+valeurs_filtre+" "+sym_filtre
			os.system(cmd)
			cmd = "rm "+ adresse+"DiagrammeVenn*.log"
			os.system(cmd)

	print("DEBUT SCRIPT FIGURE")
	current_path= os.getcwd()
	
	#Tab for Mapping
	tabFigMapping = []
	
	#Tab for the plot of bedtools
	tabBedMean = []
	den, num = 0, 0


	if imageMapping or imageCouv:
		for i in range (len(tabFichier)):
			print("----------------- Figure ", i+1 , " sur ", len(tabFichier) , "---------------------")
			os.chdir(v.adresseBwa)
			fichierBam = tabFichier[i] + ".bam"
			
			if imageMapping:
				#Mapping
				#---------------------------------------------------------------
				print("Samtools flagstat + creation fichier txt")
				flag = tabFichier[i] + ".txt"
				cmd = "samtools flagstat " + v.bamRefPostMK+fichierBam + " > " +  v.fichTxt + flag
				os.system(cmd)
				#Ajout donnee pour figure
				os.chdir(v.fichTxt)
				file = open(flag, "r")
				for k in range (4):
					line = file.readline()
				ligne5 = file.readline()
				l = ligne5.split()
				cas = l[4]
				cas = cas.split('(')
				new = cas[1]
				new = new.split("%")
				num = new[0]
				tabFigMapping.append(float(num))
				file.close()

			if imageCouv:
				#BedTools
				#-------------------------------------------------------------------
				print("Bedtools pour calculer max, min, moyenne de la couverture")
				os.chdir(v.adresseBwa)
				bedfile = tabFichier[i] + "_bed.txt"
				cmd = "bedtools genomecov -ibam " + v.bamRefPostMK+fichierBam + " -bga > " + v.fichTxt + bedfile
				os.system(cmd)
				os.chdir(v.fichTxt)
				den = num = 0
				file = open(bedfile, "r")
				line = file.readlines()
				for ligne in line:
					test = ligne.split()
					if (test[0] != "ref|NC_001224|"):
						tmp = np.abs(float(test[2])-1 - float(test[1]))
						den += tmp*float(test[-1])
						num += tmp
				file.close()
				tabBedMean.append(den/num)


	os.chdir(v.simple)
	
	if imageMapping:
		print('Figure Mapping')
		os.chdir(v.graphs+"General/")
		fig,ax = plt.subplots()
		ax.plot(tabFigMapping,"o-")
		ax.set_title("Pourcentage de donnees qui mappent sur les 26 échantillons")
		plt.savefig('MappingCourbe.png')
		
		fig,ax = plt.subplots()
		plt.hist(tabFigMapping)
		ax.set_title("Histogramme Mapping")
		plt.savefig('MappingHisto.png')

	if imageCouv:
		print("Figure pour bedtools")
		os.chdir(v.graphs+"General/")
		fig,ax = plt.subplots()
		ax.plot(tabBedMean, "o-")
		ax.set_title("Couverture moyenne des 26 échantillons")
		plt.savefig('CouvertureMoyenne.png')
	
	os.chdir(current_path)
	
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
		fichierFinal.write(txt)
		inter.close()
		
		cmd = "bcftools view -H " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Apres Filtres SNP: " + line[0]
		fichierFinal.write(txt)
		inter.close()
		
		cmd = "bcftools view -H " + v.vcf + "INDEL/outputINDEL.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Avant Filtres INDEL: " + line[0]
		fichierFinal.write(txt)
		inter.close()
		
		cmd = "bcftools view -H " + v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.vcf.gz |wc -l > nombre.txt"
		os.system(cmd)
		
		inter = open("nombre.txt", "r")
		line = inter.readlines()
		txt = "Apres Filtres INDEL: " + line[0]
		fichierFinal.write(txt)
		inter.close()
		
		#Fin
		fichierFinal.close()
		os.remove("nombre.txt")
		
	os.chdir(current_path)

	#Rajouter graphe donnees sans filtres
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
		traceSNP(v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.txt", v.graphs+"SNP/Filter/")
	if imageIndel:
		traceIndel(v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.txt", v.graphs+"INDEL/Filter/")
 
	print("FIN SCRIPT FIGURE")
