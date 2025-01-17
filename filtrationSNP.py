#George Marchment + Clemence Sebe
#Script Filtration SNP
import os
import variables as v


#Function that extrats the SNPs and filters them using the filters set in main.py
def mainFiltrationSNP(telechargementFiltreSNP, sansFiltre, avecFiltre, filtre):
	print("DEBUT SCRIPT FILTRATION SNP")
	current_path= os.getcwd()

	#We recuperate the filters
	qd= filtre['QD'][1]
	mq= filtre['MQ'][1]
	mqRankSumInf= filtre['MQRankSumInf'][1]
	mqRankSumSup= filtre['MQRankSumSup'][1]
	readPosRankSumInf= filtre['ReadPosRankSumInf'][1]
	readPosRankSumSup= filtre['ReadPosRankSumSup'][1]
	sor= filtre['SOR'][1]
 
 	#We recuperate the comparaisons symbols for the filters 
	sym_qd= filtre['QD'][0]
	sym_mq= filtre['MQ'][0]
	sym_mqRankSumInf= filtre['MQRankSumInf'][0]
	sym_mqRankSumSup= filtre['MQRankSumSup'][0]
	sym_readPosRankSumInf= filtre['ReadPosRankSumInf'][0]
	sym_readPosRankSumSup= filtre['ReadPosRankSumSup'][0]
	sym_sor= filtre['SOR'][0]

	#We set the filters to give to gatk VariantFiltration
	filtre_qd= " --filter-name \'QD"+str(qd)+"\' --filter-expression \"QD"+sym_qd+str(qd)+"\""
	filtre_mq= " --filter-name \'MQ"+str(mq)+"\' --filter-expression \"MQ"+sym_mq+str(mq)+"\""
	filtre_mqRankSumInf= " --filter-name \'MQRankSumInf"+str(mqRankSumInf)+"\' --filter-expression \"MQRankSumInf"+sym_mqRankSumInf+str(mqRankSumInf)+"\""
	filtre_mqRankSumSup= " --filter-name \'MQRankSumSup"+str(mqRankSumSup)+"\' --filter-expression \"MQRankSumSup"+sym_mqRankSumSup+str(mqRankSumSup)+"\""
	filtre_readPosRankSumInf= " --filter-name \'ReadPosRankSumInf"+str(readPosRankSumInf)+"\' --filter-expression \"ReadPosRankSumInf"+sym_readPosRankSumInf+str(readPosRankSumInf)+"\""
	filtre_readPosRankSumSup= " --filter-name \'ReadPosRankSumSup"+str(readPosRankSumSup)+"\' --filter-expression \"ReadPosRankSumSup"+sym_readPosRankSumSup+str(readPosRankSumSup)+"\""
	filtre_sor= " --filter-name \'SOR"+str(sor)+"\' --filter-expression \"SOR"+sym_sor+str(sor)+"\""
	
	filtres= filtre_qd+ filtre_mq+ filtre_mqRankSumInf+ filtre_mqRankSumSup+ filtre_readPosRankSumInf+ filtre_readPosRankSumSup+ filtre_sor


	if telechargementFiltreSNP:
		#We select the SNPs 
		cmd = "gatk SelectVariants -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta" + " -V " +  v.vcf + "output.vcf.gz --select-type-to-include SNP  -O " + v.vcf + "SNP/outputSNP.vcf.gz"
		os.system(cmd)
		
		#Without Filter
		if(sansFiltre):
			#Extract the data wanted (POS, QD ect..)
			cmd = "bcftools query " + v.vcf + "SNP/outputSNP.vcf.gz -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%FS\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.vcf + "SNP/PRE_FILTRE/outputSnpNoFiltrer.txt"
			os.system(cmd)
   
			#Addition legend to the first line 
			cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tFS\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.vcf + "SNP/PRE_FILTRE/outputSnpNoFiltrer.txt"
			os.system(cmd)	

		#With filter
		if(avecFiltre):
			#Set filters
			cmd = "gatk VariantFiltration -R " + v.geneRefDossier +  "S288C_reference_sequence_R64-2-1_20150113.fasta -V " + v.vcf + "SNP/outputSNP.vcf.gz -O " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.vcf.gz"+filtres
			os.system(cmd)
			
			#Extract the data wanted (POS, QD ect..)
			cmd = "bcftools query " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.vcf.gz -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\t%FILTER\n' > " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.txt"
			os.system(cmd)

			#Addition legend to the first line 
			cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP\tFILTER' " + v.vcf + "SNP/POST_FILTRE/outputSnpFiltrer.txt"
			os.system(cmd)
		
	print("FIN SCRIPT FILTRATION SNP")
