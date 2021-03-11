#R script pour faire des distributions
#!/usr/bin/env Rscript
library(lattice)

args = commandArgs(trailingOnly=TRUE)  
entree= args[1]
sortie = args[2]

# LECTURE DU FICHIER
annot.file = entree
annotations = read.table(annot.file, h=TRUE,na.strings=".")

## FIGURE COURBE
pdf(paste(sortie, "courbe.pdf", sep = "", collapse=NULL))
plot(density(annotations$QD,na.rm=T),main="QD", sub = " QD " ) 
plot(density(annotations$FS,na.rm=T),main="FS", sub = " FS " ) 
plot(density(annotations$MQ,na.rm=T),main="MQ", sub = " MQ " ) 
plot(density(annotations$MQRankSum,na.rm=T),main="MQRankSum", sub = " MQRankSum " ) 
plot(density(annotations$ReadPosRankSum,na.rm=T),main="ReadPosRankSum", sub = " ReadPosRankSum " ) 
plot(density(annotations$SOR,na.rm=T),main="SOR", sub = " SOR " ) 

##FIGURE HISTOGRAMME
pdf(paste(sortie,"histogramme.pdf", sep = "", collapse=NULL))
hist(annotations$QD, breaks = 20, main= "QD", col = "steelblue")
hist(annotations$FS, breaks = 20, main= "FS", col = "steelblue")
hist(annotations$MQ, breaks = 20, main= "MQ", col = "steelblue")
hist(annotations$MQRankSum, breaks = 20, main= "MQRankSum", col = "steelblue")
hist(annotations$ReadPosRankSum, breaks = 20,main= "ReadPosRankSum", col = "steelblue")
hist(annotations$SOR, breaks = 20, main= "SOR", col = "steelblue")

##ECART TYPE "BOITE"
pdf(paste(sortie,"repartition.pdf", sep = "", collapse=NULL))
boxplot(annotations$QD, range=0, main= "QD", horizontal=TRUE)
boxplot(annotations$FS, range=0, main= "FS", horizontal=TRUE)
boxplot(annotations$MQ, range=0, main= "MQ", horizontal=TRUE)
boxplot(annotations$MQRankSum, range=0, main= "MQRankSum", horizontal=TRUE)
boxplot(annotations$ReadPosRankSum, range=0, main= "ReadPosRankSum", horizontal=TRUE)
boxplot(annotations$SOR, range=0, main= "SOR", horizontal=TRUE)

#Autre donnee
fichier <- file(paste(sortie,"autreInfo.txt", sep = "", collapse=NULL), open="w")

val <- "QD :"
writeLines(val, con = fichier)
val <- paste("Moyenne : ", mean(annotations$QD,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Mediane : ", median(annotations$QD,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Maximum : ", max(annotations$QD,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Minimum : ", min(annotations$QD,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Ecart-type : ", sd(annotations$QD,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- " "
writeLines(val, con = fichier)

val <- "FS :"
writeLines(val, con = fichier)
val <- paste("Moyenne : ", mean(annotations$FS,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Mediane : ", median(annotations$FS,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Maximum : ", max(annotations$FS,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Minimum : ", min(annotations$FS,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Ecart-type : ", sd(annotations$FS,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- " "
writeLines(val, con = fichier)

val <- "MQ :"
writeLines(val, con = fichier)
val <- paste("Moyenne : ", mean(annotations$MQ,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Mediane : ", median(annotations$MQ,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Maximum : ", max(annotations$MQ,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Minimum : ", min(annotations$MQ,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Ecart-type : ", sd(annotations$MQ,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- " "
writeLines(val, con = fichier)

val <- "MQRankSum :"
writeLines(val, con = fichier)
val <- paste("Moyenne : ", mean(annotations$MQRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Mediane : ", median(annotations$MQRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Maximum : ", max(annotations$MQRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Minimum : ", min(annotations$MQRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Ecart-type : ", sd(annotations$MQRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- " "
writeLines(val, con = fichier)

val <- "ReadPosRankSum :"
writeLines(val, con = fichier)
val <- paste("Moyenne : ", mean(annotations$ReadPosRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Mediane : ", median(annotations$ReadPosRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Maximum : ", max(annotations$ReadPosRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Minimum : ", min(annotations$ReadPosRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Ecart-type : ", sd(annotations$ReadPosRankSum,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- " "
writeLines(val, con = fichier)

val <- "SOR :"
writeLines(val, con = fichier)
val <- paste("Moyenne : ", mean(annotations$SOR,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Mediane : ", median(annotations$SOR,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Maximum : ", max(annotations$SOR,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Minimum : ", min(annotations$SOR,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- paste("Ecart-type : ", sd(annotations$SOR,na.rm=T), sep ="", collapse=NULL)
writeLines(val, con = fichier)
val <- " "
writeLines(val, con = fichier)

close(fichier)
