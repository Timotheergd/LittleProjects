#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import sqrt
import pygame
pygame.init()

class Noeud:
    def __init__(self, x_, y_, parent_=None):
        self.x = x_
        self.y = y_
        self.parent = parent_

    def __repr__(self):
        return "Noeud:("+str(self.x)+","+str(self.y)+")"
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.x == other.x and self.y == other.y

    def getParent(self):
        return self.parent
    
    def setParent(self, parent_):
        self.parent = parent_

def h(n, goal): # distance estimée d'un nœud i au nœud d'arrivée
    return sqrt((n.x-goal.x)**2+(n.y-goal.y)**2)

def g(n, start, d=0): # distance réelle d'un nœud i au nœud de départ
    if n == start:
        return d
    return g(n.getParent(), start, d+1)

def f(n, start, goal): # somme des distances h(i) et g(i)
    return h(n, goal) + g(n, start)

def min(n1, n2, start, goal):
    if f(n1, start, goal)<f(n2, start, goal):
        return n1
    else:
        return n2

def AStar(start, goal, grid):
    open = [] # liste des nœuds à traiter
    closed = [] # liste des nœuds traités
    N = 0 # Nombre de noeuds à traiter

    open.append(start)
    grid[start.x][start.y] = 1
    while(len(open)>0):
        gprint()
        n_min=start
        for n in open:
            n_min = min(n, n_min, start, goal)
        if n_min in open:
            open.remove(n_min)
            grid[n_min.x][n_min.y] = 0
        if n_min == goal:
            return n_min
        else:
            closed.append(n_min)
        
        successeurs = []

        print("yep"*10)

        # for i in range(n_min.x-1, n_min.x+1+1):
        #     for j in range(n_min.y-1, n_min.y+1+1):
        #         if i == n_min.x and j == n_min.y:
        #             continue
        for (i,j) in [(n_min.x, n_min.y-1), (n_min.x, n_min.y+1), (n_min.x-1, n_min.y), (n_min.x+1, n_min.y)]:
            try:
                print(i, j)
                if grid[i][j] == 0:
                    successeurs.append(Noeud(i, j, n))
            except IndexError:
                print("indexError", n_min, i, j)
            except:
                print("autre erreur")

        for n in successeurs:
            heuristique = h(n, goal)
            G_tmp = g(n, start)+1
            F_tmp = G_tmp+heuristique

            # for nopen in open:
            #     if n == nopen and f(n, start, goal)>f(nopen, start, goal):
            #         continue # passer au point suvant. Break ???

            # for nclosed in closed:
            #     if n == nclosed and f(n, start, goal)>f(nclosed, start, goal):
            #         continue # passer au point suvant. Break ???

            for nopen in open:
                if n == nopen:
                    oheuristique = h(nopen, goal)
                    oG_tmp = g(nopen, start)+1
                    oF_tmp = oG_tmp+oheuristique
                    if F_tmp>oF_tmp:
                        continue # passer au point suvant. Break ???

            for nclosed in closed:
                cheuristique = h(nclosed, goal)
                cG_tmp = g(nclosed, start)+1
                cF_tmp = cG_tmp+cheuristique
                if n == nclosed and F_tmp<cF_tmp:
                    continue # passer au point suvant. Break ???

            n.setParent(n_min)

            if n in open:
                open.remove(n)
                grid[n.x][n.y] = 0

            if n in closed:
                closed.remove(n)

            open.append(n)
            grid[n.x][n.y] = 1

        closed.append(n_min)

def backpath(n, path=[]):
    print("back")
    if n.getParent() == None:
        return path+[(n.x, n.y)]
    return backpath(n.getParent(), path+[(n.x, n.y)])



grid = [[0]*10 for i in range(10)]

def gprint():
    for line in grid:
        print(line)


start = Noeud(1,1)
goal = Noeud(9,9)

path = backpath(AStar(start, goal, grid))[::-1]

print(path)

for i,j in path:
    grid[i][j] = 2

gprint()
