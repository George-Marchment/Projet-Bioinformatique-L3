#George Marchment + Clemence Sebe
#Script Filtration
import os
import variables as v



def mainFiltration(telechargementFiltreSNP, telechargementFiltreINDEL, sansFiltre, avecFiltre, filtre):
	print("DEBUT SCRIPT FILTRATION")
	current_path= os.getcwd()

	#On récupère les filtre
	qd= filtre['QD'][1]
	fs= filtre['FS'][1]
	mq= filtre['MQ'][1]
	mqRankSum= filtre['MQRankSum'][1]
	readPosRankSum= filtre['ReadPosRankSum'][1]
	sor= filtre['SOR'][1]
 
 	#On récupère les synmboles de comparaison pour les filtres
	sym_qd= filtre['QD'][0]
	sym_fs= filtre['FS'][0]
	sym_mq= filtre['MQ'][0]
	sym_mqRankSum= filtre['MQRankSum'][0]
	sym_readPosRankSum= filtre['ReadPosRankSum'][0]
	sym_sor= filtre['SOR'][0]

	filtre_qd= " --filter-name \'QD"+str(qd)+"\' --filter-expression \"QD"+sym_qd+str(qd)+"\""
	filtre_fs= " --filter-name \'QD"+str(qd)+"\' --filter-expression \"QD"+sym_qd+str(qd)+"\""
	filtre_mq= " --filter-name \'MQ"+str(mq)+"\' --filter-expression \"MQ"+sym_mq+str(mq)+"\""
	filtre_mqRankSum= " --filter-name \'MQRankSum"+str(mqRankSum)+"\' --filter-expression \"MQRankSum"+sym_mqRankSum+str(mqRankSum)+"\""
	filtre_readPosRankSum= " --filter-name \'ReadPosRankSum"+str(readPosRankSum)+"\' --filter-expression \"ReadPosRankSum"+sym_readPosRankSum+str(readPosRankSum)+"\""
	filtre_sor= " --filter-name \'SOR"+str(qd)+"\' --filter-expression \"SOR"+sym_sor+str(sor)+"\""
	filtres= filtre_qd+filtre_fs+filtre_mq+filtre_mqRankSum+filtre_readPosRankSum+filtre_sor

	#Cette partie du code est clairement écrit d'un manière pour simplifier la lecture, elle n'est pas optimisé ni 'facile' à modifier comme on rèpète souvent les mêmes choses
	
	#SNP
	if telechargementFiltreSNP:
		#On selectionne les SNP 
		cmd = "gatk SelectVariants -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta" + " -V " +  v.vcf + "output.vcf.gz --select-type-to-include SNP  -O " + v.vcf + "SNP/outputSNP.vcf.gz"
		os.system(cmd)
		
		if(sansFiltre):
			#Extraire donnee pour figure : (meme colonne que ds l'exemple)
			cmd = "bcftools query " + v.vcf + "SNP/outputSNP.vcf.gz -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%FS\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.vcf + "SNP/PRE_FILTRE/outputSnpNoFiltrer.txt"
			os.system(cmd)
   
			#Rajout legende premiere ligne
			cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tFS\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.vcf + "SNP/PRE_FILTRE/outputSnpNoFiltrer.txt"
			os.system(cmd)	

		if(avecFiltre):
			#Select Variant
			#Les deux options en dessus pour les filtres
			cmd = "gatk VariantFiltration -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta -V " + v.vcf + "SNP/outputSNP.vcf.gz -O " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.vcf.gz"+filtres
			#cmd= "bcftools filter -e 'QD "+sym_qd+str(qd)+ " || FS "+sym_fs+str(fs)+" || MQ "+sym_mq+str(mq)+" || MQRankSum "+sym_mqRankSum+str(mqRankSum)+" || ReadPosRankSum "+sym_readPosRankSum+str(readPosRankSum)+" || SOR "+sym_sor+str(sor)+"' -O z -o " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.vcf.gz " + v.vcf + "SNP/outputSNP.vcf.gz"
			os.system(cmd)
			
			#Extraire donnee pour figure : (meme colonne que ds l'exemple)
			cmd = "bcftools query " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.vcf.gz -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%FS\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.txt"
			os.system(cmd)

			#Rajout legende premiere ligne
			cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tFS\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.txt"
			os.system(cmd)


	#INDEL
	if telechargementFiltreINDEL:
		#On selectionne les INDEL 
		cmd = "gatk SelectVariants -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta" + " -V " +  v.vcf + "output.vcf.gz --select-type-to-include INDEL  -O " + v.vcf + "INDEL/outputINDEL.vcf.gz"
		os.system(cmd)
		
		if(sansFiltre):
			#Extraire donnee pour figure : (meme colonne que ds l'exemple)
			cmd = "bcftools query " + v.vcf + "INDEL/outputINDEL.vcf.gz -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%FS\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.vcf + "INDEL/PRE_FILTRE/outputIndelNoFiltrer.txt"
			os.system(cmd)
   
			#Rajout legende premiere ligne
			cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tFS\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.vcf + "INDEL/PRE_FILTRE/outputIndelNoFiltrer.txt"
			os.system(cmd)	

		if(avecFiltre):
      
			#Select Variant
			#Vieux
			#SEMBLE NE PAS FONCTIONNER -> a Voir Pourquoi
			#cmd = "gatk VariantFiltration -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta -V " + v.vcf + "INDEL/outputINDEL.vcf.gz -O " + v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.vcf.gz -filter \"QD"+sym_qd+str(qd)+" \" --filter-name \'QD\'"#'QD"+sym_qd+str(qd)+ "
			#Les Deux Choix en dessus
			cmd = "gatk VariantFiltration -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta -V " + v.vcf + "INDEL/outputINDEL.vcf.gz -O " + v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.vcf.gz"+filtres
			#cmd= "bcftools filter -e 'QD "+sym_qd+str(qd)+ " || FS "+sym_fs+str(fs)+" || MQ "+sym_mq+str(mq)+" || MQRankSum "+sym_mqRankSum+str(mqRankSum)+" || ReadPosRankSum "+sym_readPosRankSum+str(readPosRankSum)+" || SOR "+sym_sor+str(sor)+"' -O z -o " + v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.vcf.gz " + v.vcf + "INDEL/outputINDEL.vcf.gz"
			os.system(cmd)

			#Extraire donnee pour figure : (meme colonne que ds l'exemple)
			cmd = "bcftools query " + v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.vcf.gz -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%FS\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\t%FILTER\n' > " + v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.txt"
			os.system(cmd)	
			
			#Rajout legende premiere ligne
			cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tFS\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP\tFILTER' " + v.vcf + "INDEL/POST_FILTRE/outputIndelFiltrer.txt"
			os.system(cmd)

		
	print("FIN SCRIPT FILTRATION")
