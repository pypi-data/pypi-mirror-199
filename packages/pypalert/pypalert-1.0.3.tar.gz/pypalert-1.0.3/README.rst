pip install pypalert

from pypalert import pypalert

#connect to S303 
pypalert.connect(IP,port)

#disconnect with S303
pypalert.connect_exit()

#get now Unixtime
pypalert.get_Now_UnixTime()

#get XAxis datas in this second
pypalert.get_Now_XAxis()

#get YAxis datas in this second
pypalert.get_Now_YAxis()

#get ZAxis datas in this second
pypalert.get_Now_ZAxis()

#get FAxis datas in this second
pypalert.get_Now_FAxis()

#get SPS in this second
pypalert.get_Now_SPS()

#get Scale in this second
pypalert.get_Now_Scale()

#get data in this N second
pypalert.get_NsecondData(N)
