#George Marchment + Clemence Sebe
#Script telechargement
import subprocess as sp
import hashlib as hb
import gzip
import shutil
import os
import download
import variables as v
import matplotlib.pyplot as plt
import numpy as np

def unzip(nomDossier, nomUnzip):
	#unzip
	with gzip.open(nomDossier, 'rb') as f_in:
		with open(nomUnzip, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)

def mainBWA(telechargement=True, numberDownload=-1):
	#recuperer tab
	tabFichier = download.mainDownload(telechargement, numberDownload)
	print(tabFichier)
	tabFig = []

	print("DEBUT SCRIPT BWA")

	current_path= os.getcwd()
	os.chdir(v.adresseBwa)

	#nom fichier genome ref : S288C_reference_sequence_R64-2-1_20150113.fsa
	#definir index:
	
	cmd = "./bwa index " + v.geneRef
	os.system(cmd)
 	
    #boucle qui parcourt tous les fichiers         ./bwa mem ref.fa read-se.fq.gz        | gzip -3 > aln-se.sam.gz
	#cmd = "./bwa mem " + geneRef + " " + "../Donnees/" + tabFichier[i] + ".fastq.gz"  + " | gzip -3 > " + nomZip
 
	for i in range (len(tabFichier)):
		os.chdir(v.adresseBwa)
		print("----------------------BOUCLE----------------------", i+1 , " sur " , len(tabFichier)) 
	
		nomZip = v.zipSam + tabFichier[i] + ".sam.gz"
		nomUnzip = v.zipSam + tabFichier[i] + ".sam"
		cmd = "./bwa mem " + v.geneRef + " " + v.samRef + tabFichier[i] + ".fastq.gz"  + " | gzip -3 > " + nomZip
		os.system(cmd)
		
		print("Convertion du fichier : ", nomZip, " en un fichier .bam")
		unzip(nomZip, nomUnzip)
		os.remove(nomZip)
		fichierBam = v.bamRef + tabFichier[i] + ".bam"
		#Use samtools view. The -S indicates the input is in SAM format and the "b" indicates that you'd like BAM output.
		cmd = "samtools view -bS " + nomUnzip + " > " + fichierBam 
		os.system(cmd)
  
		"""print("MarkDuplicatesSpark de : "+fichierBam)
		cmd = "gatk MarkDuplicatesSpark -I " +fichierBam+ " -O "+ fichierBam
		os.system(cmd)"""
		
		print("Samtools flagstat + creation fichier txt")
		flag = tabFichier[i] + ".txt"
		cmd = "samtools flagstat " + fichierBam + " > " +  v.bamRef + flag
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
		
	os.chdir(current_path)
	print("FINI")
	
