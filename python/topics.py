# -*- coding: utf-8 -*-
from itertools import izip
topics   = []
topic    = lambda : {'title':'', 'classifier':'', 'filter':{}}

majorKey = ['19'  , '11'  , '17'  , '12'  , '16'  , '10'  , '13'  , '15'  ]
majorID  = [u'外文', u'機械', u'生科', u'數學', u'資工', u'電機', u'運管', u'人社']
new = topic()
new['title']      = u'主修科系'
new['classifier'] = lambda record : record[0][2:4]
new['filter']     = dict (izip (majorKey, majorID))
topics.append(new)

new = topic()
gradKey  = ['00'     , '01'     , '02'     , '03'     ]
gradID   = [u'100學年', u'101學年', u'102學年', u'103學年']
new['title']      = u'入學年度'
new['classifier'] = lambda record : record[0][0:2]
new['filter']     = dict (izip (gradKey, gradID))
topics.append(new)

