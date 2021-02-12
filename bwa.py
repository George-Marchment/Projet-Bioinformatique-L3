#George Marchment + Clemence Sebe
#Script Pipeline
import subprocess as sp
import hashlib as hb
import gzip
import shutil
import os
import download
import variables as v
import matplotlib.pyplot as plt
import numpy as np


#Function that unzips a file, it takes the original file(+adress) to unzip and the name(+adress) of the unzipped file
def unzip(nomDossier, nomUnzip):
	#unzip
	with gzip.open(nomDossier, 'rb') as f_in:
		with open(nomUnzip, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)


def mainBWA(telechargement=True, telechargementBam=True, numberDownload=-1):
	
	#IMPORTANT: this script is called bwa.py but it does many other thing
	# We will most likely decompose the script into multiple scripts later on
	print("DEBUT SCRIPT BWA")
	
 	#Getting Tab names 
	tabFichierNom = download.mainDownload(telechargement, numberDownload)
	print("tabFichierNom: ", tabFichierNom)
	print("len(tabFichierNom): ", len(tabFichierNom))
	
	tabFichier=[]
	for i in range(len(tabFichierNom)):
		if(len(tabFichierNom[i])!=1):
			tabFichier.append(tabFichierNom[i][0][:-2])
		else:
			tabFichier.append(tabFichierNom[i][0])

	print("tabFichier: ", tabFichier)
	
	#Tab Used for the percentage plot at the end
	tabFig = []
	
	#Tab for the plot of bedtools
	tabBedMax = []
	tabBedMin = []
	tabBedMean = []
	
	#Tab for the finish with the name of the fichier .bam
	tabFinish = []
	
	
	#Saving the current path
	current_path= os.getcwd()
	#Moving to the adress of the BWA folder to be able to use ./bwa
	os.chdir(v.adresseBwa)
	if telechargementBam:
		#Deinfing the Index of bwa thanks to the Reference Genome
		cmd = "./bwa index " + v.geneRef
		os.system(cmd)
 	
	

	#For every fastq file..
	for i in range (len(tabFichier)):
		print("----------------------BOUCLE BWA----------------------", i+1 , " sur " , len(tabFichier)) 
		fichierBam = tabFichier[i] + ".bam"
		os.chdir(v.adresseBwa)
		if telechargementBam :
		
			#.fastq -> .sam using ./bwa mem
			print("Convertion du fichier : ", tabFichier[i] + ".fastq.gz", " en un fichier .sam")
			nomZip = v.zipSam + tabFichier[i] + ".sam.gz"
			if(len(tabFichierNom[i])!=1):
				c=""
				for k in range(len(tabFichierNom[i])):
					c+= " " + v.adresseTelechargement + tabFichierNom[i][k] + ".fastq.gz"
				cmd = "./bwa mem -R \"@RG\\tID:"+tabFichier[i]+"\\tSM:"+tabFichier[i]+"_sample"+"\\tPL:Illumina\\tPU:PU\\tLB:LB\" "  + v.geneRef + c  + " | gzip -3 > " + nomZip
			else:
				cmd = "./bwa mem -R \"@RG\\tID:"+tabFichier[i]+"\\tSM:"+tabFichier[i]+"_sample"+"\\tPL:Illumina\\tPU:PU\\tLB:LB\" " + v.geneRef + " " + v.adresseTelechargement + tabFichier[i] + ".fastq.gz"  + " | gzip -3 > " + nomZip
			
			os.system(cmd)
			
			#.sam -> .bam using samtools
			print("Convertion du fichier : ", tabFichier[i] + ".sam.gz", " en un fichier .bam")
			
			#Use samtools view. The -S indicates the input is in SAM format and the "b" indicates that you'd like BAM output.
			cmd = "samtools view -bS " + nomZip + " > " + v.bamRefPreMK+fichierBam
			os.system(cmd)
			
			#Use samtools sort
			print("Samtools sort:")
			trie = tabFichier[i] + "_sorted.bam"
			cmd = "samtools sort " + v.bamRefPreMK+fichierBam + " > " + v.bamRefPreMK + trie
			os.system(cmd)
	  		
			#Marking the duplicates thanks to gatk MarfDuplicateSpark
			print("MarkDuplicatesSpark de : "+ trie)
			cmd = "gatk MarkDuplicatesSpark -I " + v.bamRefPreMK+ trie + " -O "+ v.bamRefPostMK+fichierBam 
			os.system(cmd)
	  
			#These should be "un"commented to conserve memory for tests we will leave them
			os.remove(nomZip)
			os.remove(v.bamRefPreMK+fichierBam)
			os.remove(v.bamRefPreMK+trie)
		
				
		#Temporary Things which are interesting for now!
		#----------------------------------------------------------------------
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
		tabFig.append(float(num))
		file.close()
		#ajout ds tab pour la suite
		tabFinish.append(fichierBam)
		
		
		#BedTools
		#-------------------------------------------------------------------
		print("Bedtools pour calculer max, min, moyenne de la couverture")
		os.chdir(v.adresseBwa)
		bedfile = tabFichier[i] + "_bed.txt"
		cmd = "bedtools genomecov -ibam " + v.bamRefPostMK+fichierBam + " -bga > " + v.fichTxt + bedfile
		os.system(cmd)
		os.chdir(v.fichTxt)
		tabDonnees = []
		file = open(bedfile, "r")
		line = file.readlines()
		for ligne in line:
			test = ligne.split()
			tabDonnees.append(float(test[-1]))
		file.close()
		tab = np.array(tabDonnees)
		print(tab)
		maxi = np.max(tab)
		mini = np.min(tab)
		moyenne = np.mean(tab)
		tabBedMax.append(maxi)
		tabBedMin.append(mini)
		tabBedMean.append(moyenne)
	
	os.chdir(v.simple)
	print("Creation figure")
	fig,ax = plt.subplots()
	ax.plot(tabFig)
	ax.set_title("Pourcentage de donnees qui mappe")
	plt.savefig('imageMapping.png')
	
	print("Figure pour bedtools")
	fig,ax = plt.subplots()
	ax.plot(tabBedMax) # arevoir 
	ax.set_title("Couverture : max")
	plt.savefig('imageCouvertureMax.png')
	fig,ax = plt.subplots()
	ax.plot(tabBedMin) # arevoir 
	ax.set_title("Couverture : min")
	plt.savefig('imageCouvertureMin.png')
	fig,ax = plt.subplots()
	ax.plot(tabBedMean) # arevoir 
	ax.set_title("Couverture : moyenne")
	plt.savefig('imageCouvertureMoyenne.png')
	#--------------------------------------------------------------------------

	#Returning to the current path
	os.chdir(current_path)
	tabFichierFASTQ= tabFichier
	return tabFichierFASTQ, tabFinish
	
