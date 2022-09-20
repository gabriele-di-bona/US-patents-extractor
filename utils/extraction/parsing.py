import os
import xml.etree.ElementTree as ElementTree
from tqdm import tqdm
from bs4 import BeautifulSoup
# local utils
from projection import *
from parsing_auxiliary import *


########################### PARSING FUNCTIONS ###########################
# parsers for various file types

def parse_file(f,file_object=None,year=None) :
    if f.endswith('.dat') or f.endswith('.DAT') or f.endswith('.txt') or f.endswith('.TXT'):
        proj_data = [dat_projection(parse_sub_fields(r)) for r in read_dat_as_raw(f,file_object=file_object,year=year)]
    elif f.endswith('.xml') or f.endswith('.XML') : 
        if f.startswith('pftaps'):
            proj_data = [xml_25_projection(r) for r in parse_xml_file_raw(f,file_object=file_object,year=year)]
        elif f.startswith('ipg'):
            proj_data = [xml_45_projection(r) for r in parse_xml_file_raw(f,file_object=file_object,year=year)]
    elif f.endswith('.sgm') or f.endswith('.SGML') or f.endswith('.SGM')  : 
        proj_data = [sgm_25_projection(r) for r in parse_sgm_file_raw(f,file_object=file_object,year=year)]
    for r in proj_data :
        if year is None and 'grant_date' in r and len(r['grant_date']) >= 4:
            r['year']=int(r['grant_date'][:4])
        else:
            r['year']=year
    return proj_data

def parse_xml_file_raw(f,file_object=None,year=None) :
    # read the file
    if file_object is None:
        print('reading file '+str(f))
        r = open(f,'r')
    else:
        r = file_object
    docs = []
    currentLine = get_current_line(r)
    currentDoc=''
    while currentLine != '':
        currentLine=get_current_line(r)
        if currentLine.startswith('<?xml version="1.0" encoding="UTF-8"?>') :
            docs.append(remove_style_formatting(currentDoc))
            currentLine=get_current_line(r)
            currentDoc = ''
        currentDoc=currentDoc+currentLine
    docs.append(remove_style_formatting(currentDoc))
    parsed_docs = []
    for doc in tqdm(docs) :
        try :
            tree = ElementTree.fromstring(doc)
            parsed_docs.append(tree)
        except :
            os.makedirs('errors', exist_ok = True)
            log = open('errors/'+str(f)+'.log','a')
            log.write(doc)
    print('parsed_docs : '+str(len(parsed_docs)))
    return parsed_docs

def parse_sgm_file_raw(f,file_object=None,year=None) :
    # read the file
    if file_object is None:
        print('reading file '+str(f))
        r = open(f,'r')
    else:
        r = file_object
    docs = []
    currentLine=get_current_line(r)
    currentDoc=''
    while currentLine != '':
        currentLine=get_current_line(r)
        if currentLine.startswith('<!DOCTYPE PATDOC PUBLIC "-//USPTO//DTD ST.32 US PATENT GRANT V2.4 2000-09-20//EN" [') :
            docs.append(remove_style_formatting(currentDoc))
            currentLine=get_current_line(r)
            currentDoc = ''
        if not currentLine.startswith('<!ENTITY') and not currentLine.startswith(']>'):
            currentDoc=currentDoc+currentLine
    docs.append(remove_style_formatting(currentDoc))
    parsed_docs = []
    for doc in tqdm(docs) :
        try :
            better_doc = BeautifulSoup(doc)
            tree = ElementTree.fromstring(str(better_doc)[12:-15])
            parsed_docs.append(tree)
        except :
            log = open('errors/'+str(f)+'.log','a')
            log.write(doc)
    print('parsed_docs : '+str(len(parsed_docs)))
    return parsed_docs


def read_dat_as_raw(f,file_object=None,year=None) :
    res = []
    if file_object is None:
        print('reading file '+str(f))
        r = open(f,'r')
    else:
        r = file_object
    currentLine=get_current_line(r, replace=False) # avoid first line which is ISSUE INFO
    # check if we are not already in PATN:
    if not currentLine.startswith('PATN'):
        currentLine=get_current_line(r, replace=False).replace('\n','').replace('\r','').rstrip(' ') # This should be PATN
        if not currentLine.startswith('PATN'):
            print('THERE IS A MISTAKE AT LINE 2 OF THE FILE')
        else:
            currentLine=get_current_line(r, replace=False).replace('\n','').replace('\r','').rstrip(' ') # Start the patent info
    currentPatent = []
    while currentLine != '':
        if currentLine.startswith('PATN'):
            res.append(currentPatent)
            currentPatent = []
        else :
            if currentLine != '' : 
                currentPatent.append(currentLine)
        currentLine=get_current_line(r, replace=False).replace('\n','').replace('\r','').rstrip(' ')
    res.append(currentPatent)
    return res