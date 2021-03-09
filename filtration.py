#George Marchment + Clemence Sebe
#Script Filtration
import os
import variables as v


def mainFiltration(telechargementFiltreSNP, telechargementFiltreINDEL):
	print("DEBUT SCRIPT FILTRATION")
	if telechargementFiltreSNP:
		#On selectionne les SNP 
		cmd = "gatk SelectVariants -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta" + " -V " +  v.donnees + "output.vcf.gz --select-type-to-include SNP  -O " + v.donnees + "outputSNP.vcf.gz"
		os.system(cmd)
		
		#Select Variant
		# A revoir niveau filtre !!!!!! 
		#cmd = "gatk VariantFiltration -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta -V " + v.donnees + "outputSNP.vcf.gz -O " + v.donnees +  "outputSnpFiltrer.vcf.gz --filter-expression \"QD < 10.0 \" --filter-name \"filtering_snp\""
		
		cmd = "bcftools filter -e 'QD < 2.0 || FS < 1.0  || MQ < 1.0 || MQRankSum < 1.0 || ReadPosRankSum >= 0.0 || SOR < 1.0' -O z -o " + v.donnees + "outputSnpFiltrer.vcf.gz " + v.donnees + "outputSNP.vcf.gz"
		# -e : exclude ||
		# -i include &&
		os.system(cmd)
		
		#QD < 2.0 || FS < 1.0  || MQ < 1.0 || MQRankSum < 1.0 || ReadPosRankSum >= 0.0 || SOR < 1.0
		
		#Extraire donnee pour figure : (meme colonne que ds l'exemple)
		cmd = "bcftools query " + v.donnees +  "outputSnpFiltrer.vcf.gz -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%FS\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.donnees + "outputSnpFiltrer.txt"
		os.system(cmd)

		#Rajout legende premiere ligne
		cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tFS\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.donnees  + "outputSnpFiltrer.txt"
		os.system(cmd)	
		
	if telechargementFiltreINDEL:
		cmd = "gatk SelectVariants -R " + v.geneRefDossier + "S288C_reference_sequence_R64-2-1_20150113.fasta" + " -V " +  v.donnees + "output.vcf.gz --select-type-to-include INDEL  -O " + v.donnees + "outputINDEL.vcf.gz"
		os.system(cmd)
	
		#Select Variant
		# A revoir niveau filtre !!!!!! 		
		cmd = "bcftools filter -e 'QD < 2.0 || FS < 1.0  || MQ < 1.0 || MQRankSum < 1.0 || ReadPosRankSum >= 0.0 || SOR < 1.0' -O z -o " + v.donnees + "outputIndelFiltrer.vcf.gz " + v.donnees + "outputINDEL.vcf.gz"
		os.system(cmd)
		
		#Extraire donnee pour figure : (meme colonne que ds l'exemple)
		cmd = "bcftools query " + v.donnees +  "outputIndelFiltrer.vcf.gz -f '%CHROM\t%POS\t%REF\t%ALT\t%QD\t%FS\t%MQ\t%MQRankSum\t%ReadPosRankSum\t%SOR\t%DP\n' > " + v.donnees + "outputIndelFiltrer.txt"
		os.system(cmd)

		#Rajout legende premiere ligne
		cmd = "sed -i '1iCHROM\tPOS\tREF\tALT\tQD\tFS\tMQ\tMQRankSum\tReadPosRankSum\tSOR\tDP' " + v.donnees  + "outputIndelFiltrer.txt"
		os.system(cmd)

	print("FIN SCRIPT FILTRATION")
