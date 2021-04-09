#George Marchment + Clemence Sebe
#Script GVCF
import gzip
import shutil
import os
import variables as v


#Function that does everything from gatk CreateSequenceDictionary to gatk GenotypeGVCFs
#At the end of the function we have a .vcf containing a summary of all the sample 
def mainGVCF(telechargementGVCF, createBbOutput, tabFichierNom, tabFichierBam, tabSampleAlias):
	print("DEBUT SCRIPT GVCF")
	
	if telechargementGVCF:
		#initialisation creation fichier pour fichier de ref
		#Saving the current path
		current_path= os.getcwd()
		os.chdir(v.geneRefDossier)
		
		#Converting the reference sequence to .fasta format
		print("Conversion gene de reference .fsa en .fasta")
		fsa = "S288C_reference_sequence_R64-2-1_20150113.fsa"
		fasta = "S288C_reference_sequence_R64-2-1_20150113.fasta"
		cmd = "cp " + fsa + " " + fasta
		os.system(cmd)

		#Initialisation => Creates a sequence dictionary for a reference sequence		
		print("Creation fichier utilse pour HaplotypeCaller")
		cmd = "gatk CreateSequenceDictionary -R " + fasta
		os.system(cmd)
		cmd = "samtools faidx " + fasta
		os.system(cmd)
		
		#rajouter lien pour cohort
		#fichier = open(v.donnees + "cohort.sample_map", "a")
		
		# .bam => .g.vcf using HaplotypeCaller
		#Extract variants for every sample
		os.chdir(current_path)
		for i in range (len(tabFichierBam)):
			print("----------------------BOUCLE HAPlOTYPECALLER----------------------", i+1 , " sur " , len(tabFichierBam)) 
			ref = v.geneRefDossier + fasta 
			entree = v.adressePostMk + tabFichierBam[i]
			sortie = v.adresseGVCF + tabFichierNom[i] + ".g.vcf.gz"
			sortiebis = v.adresseGVCF + tabFichierNom[i]
			cmd = "gatk HaplotypeCaller -R " + ref + " -I " + entree + " -O " + sortie + " -ERC GVCF"
			os.system(cmd) 
	print("END HAPLTYPECALLER")
		
		
	#rajouter lien pour cohort
	#Creating Sample map to create database
	fichier = open(v.donnees + "cohort.sample_map", "w")	
	for i in range (len(tabFichierBam)):
		sortie = v.adresseGVCF + tabFichierNom[i] + ".g.vcf.gz"
		sortiebis = tabSampleAlias[i]	
		ligne = sortiebis + "\t" + sortie + "\n"
		fichier.write(ligne)
	fichier.close()
	
	if createBbOutput:
		#create database
		cmd = "gatk GenomicsDBImport --genomicsdb-workspace-path " +v.adresseBDD + "my_database " + "--sample-name-map " + v.donnees + "cohort.sample_map" + " -L "+ v.donnees +  "chromosome.list"
		os.system(cmd)

		#Create final vcf
		cmd = "gatk GenotypeGVCFs -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta" + " -V gendb://"+ v.adresseBDD+"my_database -O " + v.vcf + "output.vcf.gz"
		os.system(cmd)
		shutil.rmtree(v.adresseBDD + "my_database")
					
	#os.remove(v.donnees + "cohort.sample_map")
	print("FIN SCRIPT GVCF")
	
