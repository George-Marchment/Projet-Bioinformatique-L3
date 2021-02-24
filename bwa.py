#George Marchment + Clemence Sebe
#Script BWA
import gzip
import shutil
import os
import variables as v


#Function that unzips a file, it takes the original file(+adress) to unzip and the name(+adress) of the unzipped file
def unzip(nomDossier, nomUnzip):
	#unzip
	with gzip.open(nomDossier, 'rb') as f_in:
		with open(nomUnzip, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)


def mainBWA(telechargementBam, tabFichierNom):
	
	#IMPORTANT: this script is called bwa.py but it does many other thing
	# We will most likely decompose the script into multiple scripts later on
	print("DEBUT SCRIPT BWA")
		
	tabFichier=[]
	for i in range(len(tabFichierNom)):
		if(len(tabFichierNom[i])!=1):
			tabFichier.append(tabFichierNom[i][0][:-2])
		else:
			tabFichier.append(tabFichierNom[i][0])
	
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
		fichierBam = tabFichier[i] + ".bam"
		os.chdir(v.adresseBwa)
		if telechargementBam :
			print("----------------------BOUCLE BWA----------------------", i+1 , " sur " , len(tabFichier))
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
		
		#ajout ds tab pour la suite
		tabFinish.append(fichierBam)

	#Returning to the current path
	os.chdir(current_path)
	tabFichierFASTQ= tabFichier
	print("FIN SCRIPT BWA")
	return tabFichierFASTQ, tabFinish
	
