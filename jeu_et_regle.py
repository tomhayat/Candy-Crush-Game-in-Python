# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 10:39:52 2015

@author: tom
"""

import random


class elem_grille:
    def __init__(self):
        self.type = random.randint(1, 7)
    def __str__(self):
        return str(self.type)     
    def __repr__(self):
        return '{}'.format(self.type)
    def __eq__(self,x):
        return (self.type == x)
  
        

class GrilleJeu():    
    def __init__(self):
        # On veut une grille sans match3      
        grid_bool = True
        while grid_bool:
            self.grille = [[elem_grille() for j in range(7)] for i in range(7)]    
            self.visited = [[0 for j in range(len(self.grille))] 
                            for i in range(len(self.grille))]
            grid_bool = self.initGrille()
        self.score = 0
        self.moves = 0
    
    def initGrille(self):
        for i in range(len(self.grille)):
            for j in range(len(self.grille)):
                self.visited_refill()                
                self.flood(i, j, self.get_item(i, j))
                if self.match3(i, j):
                    return True
    
        
    def visited_refill(self):
        self.visited = [[0 for j in range(len(self.visited))] 
                            for i in range(len(self.visited))]
    
       
    def match3 (self, i, j):
        # Permet de controler quon a au moins 3 balles de la meme couleur 
        sumi = 0
        sumj = 0
        for p in range(len(self.visited)):
            sumi = sumi + self.visited[i][p]
            sumj = sumj + self.visited[p][j]
        return( sumi > 2 or sumj > 2)
        
        
    def __str__(self):
        s = ""
        for  elem in self.grille:
            s = s +"\n" + str(elem)
        return s           
    
    def __repr__(self):
        print(str(self.grille))
    
    def get_item(self, i, j):
        if( 0 <= i and i < len(self.grille) and 
            0 <= j and j < len(self.grille)):       
                return self.grille[i][j].type
    
    def set_item(self, i, j, x):
        self.grille[i][j].type = x
        
    def invert(self, i, j, k, l):
        # intervertie la position de 2 balles
        if (abs(i - k)+ abs(j - l) == 1 ): # si la norme1 vaut 1
            temp = self.get_item(i, j)         
            self.set_item(i, j, self.get_item(k, l))
            self.set_item(k, l, temp)
            
    def flood(self, i, j,ref):
        # algorithme de diffusion pour voir les voisins ayant la meme couleur
        if ((0 <= i) and (i < 7) and (0 <= j) and (j < 7)):
            if  ((self.get_item(i, j) == ref) and 
                (self.visited[i][j] == 0)):
                self.visited[i][j] = 1;
                self.flood(i+1, j, ref)
                self.flood(i-1, j, ref)
                self.flood(i, j+1, ref)
                self.flood(i, j-1, ref)    
    
   
    def action(self, i, j):
        # action lors d un mouvement        
        self.visited_refill()                
        self.flood(i,j,self.get_item(i, j))        
        score = 0        
        if (self.match3(i, j)):
            for y in range(len(self.visited)):
                if self.detect_0(y):                   
                    count = self.number_0_column(y)                
                    if (count[1] > 0):                    
                        for x in reversed(range(count[1])):
                            self.set_item(x + count[0], y, self.get_item(x, y))
                            self.set_item(x, y, random.randint(1, 7))
                            score += 1
                    else:
                        for x in range(count[0]):
                            self.set_item(x, y, random.randint(1, 7))
                            score += 1
        return score

    
    
    def detect_0(self, y):
        # detecte sil y a une case a enlever
        for x in range(len(self.visited)):
            if (self.visited[x][y] == 1):
                    return True
        else:
            return False
    
    def number_0_column(self, y):
        #detecte sil y a le nb de cases a enlever et la premiere
        count = [0, 7]       
        for x in range(len(self.visited)):
            if (self.visited[x][y] == 1):
                count = [count[0] + 1, min(count[1], x)]
        return count
    
       
    def move(self, i, j, k, l):
        # mouvement lors dune action        
        if (self.moves < 20):        
            self.invert(i, j, k, l)
            index = [i, j, k, l]
            self.score += (self.action(index[0], index[1]))**2
            ij = self.match3(index[0], index[1])
            self.score += (self.action(index[2], index[3]))**2
            kl = self.match3(index[2], index[3])
            if (ij == False and kl == False):
                self.invert(i, j, k, l)
                self.moves += -1 
            self.visited_refill() 
            self.moves += 1 
            self.score += (self.combo())**2
    
    def combo(self):
        grid_bool = self.initGrille()
        count = 0
        score = 0
        while grid_bool:
            for i in range(len(self.grille)):
                for j in range(len(self.grille)):
                    k = self.action(i, j)
                    if k > 0:
                        count += 1
                        k = count*k
                        score += k        
            grid_bool = self.initGrille()
        return score

