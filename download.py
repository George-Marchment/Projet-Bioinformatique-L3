#George Marchment + Clemence Sebe
#Script telechargement
import subprocess as sp
import hashlib as hb
import gzip
import shutil
import os


def telecharger(nom):
    sp.call(['wget', nom])
 
def calculMd5(nom):
	md5 = hb.md5(open(nom,'rb').read()).hexdigest()
	return md5

def unzip(nomDossier, nomUnzip):
	#unzip
	with gzip.open(nomDossier, 'rb') as f_in:
		with open(nomUnzip, 'wb') as f_out:
			shutil.copyfileobj(f_in, f_out)

def mainD(telechargement):
	#ADRESSE TELECHARGEMENT GEORGE
	adresse_George="/media/george/USB2GM/Projet_BioInformatique/Données"
	#ADRESSE TELECHARGEMENT CLEMENCE
	adresse_Clemence="/home/clemence/L3/S6/ProjetBioInformatique/Projet-Bioinformatique-L3/Donnees/" 
	#BOOL GEORGE QUI UTILISE SCRIPT 
	#george= True #George
	george= False #Clemence
	#Garder en memoire nomFichier
	tabFichier = []


	print("DEBUT SCRIPT TELECHARCHEMENT")
	#------------------------Etape1: lire fichier + creation dictionnaire------------------------
	fichierDonnees = open("donnees.txt", 'r')

	lignes = fichierDonnees.readlines()

	prems = lignes[0].split('\t')
	prems[-1] = prems[-1].strip() #enlever \n

	dicoDonnees = []

	for i in range (1,len(lignes)):
		temp = lignes[i].split('\t')
		temp[-1] = temp[-1].strip()
		
		donnees = {}
		for j in range (len(prems)):
			donnees.update({prems[j]: temp[j]})

		dicoDonnees.append(donnees)

	fichierDonnees.close()
	
	#------------------------Etape2 : telechargement------------------------
	current_path= os.getcwd()
	if george:
	    path= adresse_George
	else:
	    path= adresse_Clemence
	os.chdir(path)

	for i in range (2): #(len(dicoDonnees)):
		print('-----------------------------BOUCLE-------------------- ', i, 'sur ' , len(dicoDonnees))
		etude = dicoDonnees[i]['fastq_ftp']
		etude = etude.split(';')
		
		md5fichier = dicoDonnees[i]['fastq_md5']
		md5fichier = md5fichier.split(';')
			
		for j in range (len(etude)):
			if (etude[j] != ''):
				down = 'ftp://' + etude[j]
				if telechargement:
					telecharger(down)
				
				if len(etude) != 1:
					nomDossier = dicoDonnees[i]['run_accession'] + "_" + str(j+1) + ".fastq.gz"
					nomUnzip = dicoDonnees[i]['run_accession'] + "_" + str(j+1) + ".fastq"
					nomNom = dicoDonnees[i]['run_accession'] + "_" + str(j+1)
				else:
					nomDossier = dicoDonnees[i]['run_accession'] + ".fastq.gz"
					nomUnzip = dicoDonnees[i]['run_accession'] + ".fastq"
					nomNom = dicoDonnees[i]['run_accession'] + "_" + str(j+1)

				if telechargement:
					md5 = calculMd5(nomDossier)
					while(md5 != md5fichier[j]):
						print('ERREUR retelechargement\n')
						telecharger()
						md5 = calculMd5(nomDossier)
						
					#unzip(nomDossier, nomUnzip)
				tabFichier.append(nomNom)		
				#supp .gz
				#os.remove(nomDossier)
	os.chdir(current_path)
	print("FIN SCRIPT TELECHARCHEMENT")
	return tabFichier

