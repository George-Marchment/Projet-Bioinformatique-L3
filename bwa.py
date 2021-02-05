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


def mainBWA(telechargement=True, numberDownload=-1):
	
	#IMPORTANT: this script is called bwa.py but it does many other thing
	# We will most likely decompose the script into multiple scripts later on
	print("DEBUT SCRIPT BWA")
	
 	#Getting Tab names 
	tabFichier = download.mainDownload(telechargement, numberDownload)
	print(tabFichier)
	
	#Tab Used for the percentage plot at the end
	tabFig = []

	#Saving the current path
	current_path= os.getcwd()
	#Moving to the adress of the BWA folder to be able to use ./bwa
	os.chdir(v.adresseBwa)
	
	#Deinfing the Index of bwa thanks to the Reference Genome
	cmd = "./bwa index " + v.geneRef
	os.system(cmd)
 	
	

	#For every fastq file..
	for i in range (len(tabFichier)):
		os.chdir(v.adresseBwa)
		print("----------------------BOUCLE PIPELINE----------------------", i+1 , " sur " , len(tabFichier)) 
	
		#.fastq -> .sam using ./bwa mem
		print("Convertion du fichier : ", tabFichier[i] + ".fastq.gz", " en un fichier .sam")
		nomZip = v.zipSam + tabFichier[i] + ".sam.gz"
		cmd = "./bwa mem -R \"@RG\\tID:ID\\tSM:SAMPLE_NAME\\tPL:Illumina\\tPU:PU\\tLB:LB\" " + v.geneRef + " " + v.adresseTelechargement + tabFichier[i] + ".fastq.gz"  + " | gzip -3 > " + nomZip
		os.system(cmd)
		
		#.sam -> .bam using samtools
		print("Convertion du fichier : ", tabFichier[i] + ".sam.gz", " en un fichier .bam")
		fichierBam = tabFichier[i] + ".bam"
		#Use samtools view. The -S indicates the input is in SAM format and the "b" indicates that you'd like BAM output.
		cmd = "samtools view -bS " + nomZip + " > " + v.bamRefPreMK+fichierBam 
		os.system(cmd)
  
		#Marking the duplicates thanks to gatk MarfDuplicateSpark
		print("MarkDuplicatesSpark de : "+fichierBam)
		cmd = "gatk MarkDuplicatesSpark -I " + v.bamRefPreMK+fichierBam+ " -O "+ v.bamRefPostMK+fichierBam 
		os.system(cmd)
  
		#These should be "un"commented to conserve memory for tests we will leave them
		#os.remove(nomZip)
		#os.remove(v.bamRefPreMK+fichierBam)
		
		#Temporary Things which are interesting for now!
		#----------------------------------------------------------------------
		print("Samtools flagstat + creation fichier txt")
		flag = tabFichier[i] + ".txt"
		cmd = "samtools flagstat " + v.bamRefPostMK+fichierBam + " > " +  v.fichTxt + flag
		os.system(cmd)
	
		print("Ajout du pourcentage dans un tableau pour figure % qui mappe")
		#Ajout donnee pour figure
		os.chdir(v.fichTxt)
		file = open(flag, "r")
		for i in range (4):
			line = file.readline()
		ligne5 = file.readline()
		l = ligne5.split()
		cas = l[4]
		cas = cas.split('(')
		new = cas[1]
		new = new.split("%")
		num = new[0]
		tabFig.append(num)
		file.close()
	
	os.chdir(v.simple)
	print("Creation figure")
	fig,ax = plt.subplots()
	ax.plot(tabFig)
	ax.set_title("% de donnees qui mappe")
	plt.savefig('image.png')
	#--------------------------------------------------------------------------
	
	#Returning to the current path
	os.chdir(current_path)
	print("FINI")
	
