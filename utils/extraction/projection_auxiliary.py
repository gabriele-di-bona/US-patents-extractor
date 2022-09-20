from functools import reduce


########################### PROJECTION AUXILIARY FUNCTIONS ###########################

def xpath(tree,path):
    element = tree
    for p in path :
        index = -1;i=0
        for child in element :
            if child.tag==p : index = i
            i=i+1
        if index ==-1 : return None
        element = element[index]
    return element

def multiple_xpath(tree,path):
    currentPaths = [[]]
    for p in path :
        nextPaths = []
        for currentPath in currentPaths :
            indexes = []
            for i,child in enumerate(list(get_element(tree,currentPath))) :
                if child.tag==p : 
                    indexes.append(i)
            if indexes != [] :
                for i in indexes:
                    np = currentPath.copy()
                    np.append(i)
                    nextPaths.append(np)
        currentPaths = nextPaths
    return [get_element(tree,p) for p in currentPaths]

def get_element(tree,idpath):
    element = tree
    for i in idpath:
        # print i
        element = element[i]
    return element

def text_leaves(element):
    if element is None : return ''
    if len(element)==0 :
        if element.text is None :
            return ''
        else :
            return element.text
    text = ''
    for child in element :
        if (child.text!= None) :
            text = text+' '+child.text
        else :
            text = text+' '+str(text_leaves(child))
    return text

def reduce_field(l) :
    if type(l)==type([]) :
        return(reduce(lambda s1,s2 : s1+' '+s2,l))
    else :
        return(l)

