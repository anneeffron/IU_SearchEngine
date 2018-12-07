#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 17:15:40 2018

@author: ayeffron
"""

#---------------------------------------------------

#Helper functions for creating the spider

#---------------------------------------------------
import os

def relativeLink(domain, link):
    if link.startswith('/'):
        return "https://" + domain + link
    else:
        return link
    
    
#function to create folder 
def createFolder(dName):
    #trying to see if folder already exists, if it does create the folder
    try:
        if not os.path.exists(dName):
            os.makedirs(dName)
       
    except:
        print("Error in making directory", dName)
    return dName


#---------------------------------------------------

#Helper functions 

#---------------------------------------------------
def fixTitle(title):
    title = title.replace(" ", "")
    title = title.replace("\n", "")
    return title
