# local utils
from projection_auxiliary import *


########################### PROJECTION FUNCTIONS ###########################

def xml_45_projection(patent):
    # from https://bulkdata.uspto.gov/data/patent/grant/redbook/2015/PatentGrantXMLv4.5Documentation.docx
    res = {}
    res['uid'] =  text_leaves(xpath(patent ,['us-bibliographic-data-grant','publication-reference','document-id','doc-number'])).lstrip('0')
    res['grant_date'] = text_leaves(xpath(patent ,['us-bibliographic-data-grant','publication-reference','document-id','date']))
    res['kind'] = text_leaves(xpath(patent ,['us-bibliographic-data-grant','publication-reference','document-id','kind']))
    res['app_date'] = text_leaves(xpath(patent ,['us-bibliographic-data-grant','application-reference','document-id','date']))
    res['abstract'] = text_leaves(xpath(patent ,['abstract']))
    res['title'] = text_leaves(xpath(patent ,['us-bibliographic-data-grant','invention-title']))
    res['citations'] = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant', 'references-cited', 'citation', 'patcit', 'document-id', 'doc-number'])]
    if len(res['citations']) == 0:
        res['citations'] = [text_leaves(xpath(patent,['us-bibliographic-data-grant', 'references-cited', 'citation', 'patcit', 'document-id', 'doc-number']))]
        if len(res['citations'][0]) == 0:
            res['citations'] = []
    res['IPC_main_class'] = text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-ipc','main-classification']))
    res['IPC_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classification-ipc','further-classification'])]
    if len(res['IPC_further_classes']) == 0:
        res['IPC_further_classes'] = [text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-ipc','further-classification']))]
        if len(res['IPC_further_classes'][0]) == 0:
            res['IPC_further_classes'] = []
    res['IPC_edition'] = text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-ipc','edition']))
    res['US_main_class'] = text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-national','main-classification']))
    res['US_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classification-national','further-classification'])]
    if len(res['US_further_classes']) == 0:
        res['US_further_classes'] = [text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-national','further-classification']))]
        if len(res['US_further_classes'][0]) == 0:
            res['US_further_classes'] = []
    res['US_edition'] = text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-national','edition']))
    return res

def xml_25_projection(patent):
    res = {}
    res['uid'] =  text_leaves(xpath(patent ,['SDOBI','B100','B110','DNUM','PDAT'])).lstrip('0')
    res['kind'] =  text_leaves(xpath(patent ,['SDOBI','B100','B130','DNUM','PDAT'])).lstrip('0')
    res['grant_date'] = text_leaves(xpath(patent ,['SDOBI','B100','B140','DATE','PDAT']))
    res['app_date'] = text_leaves(xpath(patent ,['SDOBI','B200','B220','DATE','PDAT']))
    res['abstract'] = text_leaves(xpath(patent ,['SDOAB','BTEXT']))
    res['title'] = text_leaves(xpath(patent ,['SDOBI','B500','B540','STEXT','PDAT']))
    res['IPC_main_class'] = text_leaves(xpath(patent,['SDOBI','B500','B510','B511','PDAT']))
    res['IPC_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,['SDOBI','B500','B510','B512','PDAT'])]
    if len(res['IPC_further_classes']) == 0:
        res['IPC_further_classes'] = [text_leaves(xpath(patent,['SDOBI','B500','B510','B512','PDAT']))]
        if len(res['IPC_further_classes'][0]) == 0:
            res['IPC_further_classes'] = []
    res['IPC_edition'] = text_leaves(xpath(patent,['SDOBI','B500','B510','B516','PDAT']))
    res['US_main_class'] = text_leaves(xpath(patent,['SDOBI','B500','B520','B521','PDAT']))
    res['US_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,['SDOBI','B500','B520','B522','PDAT'])]
    if len(res['US_further_classes']) == 0:
        res['US_further_classes'] = [text_leaves(xpath(patent,['SDOBI','B500','B520','B522','PDAT']))]
        if len(res['US_further_classes'][0]) == 0:
            res['US_further_classes'] = []
    res['US_edition'] = text_leaves(xpath(patent,['SDOBI','B500','B520','B526','PDAT']))
    res['keywords'] = [text_leaves(e) for e in multiple_xpath(patent,['SDOBI','B500','B550','B552','PDAT'])]
    res['citations'] = [text_leaves(e) for e in multiple_xpath(patent,['SDOBI','B500','B560','B561','PCIT','DOC', 'DNUM', 'PDAT'])]
    if len(res['citations']) == 0:
        res['citations'] = [text_leaves(xpath(patent,['SDOBI','B500','B560','B561','PCIT','DOC', 'DNUM', 'PDAT']))]
        if len(res['citations'][0]) == 0:
            res['citations'] = []
    return res

# lxml object to data dico for one record
def sgm_25_projection(patent):
    # From https://www.wipo.int/export/sites/www/standards/en/pdf/03-32-01.pdf
    res = {}
    res['uid'] =  text_leaves(xpath(patent ,['SDOBI'.lower(),'B100'.lower(),'B110'.lower(),'DNUM'.lower(),'PDAT'.lower()])).lstrip('0')
    res['kind'] =  text_leaves(xpath(patent ,['SDOBI'.lower(),'B100'.lower(),'B130'.lower(),'DNUM'.lower(),'PDAT'.lower()]))
    res['grant_date'] = text_leaves(xpath(patent ,['SDOBI'.lower(),'B100'.lower(),'B140'.lower(),'DATE'.lower(),'PDAT'.lower()]))
    res['app_date'] = text_leaves(xpath(patent ,['SDOBI'.lower(),'B200','B220'.lower(),'DATE'.lower(),'PDAT'.lower()]))
    res['abstract'] = text_leaves(xpath(patent ,['SDOAB'.lower(),'BTEXT'.lower()]))
    res['title'] = text_leaves(xpath(patent ,['SDOBI'.lower(),'B500'.lower(),'B540'.lower(),'STEXT'.lower(),'PDAT'.lower()]))
    res['language_title'] = text_leaves(xpath(patent ,['SDOBI'.lower(),'B500'.lower(),'B540'.lower(),'B541'.lower(),'STEXT'.lower(),'PDAT'.lower()]))
    res['IPC_main_class'] = text_leaves(xpath(patent,[s.lower() for s in ['SDOBI','B500','B510','B511','PDAT']]))
    res['IPC_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,[s.lower() for s in ['SDOBI','B500','B510','B512','PDAT']])]
    if len(res['IPC_further_classes']) == 0:
        res['IPC_further_classes'] = [text_leaves(xpath(patent,[s.lower() for s in ['SDOBI','B500','B510','B512','PDAT']]))]
        if len(res['IPC_further_classes'][0]) == 0:
            res['IPC_further_classes'] = []
    res['IPC_edition'] = text_leaves(xpath(patent,[s.lower() for s in ['SDOBI','B500','B510','B516','PDAT']]))
    res['US_main_class'] = text_leaves(xpath(patent,[s.lower() for s in ['SDOBI','B500','B520','B521','PDAT']]))
    res['US_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,[s.lower() for s in ['SDOBI','B500','B520','B522','PDAT']])]
    if len(res['US_further_classes']) == 0:
        res['US_further_classes'] = [text_leaves(xpath(patent,[s.lower() for s in ['SDOBI','B500','B520','B522','PDAT']]))]
        if len(res['US_further_classes'][0]) == 0:
            res['US_further_classes'] = []
    res['US_edition'] = text_leaves(xpath(patent,[s.lower() for s in ['SDOBI','B500','B520','B526','PDAT']]))
    res['keywords'] = [text_leaves(e) for e in multiple_xpath(patent,[s.lower() for s in ['SDOBI','B500','B550','B552','PDAT']])]
    res['citations'] = [text_leaves(e) for e in multiple_xpath(patent,['SDOBI'.lower(),'B500'.lower(),'B560'.lower(),'B561'.lower(),'PCIT'.lower(),'DOC'.lower(), 'DNUM'.lower(), 'PDAT'.lower()])]
    if len(res['citations']) == 0:
        res['citations'] = [text_leaves(xpath(patent,['SDOBI'.lower(),'B500'.lower(),'B560'.lower(),'B561'.lower(),'PCIT'.lower(),'DOC'.lower(), 'DNUM'.lower(), 'PDAT'.lower()]))]
        if len(res['citations'][0]) == 0:
            res['citations'] = []
    return res


def dat_projection(patent):
    # From https://www.uspto.gov/sites/default/files/products/PatentFullTextAPSGreenBook-Documentation.pdf
    res = {}
    list_references = []
    list_inventor_names = []
    for k in patent.keys() :
        if k=='WKU' : # patent number
            res['uid'] = patent[k][:8].lstrip('0')#[:7] # there is a leading zero if it is a utility, and there is a check digit at the end (9th position)
        elif k=='ISD':# issue date
            res['grant_date'] = patent[k]
        elif k=='APT' : # application type
            types_dict = {1:'Utility', 2:'Reissue', 3:'TVPP', 4:'Design', 5:'Defensive', 6:'Plant', 7:'SIR'}
            res['kind']=patent[k]
            if res['kind'] is not None and len(res['kind']) > 0 and int(res['kind']) in types_dict.keys():
                res['kind'] = types_dict[int(res['kind'])]
        elif k=='APD' : # application filing date
            res['app_date']=patent[k]
        elif k=='TTL' :
            res['title']=patent[k]
        elif k=='TTL' :
            res['title']=patent[k]
        elif k=='ABST' :
            abstract = patent[k]
            text = ""
            additional = {}
            for kk in abstract.keys():
                if kk=='EQU' or kk=='TBL' :
                    additional[kk] = abstract[kk]
                else :
                    text = text+' '+reduce_field(abstract[kk])
            res['abstract']=text.lstrip()
            if len(additional) > 0:
                res['additional_abstract']=additional
        elif k=='CLAS' : # classes
            classes = patent[k]
            for kk in classes:
                if kk=='OCL' : # US classification
                    res['US_main_class']=classes[kk]
                elif kk=='XCL' : # cross reference
                    res['US_further_classes']=classes[kk]
                elif kk=='EDF' : # US edition
                    res['US_edition']=classes[kk]
                elif kk=='ICL' : # International classification
                    if type(classes[kk]) == type([]):
                        if 'IPC_main_class' not in res:
                            res['IPC_main_class'] = classes[kk][0]
                            res['IPC_further_classes'] = classes[kk][1:]
                        else:
                            res['IPC_further_classes'] += classes[kk]
                    else:
                        if 'IPC_main_class' not in res:
                            res['IPC_main_class'] = classes[kk]
                            res['IPC_further_classes'] = []
                        else:
                            res['IPC_further_classes'].append(classes[kk])
            # res['classes']=classes
        elif k=='INVT' : # classes
            inventor_tree = patent[k]
            for kk in inventor_tree:
                if kk=='NAM' : # name of the inventor. 
                    list_inventor_names.append(inventor_tree[kk])
            res['inventors']=list_inventor_names
            # res['classes']=classes
        elif k=='UREF' or k == 'FREF' or k == 'OREF': # US references and Foreign references and other references
            for kk in patent[k]:
                for kkk in kk:
                    if kkk=='PNO' : # patent number
                        list_references.append(kk[kkk])#[:8])
            res['citations']=list_references

    # Check that all are at least initialized
    for key in ['uid', 'kind', 'grant_date', 'app_date', 'abstract', 'title', 'language_title', 'IPC_main_class', 'IPC_edition', 'US_main_class', 'US_edition']:
        if key not in res:
            res[key] = ''
    if 'US_edition' not in res:
            res['US_edition'] = '1' # if it is not shown, it is the first for these set of patents
    for key in ['IPC_further_classes', 'US_further_classes', 'keywords', 'citations', 'inventors']:
        if key not in res:
            res[key] = []
    
    return(res)