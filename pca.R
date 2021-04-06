#!/usr/bin/env Rscript
library(SNPRelate)
library(gdsfmt)
library(ape)
library(RColorBrewer)

#------------------------------------------------------------------------
args = commandArgs(trailingOnly=TRUE)   #la liste des arguments donc arg1  arg2 et arg3
entree = args[1]  #fichier sur lequel on travaille (adresse + nom)
adresseSortie = args[2] #adresee ou l'on veut que les fichiers crées soient sauvegardes
adresseSample = args[3]

#------------------------------------------------------------------------
#Lecture du fichier vcf et creation des fichiers pour le PCA
vcf.file =  entree
snpgdsVCF2GDS(vcf.file, paste(adresseSortie,"tmp.gds",sep="", collapse=NULL), method="biallelic.only")
genofile <- snpgdsOpen(paste(adresseSortie,"tmp.gds",sep="", collapse=NULL))
sample.id <- read.gdsn(index.gdsn(genofile, "sample.id"))

#Lecture fichier cluster
cluster.file = adresseSample
annotations = read.table(cluster.file, h=TRUE,na.strings=".")
clustering = c(annotations)

#------------------------------------------------------------------------
#Palette de couleurs
n <- length(sample.id)
qual.col.pals <- brewer.pal.info[brewer.pal.info$category == 'qual',]
col.vector <- unlist(mapply(brewer.pal, qual.col.pals$maxcolors, rownames(qual.col.pals)))[1:n]

#------------------------------------------------------------------------
#PCA
PCA <- snpgdsPCA(genofile, autosome.only=FALSE, remove.monosnp=TRUE, maf=NaN, missing.rate=NaN, eigen.cnt=0, sample.id=sample.id)
colnames(PCA$eigenvect)=PCA$varprop
rownames(PCA$eigenvect)=sample.id

#------------------------------------------------------------------------
#Plot
#Chaque point
pdf(paste(adresseSortie,"R_pca.pdf",sep="", collapse=NULL))
plot(x=PCA$eigenvect[,1], y=PCA$eigenvect[,2], main=paste("PCA (SNPRelate, no projection, ",length(PCA$snp.id)," SNPs)",sep=""), 
	xlab=paste("PC1 (",round(as.numeric(colnames(PCA$eigenvect)[1])*100,2),"%)",sep=""), 
        ylab=paste("PC2 (",round(as.numeric(colnames(PCA$eigenvect)[2])*100,2),"%)",sep=""),
        pch=0:25, col=col.vector)

legend("topright",legend = sample.id , pch=0:25, col=col.vector, ncol=2)

#Clustering
plot(x=PCA$eigenvect[,1], y=PCA$eigenvect[,2], main=paste("PCA (SNPRelate, no projection, ",length(PCA$snp.id)," SNPs) \n Clustering",sep=""), 
	xlab=paste("PC1 (",round(as.numeric(colnames(PCA$eigenvect)[1])*100,2),"%)",sep=""), 
       ylab=paste("PC2 (",round(as.numeric(colnames(PCA$eigenvect)[2])*100,2),"%)",sep=""),
      pch="o", col=as.integer(annotations$Groupe))
      
legend("topright",legend = levels(annotations$Groupe),pch="o", col=1:6, ncol=2)    
dev.off()

#------------------------------------------------------------------------
#Creation d'un tableau de sortie pour etude mais sous python 
tab <- data.frame(
    PCA1= PCA$eigenvect[,1],    # the first eigenvector
    PCA2 = PCA$eigenvect[,2],    # the second eigenvector
    stringsAsFactors = FALSE)

#on ecrit le tableau dans un fichier de sortie pour apres faire des graphiques en Python 
sink(paste(adresseSortie,"tabDonnees.txt",sep="", collapse=NULL))
tab
sink()

#------------------------------------------------------------------------
pop.level <- clustering$Groupe #levels(clustering)
#Arbre
ibs.hc <- snpgdsHCluster(snpgdsIBS(genofile, num.thread=2, autosome.only=FALSE))
rv <- snpgdsCutTree(ibs.hc, col.list=col.vector, samp.group=pop.level)
pdf(paste(adresseSortie,"R_arbre.pdf",sep="", collapse=NULL)) #, width=20)
plot(rv$dendrogram, main="Arbre selon IBS") #,horiz=T)
legend("topright",legend = levels(annotations$Groupe),col=col.vector,pch=19, ncol=2)  
 
dev.off()

snpgdsClose(genofile)
