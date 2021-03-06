#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
import sys, csv, getopt, topics, os

def toASCII (string):
    ascii_string = ''
    for unicode_char in string:
        code = ord(unicode_char)
        if code >= 0x0021 and code <= 0x7e:
            ascii_string += unicode_char
        elif code == 0x3000:
            ascii_string += unichr (0x0020)
        else:
            ascii_string += unichr (code - 0xfee0)
    return ascii_string

def Open (file, flags = 'r'):
    __location__ = os.path.realpath( os.path.join(os.getcwdu(), os.path.dirname(__file__)))
    return open (os.path.join (__location__, file), flags)

class Statistics(object):
    def __init__(this, record=lambda : {1:[0, 0], 2:[0, 0], 3:[0, 0, 0, 0, 0], 4:[0, 0], 5:[0, 0], 6:[0, 0] }):
        this.db_item = record
        this.infile = '2015.dat'
        this.parseFile = ''
        this.view = {}

    def getOptions(this, argv):
        try:
            opts, args = getopt.getopt (argv, 'hl:p:', ['help', 'load=', 'parse='])
        except:
            this.usage ()
            sys.exit ()
        for opt, arg in opts:
            if opt in ['-h', '--help']:
                this.usage()
                sys.exit()
            elif opt in ['-p', '--parse']:
                this.parseFile = arg
            elif opt in ['-l', '--load']:
                this.infile = arg
        this.parse () if this.parseFile != u'' else []
    
    def usage(this):
        usage = u'''
        Usage: {} [-opt] [--options]
        options
          -h --help: display this message
          [-l | --load]  infile: load database from a infile
          [-p | --parse] parse csv file first
          '''.format(sys.argv[0])
        print usage
    
    # getStatistics (infile, classifier = lambda record : True)
    # get statistics of each class in the range of classifier
    # parameter: classifier: list -> class, it classify a record to one of the classes
    #            default is classifying all record to 'nctu' class
    # value:     list of results for each classes
    def getStatistics (this, classifier = lambda record : True):
        for line in Open(this.infile):
            l = line.split(u',')
            key = classifier(l)
            if not key in this.view:
                this.view[key] = this.db_item()
            for i in xrange(1, 7):
                this.view[key][i][int(l[i])] += 1
        return this.view
    
    def printHeader (this, s):
        print u'{:6}{:8}{:8}{:8}{:8}{:8}{:8}'.format (
                s, u'通識學分', u'反對現行  ', u'希望外文',
                u'希望通識', u'認為通識', u'認為通識')
        print u'{:6}{:8}{:8}{:8}{:8}{:8}{:8}'.format (
                u' '*11, u' 過多   ', u'五項度作法', u'比例提高',
                u'變三學分', u'品質不好', u'品質尚可')
    
    def render (this, filter = {True: u'全校'}):
        for key in this.view:
            if key in filter:
                q = [100 * this.view[key][i][j] / sum(this.view[key][i]) 
                    for (i, j) in 
                    [(1, 1), (2, 0), (3, 1), (4, 1), (5, 1), (6, 1)]]
                format_string = u'{:8}{:.3f}      {:.3f}      {:.3f}'
                format_string += '      {:.3f}      {:.3f}      {:.3f}'
                print format_string.format (filter[key], q[0], q[1], q[2], q[3], q[4], q[5])
    
    def parse (this):
        reader    = csv.reader(Open (this.parseFile))
        response  = {u'恰當':0, u'通識學分過多':1, u'外語學分過多':2, u'其他':3}
        extract   = lambda row : [toASCII (row[1]), row[2], row[4], 
                                  response[row[6]], row[8], row[10], row[11]]
        check     = lambda row : True if row[1].isdigit() and len(row[1]) == 7 else False
        sanitized = (extract ([unicode(cell, 'utf-8') for cell in row]) 
                     for row in reader if check(row))
        csvWrite  = csv.writer(Open (this.infile, 'wt'))
        for l in sanitized:
            csvWrite.writerow(l)

################################
# Main program Begins          #
################################
main = Statistics ()
main.getOptions (sys.argv[1:]) # bad design here, will change this later

if __name__ == '__main__':
    for topic in topics.topics:
        main.printHeader (topic['title'])
        main.getStatistics (topic['classifier'])
        main.render (topic['filter'])

    # get result for the whole school
    main.getStatistics ()
    main.render ()
    
