#!/usr/bin/env Rscript
#!/usr/bin/env Rscript
library(SNPRelate)
library(ggplot2)

args = commandArgs(trailingOnly=TRUE)   #la liste des arguments donc arg1  arg2 et arg3
entree = args[1]  #fichier sur lequel on travaille (adresse + nom)
adresseSortie = args[2] #adresee ou l'on veut que les fichiers crées soient sauvegardes


#Lecture du fichier vcf et creation des fichiers pour le PCA
vcf.file =  entree
snpgdsVCF2GDS(vcf.file, paste(adresseSortie,"tmp.gds",sep="", collapse=NULL), method="biallelic.only")
genofile <- snpgdsOpen(paste(adresseSortie,"tmp.gds",sep="", collapse=NULL))

#PCA 
res.pca <- snpgdsPCA(genofile, autosome.only=FALSE)

#On ressort les id des samples ainsi que les colonnes pour les representer graphiquement
tab <- data.frame(sample.id = res.pca$sample.id,
    PCA1= res.pca$eigenvect[,1],    # the first eigenvector
    PCA2 = res.pca$eigenvect[,2],    # the second eigenvector
    stringsAsFactors = FALSE)

#on ecrit le tableau dans un fichier de sortie pour apres faire des graphiques en python 
sink(paste(adresseSortie,"tabDonnees.txt",sep="", collapse=NULL))
tab
sink()

#premiere image avec R - pas tres lisible
pdf(paste(adresseSortie,"firstImagePCA.pdf",sep="", collapse=NULL))
plot(res.pca, main="PCA SNP") 
