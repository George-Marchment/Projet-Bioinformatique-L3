#George Marchment + Clemence Sebe
#Script telechargement
import subprocess as sp
import hashlib as hb
import gzip
import shutil
import os
from download import mainD 

#ADRESSE TELECHARGEMENT GEORGE
adresse_George="/media/george/USB2GM/Projet_BioInformatique/Données"
#ADRESSE TELECHARGEMENT CLEMENCE
adresse_Clemence="/home/clemence/L3/S6/ProjetBioInformatique/Projet-Bioinformatique-L3/" 
#BOOL GEORGE QUI UTILISE SCRIPT 
#george= True #George
george= False #Clemence

#recuperer tab
tabFichier = mainD(False)
print(tabFichier)

print("DEBUT SCRIPT BWA")

current_path= os.getcwd()
if george:
    path= adresse_George
else:
    path= adresse_Clemence + "bwa/"
os.chdir(path)

#nom fichier genome ref : S288C_reference_sequence_R64-2-1_20150113.fsa
#definir index:
geneRef = "../Donnees/Genome/S288C_reference_sequence_R64-2-1_20150113.fsa"
cmd = "./bwa index " + geneRef
os.system(cmd)
               
print(len(tabFichier))                                  
#boucle qui parcourt tous les fichiers         ./bwa mem ref.fa read-se.fq.gz        | gzip -3 > aln-se.sam.gz
for i in range (len(tabFichier)):
	print("----------------------BOUCLE----------------------", i , " sur " , len(tabFichier)) 
	nomZip = "../Donnees/" + tabFichier[i] + ".sam.gz"
	cmd = "./bwa mem " + geneRef + " " + "../Donnees/" + tabFichier[i] + ".fastq"  + " | gzip -3 > " + nomZip
	os.system(cmd)





