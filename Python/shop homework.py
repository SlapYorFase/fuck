# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 07:39:12 2022

@author: Philip
"""

SHOP= {"banana":25,
        "apple":35,
        "milk":105, 
        "cake":85,
        "egg":10}
SHOP=25
if SHOP==25:
    print(SHOP["banana"])
elif SHOP==35:
    print(SHOP["apple"])
elif SHOP==105:
    print(SHOP["milk"])
elif SHOP==85:
    print(SHOP["cake"])
else:
    print (SHOP["egg"])
    
'''why does it only print egg?'''