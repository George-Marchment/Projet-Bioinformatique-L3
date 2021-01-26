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
    
    if utilisateur == "george":
        print("")
        print("L'utilsateur est George")
        print("")
        adresseTelechargement= "/media/george/USB2GM/Projet_BioInformatique/Données"
        adresseBwa= "/home/george/Bureau/bwa/"
        geneRef= "../../../../media/george/USB2GM/Projet_BioInformatique/Données/Genome/S288C_reference_sequence_R64-2-1_20150113.fsa"
        samRef= "../../../../media/george/USB2GM/Projet_BioInformatique/Données/"
        
    elif utilisateur == "clemence":
        print("")
        print("L'utilsateur est Clémence")
        print("")
        adresseTelechargement= "/home/clemence/L3/S6/ProjetBioInformatique/Projet-Bioinformatique-L3/Donnees/" 
        adresseBwa= adresseTelechargement + "bwa/"
        geneRef= "../Donnees/Genome/S288C_reference_sequence_R64-2-1_20150113.fsa"
        samRef= "../Donnees/"
        
    else:
        os.exit()