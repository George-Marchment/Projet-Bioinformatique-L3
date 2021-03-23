#R script pour faire des distributions
#!/usr/bin/env Rscript
library(lattice)
library(VennDiagram)



args = commandArgs(trailingOnly=TRUE)   #la liste des arguments donc arg1  arg2 et arg3
entree= args[1]
adresse = args[2]

qd=args[3]
mq=args[4]
mqRankSumInf=args[5]
mqRankSumSup=args[6]
readPosRankSumInf=args[7]
readPosRankSumSup=args[8]
sor=args[9]

sym_qd=args[10]
sym_mq=args[11]
sym_mqRankSumInf=args[12]
sym_mqRankSumSup=args[13]
sym_readPosRankSumInf=args[14]
sym_readPosRankSumSup=args[15]
sym_sor=args[16]

# LECTURE DU FICHIER
annot.file = entree
annotations = read.table(annot.file, h=TRUE,na.strings=".")


#On doit changer le sens des inégalités car ds l'un on veut enlever les donnees supérieures mais 
#maintenant on regarde les valeurs qu'on a obtenu - A revoir niveau francais
compare <- function(a, symbol, b){
if(symbol=='<'){
    return (a>=b)
}
if(symbol=='>'){
    return (a<=b)
}
}

# INITIALISATION DES SEUILS
lim.QD = qd
lim.MQ = mq
lim.MQRankSumInf = mqRankSumInf
lim.MQRankSumSup = mqRankSumSup
lim.ReadPosRankSumInf = readPosRankSumInf
lim.ReadPosRankSumSup = readPosRankSumSup
lim.SOR = sor

# CREATION DES FIGURES
pdf(paste(adresse, "FiltresSNP.pdf", sep = "", collapse=NULL))

## FIGURE DE QD
  prop.QD=length( which(compare(annotations$QD, sym_qd ,lim.QD))) / nrow(annotations)
   plot(density(annotations$QD,na.rm=T),main="QD", sub = paste(paste("Filtre: QD ", sym_qd, sep = "", collapse=NULL),lim.QD,"( = ", signif(prop.QD,3),"% des SNP) " ,sep="") ) 
   abline(v=lim.QD, col="red")

## FIGURE DE MQ
   prop.MQ=length( which(compare(annotations$MQ, sym_mq ,lim.MQ))) / nrow(annotations)
  plot(density(annotations$MQ,na.rm=T),main="MQ", sub = paste(paste("Filtre: MQ ", sym_mq, sep = "", collapse=NULL),lim.MQ,"( = ", signif(prop.MQ,3),"% des SNP) " ,sep="") ) 
  abline(v=lim.MQ, col="red")

## FIGURE DE MQRankSum
# prop.MQRankSum=length( which(compare(annotations$MQRankSum, sym_mqRankSum ,lim.MQRankSum))) / nrow(annotations)
 #plot(density(annotations$MQRankSum,na.rm=T),main="MQRankSum", sub = paste(paste("Filtre: MQRankSum ", sym_mqRankSum, sep = "", collapse=NULL),lim.MQRankSum,"( = ", signif(prop.MQRankSum,3),"% des SNP) " ,sep="") ) 
  #abline(v=lim.MQRankSum, col="red")

## FIGURE DE ReadPosRankSum
  #prop.ReadPosRankSum=length( which(compare(annotations$ReadPosRankSum, sym_readPosRankSum ,lim.ReadPosRankSum))) / nrow(annotations)
 #plot(density(annotations$ReadPosRankSum,na.rm=T),main="ReadPosRankSum", sub = paste(paste("Filtre: ReadPosRankSum ", sym_readPosRankSum, sep = "", collapse=NULL),lim.ReadPosRankSum,"( = ", signif(prop.ReadPosRankSum,3),"% des SNP) " ,sep="") ) 
  #abline(v=lim.ReadPosRankSum, col="red")

## FIGURE DE SOR
  prop.SOR=length( which(compare(annotations$SOR, sym_sor ,lim.SOR))) / nrow(annotations)
   plot(density(annotations$SOR,na.rm=T),main="SOR", sub = paste(paste("Filtre: SOR ", sym_sor, sep = "", collapse=NULL),lim.SOR,"( = ", signif(prop.SOR,3),"% des SNP) " ,sep="") ) 
  abline(v=lim.SOR, col="red")

 dev.off()


# DIAGRAMME DE VENN
qd.pass = which(compare(annotations$QD, sym_qd ,lim.QD))
sor.pass = which(compare(annotations$SOR, sym_sor ,lim.SOR))
mq.pass = which(compare(annotations$MQ, sym_mq ,lim.MQ))
mqrs.pass= which(compare(annotations$MQRankSum, sym_mqRankSumInf ,lim.MQRankSumInf) & compare(annotations$MQRankSum, sym_mqRankSumSup,lim.MQRankSumSup))
rprs.pass= which(compare(annotations$ReadPosRankSum, sym_readPosRankSumInf ,lim.ReadPosRankSumInf) & compare(annotations$ReadPosRankSum, sym_readPosRankSumSup ,lim.ReadPosRankSumSup))

venn.diagram(
  x=list(qd.pass,mq.pass,sor.pass,mqrs.pass,rprs.pass ),  #,fs.pass
  category.names = c("QD", "MQ", "SOR","MQRanksSum", "ReadPosRankSum"), # "ReadPosRankSum"
  fill = c("blue","darkgreen","orange","yellow","red"), #,"purple"
  output=TRUE,
  filename = paste(adresse, "DiagrammeVennSNP", sep = "", collapse=NULL)
  )

