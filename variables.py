import os

def initialize(): 
    global utilisateur 
    
    #------------------------SEUL VARIABLE A CHANGER------------------------
    #-----------------------------------------------------------------------
    utilisateur= "george" #george ou clemence
    #-----------------------------------------------------------------------
    #-----------------------------------------------------------------------
    
    global adresseTelechargement
    global adresseBwa
    global geneRef
    global samRef
    global zipSam
    global bamRef
    global fichTxt
    global simple
    
    if utilisateur == "george":
        print("")
        print("L'utilsateur est George")
        print("")
        simple = "/media/george/USB2GM/Projet_BioInformatique/"
        adresseTelechargement= "/media/george/USB2GM/Projet_BioInformatique/Données"
        adresseBwa= "/home/george/Bureau/bwa/"
        geneRef= "../../../../media/george/USB2GM/Projet_BioInformatique/Données/Genome/S288C_reference_sequence_R64-2-1_20150113.fsa"
        samRef= "../../../../media/george/USB2GM/Projet_BioInformatique/Données/"
        zipSam = samRef
        bamRef = samRef
        fichTxt = samRef
        
    elif utilisateur == "clemence":
        print("")
        print("L'utilsateur est Clémence")
        print("")
        simple = "/home/clemence/L3/S6/Projet-Bioinformatique-L3/"
        adresseTelechargement= "/home/clemence/L3/S6/Projet-Bioinformatique-L3/Donnees/" 
        adresseBwa= "/home/clemence/L3/S6/Projet-Bioinformatique-L3/bwa/"
        geneRef= "../Donnees/Genome/S288C_reference_sequence_R64-2-1_20150113.fsa"
        samRef= "../Donnees/"
        zipSam =  "../Donnees/SamRef/"
        bamRef = "../Donnees/FichierBam/"
        fichTxt = "/home/clemence/L3/S6/Projet-Bioinformatique-L3/Donnees/FichierBam/"
        
    else:               
        os.exit()
