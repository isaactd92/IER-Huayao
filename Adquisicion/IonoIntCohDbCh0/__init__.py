#***************************************************************************************************************************
#***************************************************************************************************************************
#Codigo: Ionograma Integraciones Coherentes forma autonoma 
#Version: 2.0
#Autor: Isaac Tupac
#Fecha: 09 de Enero del 2023
#Codigo para generar imagenes de Ionogramas .png desde una carpeta con archivos .h5 adquiridos con el demodulador de Ionosonda 
#SDR implementado en GNU Radio Companion de manera autonoma para el canal 0. 
#Unidades: Potencia (Db)
#IPP:10ms, Ancho de banda:10MHz, Frecuencia central:5MHz, steps:4, repeats:4, frecuencia de muestreo final:100kHz
#Proyecto= Receptor de ionosonda SDR 
#Radio Observatorio de Jicamarca-Universidad de Texas en Dallas
#Obs:
#Ch0: Ordinary (parallel)
#Se realizó el promedio de los valores complejos, luego se halló el valor de potencia (abs(Ploteo)**2) y luego se pasó a Db
#Se comenzó el almacenamiento exactamente 1seg después que el PPS de Tx se originó
#******************************Exp1:Ipp=10000us,DH=15km,Tiempo=1segundo,freq=100freqs*****************************************
import h5py,stat
import numpy as np
import matplotlib.pyplot as plt
import math
import os, time,glob
from datetime import datetime
import cmath
import netCDF4 as nc
from numpy import complex64

Escala=1/20000.0
#************Hora actual*************
'''now = datetime.utcnow()

current_time = now.strftime("%d/%m/%Y-%H:%M:%S")

year=int(now.strftime("%Y"))
month=int(now.strftime("%m"))
day=int(now.strftime("%d"))
hour0=int(now.strftime("%H"))
minute=int(now.strftime("%M"))
second=int(now.strftime("%S"))'''

#***********************************Lectura de los archivos de configuracion**************************************************
#file0 = open('/home/itupac/IsaacTupac/IONOSONDA/InforCesar/vipir_configuration/100freq.txt','r')
#file0 = open('/home/usuario/Isaac/Ionosonda/ArchivosConfig/vipir_configuration/100freq.txt','r')
#file0 = open('/home/usuario/Isaac/Ionosonda/ArchivosConfig/vipir_configuration/200freq.txt','r')
#file0 = open('/home/itupac/IsaacTupac/IONOSONDA/InforCesar/vipir_configuration/all_freq_list_5Mhz_15Mhz.txt','r')
#file0 = open('/home/itupac/IsaacTupac/IONOSONDA/InforCesar/vipir_configuration/all_freq_list_1Mhz_10Mhz_4st_4rp_bakcup.txt','r')
#file0 = open('/home/itupac/IsaacTupac/IONOSONDA/InforCesar/vipir_configuration/all_freq_list_1Mhz_10Mhz_4st_4rp.txt','r')
#file0 = open('/home/usuario/Isaac/ProgramasIonog/Eco10MHz/all_freq_list_160ms.txt','r')
#file0 = open('/home/usuario/Isaac/ProgramasIonog/Eco20MHz/all_freq_list_c.txt','r')
#file0 = open('/home/itupac/IsaacTupac/IONOSONDA/InforCesar/vipir_configuration/all_freq_list_Tot_160ms.txt','r')
file0 = open('/home/soporte/Isaac/ProgrDemo/all_freq_list_10ms.txt','r')
f=file0.readlines()
#print "La cantidad de lineas en 100freq.txt es: ",len(f)

#file1 = open('/home/usuario/Isaac/ProgramasIonog/Eco20MHz/time_settings_oct20.txt','r')
#file1 = open('/home/itupac/IsaacTupac/IONOSONDA/InforCesar/vipir_configuration/time_settings_oct20.txt','r')
file1 = open('/home/soporte/Isaac/ProgrDemo/time_settings_oct20.txt','r')
f1=file1.readlines()
#print "La cantidad de lineas en time_settings_oct20.txt texto es: ",len(f1)

#file2 = open('/home/usuario/Isaac/ProgramasIonog/Eco20MHz/freq_settings_oct20.txt','r')
#file2 = open('/home/itupac/IsaacTupac/IONOSONDA/InforCesar/vipir_configuration/freq_settings_oct20.txt','r')
file2 = open('/home/soporte/Isaac/ProgrDemo/freq_settings_oct20.txt','r')
f2=file2.readlines()
#***********************************Define el arreglo de frecuencias en freq*************************************************
freqT = [] # Lista vacia para almacenar los valores de frecuencia.
i=0
while i<len(f): #El valor de 100 sera cambiado.Tomara el valor de la cantidad de frecuencias en all_freq_list.txt
    fline=f[i]
    #Halla el valor de la frecuencia: convierte de string a float
    z= float(fline[24]+fline[25]+fline[26]+fline[27]+fline[28]+fline[29]+fline[30]+fline[31])
    z1=z*1000 #Valor en MegaHertz
    i=i+1
    freqT.append(z1)
    #print z1
print ("Las frecuencias adquiridas son: ",len(freqT))

#***********************************Define IPP, DH **************************************************************************
#Define el Ipp en kms
Ipp=f1[1] #string IPP
Ippus= int(Ipp[4]+Ipp[5]+Ipp[6]+Ipp[7]+Ipp[8]) #valor IPP entero
#print Ippus
Ippkm=(Ippus*0.3)/1
print ("El valor del Ipp es: ",Ippkm,"km")

#Define la resolucion: Necesitamos la frecuencia decimada (10KHz en este caso= 10000 muestras por segundo)
Decimacion=100000 #frecuencia final decimada (PONER A MANO)
MuestrasIpp=(Ippus*0.000001*Decimacion) #Numero de muestras en un Ipp
#print MuestrasSeg
Resolucionkm=(Ippkm/MuestrasIpp)
print ("El valor de la resolucion es: ",Resolucionkm,"km")

#***********************************Lectura del archivo de datos demodulados en hdf5 ****************************************
#parent="/home/itupac/IsaacTupac/IONOSONDA/DigitalRF/Prueba_VIPIR_USRP/Prueba10MHz_4steps_2seg_00/2022-02-23T21-00-00"
#parent="/home/usuario/Isaac/ProgramasIonog/Eco10MHz/Sync_10MHz_160ms_eco/2022-02-24T21-00-00"
#parent="/home/usuario/Isaac/ProgramasIonog/Eco20MHz/Sync_20MHz_160ms_eco/2022-02-24T22-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/DigitalRF/Prueba_VIPIR_USRP/Iono20MHz_corr/2022-03-04T16-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/DigitalRF/Prueba_VIPIR_USRP/Iono20MHz_Loop/2022-03-04T21-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/DigitalRF/Prueba_VIPIR_USRP/Iono20MHz_Valladares/2022-03-07T17-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/DigitalRF/Prueba_VIPIR_USRP/Prueba_nivel0_3/2022-03-09T13-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/DigitalRF/Prueba_VIPIR_USRP/Prueba_nivel0_3/2022-03-09T13-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/DigitalRF/Prueba_VIPIR_USRP/Sync_160ms_09_03_2022_Bien/2022-03-09T21-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/DigitalRF/Prueba_VIPIR_USRP/Prueba_4_4_20ms/2022-03-10T17-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/Adqui20ms_Loop/Adqui20ms_Loop_Amplif/2022-06-17T22-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/Adquisicion/Demod/Prueba5segExac/2022-11-28T22-00-00"
#parent="/home/itupac/IsaacTupac/IONOSONDA/PruebaAnchoBanda/DataDemod4_5_300m/2022-11-28T22-00-00"
#parent="/home/soporte/Isaac/ProgrDemo/DataDemod5segExact2/2022-11-28T22-00-00"

parent="/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal0" ###2canales 10MHZ

#parent="/home/soporte/Isaac/PruebaData"

subdr=max(glob.glob(os.path.join(parent,'*')),key=os.path.getmtime)

print(subdr)

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(subdr):  #Crea una lista de archivos en todos los subdirectorios bajo de "parent"
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    
'''
listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(parent):  #Crea una lista de archivos en todos los subdirectorios bajo de "parent"
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]'''

'''ListPath=[]
timeNow=time.time()   # actual seconds since the epoch  (SSE)
minDeltaTime=timeNow   # Inicializacion del tiempo
for fileT in listOfFiles:  # Barre todos los archivos de la lista creada arriba
    creationTime = os.path.getctime(fileT)    # fecha de creacion de cada archivo
    if timeNow-creationTime < minDeltaTime:    # Diferencia entre SSE actual y fecha del archivo
        newestFile = fileT                            
        ListPath.append(newestFile)
        minDeltaTime=timeNow-creationTime''' 

#    return newestFile

NumElem=len(listOfFiles)
print("La longitud de ListPath es:",NumElem)
#print( listOfFiles)
listOfFiles.sort()
print( listOfFiles)

path_metadata=listOfFiles[(NumElem-2)] # Direcction donde se encuntra la metadata del Epoch
print("La metadata del epoch es:",path_metadata)

#Borra los archivos de metada encontrados. Esto varia dependiendo del experimento. Verificar!!!
listOfFiles.remove(listOfFiles[len(listOfFiles)-1])
listOfFiles.remove(listOfFiles[len(listOfFiles)-1])
listOfFiles.remove(listOfFiles[len(listOfFiles)-1])
#listOfFiles.remove(listOfFiles[len(listOfFiles)-1])

NumElem=len(listOfFiles)
print("La longitud de listOfFiles es:",NumElem)
print(listOfFiles)

rev_metadata=listOfFiles[(NumElem-1)]
print("El path de revision metadata es:",rev_metadata) 

head_tail=os.path.split(rev_metadata)
print("El valor de head_tail[1] es:",head_tail[1])

# A veces GNU Radio genera dos archivos de metadata
# Posible pérdida de datos en la adquisición
while(head_tail[1][0]=="d" or head_tail[1][0]=="m"):
  print("Se almaceno como dato drf_properties.h5. Eliminando este archivo ...")
  listOfFiles.remove(rev_metadata)
  print("El nuevo listOfFiles es:",listOfFiles)
  NumElem=len(listOfFiles)
  print("La longitud de listOfFiles es:",NumElem)
  
  rev_metadata=listOfFiles[(NumElem-1)]
  print("El path de revision metadata es:",rev_metadata) 
  head_tail=os.path.split(rev_metadata)
  print("El valor de head_tail[1] es:",head_tail[1])
    
ArregloData=[]
ArrayAbsolxseg=[]
m=0
#indc=0
#indp=0
while m<NumElem:
    with h5py.File(listOfFiles[m]) as hdf: #(Adecuado)
        ls = list(hdf.keys())
    #    print("Los keys son:",ls)
        dataset=hdf.get("rf_data")
    #    print("El tipo de dato (bytes Real(32B)+Imag(32B)) es:",dataset1.dtype)
        data0=np.array(dataset)
    #    ArregloData.append(data)
        #sd=data.shape
    #   print(sd)
        #print("La longitud de data es:",len(data0))
        data=data0/Escala
        #print("El valor de data es:",data)
        print("*****************Comenzamos .......")
        #***********************************Divide los arreglos de muestra por frecuencias y determina la matriz de ploteo************************
    #    ValoresAbs=abs(data) #hallamos los valores absolutos de las muestras para graficarlos en el Ionograma
        MuestrasTotal=len(data)
        print ("Las muestras totales por segundo son:",MuestrasTotal)
        print ("Las muestras por IPP:",MuestrasIpp)
        divid= int(MuestrasTotal/MuestrasIpp) #Cantidad de segmentos (Ipp's)
        print ("La cantidad de divisiones son:",divid) 
        print("El valor de m es:",m)
        
        if(MuestrasTotal!=Decimacion):
            print("¡ALERTA!....Estamos perdiendo datos o recibiendo nan+jnan")
            print("La cantidad de ceros agragados es:",Decimacion-MuestrasTotal)
            arrayZeros=[[(0+0j)]]*(Decimacion-MuestrasTotal)
        print("El valor de data es:",data)
        
        print("el valor de divid es:",divid)

        #if(divid==100):#IPP=10ms 
        if(divid==50):#IPP=20ms      
            ArrayAbs=data.reshape((divid,int(MuestrasIpp))) #Arreglo dvidido en #muestras por IPP para 1 segundo
            print("La longitud de data es:",len(data))
            ArrayAbsolxseg.append(ArrayAbs)
            #print(ArrayAbsolxseg)
            #print ("El arreglo ArrayAbs[0] es:",len(ArrayAbs[0]))
            m=m+1;
            print("La cantidad de segundos desde 0 es:",m)
        else:
            dataC=np.concatenate((data,arrayZeros)) #arreglo completado con ceros
            #print(dataC)
            print("La longitud del arreglo 'data' completo es:",len(dataC))
            divid=int(len(dataC)/MuestrasIpp)
            print("El valor de divid es:",divid)
            ArrayAbs=dataC.reshape((divid,int(MuestrasIpp))) #Arreglo dvidido en #muestras por IPP para 1 segundo
            #print(ArrayAbs)
            ArrayAbsolxseg.append(ArrayAbs)
            #print(ArrayAbsolxseg)
            #print ("El arreglo ArrayAbs[0] es:",len(ArrayAbs[0]))
            m=m+1;
            print("La cantidad de segundos desde 0 es:",m)  
                  
                     
        ''' ArrayAbs=data.reshape((divid,int(MuestrasIpp))) #Arreglo dvidido en #muestras por IPP para 1 segundo
        ArrayAbsolxseg.append(ArrayAbs)
        print ("El arreglo ArrayAbs[0] es:",len(ArrayAbs[0]))
        m=m+1
        print (m)    '''    
        
        
        #Agregado por si el ultimo segundo de almacenamiento viene corrompido (Segundo 19-20)
        #OBS: El eco se adquiere hasta el segundo 18 
        '''if(divid==100):
            if (m==(NumElem-2) and indc==1):
                print("Reemplazando ultimo arreglo por uno anterior")
                #data=np.zeros(100000,dtype=np.complex64)
            if(indp!=0):
                data=np.zeros(100000,dtype=np.complex64)    
            ArrayAbs=data.reshape((divid,int(MuestrasIpp))) #Arreglo dvidido en #muestras por IPP para 1 segundo
            #print(ArrayAbs)
            ArrayAbsolxseg.append(ArrayAbs)
            #print(ArrayAbsolxseg)
            #print ("El arreglo ArrayAbs[0] es:",len(ArrayAbs[0]))
            m=m+1;
            print("La cantidad de segundos desde 0 es:",m)
            print("Si ",m,"menor que",(NumElem-1)," gpsdo desincronizado o USRP esta perdiendo datos (DD)")
            if(m==(NumElem-1) and indc==1):
              m=NumElem;
              print("Estoy dentro")
            if(indp!=0):
              m=m+indp
              indp=0
              if(indc==1):
                m=m+1
              print("El valor de m final es:",m)    
        else:
            if(m==(NumElem-1) and indc==0):
              m=NumElem-2
              indc=1
              print("Llegue al último segundo con perdida de datos")
            elif(m<NumElem):
              print("Estoy en una perdida de datos..")
              m=m-1
              print("el valor de m en perdida de datos es:",m)
              indp=indp+1
              print("El valor de indp es:",indp)'''
                          
        #Adq cada minuto (se duplica el ultimo segundo ya que llega corrompido)
        '''if(m==18 and indc==0):
         m=17;
         indc=1;
        if(m==18 and indc==1):
         m=19;'''
    
   
#print ("La longitud de ArrayAbsolTotal es:",len(ArrayAbsolTotal[0][0]))

#*************************** Pone todos las muestras por Ipp del experimento en el arreglo ArrayAbsTotal ****************************************
#ArrayAbsTotal=np.zeros(((18*divid),int(MuestrasIpp)))
ArrayAbsTotal=np.zeros(((NumElem*divid),int(MuestrasIpp)),dtype=np.complex64)

#ArrayAbsTotal[0]=ArrayAbs[0]
#print("El valor de ArrayAbsTotal es: ",ArrayAbsTotal)
#print("El valor de ArrayAbsTotal es: ",ArrayAbs[0])

print( len(ArrayAbsolxseg[0][0]))
print( len(ArrayAbsTotal[0]))
#ArrayAbsTotal[0]=ArrayAbsolxseg[0][0]
#print ArrayAbsTotal[0]

iterT=0
p=0
j=0
#ArrayAbsTotal=[]
#print(NumElem*divid)
#print(NumElem)
#print(divid)
while p<(NumElem*divid):
    ArrayAbsTotal[p]=ArrayAbsolxseg[j][iterT]      
    p=p+1
    #print(p)
    iterT=iterT+1
    if (p%divid)==0:
        j=j+1 
        iterT=0

   
print ("La longitud de ArrayAbsTotal es:",len(ArrayAbsTotal))
#print ("El valor de ArrayAbsTotal es:",ArrayAbsTotal)

#************************************Logica separacion de grupos de 4***************************************************
#******************************Agregar codigo dependiendo del residuo a encontrar***************************************
Repe=int(f2[13][8])
Step=int(f2[12][6])
DivGrupos_4=math.floor((len(f))/(Repe*Step)) # Agrupa las frecuencias en grupos de valores iguales
print ("La division de grupos es:",DivGrupos_4)
#print (Repe*Step)
residuo=(len(f))%(Repe*Step)
print ("El valor de residuo es:",residuo)

if(residuo<=Step):
    prim_grup=(DivGrupos_4*Step)+residuo #cantidad de frecuencias del primer ionograma a dibujar
    segu_grup=(DivGrupos_4)*Step
    terc_grup=(DivGrupos_4)*Step
    cuar_grup=(DivGrupos_4)*Step


if(residuo>Step & residuo<=2*Step):
    prim_grup=(DivGrupos_4*Step)+(residuo/2) #cantidad de frecuencias del primer ionograma a dibujar
    segu_grup=(DivGrupos_4)*Step+(residuo/2)
    terc_grup=(DivGrupos_4)*Step
    cuar_grup=(DivGrupos_4)*Step  
    
      
print ("El valor del prim_grup es:",prim_grup)
print ("El valor del seg_grup es:",segu_grup)
    
#*****************Arreglo de muestras de las primeras 4 frecuencias de grupos de cuatro*********************************

mi=1
ni=0
qi=0
ValoresCoherentes=[]
ValorPromdb=[]

zi=0
ki=0
print("El valor de longitud de ArrayAbsTotal[0] fue:", len(ArrayAbsTotal))
while ni<DivGrupos_4:
    while qi>-4:
        valor1=ArrayAbsTotal[((Step*mi)-(4+qi))+(16*ni)]
        valor2=ArrayAbsTotal[((Step*(mi+1))-(4+qi))+(16*ni)]
        valor3=ArrayAbsTotal[((Step*(mi+2))-(4+qi))+(16*ni)]
        valor4=ArrayAbsTotal[((Step*(mi+3))-(4+qi))+(16*ni)]
        ValorProm=(valor1+valor2+valor3+valor4)/2
        ValorPromabs=abs(ValorProm)
        while (zi<len(ValorProm)):
            if(ValorPromabs[zi]==0):
                ValorPromabs[zi]=0.000001
            Valordb=10*math.log((((ValorPromabs[zi]**2))),10)
    #           ArregloDatadbm4.append(Valoresdbm4)
            ValorPromdb.append(Valordb)#Array promedio por Ipp
            zi=zi+1                    
#        ValorProm=(np.array(ArregloDatadbm1)+np.array(ArregloDatadbm2)+np.array(ArregloDatadbm3)+np.array(ArregloDatadbm4))/4
    #  print ("dasdas",len(ValorProm))
#        ValoresCoherentes.append(ValorProm)
        qi=qi-1
        zi=0
    if (qi==-4):
        ni=ni+1    
        qi=0
       
print("La longitud de ValorProm es:",len(ValorProm))
print("La longitud de ValorPromabs es:",len(ValorPromabs))
print("La longitud de ValorPromdbm es:",len(ValorPromdb))
c0=np.array(ValorPromdb) 
PloteoCoherente=c0.reshape(int(prim_grup),int(MuestrasIpp)) 
        

#***********************Cambio de orden de atras hacia adelante y transpuesta del primer grupo de frecuencias****************** 

#**Transpuesta del arreglo debido a que al plotear lo hace punto por punto de arreglos sucesivos y no de un mismo arreglo***********
Ploteo=np.transpose(PloteoCoherente)
#Ploteo=np.transpose(ArrayIpp)
print ("La matriz a plotear es:",Ploteo)
print ("La longitud de la matriz a plotear es:",len(Ploteo))
print ("La longitud de cada elemento de la matriz a plotear es:",len(Ploteo[0]))

#Ploteo_2grup=np.transpose(ArrayIpp_2grup)
#print ("La longitud de la matriz Ploteo_2grup es:",len(Ploteo_2grup))
#print ("La longitud de cada elemento de la matriz Ploteo_2grup es:",len(Ploteo_2grup[0]))

#*********************************Ejes X y Ejes Y para el primer Ionograma ***************************************************
Repe=int(f2[13][8]) #Cantidad repetidas de frecuencias
#CantFreq=divid/Repe #FreqUtiliz=Numero de frecuencias totales/Cantidad de veces que se repiten frecuencias
#Subfreq0=((CantFreq-1)+4)/4
#Subfreq1= (4*Subfreq0)
#cantidad de frecuencias: step*Numero de subgrupos
Step=int(f2[12][6]) #Cantidad de frecuencias por grupo
#Subfreq1= Step*7 #(100/16=6+1=7)
#print ("La cantidad de frecuencias en el Ionograma :",Subfreq0)
#print ("La cantidad de frecuencias totales a dibujar en el primer Ionograma es:",prim_grup)

numpyFreq=np.array(freqT)
#print (len(numpyFreq)/Repe)
#print (Repe)
#Freq=numpyFreq.reshape((int(len(numpyFreq)/Repe),Repe)) #Divison del total de frecuencias en multiplos del valor de repeticion(repe)
Freq=numpyFreq.reshape((int(len(numpyFreq)/Repe),Step)) #Agrupacion de las 100 frecuencias en grupos de 4
print ("El 24avo grupo de cuatro frecuencias es:",len(Freq))

Pe=f2[3]
Percnt=float(Pe[8]+Pe[9]+Pe[10]) #Porcentaje entre frecuencias dado por el archivo de configuracion
#print ("El porcentaje de variacion entre frecuencias es:",Percnt)

j=0
PuntosX=[(Freq[0][0])*((100-(Percnt/2))/100)]#Almacenara todos los puntos de un solo eje X
print( "El primer valor del Ejex X es:",PuntosX)

#while j<452: #ultimo grupo de cuatros (cociente*4+1)
print( "El cociente es: ",(((len(f))//(Repe*Step))*4)+1)

#while j<((((len(f))//(Repe*Step))*4)+1-4):
while j<=(len(Freq)-4):     
    for k in [0,1,2,3]:
        Punto1=Freq[j][k]*((100+(Percnt/2))/100)# Punto medio entre las dos primeras frecuencias
        PuntosX.append(Punto1)
    j=j+4    

print ("El ultimo punto es: ",PuntosX[452])
print ("El total de puntos en el eje X es: ",len(PuntosX))

TotalPuntosEjeY=(Ippkm/Resolucionkm)+1 #Se agrag un punto mas por el (0,0)
print ("El total de puntos en el eje Y es: ",TotalPuntosEjeY)

m=0
EjesX=[] #Todos los puntos de los Ejes X en el Ionograma
while m<TotalPuntosEjeY: #TotalPuntosEjeY
    EjesX.append(PuntosX)
    m=m+1 
    
#print "El eje X es:",EjesX

EjesXMHz=(np.array(EjesX)/1000000) # valores del EjeX expresado en unidades de MHz


PuntosY1=[]
EjesY=[] #Todos los puntos de los Ejes Y
p=0
q=0
while q<TotalPuntosEjeY:
    while p<len(PuntosX):
        PuntosY1.append(Resolucionkm*q) # Puntos del cada Eje Y (15=RESOLUC:CAMBIAR A GENERAL)
        p=p+1
    EjesY.append(PuntosY1)
    PuntosY1=[]
    q=q+1    
    p=0
 
#print ("El valor de EjesXMHz es: ",EjesXMHz)
#print ("La longitud del EjesXMHz es:",len(EjesXMHz))
#print ("El valor de EjesY es: ",EjesY)
#print ("La longitud del EjeY es:",len(EjesY))

#************************************************ Epoch leída del Metadata *************************************************
FileNetCDF4= nc.Dataset(path_metadata,"r")
#FileHdf5=nc.Dataset(pathHdf5,"r")

print("*****************Metadata**********************************")
print(FileNetCDF4)
print("la cantidad de dimensiones son:",len(FileNetCDF4.dimensions))
print("la cantidad de variables son:",len(FileNetCDF4.variables))
print("*************************************************")
Var_Dim=FileNetCDF4.dimensions
print("Las dimensiones son:\n",Var_Dim)
print("*************************************************")
Var_variable=FileNetCDF4.variables
print("Las variables son:\n",Var_variable)
print("*************************************************")
Var_group=FileNetCDF4.groups
print("El grupo es:\n",Var_group)
print("*************************************************")
Var_groupList=list(FileNetCDF4.groups)
print("El primer valor de la lista grupo es:\n",Var_groupList[0])
print("*************************************************")
Groupint=Var_group[Var_groupList[0]]
print("El interior del grupo es:",Groupint)
print("*************************************************")
print("La dimension del grupo 1010 es:",Groupint.dimensions)
print("*************************************************")
print("Las variables del grupo 1010 es:",Groupint.variables)
print("*************************************************")
#print("El valor de metadata es:",Groupint.variables['valorUTC'][:])

epochf=float(Var_groupList[0][0:10])
print("El epoch es",epochf)

timeEpoch = datetime.utcfromtimestamp(epochf)
print("La hora UTC es:",timeEpoch)

year=int(timeEpoch.strftime("%Y"))
month=int(timeEpoch.strftime("%m"))
day=int(timeEpoch.strftime("%d"))
hour0=int(timeEpoch.strftime("%H"))
minute=int(timeEpoch.strftime("%M"))
second=int(timeEpoch.strftime("%S"))

#Transforma a día Juliano

tt = timeEpoch.timetuple()
dj = tt.tm_yday 
print("El dia Juliano es:",dj)

print("The storage time is :", str("%02d" %month)+"/"+str("%02d" %day)+"/"+str(year)+"-"+str("%02d" %hour0)+":"+str("%02d" %minute)+":"+str("%02d" %second))

if month == 1 or month == 2 or month == 3:
    season = "Winter-EEUU"

elif month == 4 or month == 5 or month == 6:
    season = "Spring-EEUU"

elif month == 7 or month == 8 or month == 9:
    season = "Summer-EEUU"

elif month == 10 or month == 11 or month == 12:
    season = "Fall-EEUU"

#************************************************Ploteo pcolormesh***********************************************************
plt.title("Ionogram Jicamarca-Huayao Polarization NW45° \n"+ str("%02d" %month)+"/"+str("%02d" %day)+"/"+str(year)+"-"+str("%02d" %hour0)+":"+str("%02d" %minute)+":"+str("%02d" %second)+" "+"UTC")
#plt.title("Height vs Frecuency (dBm) \n Time : 11/28/2022-22:03:30")
#plt.title("Height vs Frecuency (Vrms)\n UTC Time : 11/28/2022-22:03:30")
plt.xlabel('Frequency[MHz]') 
plt.ylabel('Virtual Distance[km]')

#plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=0,vmax=-37)#0.08 10MHz 
#plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=30,vmax=42)#-25 20MHz Dipolo
#plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=50,vmax=65)#-25 20MHz Dipolo
#plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=0,vmax=-35)#-25 20MHz Loop

#if((5<=hour0<14) or ((1<=hour0 and minute>=30)) or (2<=hour0<=4)): #00-9am / 8:30pm ->9:30 / 9pm-11pm (MAL) 
#if((1<=hour0)and(hour0<=11 and minute<=13)): #[8pm-6am] Debe ser correlacionado con el crontab
if((20<=hour0) or (hour0<=12)): #[5pm-7am] Debe ser correlacionado con el crontab  IPP=20ms    
    #plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=48,vmax=58)#fc=5MHz
    #plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=45,vmax=55)#fc=5MHz
    plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=0,vmax=40)#IPP=10ms 
else:
    #plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=0,vmax=40)#fc=6MHz Ipp=20ms
    plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=0,vmax=38)#Ipp=10ms 

plt.colorbar(label=f'Power [dB]')
#plott= plt.colorbar()#.set_labe()l('label', labelpad=-40, y=1.05, rotation=0)#(label=f'SNR[dB]')
#plott.ax.set_title('SNR[dB]')

#***********************Axis per IPP*******************************
#plt.axis([1.5969975,15.209909,0,2000]) # IPP=40ms
plt.axis([1.5969975,15.209909,0,3000])  # IPP=20ms

#fig.suptitle("Ionogramas")

#plt.savefig("/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Canal0/DB/Iono-"+str("%02d" %month)+"-"+str("%02d" %day)+"-"+str(year)+"-"+str("%02d" %hour0)+":"+str("%02d" %minute)+":"+str("%02d" %second)+"UTC"+".png") #2 canales 10MHz rev
plt.savefig("/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Canal0/DB/HYWJM"+"_"+str(year)+str(dj)+str("%02d" %hour0)+str("%02d" %minute)+str("%02d" %second)+"_PWR"+".png") #2 canales 10MHz rev
#plt.savefig("/home/soporte/Isaac/Pruebas/Ionograma/10_01_2023/canal0/IonoDb.png")
#plt.savefig("/home/soporte/Isaac/ComparCabl/RG8/Db.png") ##### 1 canales 20MHz
#plt.show()
#os.chmod("/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Canal0/DB/HY0JM"+"_"+str(year)+str(dj)+str("%02d" %hour0)+str("%02d" %minute)+str("%02d" %second)+"_PWR"+".png",stat.S_IRUSR)
    
#************************************************Cerramos Files**************************************************************
file0.close()
file1.close()
file2.close()