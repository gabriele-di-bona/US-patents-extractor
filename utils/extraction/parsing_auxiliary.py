from functools import reduce
import sys

########################### PARSING AUXILIARY FUNCTIONS ###########################

def remove_style_formatting(string):
    for formatting in ['b', 'i', 'o', 'u', 'em', 'sb', 'sp', 'B', 'I', 'O', 'U', 'EM', 'SB', 'SP', 'u style="single"', 'o ostyle="single"', 'u style="double"', 'o ostyle="double"']:
        string = string.replace(f'<{formatting}>', '')
        string = string.replace(f'</{formatting}>', '')
    return string

def get_current_line(r, replace=True):
    currentLine = r.readline()
    try:
        currentLine = currentLine.decode(errors='replace')
    except (UnicodeDecodeError, AttributeError) as e:
        print(currentLine, e)
        pass
    if replace == True:
        currentLine=currentLine.replace('&','&amp;')
    return currentLine

def parse_sub_fields(raw):
    #print raw
    res = {}
    if len(raw)==0 : return res
    currentField = [raw[0]]
    i=1
    singleRecords = False
    if len(raw)>1 : singleRecords = len(raw[i].split(' '))>1
    while i<len(raw) and singleRecords :
        if raw[i].startswith(' '):
            currentField.append(raw[i])
        else :
            [fieldName,fieldValue] = parse_field(currentField)
            res = append_dico(res,fieldName,fieldValue)
            currentField=[raw[i]]
        i = i+1
        if i<len(raw): singleRecords = len(raw[i].split(' '))>1
    [fieldName,fieldValue] = parse_field(currentField)
    res = append_dico(res,fieldName,fieldValue)
    if i<len(raw):
        currentField = [raw[i]]
        for j in range(i+1,len(raw)):
            if len(raw[j].split(' '))==1 :
                [fieldName,fieldValue] = parse_field(currentField)
                res = append_dico(res,fieldName,fieldValue)
                currentField=[]
            currentField.append(raw[j])
        [fieldName,fieldValue] = parse_field(currentField)
        res = append_dico(res,fieldName,fieldValue)
    return(res)


def parse_field(rows) :
    if len(rows)==1:
        return(split_field(rows[0]))
    else :
        if len(rows[0].split(' '))>1:
            [fieldName,row1]=split_field(rows[0])
            return [fieldName,row1+' '+reduce(lambda s1,s2 : s1.lstrip()+' '+s2.lstrip(),[rows[j] for j in range(1,len(rows))])]
        else :
            fieldName = rows[0]
            subfields = {}
            currentSubField = split_field(rows[1])
            for j in range(2,len(rows)) :
                if rows[j].startswith(' '):
                    currentSubField = [currentSubField[0],currentSubField[1]+' '+rows[j].lstrip()]
                else :
                    subfields=append_dico(subfields,currentSubField[0],currentSubField[1])
                    currentSubField = split_field(rows[j])
            subfields=append_dico(subfields,currentSubField[0],currentSubField[1])
            return([fieldName,subfields])


def split_field(row) :
    s = row.split(' ',1)
    if len(s)>1 :
        return([s[0],s[1].lstrip()])
    else :
        return(s[0],{})


def append_dico(dico,key,value):
    if key in dico :
        l=dico[key]
        if type(l)!=type([]): l = [l]
        l.append(value)
        dico[key]=l
    else :
        dico[key] = value
    return(dico)


class recursion_depth:
    """
    To change the recursion depth only temporarily. Default depth is 1000.
    
    Usage: 
    with recursion_depth(2000):
        do_stuff_recursively()
    """
    def __init__(self, limit):
        self.limit = limit
        self.default_limit = sys.getrecursionlimit()
    def __enter__(self):
        sys.setrecursionlimit(self.limit)
    def __exit__(self, type, value, traceback):
        sys.setrecursionlimit(self.default_limit)