#George Marchment + Clemence Sebe
#Script Analyse SNP
import os
import variables as v
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import arbreSNP as a
from ete3 import Tree, TreeStyle

#Functions that check if a 'name' is in a list
def appartient(tab, nom):
	for i in range (len(tab)):
		if tab[i][0] == nom:
			return True
	return False
def appartientBis(tab, nom):
	for i in range (len(tab)):
		if tab[i] == nom:
			return True
	return False

#Function that creates the Clusters and Trees
def mainAnalyseSNP(analyse):
	print("DEBUT SCRIPT ANALYSE SNP")
	lien = v.vcf + "SNP/POST_FILTRE/SNP_PASS.vcf"
	sortie = v.graphs + "SNP/"
	
	if analyse:
		#Start the PCA analyse using our R script 
		print("PCA avec R")
		cmd = "Rscript pca.R " + lien + " " + sortie + " " + v.sample
		os.system(cmd)
		#Removing tmp.gds
		os.remove(sortie + "tmp.gds")
		
		#Graphs with python
		print("Figure avec Python")
			
		#'Dark' color palette
		marquer = ['o', 's', 'p', '*', '1', 'D','P', 'X']
		colorNames = list(matplotlib.colors.cnames.keys())
		cmap =[]
		for i in range (len(colorNames)):
			if colorNames[i][0] == 'd':
				cmap.append(colorNames[i])
		cmap.append('aqua')
		cmap.append('brown')
		
		#Read and extract the tabDonnees.txt file to a dictionnary
		file = open(sortie + "tabDonnees.txt", 'r')
		line = file.readlines()
		sample = []
		dico = {}
		for i in range(1,len(line)):
			etude = line[i].split()
			sample.append(etude[0])
			dico.update({etude[0] : [float(etude[1]), float(etude[2])]})
		file.close()

		#Creating the clustering 
		file = open(v.sample ,'r')
		line = file.readlines()
		nomGroupe = []
		titre = []
		cluster = {}
		idx = 0
		for i in range(1,len(line)):
			etude = line[i].split()
			cluster.update({etude[0] : etude[1]})
			if not appartient(nomGroupe, etude[1]):
				nomGroupe.append([etude[1], idx])
				titre.append(etude[1])
				idx +=1
		file.close()

		#Function that returns the color referencing the the cluster name
		def whichCouleur (c):
			for i in range(len(nomGroupe)):
				if c == nomGroupe[i][0]:
					return nomGroupe[i][1]
			return "ERROR"

		#Writing the clusters to the graph (Clustering.png)
		fig, ax = plt.subplots()
		couleur = ["blue", "red", "yellow", "green", "pink", "purple"]
		marquer = ['o', 's', 'p', '*', 'H', 'D']
		dejaVu = []
		idx = 0
		for name in sample:
			idx = whichCouleur(cluster[name])
			if not appartientBis(dejaVu, cluster[name]):
				ax.scatter(dico[name][0], dico[name][1], color=couleur[idx], marker=marquer[idx%len(marquer)] ,label=cluster[name]) 
				dejaVu.append(cluster[name])
			else:
				ax.scatter(dico[name][0], dico[name][1], color=couleur[idx], marker=marquer[idx%len(marquer)])
		ax.legend()		
		ax.set_title("Clustering")
		plt.savefig(sortie +'Clustering.png')


		#Creating the two 'handmade' trees using the UPGMA and Neighbor Joining algorithms		
		#UPGMA
		newick_tree = a.UPGMA(a.read(sortie + "tabDonnees.txt"))  
		t = Tree(newick_tree)
		ts = TreeStyle()
		ts.show_branch_length = True
		t.render(sortie + "UPGMA_treeSNP.png", w=180, units="mm", tree_style=ts)
		#Neighbor Joining 
		newick_tree = a.neighbor_joining(a.read(sortie + "tabDonnees.txt"))
		t = Tree(newick_tree)
		ts = TreeStyle()
		ts.show_branch_length = True
		t.render(sortie + "NEIGHBOR_JOINING_treeSNP.png", w=180, units="mm", tree_style=ts)

	print("FIN SCRIPT ANALYSE SNP")
