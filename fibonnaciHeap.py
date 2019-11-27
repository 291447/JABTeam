# -*- coding: utf-8 -*-

import math

# Klasa pojedyncze drzewo
class Tree:
    def __init__(self, key):
        self.key = key                                  #key - tablica[wartosc f, id wierzcholka] 
        self.children = []
        self.degree = 0		
    
    #łączenie drzew
    def append(self, deg):
        self.children.append(deg)
        self.degree = self.degree + 1

#Kopiec Fibonacciego        
class FibonacciHeap:
    def __init__(self):
        self.trees = []
        self.least = None
        self.count = 0
            
    #zwraca najmniejszy element kopca     
    def get_min(self):
        return self.least.key        

    #dodanie elementu do kopca    
    def insert(self, key):
        sprout = Tree(key)                                   #stwórz drzewo stopnia 0 o podanym kluczu
        self.trees.append(sprout)                            #dodaj drzewo do kopca
        if (self.least is None or key[0] < self.least.key[0]):     #oznacz najmniejszą wartosć w kopcu 
            self.least = sprout                           
        self.count = self.count + 1                          #zwiększ zmienną "rozmiar" o 1

    
    def extract_min(self):
        sprig = self.least                                   #najmniejsze drzewko
        for child in sprig.children:                         #dodaj dzieci usuwanego drzewa do drzew kopca
            self.trees.append(child)
            
        self.trees.remove(sprig)                             #usuń drzewo z kopca
        self.least = self.trees[0]  
        self.reorder()                                       #przekształć kopiec
        self.count = self.count - 1                          #zmniejsz rozmiar o 1
        
        return sprig.key
    
    #przekształcenie kopca
    def reorder(self):
        A = int((math.floor(math.frexp(self.count)[1])+1))*[None]
        while self.trees != []:
            x = self.trees[0]
            degree = x.degree
            self.trees.remove(x)
            while A[degree] is not None:
                y = A[degree]
                if x.key[0] > y.key[0]:
                    temp = x
                    x = y
                    y = temp
                x.append(y)
                A[degree] = None
                degree = degree + 1
            A[degree] = x
            
        self.least = None
        for k in A:
            if k is not None:
                self.trees.append(k)
                if (self.least is None or k.key[0] < self.least.key[0]):
                    self.least = k
                

        
heap = FibonacciHeap()
heap.insert([1, 1])
heap.insert([2, 2])
heap.insert([29, 3])
heap.insert([0, 4])
heap.insert([5, 5])
heap.insert([5, 6])
#heap.reorder()

#print(heap.extract_min())
#print(heap.extract_min())