#!/usr/bin/env Rscript
library(SNPRelate)
library(gdsfmt)
library(ape)
library(RColorBrewer)


#Script creating the graphs for the Filterd INDEL samples


#Retrieving Arguments given by the python script
#------------------------------------------------------------------------
args = commandArgs(trailingOnly=TRUE)  
entree = args[1]  #fichier sur lequel on travaille (adresse + nom)
adresseSortie = args[2] #adresee ou l'on veut que les fichiers crées soient sauvegardes
adresseSample = args[3]

#Reading the .vcf file and creating the files for the PCA
#------------------------------------------------------------------------
vcf.file =  entree
snpgdsVCF2GDS(vcf.file, paste(adresseSortie,"tmp.gds",sep="", collapse=NULL), method="biallelic.only")
genofile <- snpgdsOpen(paste(adresseSortie,"tmp.gds",sep="", collapse=NULL))
sample.id <- read.gdsn(index.gdsn(genofile, "sample.id"))

#Reading cluster file
#------------------------------------------------------------------------
cluster.file = adresseSample
annotations = read.table(cluster.file, h=TRUE,na.strings=".")
clustering = c(annotations)

#Color Pallet
#------------------------------------------------------------------------
n <- length(sample.id)
qual.col.pals <- brewer.pal.info[brewer.pal.info$category == 'qual',]
col.vector <- unlist(mapply(brewer.pal, qual.col.pals$maxcolors, rownames(qual.col.pals)))[1:n]

#PCA
#------------------------------------------------------------------------
PCA <- snpgdsPCA(genofile, autosome.only=FALSE, remove.monosnp=TRUE, maf=NaN, missing.rate=NaN, eigen.cnt=0, sample.id=sample.id)
colnames(PCA$eigenvect)=PCA$varprop
rownames(PCA$eigenvect)=sample.id

#Creating the R_pca.pdf file
#------------------------------------------------------------------------
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
      pch=as.integer(annotations$Groupe), col=as.integer(annotations$Groupe))
      
legend("topright",legend = levels(annotations$Groupe),pch=1:6, col=1:6, ncol=2)    
dev.off()

#Creating list du give back to the python script => we write it to tabDonnes.txt to be able to recuperate it later on
#------------------------------------------------------------------------
tab <- data.frame(
    PCA1= PCA$eigenvect[,1],    # the first eigenvector
    PCA2 = PCA$eigenvect[,2],    # the second eigenvector
    stringsAsFactors = FALSE)

sink(paste(adresseSortie,"tabDonnees.txt",sep="", collapse=NULL))
tab
sink()

#Creating the tree using snpgdsCutTree
#------------------------------------------------------------------------
pop.level <- clustering$Groupe #levels(clustering)
ibs.hc <- snpgdsHCluster(snpgdsIBS(genofile, num.thread=2, autosome.only=FALSE))
rv <- snpgdsCutTree(ibs.hc, col.list=col.vector, samp.group=pop.level)
pdf(paste(adresseSortie,"R_arbre.pdf",sep="", collapse=NULL)) #, width=20)
plot(rv$dendrogram, main="Arbre selon IBS") #,horiz=T)
legend("topright",legend = levels(annotations$Groupe),col=col.vector,pch=19, ncol=2)  
 
dev.off()

snpgdsClose(genofile)
