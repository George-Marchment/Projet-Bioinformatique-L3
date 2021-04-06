#George Marchment + Clemence Sebe
#Script Analyse SNP
import os
import variables as v
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import arbreSNP as a
from ete3 import Tree, TreeStyle

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

def mainAnalyseSNP(analyse):
	print("DEBUT SCRIPT ANALYSE SNP")
	lien = v.vcf + "SNP/POST_FILTRE/SNP_PASS.vcf"
	sortie = v.graphs + "SNP/"
	
	if analyse:
		# R
		print("PCA avec R")
		cmd = "Rscript pca.R " + lien + " " + sortie
		os.system(cmd)
		os.remove(sortie + "tmp.gds")
		
		#Figure avec python
		print("Figure avec Python")
			
		#Pallette de couleur "foncee"
		marquer = ['o', 's', 'p', '*', '1', 'D','P', 'X']
		colorNames = list(matplotlib.colors.cnames.keys())
		cmap =[]
		for i in range (len(colorNames)):
			if colorNames[i][0] == 'd':
				cmap.append(colorNames[i])
		cmap.append('aqua')
		cmap.append('brown')
		
		#Lecture fichier
		file = open(sortie + "tabDonnees.txt", 'r')
		line = file.readlines()
		sample = []
		dico = {}
		for i in range(1,len(line)):
			etude = line[i].split()
			sample.append(etude[0])
			dico.update({etude[0] : [float(etude[1]), float(etude[2])]})
		file.close()

		"""
		#Premiere image non zoomee
		fig, ax = plt.subplots(figsize=(7, 8))
		idx =0
		for name in sample:
			ax.scatter(dico[name][0], dico[name][1], label=name, color= cmap[idx], marker=marquer[idx%len(marquer)])
			idx += 1
		ax.legend()
		ax.set_title("PCA")
		plt.savefig(sortie +'PcaNonZoomee.png')

		#Teste image non zoommee annote
		fig, ax = plt.subplots(figsize=(5, 5)) 
		for name in sample:  
			ax.scatter(dico[name][0], dico[name][1], s=100, alpha=0.5,linewidths=1, color='blue')  
			ax.annotate(name,xy=(dico[name][0], dico[name][1])) 
		ax.set_title("PCA")
		plt.savefig(sortie +'PcaNonZoomeeAnnote.png')
		"""

		#Cluster 
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
		def whichCouleur (c):
			for i in range(len(nomGroupe)):
				if c == nomGroupe[i][0]:
					return nomGroupe[i][1]
			return "ERROR"
			
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
			
		#Arbre de distance
		#On applique l'algo sur nos donnees
		#UPGMA
		arbre = a.UPGMA(a.read(sortie + "tabDonnees.txt"))   
		
		#Affichage 
		newick_tree = arbre
		t = Tree(newick_tree)
		ts = TreeStyle()
		ts.show_branch_length = True
		t.render(sortie + "UPGMA_treeSNP.png", w=180, units="mm", tree_style=ts)
		
		#Autre arbre - autre méthode
		#neighbor_joining
		arbre = a.neighbor_joining(a.read(sortie + "tabDonnees.txt"))   
		
		#Affichage 
		newick_tree = arbre
		t = Tree(newick_tree)
		ts = TreeStyle()
		ts.show_branch_length = True
		t.render(sortie + "NEIGHBOR_JOINING_treeSNP.png", w=180, units="mm", tree_style=ts)

	print("FIN SCRIPT ANALYSE SNP")
