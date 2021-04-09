#George Marchment + Clemence Sebe
#Script Variables
import os

#Note:
#We decided to use a .py file instead of a .txt file since we are only two people working on the pipeline
#and there isn't (really) any sensitive information beeing shared, might add it later on

def initialize(): 
    global utilisateur 
    
    #------------------------ONLY VARIABLE TO CHANGE------------------------
    #-----------------------------------------------------------------------
    utilisateur= "clemence" #george or clemence
    #-----------------------------------------------------------------------
    #-----------------------------------------------------------------------
    
    #Address where the FASTQs will be downloaded
    global adresseTelechargement
    #Address where the BWA folder is situated
    global adresseBwa
    #Address where the "Donnees" (Data) folder is situated
    global donnees
    #Address to create database (For George it is on desktop since to write the database, we cannot use the usb stick)
    global adresseBDD
    #Address of the reference genome in relation to the BWA adress (variable declared just above: adresseBwa)
    global geneRef
    #Address of the gene folder reference
    global geneRefDossier
    #Address where the .sam files will be cretead in relation to the BWA adress (adresseBwa)
    global zipSam
    #Address where the .bam files pre MarkDuplicate will be created in relation to the BWA adress (adresseBwa)
    global bamRefPreMK
    #Address where the .bam files post MarkDuplicate will be created in relation to the BWA adress (adresseBwa)
    global bamRefPostMK
    #Temporary file adresses
    global fichTxt
    global simple
    #Address where the the .bam files are situated post MarkDuplicate
    global adressePostMk
    #Address where the .g.vcf files are situtates
    global adresseGVCF 
    #Adress where the .vcf files are situated
    global vcf
    #Adress where the graphs are situated 
    global graphs
    #Adress where the results are situated
    global results
    #Adress where the sample.txt file is situated
    global sample 
    
    #The assignment of the different variables (the adresses used on both machines)
    if utilisateur == "george":
        print("")
        print("L'utilisateur est George")
        print("")
        adresseTelechargement= "/media/george/USB2GM/Projet_BioInformatique/Donnees/FASTQ/"
        adresseBwa= "/home/george/Bureau/bwa/"
        donnees = "/media/george/USB2GM/Projet_BioInformatique/Donnees/" 
        adresseBDD = "/home/george/Bureau/" 
        geneRef= "../../../../media/george/USB2GM/Projet_BioInformatique/Donnees/Genome/S288C_reference_sequence_R64-2-1_20150113.fsa"
        geneRefDossier =  "/media/george/USB2GM/Projet_BioInformatique/Donnees/Genome/"  
        zipSam = "../../../../media/george/USB2GM/Projet_BioInformatique/Donnees/SAM/"
        bamRefPreMK= "../../../../media/george/USB2GM/Projet_BioInformatique/Donnees/BAM/BAM_PRE_MK/"
        bamRefPostMK= "../../../../media/george/USB2GM/Projet_BioInformatique/Donnees/BAM/BAM_POST_MK/"
        fichTxt = "/media/george/USB2GM/Projet_BioInformatique/Donnees/BAM/"
        simple = "/media/george/USB2GM/Projet_BioInformatique/"
        adressePostMk = "/media/george/USB2GM/Projet_BioInformatique/Donnees/BAM/BAM_POST_MK/"  
        adresseGVCF = "/media/george/USB2GM/Projet_BioInformatique/Donnees/GVCF/"  
        graphs= "/media/george/USB2GM/Projet_BioInformatique/Results/Graphs/"
        results= "/media/george/USB2GM/Projet_BioInformatique/Results/"
        vcf= "/media/george/USB2GM/Projet_BioInformatique/Donnees/VCF/" 
        sample = "/media/george/USB2GM/Projet_BioInformatique/Donnees/sample.txt"
        
    elif utilisateur == "clemence":
    	#Je travaille totalement sur mon ordinateur :
    	#Uniquement besoin d'une variable qui me situe dans mon bon repertoire et les autres découle de celle-ci
        print("")
        print("L'utilisateur est Clémence")
        print("")
        simple = "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/"
        donnees =  simple + "Donnees/"
        adresseBDD = donnees
        adresseTelechargement = simple + "Donnees/FASTQ/" 
        adresseBwa = simple + "bwa/"
        geneRef = "../Donnees/Genome/S288C_reference_sequence_R64-2-1_20150113.fsa"
        geneRefDossier = simple + "Donnees/Genome/"
        zipSam =  "../Donnees/SAM/"
        bamRefPreMK = "../Donnees/BAM/BAM_PRE_MK/"
        bamRefPostMK = "../Donnees/BAM/BAM_POST_MK/"
        fichTxt = simple + "Donnees/BAM/"
        adressePostMk = simple + "Donnees/BAM/BAM_POST_MK/"
        adresseGVCF = simple + "Donnees/GVCF/"
        results = simple + "Results/"
        graphs = simple + "Results/Graphs/"
        vcf = simple + "Donnees/VCF/"
        sample = simple + "Donnees/sample.txt"
        

    else:               
        os.exit()
