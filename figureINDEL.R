#R script pour faire des distributions
#!/usr/bin/env Rscript
library(lattice)
library(VennDiagram)


args = commandArgs(trailingOnly=TRUE)   #la liste des arguments donc arg1  arg2 et arg3
entree= args[1]
adresse = args[2]
qd=args[3]
fs=args[4]
mq=args[5]
mqRankSum=args[6]
readPosRankSum=args[7]
sor=args[8]

sym_qd=args[9]
sym_fs=args[10]
sym_mq=args[11]
sym_mqRankSum=args[12]
sym_readPosRankSum=args[13]
sym_sor=args[14]

# LECTURE DU FICHIER
annot.file = entree
annotations = read.table(annot.file, h=TRUE,na.strings=".")


# INITIALISATION DES SEUILS
lim.QD = qd
lim.FS = fs
lim.MQ = mq
lim.MQRankSum = mqRankSum
lim.ReadPosRankSum = readPosRankSum
lim.SOR = sor

compare <- function(a, symbol, b){
if(symbol=='<'){
    return (a<b)
}
if(symbol=='>'){
    return (a>b)
}
if(symbol=='<='){
    return (a<=b)
}
if(symbol=='>='){
    return (a>=b)
}
}


# CREATION DES FIGURES
pdf(paste(adresse, "FiltresINDEL.pdf", sep = "", collapse=NULL))

## FIGURE DE QD
  prop.QD=length( which(compare(annotations$QD, sym_qd ,lim.QD))) / nrow(annotations)
  plot(density(annotations$QD,na.rm=T),main="QD", sub = paste(paste("Filtre: QD ", sym_qd, sep = "", collapse=NULL),lim.QD,"( = ", signif(prop.QD,3),"% des INDEL) " ,sep="") ) 
  abline(v=lim.QD, col="red")

## FIGURE DE FS
  prop.FS=length( which(compare(annotations$FS, sym_fs ,lim.FS))) / nrow(annotations)
  plot(density(annotations$FS,na.rm=T),main="FS", sub = paste(paste("Filtre: FS ", sym_fs, sep = "", collapse=NULL),lim.FS,"( = ", signif(prop.FS,3),"% des INDEL) " ,sep="") ) 
  abline(v=lim.FS, col="red")

## FIGURE DE MQ
  prop.MQ=length( which(compare(annotations$MQ, sym_mq ,lim.MQ))) / nrow(annotations)
  plot(density(annotations$MQ,na.rm=T),main="MQ", sub = paste(paste("Filtre: MQ ", sym_mq, sep = "", collapse=NULL),lim.MQ,"( = ", signif(prop.MQ,3),"% des INDEL) " ,sep="") ) 
  abline(v=lim.MQ, col="red")

## FIGURE DE MQRankSum
  prop.MQRankSum=length( which(compare(annotations$MQRankSum, sym_mqRankSum ,lim.MQRankSum))) / nrow(annotations)
  plot(density(annotations$MQRankSum,na.rm=T),main="MQRankSum", sub = paste(paste("Filtre: MQRankSum ", sym_mqRankSum, sep = "", collapse=NULL),lim.MQRankSum,"( = ", signif(prop.MQRankSum,3),"% des INDEL) " ,sep="") ) 
  abline(v=lim.MQRankSum, col="red")

## FIGURE DE ReadPosRankSum
  prop.ReadPosRankSum=length( which(compare(annotations$ReadPosRankSum, sym_readPosRankSum ,lim.ReadPosRankSum))) / nrow(annotations)
  plot(density(annotations$ReadPosRankSum,na.rm=T),main="ReadPosRankSum", sub = paste(paste("Filtre: ReadPosRankSum ", sym_readPosRankSum, sep = "", collapse=NULL),lim.ReadPosRankSum,"( = ", signif(prop.ReadPosRankSum,3),"% des INDEL) " ,sep="") ) 
  abline(v=lim.ReadPosRankSum, col="red")

## FIGURE DE SOR
  prop.SOR=length( which(compare(annotations$SOR, sym_sor ,lim.SOR))) / nrow(annotations)
  plot(density(annotations$SOR,na.rm=T),main="SOR", sub = paste(paste("Filtre: SOR ", sym_sor, sep = "", collapse=NULL),lim.SOR,"( = ", signif(prop.SOR,3),"% des INDEL) " ,sep="") ) 
  abline(v=lim.SOR, col="red")

dev.off()

#'QD < "+str(qd)+ " || FS < "+str(fs)+" || MQ < "+str(mq)+" || MQRankSum < "+str(mqRankSum)+" || ReadPosRankSum >= "+str(readPosRankSum)+" || SOR < "+str(sor)'



# DIAGRAMME DE VENN
qd.pass = which(compare(annotations$QD, sym_qd ,lim.QD))
fs.pass = which(compare(annotations$FS, sym_fs ,lim.FS))
sor.pass = which(compare(annotations$SOR, sym_sor ,lim.SOR))
mq.pass = which(compare(annotations$MQ, sym_mq ,lim.MQ))
mqrs.pass= which(compare(annotations$MQRankSum, sym_mqRankSum ,lim.MQRankSum))
rprs.pass= which(compare(annotations$ReadPosRankSum, sym_readPosRankSum ,lim.ReadPosRankSum))

venn.diagram(
  x=list(qd.pass, fs.pass,mq.pass,sor.pass),  #,mqrs.pass,rprs.pass
  category.names = c("QD" , "FS" , "MQ", "SOR"), #,"MQRanksSum", "ReadPosRankSum"
  fill = c("blue","darkgreen","orange","yellow"), #,"red","purple"
  output=TRUE,
  filename = paste(adresse, "DiagrammeVennINDEL", sep = "", collapse=NULL)
  )

