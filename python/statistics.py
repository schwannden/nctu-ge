#!/usr/local/bin/python3
import sys, csv, getopt

# getstatistics get statistics of each class in the range of classifier
# parameter: classifier: list -> class, it classify a record to one of the classes
#            default is classifying all record to 'nctu' class
# value:     list of results for each classes

def getOptions(argv):
    options = {}
    opts, args = getopt.getopt (argv, 'hl:p:', ['help', 'load=', 'parse='])
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            usage()
            sys.exit()
        elif opt in ['-p', '--parse']:
            options['parseFile'] = arg
        elif opt in ['-l', '--load']:
            options['infile'] = arg
    if not 'infile' in options:
        options['infile'] = '2015.dat'
    return options

def usage():
    print ("Usage:")

def getStatistics (infile, classifier = lambda record : True):
    db = {}
    for line in open(infile):
        l = line.split(',')
        key = classifier(l)
        if not key in db:
            db[key] = db_item()
        for i in range(1, 7):
            db[key][i][int(l[i])] += 1
    return db

def printHeader (s):
    print (
      "{:6}{:8}{:8}{:8}{:8}{:8}{:8}".format
      (s, "通識學分", "反對現行  ", "希望外文", "希望通識", "認為通識", "認為通識")
    )
    print (
      "{:6}{:8}{:8}{:8}{:8}{:8}{:8}".format
      (" "*11, " 過多   ", "五項度作法", "比例提高", "變三學分", "品質不好", "品質尚可")
    )

def render (db, filter = {True: '全校'}):
    for key in db:
        if key in filter:
            q1 = 100 * db[key][1][1] / sum(db[key][1])
            q2 = 100 * db[key][2][0] / sum(db[key][2])
            q3 = 100 * db[key][3][1] / sum(db[key][3])
            q4 = 100 * db[key][4][1] / sum(db[key][4])
            q5 = 100 * db[key][5][1] / sum(db[key][5])
            q6 = 100 * db[key][6][1] / sum(db[key][6])
            print (
              "{:8}{:.3f}      {:.3f}      {:.3f}      {:.3f}      {:.3f}      {:.3f}".format
              (filter[key], q1, q2, q3, q4, q5, q6)
            )

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

def parse (parseFile, parsed):
    f         = open (parseFile)
    reader    = csv.reader(f)
    response  = {'恰當':0, '通識學分過多':1, '外語學分過多':2, '其他':3}
    extract   = lambda row : [toASCII (row[1]), row[2], row[4], response[row[6]], row[8], row[10], row[11]]
    check     = lambda row : True if row[1].isdigit() and len(row[1]) == 7 else False
    sanitized = [ extract (row) for row in reader if check(row)]
    f.close()
    f         = open (parsed, 'wt')
    csvWrite  = csv.writer(f)
    for l in sanitized:
        csvWrite.writerow(l)
    f.close()
    return parsed

################################
# Main program Begins          #
################################
options = getOptions (sys.argv[1:])
infile = options['infile']
if 'parseFile' in options:
    parse (options['parseFile'], infile)
db_item = lambda : {1:[0, 0], 2:[0, 0], 3:[0, 0, 0, 0, 0], 4:[0, 0], 5:[0, 0], 6:[0, 0] }
printHeader ("主修科系")
# get result for the whole school
db_nctu = getStatistics (infile)
render (db_nctu)
# get result for each major (identified by 3rd and 4th digits in student ID)
majorKey = ['19'  , '11'  , '17'  , '12'  , '16'  , '10'  , '13'  , '15'  ]
majorID  = ['外文', '機械', '生科', '數學', '資工', '電機', '運管', '人社']
major    = dict (zip (majorKey, majorID))
db_major = getStatistics (infile, lambda record : record[0][2:4])
render (db_major, major)
# get result for each graduation class (identified by the first 2 digits of student ID)
printHeader ("入學年度")
gradKey = ['00' , '01' , '02' , '03']
gradID  = ['100學年', '101學年', '102學年', '103學年']
grad    = dict (zip (gradKey, gradID))
db_grad   = getStatistics (infile, lambda record : record[0][0:2])
render (db_grad, grad)
