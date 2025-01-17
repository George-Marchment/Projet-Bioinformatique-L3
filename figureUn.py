#George Marchment + Clemence Sebe
#Script Figure un
import os
import variables as v
import matplotlib.pyplot as plt
import numpy as np

#Function that creates all the function correspondint to the mapping and 'couverture' data
def mainFigureUn(tabFichier, imageMapping, imageCouv):
	print("DEBUT SCRIPT FIGURE UN")
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
			
			#Extracting the Mapping data to do this we use samtools flagstat
			if imageMapping:
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

			#Extracting the 'couverture' data to do this we use bedtools genomecov
			if imageCouv:
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

	#Jumping to the adress to create the corresponding Graphs
	os.chdir(v.simple)
	
	#Creating the Mapping graphs
	if imageMapping:
		print('Figure Mapping')
		os.chdir(v.graphs+"General/")
		#1st
		fig,ax = plt.subplots()
		ax.plot(tabFigMapping,"o-")
		ax.set_title("Pourcentage de donnees qui mappent sur les 26 échantillons")
		ax.set_xlabel('Echantillons')
		ax.set_ylabel('Pourcentage de mapping')
		plt.savefig('MappingCourbe.png')
		#2nd
		fig,ax = plt.subplots()
		plt.hist(tabFigMapping)
		ax.set_title("Histogramme Mapping")
		ax.set_xlabel('Pourcentage de Couverture')
		ax.set_ylabel("Nombre d'échantillons")
		plt.savefig('MappingHisto.png')
		
	#Creating the 'Couverture' graph
	if imageCouv:
		print("Figure pour bedtools")
		os.chdir(v.graphs+"General/")
		fig,ax = plt.subplots()
		ax.plot(tabBedMean, "o-")
		ax.set_title("Couverture moyenne des 26 échantillons")
		ax.set_xlabel('Echantillons')
		ax.set_ylabel('Couverture Moyenne')
		plt.savefig('CouvertureMoyenne.png')
	
	#Returning to the original adress
	os.chdir(current_path)

	print("FIN SCRIPT FIGURE UN")
