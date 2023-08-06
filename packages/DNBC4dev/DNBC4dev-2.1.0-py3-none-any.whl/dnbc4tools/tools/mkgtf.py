# Count gtf files and filter gtf files

import re,collections
from typing import List, Iterable
from collections import Counter

def read_gtf(fp: str, feature: str) -> Iterable[List[str]]:
    '''
    Read the gtf into the list with each gene as a split, 
    and the analysis will be processed in units of each gene
    '''
    lines = []
    with open(fp) as f:
        for line in f:
            newline = line.strip()
            if newline.startswith('#'):
                lines.append(line)
            elif newline == '':
                continue
            else:
                lst = newline.split('\t')
                if lst[2] == feature:
                    yield lines
                    lines = []
                    lines.append(line)
                else:
                    lines.append(line)
        yield lines

def filtergtf(gtf,filtergtf,keyword,attribute):
    '''
    
    '''
    d = dict([(key,keyword) for key in attribute])
    gtfread = read_gtf(gtf,'gene')
    result = open(filtergtf,'w')
    for i in gtfread:
        if i:
            if i[0].startswith('#'):
                result.writelines(i)
            else:
                aDict = collections.OrderedDict()
                pattern = re.compile(r'(\S+?)\s*"(.*?)"')
                for m in re.finditer(pattern, i[0].split('\t')[-1]):
                    key = m.group(1)
                    value = m.group(2)
                    aDict[key] = value
                for key1,value1 in aDict.items():
                    for key2,value2 in d.items():
                        if key1 == value2 and key2 == value1:
                            result.writelines(i)
    result.close()

def statgtf(gtf,keyword,outfile):
    with open(gtf,'r') as fp:
        sumDict = []
        for line in fp:
            line = line.strip()
            if line.startswith("#"):
                continue
            elif line == '':
                continue
            else:
                lst = line.split('\t')
                if lst[2] == 'gene':
                    aDict = collections.OrderedDict()
                    pattern = re.compile(r'(\S+?)\s*"(.*?)"')
                    for m in re.finditer(pattern, lst[-1]):
                        key = m.group(1)
                        value = m.group(2)
                        aDict[key] = value
                    sumDict.append(aDict[keyword])
        result = Counter(sumDict)
        outfile = open(outfile,'w')
        outfile.write('Type'+'\t'+'Count'+'\n')
        for k,v in sorted(result.items(), key = lambda x:x[1], reverse=True):
            outfile.write(f'{k}\t{v}\n')
        outfile.close()


normal_include = 'protein_coding,\
lncRNA,\
lincRNA,\
antisense,\
IG_C_gene,\
IG_D_gene,\
IG_J_gene,\
IG_LV_gene,\
IG_V_gene,\
IG_V_pseudogene,\
IG_J_pseudogene,\
IG_C_pseudogene,\
TR_C_gene,\
TR_D_gene,\
TR_J_gene,\
TR_V_gene,\
TR_V_pseudogene,\
TR_J_pseudogene'
