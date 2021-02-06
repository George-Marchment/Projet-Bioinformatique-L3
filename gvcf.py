#George Marchment + Clemence Sebe
#Script Pipeline
import subprocess as sp
import hashlib as hb
import gzip
import shutil
import os
import download
import bwa
import variables as v
import matplotlib.pyplot as plt
import numpy as np


def mainGVCF(telechargement=True, telechargementBam=True,numberDownload=-1):
	#Calling the "main" script
	nom = download.mainDownload(False, numberDownload)
	tabFichier = bwa.mainBWA(telechargement,telechargementBam, numberDownload)
	
	#initialisation creation fichier pour fichier de ref
	#Saving the current path
	current_path= os.getcwd()
	os.chdir(v.geneRefDossier)
	
	print("Conversion gene de reference .fsa en .fasta")
	fsa = "S288C_reference_sequence_R64-2-1_20150113.fsa"
	fasta = "S288C_reference_sequence_R64-2-1_20150113.fasta"
	cmd = "cp " + fsa + " " + fasta
	os.system(cmd)
	
	print("Creation fichier utilse pour HaplotypeCaller")
	cmd = "gatk CreateSequenceDictionary -R " + fasta
	os.system(cmd)
	cmd = "samtools faidx " + fasta
	os.system(cmd)
	
	
	os.chdir(current_path)
	for i in range (len(tabFichier)):
		
		print("HaplotypeCaller sur " + tabFichier[i]) 
		ref = v.geneRefDossier + fasta 
		entree = v.adressePostMk + tabFichier[i]
		sortie = v.adresseGVCF + nom[i] + ".g.vcf.gz"
		cmd = "gatk HaplotypeCaller -R " + ref + " -I " + entree + " -O " + sortie + " -ERC GVCF"
		os.system(cmd)


	print("FINI")
	
