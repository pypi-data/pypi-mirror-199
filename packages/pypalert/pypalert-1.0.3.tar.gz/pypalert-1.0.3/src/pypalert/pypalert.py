import socket
import struct
import time
from concurrent.futures import ThreadPoolExecutor
import sys




class ModbusData:
    def __init__(self, X, Y, Z, F, UT, SPS, scale):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.F = F
        self.UT = UT
        self.SPS = SPS
        self.scale = scale

Data = []
EXIT = ''
S303_3Axis=True

connect_success = False

pool = ThreadPoolExecutor(max_workers=2)
    

def connect(IP,port):
    global pool
    
    pool.submit(parallel_connect,IP,port)
    time.sleep(3)

def connect_exit():
    
    global EXIT
    EXIT ='EXIT'
    print("close")
        

def get_Now_UnixTime():
    global Data
    try:
        return Data[-1].UT                                  
    except :
        if(connect_success == True):
            print("Port Wrong, so Nothing in list")
        else:
            print("Connect Fail, so Nothing in list")
        
def get_Now_XAxis():
    global Data
    try:
        return Data[-1].X
    
    except :
        if(connect_success == True):
            print("Port Wrong, so Nothing in list")
        else:
            print("Connect Fail, so Nothing in list")
        
        
def get_Now_YAxis():
    global Data
    try:
        return Data[-1].Y
    
    except :
        if(connect_success == True):
            print("Port Wrong, so Nothing in list")
        else:
            print("Connect Fail, so Nothing in list")
        

def get_Now_ZAxis():
    global Data
    try:
        return Data[-1].Z
    
    except :
        if(connect_success == True):
            print("Port Wrong, so Nothing in list")
        else:
            print("Connect Fail, so Nothing in list")
        

def get_Now_FAxis():
    global Data
    global S303_3Axis
    if(S303_3Axis):
        print("Do not get the 4th Axis")
        
    else:
        try:
            return Data[-1].F
        
        except :
            if(connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
        

def get_Now_SPS():
    global Data
    try:
        return Data[-1].SPS
    
    except :
        if(connect_success == True):
            print("Port Wrong, so Nothing in list")
        else:
            print("Connect Fail, so Nothing in list")
        

def get_Now_Scale():
    global Data
    try:
        return Data[-1].scale
    
    except :
        if(connect_success == True):
            print("Port Wrong, so Nothing in list")
        else:
            print("Connect Fail, so Nothing in list")
        

def get_NsecondData(N):
    global Data
    global S303_3Axis
    #print("len(Data)" + str(len(Data)))
    if(N == 0):
        print("Don't input 0, return now Data")
        N = 1
    elif(len(Data)<N):
        print("Only have "+ str(len(Data)) + "Second Data")
        N = len(Data)
    elif(N >60):
        print("We only store 60s Data")    
    Xreturn = []
    Yreturn = []
    Zreturn = []
    Freturn = []
    UTreturn = []
    SPSreturn = []
    scalereturn = []
    try:
        for i in range(N):
            Xreturn.append(Data[len(Data)-N+i].X)
            Yreturn.append(Data[len(Data)-N+i].Y)
            Zreturn.append(Data[len(Data)-N+i].Z)
            UTreturn.append(Data[len(Data)-N+i].UT)
            SPSreturn.append(Data[len(Data)-N+i].SPS)
            scalereturn.append(Data[len(Data)-N+i].scale)
        if(S303_3Axis == False):
            Freturn.append(Data[len(Data)-N+i].F)
        
    except :
        if(connect_success == True):
            print("Port Wrong, so Nothing in list")
        else:
            print("Connect Fail, so Nothing in list")
    
    
    
    if(S303_3Axis):
        try:
            return Xreturn, Yreturn, Zreturn, UTreturn, SPSreturn, scalereturn
        
        except :
            if(connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")
    else:
        try:
            return Xreturn, Yreturn, Zreturn, Freturn, UTreturn, SPSreturn, scalereturn
        
        except :
            if(connect_success == True):
                print("Port Wrong, so Nothing in list")
            else:
                print("Connect Fail, so Nothing in list")



def parallel_connect(IP,port):
    global Data
    global EXIT
    global S303_3Axis
    global connect_success
    # 建立连接---发送连接请求
    arr = [0x01, 0x02, 0x00, 0x00, 0x00, 0x06, 0x01, 0x06, 0x00, 0xc0, 0x00, 0x10]
    link=struct.pack("%dB"%(len(arr)),*arr)

    try: 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e: 
        print ("Error creating socket: %s" % e) 
        sys.exit(1) 
     
    # Second try-except block -- connect to given host/port 
    try: 
        client.connect((IP,port))
    except socket.gaierror as e: 
        print ("Address-related error connecting to server: %s" % e) 
        sys.exit(1) 
    except socket.error as e: 
        print ("Connection error: %s" % e) 
        sys.exit(1) 
    
    print("connect success")
    connect_success = True
    client.send(link)
    while (EXIT != 'EXIT'):
        link1 = client.recv(24080)
        
        string = link1.hex()
        #print(string)

        #第一個    
        if('53594e43' in string):
            tmp=''
            #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' + str(datetime.now()))
            #print(string)
            tmp = tmp + string
            #print("-----T="+str(len(tmp)))  
            #XYZstorage(string[70:])
            CRC16 = tmp[-4:]
            #print(len(tmp))
            
            #header
            header =tmp[:94]
            UTime = header[30:32] + header[28:30] + header[26:28] + header[24:26] + header[22:24]  
            UTime = int(UTime, base=16)

            SPS = header[48:50] + header [46:48]
            SPS = int(SPS, base=16)
            
            scale = header [44:46] + header[42:44] + header [40:42] + header[38:40] 
            
            
            binary_number = bytes.fromhex(scale)
            
            scale = struct.unpack('!f', binary_number)[0]
            scale = format(scale,'.2f')
            #print("scale" + str(scale))

            #print(CRC16)
            XYZdata = tmp[94:-4]
            #print("XYZdata---------"+str(len(XYZdata)))
            #print(header[50:52])
            if(header[50:52] == '03'):
                S303_3Axis = True
            elif(header[50:52] == '04'):
                S303_3Axis = False

            if(S303_3Axis):
                xconnect, yconnect, zconnect = data_cut(XYZdata,S303_3Axis)
                Data.append(ModbusData(xconnect,yconnect,zconnect,'',UTime,SPS,scale))
            else:
                xconnect, yconnect, zconnect, fconnect = data_cut(XYZdata,S303_3Axis)
                Data.append(ModbusData(xconnect,yconnect,zconnect,fconnect,UTime,SPS,scale))

           
           
            if(len(Data)>60):
                del Data[0]
        

def data_cut(XYZstr,S303_3Axis):
    xdata_cut = []
    ydata_cut = []
    zdata_cut = []
    fdata_cut = []
    flag = 0
    #Little Endian 轉回正常
    XYZhex = ''
    #print(len(XYZstr))
    
    #每4個byte為一組處理
    for i in range(0, len(XYZstr), 8):
        XYZdecimal=0
        a = XYZstr[i:i+2]
        b = XYZstr[i+2:i+4]
        c = XYZstr[i+4:i+6]
        d = XYZstr[i+6:i+8]
        XYZhex = d+c+b+a
        #hex to decimal 
        if(len(XYZhex)==8):
            XYZdecimal=struct.unpack('>f',bytes.fromhex(XYZhex))[0]
        #print(type(XYZdecimal))
        #print(XYZhex)
        #print(XYZdecimal)
        
        #儲存進XYZ的陣列
        if(S303_3Axis):
            if(flag == 0):
                xdata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 1):
                ydata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 2):
                zdata_cut.append(XYZdecimal)
                flag = 0
        else:
            if(flag == 0):
                xdata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 1):
                ydata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 2):
                zdata_cut.append(XYZdecimal)
                flag = flag +1
            elif(flag == 3):
                zdata_cut.append(XYZdecimal)
                flag = 0
    
    
    #print("XYZstr: " + str(len(XYZstr)))
    if(S303_3Axis):
        return xdata_cut, ydata_cut, zdata_cut
    else:
        return xdata_cut, ydata_cut, zdata_cut, fdata_cut

#def main():
if __name__ == '__main__':
    #main()
    
    IP = '10.0.0.50'
    port = 502
    connect(IP,port)
    '''
    while True :
        #print("get_Now_UnixTime"+str(get_Now_UnixTime()))
        print("get_Now_XAxis"+str(len(get_Now_XAxis())))
        print("get_Now_YAxis"+str(len(get_Now_YAxis())))
        print("get_Now_ZAxis"+str(len(get_Now_ZAxis())))
        #print("get_Now_SPS"+str(get_Now_SPS()))
        #print("get_Now_Scale"+str(get_Now_Scale()))
        time.sleep(1)
    '''
    time.sleep(5)
    
    X,Y,Z,UT,SPS,scale=get_NsecondData(10)   
    print("get_UnixTime: "+str(len(UT)))
    print("get_XAxis: "+str(len(X)))
    print("get_YAxis: "+str(len(Y)))
    print("get_ZAxis: "+str(len(Z)))
    print("get_SPS: "+str(SPS))
    print("get_Scale: "+str(scale))
    #X,Y,Z,UT,SPS,scale=get_NsecondData(0)    

    #print(len(X))
    #print(len(X[0]))

    #for i in range(len(UT)):
        #print(X[i])    

    connect_exit()
    