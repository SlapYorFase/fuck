# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 18:02:43 2022

@author: Philip
"""

for i in range(1,10):
    for j in range(1,10):
        print(str(i)+"*"+str(j)+"="+str(i*j),end="\t")
        if j==9:
            print("\n")
