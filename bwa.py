#George Marchment + Clemence Sebe
#Script telechargement
import subprocess as sp
import hashlib as hb
import gzip
import shutil
import os
import download
import variables as v

def mainBWA(telechargement):
	#recuperer tab
	tabFichier = download.mainDownload(telechargement)
	print(tabFichier)

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
		print("----------------------BOUCLE----------------------", i+1 , " sur " , len(tabFichier)) 
		nomZip = v.zipSam + tabFichier[i] + ".sam.gz"
		cmd = "./bwa mem " + v.geneRef + " " + v.samRef + tabFichier[i] + ".fastq.gz"  + " | gzip -3 > " + nomZip
		os.system(cmd)

	os.chdir(current_path)
	print("FINI")
