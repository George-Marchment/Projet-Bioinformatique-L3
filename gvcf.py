#George Marchment + Clemence Sebe
#Script GVCF
import gzip
import shutil
import os
import variables as v



def mainGVCF(telechargementGVCF, createBbOutput, tabFichierNom, tabFichierBam, tabSampleAlias):
	print("SCRIPT GVCF")
	
	if telechargementGVCF:
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
		
		#rajouter lien pour cohort
		fichier = open(v.donnees + "cohort.sample_map", "a")
		
		os.chdir(current_path)
		for i in range (len(tabFichierBam)):
			print("----------------------BOUCLE HAPlOTYPECALLER----------------------", i+1 , " sur " , len(tabFichier)) 
			ref = v.geneRefDossier + fasta 
			entree = v.adressePostMk + tabFichierBam[i]
			sortie = v.adresseGVCF + tabFichierNom[i] + ".g.vcf.gz"
			sortiebis = v.adresseGVCF + tabFichierNom[i]
			cmd = "gatk HaplotypeCaller -R " + ref + " -I " + entree + " -O " + sortie + " -ERC GVCF"
			os.system(cmd) 
		
		
	#rajouter lien pour cohort
	fichier = open(v.donnees + "cohort.sample_map", "a")	
	for i in range (len(tabFichierBam)):
		sortie = v.adresseGVCF + tabFichierNom[i] + ".g.vcf.gz"
		sortiebis = tabSampleAlias[i]	
		ligne = sortiebis + "\t" + sortie + "\n"
		fichier.write(ligne)
	fichier.close()
	
	if createBbOutput:
		#create BDD
		cmd = "gatk GenomicsDBImport --genomicsdb-workspace-path " +v.donnees + "my_database " + "--sample-name-map " + v.donnees + "cohort.sample_map" + " -L " + v.donnees +  "chromosome.list"
		os.system(cmd)
		
		#Create final vcf
		cmd = "gatk GenotypeGVCFs -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta" + " -V gendb://"+ v.donnees+"my_database -O " + v.donnees + "output.vcf.gz"
		os.system(cmd)
		shutil.rmtree(v.donnees + "my_database")
		
		#info SNP Indel taille
		fichier = open("informationSnpIndel.txt", "a")	
		# a faire
		fichier.close()
		
	os.remove(v.donnees + "cohort.sample_map")
	print("FIN SCRIPT GVCF")
	
