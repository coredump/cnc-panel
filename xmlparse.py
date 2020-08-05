'''
Documentation, License etc.

@package xmlparse
'''

import xml.etree.ElementTree as ET
from operator import itemgetter, attrgetter, methodcaller
import sys, getopt

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'xmlparse.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'xmlparse.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is ', inputfile
    print 'Output file is ', outputfile

    data=[]
    sums=[]
    sums_val=[]
    folio=0

    tree = ET.parse(inputfile)
    root = tree.getroot()

    for diagram in root.iter('diagram'):
        folio=folio+1
        for element in diagram.iter('element'):
            Xccord = element.get('x')
            Yccord = element.get('y')
            Prefix = element.get('prefix')
            UUID = element.get('uuid')
            for ten in element.iter('ten'):
                if ten.text is not  None:
                    data.append([folio,Prefix, int(Xccord), int(Yccord), UUID, ten.text, 0])
            for hundred in element.iter('hundred'):
                if hundred.text is not None:
                    data.append([folio,Prefix, int(Xccord), int(Yccord), UUID, hundred.text, 0])                        
            
    sorted_data=sorted(data, key=itemgetter(3,2))
    sorted_data2=sorted(sorted_data, key=itemgetter(0))

    print '////////////////////////////////////////'
    print 'folio, tag, X, Y,           UUID,                      old value, new value'

    for row in sorted_data2:
        if row[1] in sums:
            sums_val[sums.index(row[1])]=sums_val[sums.index(row[1])]+1
        else:
            sums.append(row[1])
            sums_val.append(1)
        row[6] = sums_val[sums.index(row[1])]   
        print row

    print 'symbols'    
    print sums
    print 'totals'
    print sums_val
            

    for diagram in root.iter('diagram'):
        for element in diagram.iter('element'):
            UUID = element.get('uuid')
            for ten in element.iter('ten'):
                for row in sorted_data2:
                    if UUID in row:
                        ten.text=str(row[6])
            for hundred in element.iter('hundred'):
                for row in sorted_data2:
                    if UUID in row:
                        hundred.text=str(row[6])
 
 
    tree.write(outputfile)            
            
            


if __name__ == "__main__":
   main(sys.argv[1:])
            
