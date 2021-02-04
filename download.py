#George Marchment + Clemence Sebe
#Script telechargement
import subprocess as sp
import hashlib as hb
import gzip
import shutil
import os
import variables as v


#Function that takes an adress and downloads the element corresponding to the adress given
def telecharger(nom):
    sp.call(['wget', nom])

#Function that takes a fastq.gz file and returns the corresponding md5 (str)
def calculMd5(nom):
	md5 = hb.md5(open(nom,'rb').read()).hexdigest()
	return md5

#Function that unzips a file, it takes the original file(+adress) to unzip and the name(+adress) of the unzipped file
def unzip(nomDossier, nomUnzip):
	#unzip
	with gzip.open(nomDossier, 'rb') as f_in:
		with open(nomUnzip, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)

#Function that returns a tab corresponding to the names of the origianl fastq(.gz) files
#It can also download the different fastq files thanks to the .ods file taken dirrectly of the ENA website
#It's different parmeters are:
def mainDownload(telechargement=True, numD=-1):
    
    #Tab corresponding to the names of the origianl fastq(.gz) files
	tabNomFastq = []
 
	print("DEBUT SCRIPT TELECHARCHEMENT")
 
	#------------------1st step: reading the .ods file + creating the corresponding dictionnary---------------
	fichierDonnees = open("donnees.txt", 'r')
 
	#'Spliting' the file from the lignes
	lignes = fichierDonnees.readlines()
	dicoDonnees = []
 
	#The original names of the columns 
	prems = lignes[0].split('\t')
	prems[-1] = prems[-1].strip() #enlever \n
 
	for i in range (1, len(lignes)):
     
		#'Spliting' the ligne from the '\tab'
		temp = lignes[i].split('\t')
		temp[-1] = temp[-1].strip()#removing '\n'
		donnees = {}
  
		for j in range (len(prems)):
			donnees.update({prems[j]: temp[j]})
   
		dicoDonnees.append(donnees)
  
	fichierDonnees.close()
	
	#------------------------Step 2 : Downloading file (optional) + filling tabNomFastq------------------------
	#Saving current location
	current_path= os.getcwd()
 
	#Setting new location to the adress the user wants the files to be downloaded
	os.chdir(v.adresseTelechargement)

	#Setting the number of fastq files to be downloaded and to be 'worked' further on in the pipepline
	if(numD==-1):
		nombreTelechargement= len(dicoDonnees)
	else:
		nombreTelechargement= numD
  
	#Downloading the files + adding the name of the files into tabNomFastq
	for i in range (nombreTelechargement):
		print('-----------------------------BOUCLE TELECHARGEMENT-------------------- ', i+1, ' sur ' , nombreTelechargement)

		#Getting the different fastq addresses for download
		etude = dicoDonnees[i]['fastq_ftp']
		etude = etude.split(';')

		#Getting the different md5s for the fastq for verification below
		md5fichier = dicoDonnees[i]['fastq_md5']
		md5fichier = md5fichier.split(';')
			
		for j in range (len(etude)):
			if (etude[j] != ''):
				down = 'ftp://' + etude[j]
				#Download
				if telechargement:
					telecharger(down)
				
				#Getting name
				if len(etude) != 1:
					nomDossier = dicoDonnees[i]['run_accession'] + "_" + str(j+1) + ".fastq.gz"
					nomUnzip = dicoDonnees[i]['run_accession'] + "_" + str(j+1) + ".fastq"
					nameFastq = dicoDonnees[i]['run_accession'] + "_" + str(j+1)
				else:
					nomDossier = dicoDonnees[i]['run_accession'] + ".fastq.gz"
					nomUnzip = dicoDonnees[i]['run_accession'] + ".fastq"
					nameFastq = dicoDonnees[i]['run_accession']

				#Checks if it's the right md5 file: if not we redownload the fastq file
				if telechargement:
					md5 = calculMd5(nomDossier)
					while(md5 != md5fichier[j]):
						print('ERREUR retelechargement\n')
						telecharger(down)
						md5 = calculMd5(nomDossier)
						
					#unzip(nomDossier, nomUnzip)
				
    			#Adding name of the fastq file to tabNomFastq
				tabNomFastq.append(nameFastq)	
    	
				#supp .gz
				#os.remove(nomDossier)
    
    #Returning to the original adress
	os.chdir(current_path)
	print("FIN SCRIPT TELECHARCHEMENT")
	return tabNomFastq

