#!/usr/local/bin/python3
import sys, csv, getopt, topics, os

def toASCII (string):
    ascii_string = ''
    for unicode_char in string:
        code = ord(unicode_char)
        if code >= 0x0021 and code <= 0x7e:
            ascii_string += unicode_char
        elif code == 0x3000:
            ascii_string += chr (0x0020)
        else:
            ascii_string += chr (code - 0xfee0)
    return ascii_string

def Open (file, flags='r'):
    __location__ = os.path.realpath( os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return open (os.path.join (__location__, file), flags)

class Statistics:
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
        this.parse () if this.parseFile != '' else []
    
    def usage(this):
        usage = '''
        Usage: {} [-opt] [--options]
        options
          -h --help: display this message
          [-l | --load]  infile: load database from a infile
          [-p | --parse] parse csv file first
          '''.format(sys.argv[0])
        print (usage)
    
    # getStatistics (infile, classifier = lambda record : True)
    # get statistics of each class in the range of classifier
    # parameter: classifier: list -> class, it classify a record to one of the classes
    #            default is classifying all record to 'nctu' class
    # value:     list of results for each classes
    def getStatistics (this, classifier = lambda record : True):
        for line in Open(this.infile):
            l = line.split(',')
            key = classifier(l)
            if not key in this.view:
                this.view[key] = this.db_item()
            for i in range(1, 7):
                this.view[key][i][int(l[i])] += 1
        return this.view
    
    def printHeader (this, s):
        print (
          "{:6}{:8}{:8}{:8}{:8}{:8}{:8}".format
          (s, "通識學分", "反對現行  ", "希望外文", "希望通識", "認為通識", "認為通識")
        )
        print (
          "{:6}{:8}{:8}{:8}{:8}{:8}{:8}".format
          (" "*11, " 過多   ", "五項度作法", "比例提高", "變三學分", "品質不好", "品質尚可")
        )
    
    def render (this, filter = {True: '全校'}):
        for key in this.view:
            if key in filter:
                q = [100 * this.view[key][1][i] / sum(this.view[key][1]) for i in [1, 0, 1, 1, 1, 1]]
                print (
                  "{:8}{:.3f}      {:.3f}      {:.3f}      {:.3f}      {:.3f}      {:.3f}".format
                  (filter[key], q[0], q[1], q[2], q[3], q[4], q[5])
                )
    
    def parse (this):
        reader    = csv.reader(Open (this.parseFile))
        response  = {'恰當':0, '通識學分過多':1, '外語學分過多':2, '其他':3}
        extract   = lambda row : [toASCII (row[1]), row[2], row[4], response[row[6]], row[8], row[10], row[11]]
        check     = lambda row : True if row[1].isdigit() and len(row[1]) == 7 else False
        sanitized = [ extract (row) for row in reader if check(row)]
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
    
sys.exit ()
from tkinter import *
from tkinter.messagebox import showinfo

def reply ():
    showinfo (title = 'pop up', message = 'buttom pressed')

window = Frame()
window.pack (expand = YES, fill = BOTH)
Label (window, text = 'testing on mac').pack (side = TOP, fill = X, expand = YES)
button = Button (window, text='press', command=reply).pack (side = LEFT, fill = BOTH, expand = YES)
button = Button (window, text='quit', command=(lambda: print ('exiting') or sys.exit ())).pack (side = RIGHT, fill = BOTH, expand = YES)
window.mainloop ()

