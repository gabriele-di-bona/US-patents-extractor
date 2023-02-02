# local utils
from projection_auxiliary import *


########################### PROJECTION FUNCTIONS ###########################

def xml_45_projection(patent):
    # from https://bulkdata.uspto.gov/data/patent/grant/redbook/2015/PatentGrantXMLv4.5Documentation.docx
    res = {}
    res['uid'] =  text_leaves(xpath(patent ,['us-bibliographic-data-grant','publication-reference','document-id','doc-number'])).lstrip('0')
    res['grant_date'] = text_leaves(xpath(patent ,['us-bibliographic-data-grant','publication-reference','document-id','date']))
    res['kind'] = text_leaves(xpath(patent ,['us-bibliographic-data-grant','publication-reference','document-id','kind'])).lstrip('0')
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
    if len(res['IPC_main_class'].lstrip(' ')) == 0:
        # they have changed the structure of this
        res['IPC_further_classes'] = []
        sections = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-ipcr','classification-ipcr', 'section'])]
        classes = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-ipcr','classification-ipcr', 'class'])]
        subclasses = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-ipcr','classification-ipcr', 'subclass'])]
        maingroups = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-ipcr','classification-ipcr', 'main-group'])]
        subgroups = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-ipcr','classification-ipcr', 'subgroup'])]
        for i in range(len(sections)):
            if i == 0:
                res['IPC_main_class'] = f"{sections[0]}{classes[0]}{subclasses[0]} {maingroups[0]}/{subgroups[0]}"
            else:
                res['IPC_further_classes'].append(f"{sections[i]}{classes[i]}{subclasses[i]} {maingroups[i]}/{subgroups[i]}")
        res['IPC_edition'] = text_leaves(xpath(patent,['us-bibliographic-data-grant','classifications-ipcr','classification-ipcr','ipc-version-indicator','date']))
    res['US_main_class'] = text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-national','main-classification']))
    res['US_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classification-national','further-classification'])]
    if len(res['US_further_classes']) == 0:
        res['US_further_classes'] = [text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-national','further-classification']))]
        if len(res['US_further_classes'][0]) == 0:
            res['US_further_classes'] = []
    res['US_edition'] = text_leaves(xpath(patent,['us-bibliographic-data-grant','classification-national','edition']))
    if len(res['US_main_class'].lstrip(' ')) == 0:
        # they have changed the structure of this
        section = text_leaves(xpath(patent,['us-bibliographic-data-grant','classifications-cpc','main-cpc','classification-cpc', 'section']))
        classe = text_leaves(xpath(patent,['us-bibliographic-data-grant','classifications-cpc','main-cpc','classification-cpc', 'class']))
        subclasse = text_leaves(xpath(patent,['us-bibliographic-data-grant','classifications-cpc','main-cpc','classification-cpc', 'subclass']))
        maingroup = text_leaves(xpath(patent,['us-bibliographic-data-grant','classifications-cpc','main-cpc','classification-cpc', 'main-group']))
        subgroup = text_leaves(xpath(patent,['us-bibliographic-data-grant','classifications-cpc','main-cpc','classification-cpc', 'subgroup']))
        res['US_main_class'] = f"{section}{classe}{subclasse} {maingroup}/{subgroup}"
        res['US_further_classes'] = []
        sections = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-cpc','further-cpc','classification-cpc', 'section'])]
        classes = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-cpc','further-cpc','classification-cpc', 'class'])]
        subclasses = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-cpc','further-cpc','classification-cpc', 'subclass'])]
        maingroups = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-cpc','further-cpc','classification-cpc', 'main-group'])]
        subgroups = [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','classifications-cpc','further-cpc','classification-cpc', 'subgroup'])]
        for i in range(len(sections)):
            res['US_further_classes'].append(f"{sections[i]}{classes[i]}{subclasses[i]} {maingroups[i]}/{subgroups[i]}")
        res['US_edition'] = text_leaves(xpath(patent,['us-bibliographic-data-grant','classifications-cpc','main-cpc','classification-cpc','cpc-version-indicator','date']))
    
    # get inventors
    # last_names = []
    # first_names = []
    # if xpath(patent,['us-bibliographic-data-grant','parties','inventors']) is not None:
    #     last_names += [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','parties','inventors', 'inventor', 'addressbook', 'last-name'])]
    #     first_names += [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','parties','inventors', 'inventor', 'addressbook', 'first-name'])]
    # if xpath(patent,['us-bibliographic-data-grant','parties','applicants']) is not None:
    #     for e in multiple_xpath(patent,['us-bibliographic-data-grant','parties','applicants', 'applicant']):
    #         if 'inventor' in e.attrib['app-type']:
    #             last_names.append(text_leaves(xpath(e,['addressbook', 'last-name'])))
    #             first_names.append(text_leaves(xpath(e,['addressbook', 'first-name'])))
    # if xpath(patent,['us-bibliographic-data-grant','us-parties','inventors']) is not None:
    #     last_names += [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','us-parties','inventors', 'inventor', 'addressbook', 'last-name'])]
    #     first_names += [text_leaves(e) for e in multiple_xpath(patent,['us-bibliographic-data-grant','us-parties','inventors', 'inventor', 'addressbook', 'first-name'])]
    # if xpath(patent,['us-bibliographic-data-grant','us-parties','applicants']) is not None:
    #     for e in multiple_xpath(patent,['us-bibliographic-data-grant','us-parties','applicants', 'applicant']):
    #         if 'inventor' in e.attrib['app-type']:
    #             last_names.append(text_leaves(xpath(e,['addressbook', 'last-name'])))
    #             first_names.append(text_leaves(xpath(e,['addressbook', 'first-name'])))
    # if xpath(patent,['us-bibliographic-data-grant','us-parties','us-applicants']) is not None:
    #     for e in multiple_xpath(patent,['us-bibliographic-data-grant','us-parties','us-applicants', 'applicant']):
    #         if 'inventor' in e.attrib['app-type']:
    #             last_names.append(text_leaves(xpath(e,['addressbook', 'last-name'])))
    #             first_names.append(text_leaves(xpath(e,['addressbook', 'first-name'])))
    # res['inventors'] = [f"{last_names[i]}; {first_names[i]}" for i in range(len(last_names))]
    
    res['inventors'] = []
    possible_tres_inventors = [
        ['us-bibliographic-data-grant','parties','inventors', 'inventor'],
        ['us-bibliographic-data-grant','us-parties','inventors', 'inventor'],
        ['us-bibliographic-data-grant','us-parties','us-inventors', 'inventor'],
    ]
    possible_tres_applicants = [
        ['us-bibliographic-data-grant','parties','applicants', 'applicant'],
        ['us-bibliographic-data-grant','us-parties','applicants', 'applicant'],
        ['us-bibliographic-data-grant','us-parties','us-applicants', 'applicant'],
    ]
    for tree in possible_tres_inventors:
        for e in multiple_xpath(patent,tree):
            if xpath(e, ['addressbook','orgname']) is not None:
                res['inventors'].append(text_leaves(xpath(e, ['addressbook','orgname'])))
            else:
                last_name = text_leaves(xpath(e,['addressbook', 'last-name'])).lstrip(' ')
                first_name = text_leaves(xpath(e,['addressbook', 'first-name'])).lstrip(' ')
                res['inventors'].append(f"{last_name}; {first_name}")
    for tree in possible_tres_applicants:
        for e in multiple_xpath(patent,tree):
            if 'inventor' in e.attrib['app-type']:
                if xpath(e, ['addressbook','orgname']) is not None:
                    res['inventors'].append(text_leaves(xpath(e, ['addressbook','orgname'])))
                else:
                    last_name = text_leaves(xpath(e,['addressbook', 'last-name'])).lstrip(' ')
                    first_name = text_leaves(xpath(e,['addressbook', 'first-name'])).lstrip(' ')
                    res['inventors'].append(f"{last_name}; {first_name}")
    
    if res['uid'] == '':
        res['uid'] =  text_leaves(xpath(patent ,['publication-reference','document-id','doc-number'])).lstrip('0')
        res['grant_date'] = text_leaves(xpath(patent ,['publication-reference','document-id','date']))
        res['kind'] = text_leaves(xpath(patent ,['publication-reference','document-id','kind'])).lstrip('0')
    return res

def xml_25_projection(patent):
    res = {}
    res['uid'] =  text_leaves(xpath(patent ,['SDOBI','B100','B110','DNUM','PDAT'])).lstrip('0')
    res['kind'] =  text_leaves(xpath(patent ,['SDOBI','B100','B130','DNUM','PDAT'])).lstrip('0')
    if len(res['kind']) == 0:
        res['kind'] =  text_leaves(xpath(patent ,['SDOBI','B100','B130','PDAT'])).lstrip('0')
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
    # res['keywords'] = [text_leaves(e) for e in multiple_xpath(patent,['SDOBI','B500','B550','B552','PDAT'])]
    res['citations'] = [text_leaves(e) for e in multiple_xpath(patent,['SDOBI','B500','B560','B561','PCIT','DOC', 'DNUM', 'PDAT'])]
    if len(res['citations']) == 0:
        res['citations'] = [text_leaves(xpath(patent,['SDOBI','B500','B560','B561','PCIT','DOC', 'DNUM', 'PDAT']))]
        if len(res['citations'][0]) == 0:
            res['citations'] = []
    res['inventors'] = []
    for e in multiple_xpath(patent,['SDOBI','B700','B720','B721', 'PARTY-US', 'NAM']):
        last_name = text_leaves(xpath(e,['SNM'])).lstrip(' ')
        if xpath(e,['FNM']) is not None:
            first_name = text_leaves(xpath(e,['FNM'])).lstrip(' ')
            res['inventors'].append(f"{last_name}; {first_name}")
        else:
            res['inventors'].append(f"{last_name}")
    return res

# lxml object to data dico for one record
def sgm_25_projection(patent):
    # From https://www.wipo.int/export/sites/www/standards/en/pdf/03-32-01.pdf
    res = {}
    res['uid'] =  text_leaves(xpath(patent ,['SDOBI'.lower(),'B100'.lower(),'B110'.lower(),'DNUM'.lower(),'PDAT'.lower()])).lstrip('0')
    res['kind'] =  text_leaves(xpath(patent ,['SDOBI'.lower(),'B100'.lower(),'B130'.lower(),'DNUM'.lower(),'PDAT'.lower()])).lstrip('0')
    if len(res['kind']) == 0:
        res['kind'] =  text_leaves(xpath(patent ,['SDOBI'.lower(),'B100'.lower(),'B130'.lower(),'PDAT'.lower()])).lstrip('0')
    res['grant_date'] = text_leaves(xpath(patent ,['SDOBI'.lower(),'B100'.lower(),'B140'.lower(),'DATE'.lower(),'PDAT'.lower()]))
    res['app_date'] = text_leaves(xpath(patent ,['SDOBI'.lower(),'B200'.lower(),'B220'.lower(),'DATE'.lower(),'PDAT'.lower()]))
    res['abstract'] = text_leaves(xpath(patent ,['SDOAB'.lower(),'BTEXT'.lower()]))
    res['title'] = text_leaves(xpath(patent ,['SDOBI'.lower(),'B500'.lower(),'B540'.lower(),'STEXT'.lower(),'PDAT'.lower()]))
    # res['language_title'] = text_leaves(xpath(patent ,['SDOBI'.lower(),'B500'.lower(),'B540'.lower(),'B541'.lower(),'STEXT'.lower(),'PDAT'.lower()]))
    res['IPC_main_class'] = text_leaves(xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B510'.lower(),'B511'.lower(),'PDAT'.lower()]]))
    res['IPC_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B510'.lower(),'B512'.lower(),'PDAT'.lower()]])]
    if len(res['IPC_further_classes']) == 0:
        res['IPC_further_classes'] = [text_leaves(xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B510'.lower(),'B512'.lower(),'PDAT'.lower()]]))]
        if len(res['IPC_further_classes'][0]) == 0:
            res['IPC_further_classes'] = []
    res['IPC_edition'] = text_leaves(xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B510'.lower(),'B516'.lower(),'PDAT'.lower()]]))
    res['US_main_class'] = text_leaves(xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B520'.lower(),'B521'.lower(),'PDAT'.lower()]]))
    res['US_further_classes'] = [text_leaves(e) for e in multiple_xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B520'.lower(),'B522'.lower(),'PDAT'.lower()]])]
    if len(res['US_further_classes']) == 0:
        res['US_further_classes'] = [text_leaves(xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B520'.lower(),'B522'.lower(),'PDAT'.lower()]]))]
        if len(res['US_further_classes'][0]) == 0:
            res['US_further_classes'] = []
    res['US_edition'] = text_leaves(xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B520'.lower(),'B526'.lower(),'PDAT'.lower()]]))
    # res['keywords'] = [text_leaves(e) for e in multiple_xpath(patent,[s.lower() for s in ['SDOBI'.lower(),'B500'.lower(),'B550'.lower(),'B552'.lower(),'PDAT'.lower()]])]
    res['citations'] = [text_leaves(e) for e in multiple_xpath(patent,['SDOBI'.lower(),'B500'.lower(),'B560'.lower(),'B561'.lower(),'PCIT'.lower(),'DOC'.lower(), 'DNUM'.lower(), 'PDAT'.lower()])]
    if len(res['citations']) == 0:
        res['citations'] = [text_leaves(xpath(patent,['SDOBI'.lower(),'B500'.lower(),'B560'.lower(),'B561'.lower(),'PCIT'.lower(),'DOC'.lower(), 'DNUM'.lower(), 'PDAT'.lower()]))]
        if len(res['citations'][0]) == 0:
            res['citations'] = []
    res['inventors'] = []
    for e in multiple_xpath(patent,['SDOBI'.lower(),'B700'.lower(),'B720'.lower(),'B721'.lower(), 'PARTY-US'.lower(), 'NAM'.lower()]):
        last_name = text_leaves(xpath(e,['SNM'.lower()])).lstrip(' ')
        if xpath(e,['FNM'.lower()]) is not None:
            first_name = text_leaves(xpath(e,['FNM'.lower()])).lstrip(' ')
            res['inventors'].append(f"{last_name}; {first_name}")
        else:
            res['inventors'].append(f"{last_name}")
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
            if type(abstract) == list:
                # In this case there is a mistake, and there are two abstracts.
                # This error has appeared only in 3 patents within pftaps19871103_wk44 and pftaps19871110_wk45.
                # In all three cases, the real abstract was the first one.
                try:
                    abstract = abstract[0]
                except:
                    continue
            for kk in abstract.keys():
                if kk=='EQU' or kk=='TBL' :
                    additional[kk] = abstract[kk]
                else :
                    text = text+' '+reduce_field(abstract[kk])
            res['abstract']=text.lstrip()
            # This is just equations or formulas that can be disregarded
            # if len(additional) > 0:
            #     res['additional_abstract']=additional
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
                        if type(kk[kkk]) == list:
                            list_references += kk[kkk]
                        else:
                            list_references.append(kk[kkk])
            res['citations']=list_references

    # Check that all are at least initialized
    for key in ['uid', 'kind', 'grant_date', 'app_date', 'abstract', 'title', 'IPC_main_class', 'IPC_edition', 'US_main_class', 'US_edition']: # 'language_title', 
        if key not in res:
            res[key] = ''
    if 'US_edition' not in res:
            res['US_edition'] = '1' # if it is not shown, it is the first for these set of patents
    for key in ['IPC_further_classes', 'US_further_classes', 'citations', 'inventors']: # 'keywords', 
        if key not in res:
            res[key] = []
    
    return(res)