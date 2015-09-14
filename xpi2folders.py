#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" xpi2folders: unpack prepare XPI for mass deployment"""

import os, getopt, sys, shutil
import zipfile
import xml.etree.ElementTree as ET
import time

__author__ = "Kirill Kozlovskiy"
__copyright__ = "Copyright 2011-2012, Kirill Kozlovskiy"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Kirill Kozlovskiy"
__email__ = "kirill.k2@gmail.com"
__status__ = "Production"


def getRdfInfo(xml_file):
    """Return parsed atributes from XPI xml"""
    tree = ET.fromstring(xml_file)
    desc = [e for e in tree.findall('.//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description') if 
    e.get('about') == 'urn:mozilla:install-manifest']
    
    r = {}
    for tag in ['id', 'name', 'version']:
        r[tag] = desc[0].find('./{http://www.mozilla.org/2004/em-rdf#}%s' % tag).text
##        print tag,"=",r[tag],"; "
    return r

def processXpi(file, outputdir):
    """Unpack single XPI and return information"""

    print "XPI: %s" % file
    zfXpi = zipfile.ZipFile(file)
    pinfo = getRdfInfo(zfXpi.read("install.rdf"))
    
    outdir = os.path.join(outputdir, pinfo['id'])
    print "\textracting to %s " % outdir
    zfXpi.extractall(outdir)
        
    # create description file with name version and id of package
    fileDesc = os.path.join(outdir, "description.txt")
    fo = open(fileDesc, "w")
    for tag in ['name', 'version', 'id']:
        fo.write(tag)
        fo.write(": ")
        fo.write(pinfo[tag])
        fo.write("\r\n")
    fo.close()

    return pinfo

def usage():
    print os.path.abspath(__file__), "[-h|--help] {-i|--input} <inputdir> {-o|--output} <outputdir> [-g|--generate-ver] [-c|--clean-output]"

def main(argv):                         
    #inputdir=os.path.dirname(os.path.abspath(__file__))
    inputdir="."
    outputdir=inputdir
    generate_ver = 0
    clean_output = 0

    try:
        opts, args = getopt.getopt(argv, "hi:o:gc", ["help", "input=","output=","generate-ver", "clean-output"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt == '-d':
            global _debug
            _debug = 1
        elif opt in ("-g", "--generate-ver"):
            generate_ver = 1
        elif opt in ("-c", "--clean-output"):
            clean_output = 1
        elif opt in ("-i", "--input"):
            inputdir = arg
        elif opt in ("-o", "--output"):
            outputdir = arg
        else:
            usage()    
            sys.exit(2)

    extension = ".xpi"

    print "Extracting %s files from %s to %s" % ( extension, inputdir, outputdir )
    
    listXpiFiles = [os.path.join(inputdir, file) for file in os.listdir(inputdir) if file.lower().endswith(extension)]

    if clean_output == 1:
        if inputdir != outputdir:
            if os.access(outputdir, os.X_OK):
                shutil.rmtree(outputdir)
        else:
            print "Warning! Can't clean output 'cause it's equal to input!"

    if generate_ver == 1:
        os.makedirs(outputdir)
        fileVer = os.path.join(outputdir, "%s.ver" % time.strftime('%Y%m%d-%H'))
        fv = open(fileVer, "w")
        for fileXpi in listXpiFiles:
            pinfo=processXpi(fileXpi, outputdir)
            fv.write(pinfo['name'])
            fv.write("\t")
            fv.write(pinfo['version'])
            fv.write("\r\n")
        fv.close()
        print "Version file is %s" % fileVer
    else:
        for fileXpi in listXpiFiles:
            processXpi(fileXpi, outputdir)


if __name__ == "__main__":
    main(sys.argv[1:])


