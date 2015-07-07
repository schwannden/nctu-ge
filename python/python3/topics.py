topics   = []
topic    = lambda : {'title':'', 'classifier':'', 'filter':{}}

majorKey = ['19'  , '11'  , '17'  , '12'  , '16'  , '10'  , '13'  , '15'  ]
majorID  = ['外文', '機械', '生科', '數學', '資工', '電機', '運管', '人社']
new = topic()
new['title']      = '主修科系'
new['classifier'] = lambda record : record[0][2:4]
new['filter']     = dict (zip (majorKey, majorID))
topics.append(new)

new = topic()
gradKey  = ['00'     , '01'     , '02'     , '03'     ]
gradID   = ['100學年', '101學年', '102學年', '103學年']
new['title']      = '入學年度'
new['classifier'] = lambda record : record[0][0:2]
new['filter']     = dict (zip (gradKey, gradID))
topics.append(new)

