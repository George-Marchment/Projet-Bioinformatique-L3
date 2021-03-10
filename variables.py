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
    utilisateur= "george" #george or clemence
    #-----------------------------------------------------------------------
    #-----------------------------------------------------------------------
    
    #Address where the FASTQs will be downloaded
    global adresseTelechargement
    #Address where the BWA folder is situated
    global adresseBwa
    
    global donnees
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
    
    # a faire 
    global adressePostMk
    global adresseGVCF 
    global image
    
    global vcf
    global graphs
    global results
    
    #The assignment of the different variables (the adresses used on both machines)
    if utilisateur == "george":
        print("")
        print("L'utilsateur est George")
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
        
        #inutile
        image = "/media/george/USB2GM/Projet_BioInformatique/Images"
        
        #Nouveau
        graphs= "/media/george/USB2GM/Projet_BioInformatique/Results/Graphs/"
        results= "/media/george/USB2GM/Projet_BioInformatique/Results/"
        vcf= "/media/george/USB2GM/Projet_BioInformatique/Donnees/VCF/" 
        
    elif utilisateur == "clemence":
        print("")
        print("L'utilsateur est Clémence")
        print("")
        simple = "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/"
        donnees = "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Donnees/"
        adresseBDD = donnees
        adresseTelechargement= "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Donnees/FASTQ/" 
        adresseBwa= "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/bwa/"
        geneRef= "../Donnees/Genome/S288C_reference_sequence_R64-2-1_20150113.fsa"
        geneRefDossier= "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Donnees/Genome/"
        zipSam =  "../Donnees/SAM/"
        bamRefPreMK= "../Donnees/BAM/BAM_PRE_MK/"
        bamRefPostMK= "../Donnees/BAM/BAM_POST_MK/"
        fichTxt = "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Donnees/BAM/"
        adressePostMk = "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Donnees/BAM/BAM_POST_MK/"
        adresseGVCF = "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Donnees/GVCF/"
        
        #Inutile
        
        #Nouvea => A VERIFIER 
        graphs= "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Results/Graphs/"
        results= "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Results/"
        vcf= "/home/clemence/data/L3/S6/Projet-Bioinformatique-L3/Donnees/VCF/"
        
        

    else:               
        os.exit()
