#***************************************************************************************************************************
#***************************************************************************************************************************
#Codigo: Ionograma Integraciones Coherentes forma autonoma 
#Version: 2.0
#Autor: Isaac Tupac
#Fecha: 20 de Enero del 2023
#Codigo para generar Ionogramas .png desde archivos .h5 adquiridos con el demodulador de Ionosonda 
#SDR implementado en GNU Radio Companion de manera autonoma para el canal 0. 
#Tambien almacena en formato NGI. 
#Unidades: Potencia (Db)
#IPP:10ms, Ancho de banda:10MHz, Frecuencia central:5MHz, steps:4, repeats:4, frecuencia de muestreo final:100kHz
#Proyecto= Receptor de ionosonda SDR 
#Radio Observatorio de Jicamarca-Universidad de Texas en Dallas
#Obs:
#Ch0: Ordinary (parallel)
#Se realizó el promedio de los valores complejos, luego se hallo el valor de potencia (abs(Ploteo)**2) y luego se pasó a Db
#Se comenzó el almacenamiento exactamente 1seg después que el PPS de Tx se origino
#******************************Exp1:Ipp=10000us,DH=15km,Tiempo=1segundo,freq=100freqs*****************************************
import h5py
import numpy as np
import matplotlib.pyplot as plt
import math
import os, time,glob
from datetime import datetime
import cmath
import netCDF4 as nc
from numpy import busday_count
from matplotlib.testing.jpl_units import sec

Escala=1/20000.0
#************Hora actual*************
now = datetime.utcnow()
'''
current_time = now.strftime("%d/%m/%Y-%H:%M:%S")

year=int(now.strftime("%Y"))
month=int(now.strftime("%m"))
day=int(now.strftime("%d"))
hour0=int(now.strftime("%H"))
minute=int(now.strftime("%M"))
second=int(now.strftime("%S"))

print("The storage time is :", str(month)+"/"+str(day)+"/"+str(year)+"-"+str(hour0)+":"+str(minute)+":"+str(second))

if month == 1 or month == 2 or month == 3:
    season = "Winter-EEUU"

elif month == 4 or month == 5 or month == 6:
    season = "Spring-EEUU"

elif month == 7 or month == 8 or month == 9:
    season = "Summer-EEUU"

elif month == 10 or month == 11 or month == 12:
    season = "Fall-EEUU"'''
#***********************************Lectura de los archivos de configuracion**************************************************
file0 = open('/home/soporte/Isaac/ProgrDemo/all_freq_list_10ms.txt','r')
f=file0.readlines()

file1 = open('/home/soporte/Isaac/ProgrDemo/time_settings_oct20.txt','r')
f1=file1.readlines()

file2 = open('/home/soporte/Isaac/ProgrDemo/freq_settings_oct20.txt','r')
f2=file2.readlines()
#***********************************Define el arreglo de frecuencias en freq*************************************************
freqT = [] # Lista vacia para almacenar los valores de frecuencia.
i=0
ArrayFreq=np.array([])
while i<len(f): #El valor de 100 sera cambiado.Tomara el valor de la cantidad de frecuencias en all_freq_list.txt
    fline=f[i]
    #Halla el valor de la frecuencia: convierte de string a float
    z= float(fline[24]+fline[25]+fline[26]+fline[27]+fline[28]+fline[29]+fline[30]+fline[31])
    if(i==0):
        zin=z/1000 #Frecuencia inicial almacencada en el archivo NGI   
    if(i==(len(f)-1)):
        zf=z/1000  #Frecuencia final almacenada en el archivo NGI
    z1=z*1000 #Valor en MegaHertz
    ArrayFreqT=z1/1000000 # Freq totales a guardar en NGI en decimales de MHz
    i=i+1
    freqT.append(z1)
    #print z1
print ("Las frecuencias adquiridas son: ",len(freqT))
print ("El valor de 1 es",zin)
print ("El valor de fin es",zf)

cont=0
m=0
ArrayFreq=np.array([])
while cont<len(f):   
    freq=float(f[cont][24]+f[cont][25]+f[cont][26]+f[cont][27]+f[cont][28]+f[cont][29]+f[cont][30]+f[cont][31]+f[cont][32])
    #print(freq)
    a=np.append(ArrayFreq,freq)
    ArrayFreq=a 
    cont=cont+1
    if(cont%4==0):
        m=m+1
        cont=16*m

print("El valor de ArrayFreq es:",len(ArrayFreq))

#***********************************Define IPP, DH **************************************************************************
#Define el Ipp en kms
Ipp=f1[1] #string IPP
Ippus= int(Ipp[4]+Ipp[5]+Ipp[6]+Ipp[7]+Ipp[8]) #valor IPP entero
#print Ippus
Ippkm=(Ippus*0.3)/1
print ("El valor del Ipp es: ",Ippkm,"km")
HoldOff=float(f1[13][8]+f1[13][9]+f1[13][10]+f1[13][11]) #string IPP
print("El valor de HoldOff es:",HoldOff)
width=int(f1[15][6]+f1[15][7])

#Define la resolucion: Necesitamos la frecuencia decimada (10KHz en este caso= 10000 muestras por segundo)
Decimacion=100000 #frecuencia final decimada (PONER A MANO)
MuestrasIpp=(Ippus*0.000001*Decimacion) #Numero de muestras en un Ipp
#Decimacion de GNU Radio
Resolucionkm=(Ippkm/MuestrasIpp)
print ("El valor de la resolucion es: ",Resolucionkm,"km")

#***********************************Lectura del archivo de datos demodulados en hdf5 ****************************************
parent="/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal0" ###2canales 10MHZ
parent1="/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal1"

#parent="/home/soporte/Isaac/PruebaData" ###2canales 10MHZ
#parent1="/home/soporte/Isaac/PruebaData1"

count_chan=0

while(count_chan<2):
    if(count_chan==1):
        parent=parent1

    subdr=max(glob.glob(os.path.join(parent,'*')),key=os.path.getmtime)
    
    print(subdr)

    listOfFiles = list()
    for (dirpath, dirnames, filenames) in os.walk(subdr):  #Crea una lista de archivos en todos los subdirectorios bajo de "parent"
        listOfFiles += [os.path.join(dirpath, file) for file in filenames]
    
    NumElem=len(listOfFiles)
    print("La longitud de ListPath es:",NumElem)
    #print("La Listof files es:", listOfFiles)
    print("Pointer1")
    listOfFiles.sort()
    print("La list of files es:",listOfFiles)
    print("Pointer2")
    
    if(count_chan==0):
        path_metadata=listOfFiles[(NumElem-2)] # Direcction donde se encuntra la metadata del Epoch
        print("La metadata 0 del epoch es:",path_metadata)
    if(count_chan==1):
        path_metadata_1=listOfFiles[(NumElem-2)]  
        print("La metadata 1 del epoch es:",path_metadata) 

    #Borra los archivos de metada encontrados. Esto varia dependiendo del experimento. Verificar!!!
    listOfFiles.remove(listOfFiles[len(listOfFiles)-1])
    listOfFiles.remove(listOfFiles[len(listOfFiles)-1])
    listOfFiles.remove(listOfFiles[len(listOfFiles)-1])
    #listOfFiles.remove(listOfFiles[len(listOfFiles)-1])
    print("Estoy antes del while -1")
    NumElem=len(listOfFiles)
    print("La longitud de listOfFiles o duracion de la recepcion es:",NumElem)
    #print(listOfFiles)
    
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


    print("Estoy antes del while 0")
    ArregloData=[]
    ArrayAbsolxseg=[]
    m=0
    indc=0
    print("Estoy antes del while")
    
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
    
    '''
    while m<NumElem:
        with h5py.File(listOfFiles[m]) as hdf: #(Adecuado)
            ls = list(hdf.keys())
            # print("Los keys son:",ls)
            dataset=hdf.get("rf_data")
            #    print("El tipo de dato (bytes Real(32B)+Imag(32B)) es:",dataset1.dtype)
            data0=np.array(dataset)
            #    ArregloData.append(data)
            #sd=data.shape
            #   print(sd)
            #   print(data1)
            data=data0/Escala
            #***********************************Divide los arreglos de muestra por frecuencias y determina la matriz de ploteo************************
            #    ValoresAbs=abs(data) #hallamos los valores absolutos de las muestras para graficarlos en el Ionograma
            MuestrasTotal=len(data)
            #        print ("Las muestras totales por segundo son:",MuestrasTotal)
            divid= int(MuestrasTotal/MuestrasIpp) #Cantidad de segmentos (Ipp's)
            #        print ("La cantidad de divisiones son:",divid) 
            
            #ArrayAbs=data.reshape((divid,int(MuestrasIpp))) #Arreglo dvidido en #muestras por IPP para 1 segundo
            #ArrayAbsolxseg.append(ArrayAbs)
            #print ("El arreglo ArrayAbs[0] es:",ArrayAbs[0])
            #m=m+1
                
            
            #Agregado por si el ultimo segundo de almacenamiento viene corrompido (Segundo 20)
            #OBS: El eco se adquiere hasta el segundo 18 
            if(divid==100):
                if (m==(NumElem-2) and indc==1):
                    print("Reemplazando ultimo arreglo por uno anterior")
                    #data=np.zeros(100000,dtype=np.complex64)
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
            else:
                if(m==(NumElem-1) and indc==0):
                    m=NumElem-2;
                    indc=1; '''           
            #Adq cada minuto (se duplica el ultimo segundo ya que llega corrompido)
            #'''if(m==18 and indc==0):
            # m=17;
            # indc=1;
            #if(m==18 and indc==1):
            # m=19;'''
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
    while p<(NumElem*divid):
        ArrayAbsTotal[p]=ArrayAbsolxseg[j][iterT]      
        p=p+1
        iterT=iterT+1
        if (p%divid)==0:
            j=j+1 
            iterT=0
   
    print ("La longitud de ArrayAbsTotal es:",len(ArrayAbsTotal))
    #print ("El valor de ArrayAbsTotal es:",ArrayAbsTotal)
    
    #************************************Logica separacion de grupos de 4***************************************************
    #******************************Agregar codigo dependiendo del residuo a encontrar***************************************
    fsource=int(f2[1][7])
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
    
    #************************************************** Matriz en unidades de Db *****************************************************************
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
            #    if(ValorProm[zi]==0):
            #        valor1[zi]=0.000001
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
    
    if(count_chan==0):
        PloteoCh0=PloteoCoherente
    if(count_chan==1):
        PloteoCh1=PloteoCoherente   
    #********************************************* Matriz en unidades de SNR**************************************************
    mi=1
    ni=0
    qi=0

    ValorPromSNR=[]
    ValorPromSNRdb=[]

    ValoresSNR=[]
    ValorPromSNR=[]

    zi=0
    ki=0
    print("El valor de longitud de ArrayAbsTotal[0] fue:", len(ArrayAbsTotal))
    while ni<DivGrupos_4:
        while qi>-4:
            valor1=ArrayAbsTotal[((Step*mi)-(4+qi))+(16*ni)]
            valor2=ArrayAbsTotal[((Step*(mi+1))-(4+qi))+(16*ni)]
            valor3=ArrayAbsTotal[((Step*(mi+2))-(4+qi))+(16*ni)]
            valor4=ArrayAbsTotal[((Step*(mi+3))-(4+qi))+(16*ni)]
            #        print("el valor de valor1 es:",valor1)

            powerW1=valor1*(np.conjugate(valor1)) #potencia Watt
            powerW2=valor2*(np.conjugate(valor2)) #potencia Watt
            powerW3=valor3*(np.conjugate(valor3)) #potencia Watt
            powerW4=valor4*(np.conjugate(valor4)) #potencia Watt
            #        print("El valor de powerW1 es:",powerW1)
            #        print("La longitud de powerW1 es:",len(powerW1))    
       
            #array20msSinEco=powerW[1000:1994]
            #array20msSinEco1=powerW1[750:994]
        
            #        array20msSinEco1=powerW1[1650:1884]
            #        array20msSinEco2=powerW2[1650:1884]
            #        array20msSinEco3=powerW3[1650:1884]
            #        array20msSinEco4=powerW4[1650:1884]
            array20msSinEco1=powerW1[0:len(ArrayAbsTotal[0])-1]
            array20msSinEco2=powerW2[0:len(ArrayAbsTotal[0])-1]
            array20msSinEco3=powerW3[0:len(ArrayAbsTotal[0])-1]
            array20msSinEco4=powerW4[0:len(ArrayAbsTotal[0])-1]

            #        print("El valor de array20msSinEco1 es:",array20msSinEco1)

            #NivelRuidoPot=array20msSinEco.max()
            #print("El nivel de ruido de la potencia es:",NivelRuidoPot)

            NivelRuidoProm1=array20msSinEco1.mean()
            NivelRuidoProm2=array20msSinEco2.mean()
            NivelRuidoProm3=array20msSinEco3.mean()
            NivelRuidoProm4=array20msSinEco4.mean()
            #        print("El nivel de ruido promedio es:",NivelRuidoProm1)

            #SNR= (NivelRuidoProm-array20msSinEco)/array20msSinEco
            SNR1=(powerW1-NivelRuidoProm1)/NivelRuidoProm1
            SNR2=(powerW2-NivelRuidoProm2)/NivelRuidoProm2
            SNR3=(powerW3-NivelRuidoProm3)/NivelRuidoProm3
            SNR4=(powerW4-NivelRuidoProm4)/NivelRuidoProm4
            #print("El valor de SNR3(W) es:",SNR3)  
             
            ValorPromSNR=(SNR1+SNR2+SNR3+SNR4)/2
            #       print("El valor de ValorPromSNR es:",ValorPromSNR)
            ValorPromSNRreal=ValorPromSNR.real
       
            while (zi<len(ValorPromSNR)):
                if(ValorPromSNRreal[zi]==0):
                    ValorPromSNRreal[zi]=0.000001
                    print("Se encontró un valor 0")
                Valordb=10*math.log((ValorPromSNRreal[zi]**2),10)
                #           ArregloDatadbm4.append(Valoresdbm4)
                ValorPromSNRdb.append(Valordb)#Array promedio por Ipp
                zi=zi+1                    #Promedio de arrays por IPP de frecuencia defin.      
            qi=qi-1
            zi=0
        if (qi==-4):
            ni=ni+1    
            qi=0
       
    print("La longitud de ValoresSNR2 es:",len(ValorPromSNRdb))

    c0=np.array(ValorPromSNRdb)
    PloteoCoherente=c0.reshape(int(prim_grup),int(MuestrasIpp))

    if(count_chan==0):
        PloteoSNRCh0=PloteoCoherente
    if(count_chan==1):
        PloteoSNRCh1=PloteoCoherente 
                
    count_chan=count_chan+1      

#***********************Cambio de orden de atras hacia adelante y transpuesta del primer grupo de frecuencias****************** 
'''
#**Transpuesta del arreglo debido a que al plotear lo hace punto por punto de arreglos sucesivos y no de un mismo arreglo***********
Ploteo=np.transpose(PloteoCoherente)
#Ploteo=np.transpose(ArrayIpp)
print ("La matriz a plotear es:",Ploteo)
print ("La longitud de la matriz a plotear es:",len(Ploteo))
print ("La longitud de cada elemento de la matriz a plotear es:",len(Ploteo[0]))
'''
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

#print ("Los puntos de las frecuencias a plotear del eje X son: ",PuntosX)
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

#************************************************Ploteo pcolormesh***********************************************************
'''plt.title("Height vs Frecuency (dB)\n UTC Integraciones Coherentes - O: "+str(month)+"/"+str(day)+"/"+str(year)+"-"+str(hour0)+":"+str(minute)+":"+str(second))
#plt.title("Height vs Frecuency (dBm) \n Time : 11/28/2022-22:03:30")
#plt.title("Height vs Frecuency (Vrms)\n UTC Time : 11/28/2022-22:03:30")
plt.xlabel('Freq(MHz)') 
plt.ylabel('Kilometers(Km)')

if((1<=hour0<=13)): #8pm-8am Debe ser correlacionado con el crontab
    #plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=48,vmax=58)#fc=5MHz
    plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=52,vmax=62)#fc=5MHz
else:
    plt.pcolormesh(EjesXMHz,EjesY,Ploteo,vmin=35,vmax=56)#fc=10MHz

plt.colorbar()
'''
# plt.savefig("/home/soporte/Isaac/Ionogramas/Canal0/IonoDb/Ionograma.png") #2 canales 10MHz rev

#************************************************ Epoch leída del Metadata *************************************************
FileNetCDF4= nc.Dataset(path_metadata,"r")
#FileHdf5=nc.Dataset(pathHdf5,"r")
FileNetCDF4_1= nc.Dataset(path_metadata_1,"r")

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
Var_group_1=FileNetCDF4_1.groups
print("El grupo es:\n",Var_group)
print("*************************************************")
Var_groupList=list(FileNetCDF4.groups)
Var_groupList_1=list(FileNetCDF4_1.groups)
print("El primer valor de la lista grupo es:\n",Var_groupList[0])
print("*************************************************")
Groupint=Var_group[Var_groupList[0]]
Groupint_1=Var_group_1[Var_groupList_1[0]]
print("El interior del grupo es:",Groupint)
print("*************************************************")
print("La dimension del grupo 1010 es:",Groupint.dimensions)
print("*************************************************")
print("Las variables del grupo 1010 es:",Groupint.variables)
print("*************************************************")
#print("El valor de metadata es:",Groupint.variables['valorUTC'][:])

bandwidth=Groupint.variables['bandwidth'][:]
centFreq=Groupint.variables['centerFreq'][:]
centFreq_1=Groupint_1.variables['centerFreq'][:]
decimation=Groupint.variables['decimation'][:]
filtTap=Groupint.variables['filterTaps'][:]
sampRate=Groupint.variables['samp_rate'][:]
storFreq=Groupint.variables['storFreq'][:]

Latitud=Groupint.variables['Latitud'][:]
Lat_ind=Groupint.variables['Lat_ind'][:]
Longitud=Groupint.variables['Longitud'][:]
Long_ind=Groupint.variables['Long_ind'][:]

print("**********************************")
print("El valor de centFreq es:",centFreq)
print("**********************************")
print("**********************************")
print("El valor de centFreq_1 es:",centFreq_1)
print("**********************************")


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

nowJul= datetime(year,month,day) #Para saber el dia Juliano
DiaJul= nowJul.strftime('%j')

print("The storage time is :", str("%02d" %month)+"/"+str("%02d" %day)+"/"+str(year)+"-"+str("%02d" %hour0)+":"+str("%02d" %minute)+":"+str("%02d" %second))
#************************************************ Almacenamiento en formato NGI *********************************************
groop_root=nc.Dataset("/media/soporte/HardDisk/DataNGI/DataNow/HY0JM_"+str(year)+str(DiaJul)+str("%02d" %hour0)+str("%02d" %minute)+str("%02d" %second)+".ngi","w")
#***********Atributos de metadata *************
#groop_root.format_version="1.0"
groop_root.id="ionogram.HY0JM_"+str(year)+str(DiaJul)+str("%02d" %hour0)+str("%02d" %minute)+str("%02d" %second) # NombreArchivo
groop_root.metadata_link="path hacia el pdf de metadatas del servidor" #pdf en el servidor
groop_root.title="Ionosonde Data"
groop_root.station_location= "Huancayo"
groop_root.instrument="SDR Receiver"
groop_root.processing_level="Power average"
groop_root.date_created=str(year)+"-"+str("%02d" %month)+"-"+str("%02d" %day)+"T"
groop_root.time_acquisition_start=str("%02d" %hour0)+":"+str("%02d" %minute)+":"+str("%02d" %second)+"Z"
groop_root.time_acquisition_end=str("%02d" %hour0)+":"+str("%02d" %minute)+":"+str(second+NumElem)+"Z"
groop_root.acquisition_duration="TM00S"+str(NumElem)
groop_root.institution="Jicamarca Radio Observatory"
groop_root.creators_names="B.Eng.Isaac Tupac, D.Sc.Marco Milla"
groop_root.creators_emails="itupac@igp.gob.pe, milla.ma@pucp.edu.pe"
groop_root.contributor_name="D.Sc Cesar Valladares"
groop_root.contributor_role="University of Texas at Dallas researcher"
groop_root.contributor_email="cesar.valladares@utdallas.edu"
groop_root.project="Peruvian Oblique SDR Receivers Network"
groop_root.publisher_name="Jicamarca Radio Observatory"
groop_root.publisher_email="roj@igp.gob.pe"
groop_root.publisher_url="path del servidor de Jicamarca"
groop_root.license="Public Domain"
groop_root.conventions="CF-1.10"
groop_root.keywords="Ionosonde,Software Defined Radio,Jicamarca"
groop_root.summary="This file contains ionogram data which can visualise in Virtual Range vs Frequency operation."
groop_root.comment="Two units are posible to see, Power(dB) and SNR (db),and in two polarizations, X and Y"
groop_root.history="Generated by WriteNCDF at %date_created%"

#********************************************Create Dimensions*******************************************
groop_root.createDimension('DIM25',25)
groop_root.createDimension('FreqsTable',None)
groop_root.createDimension('Freqs',None)
groop_root.createDimension('DIM4',4)
groop_root.createDimension('DIM5',5)
groop_root.createDimension('DIM_Freq',len(ArrayFreq))
groop_root.createDimension('DIM_Height',MuestrasIpp)
groop_root.createDimension('DIM_FiltTap',len(filtTap))
#groop_root.createDimension('DIMYEAR',None) Year no tiene dimension 

#********************************************Create Variables********************************************
j=0

Station_Name=groop_root.createVariable('Rx_station_name','S1',('DIM25'))
station="Huancayo"
for i in station:
    Station_Name[j]=i
    j=j+1
    #print (i)

Station_Name.description="Station Name"

year_var=groop_root.createVariable('Year','u2')
year_var[:]=year
year_var.units="UTC"

DayNumber_var=groop_root.createVariable('DayNumber','u2')
DayNumber_var[:]=DiaJul
DayNumber_var.description="Day of the year"
DayNumber_var.units="UTC"

Month_var=groop_root.createVariable('Month','u2')
Month_var[:]=month
Month_var.units="UTC"

Day_var=groop_root.createVariable('Day','u2')
Day_var[:]=day
Day_var.units="UTC"

Hour_var=groop_root.createVariable('Hour','u2')
Hour_var[:]=hour0
Hour_var.units="UTC"

Minute_var=groop_root.createVariable('Minute','u2')
Minute_var[:]=minute
Minute_var.units="UTC"

Second_var=groop_root.createVariable('Second','u2')
Second_var[:]=second
Second_var.units="UTC"

Epoch_var=groop_root.createVariable('Epoch','u4')
Epoch_var[:]=epochf
Epoch_var.description="UNIX epoch time"
Epoch_var.units="seconds since 1970-01-01 00:00:00 UTC"

X_PoDir_var=groop_root.createVariable('pointing_direction_1','S1',('DIM4'))
X_PoDir_var[0]='N'
X_PoDir_var[1]='E'
X_PoDir_var[2]='4'
X_PoDir_var[3]='5'
X_PoDir_var.description="First Pointing direction" 
X_PoDir_var.units="degrees"

O_PoDir_var=groop_root.createVariable('pointing_direction_2','S1',('DIM4'))
O_PoDir_var[0]='N'
O_PoDir_var[1]='W'
O_PoDir_var[2]='4'
O_PoDir_var[3]='5'
O_PoDir_var.description="Second Pointing direction"
O_PoDir_var.units="degrees"

RecLat_var=groop_root.createVariable('RecLat','f')
RecLat_var[:]=Latitud
RecLat_var.description="Receiver Station Latitude"
RecLat_var.units="2 first digits are degrees,the others minutes"

RecLatInd_var=groop_root.createVariable('RecLatInd','S1')
RecLatInd_var[:]=Lat_ind
RecLatInd_var.description="Receiver Station Latitude indicator"
RecLatInd_var.units= "[N:north, S=south, E=east, W=west]"

RecLon_var=groop_root.createVariable('RecLon','f')
RecLon_var[:]=Longitud
RecLon_var.description="Receiver Station Longitud"
RecLon_var.units="3 first digits are degrees,the others minutes"

RecLonInd_var=groop_root.createVariable('RecLonInd','S1')
RecLonInd_var[:]=Long_ind
RecLonInd_var.description="Receiver Station Longitud indicator"
RecLonInd_var.units= "[N:north, S=south, E=east, W=west]"

Pri_var=groop_root.createVariable('PRI','u4')
Pri_var[:]=Ippus
Pri_var.description="Pulse Repetition Interval"
Pri_var.units="microseconds"

Hight_0_var=groop_root.createVariable('Hight_0','f4')
Hight_0_var[:]=4.5
Hight_0_var.units="kilometers"
Hight_0_var.description="Initial hight of the transmition pulse"

StartFreq_var=groop_root.createVariable('First_Freq','f4')
StartFreq_var[:]=zin
StartFreq_var.description="First frequency"
StartFreq_var.units="megahertz"

Last_var=groop_root.createVariable('Last_Freq','f4')
Last_var[:]=zf
Last_var.description="Last frequency"
Last_var.units="megahertz"

Tune_var=groop_root.createVariable('Tune_type','u1')
Tune_var[:]=fsource
Tune_var.description="tuning method"
Tune_var.units="flag"
Tune_var.flag_values="[1 2 3]"
Tune_var.flag_meanings="1=log 2=linear 3=table"

FreqCount_var=groop_root.createVariable('Freq_count','i4')
FreqCount_var[:]=(len(f)/(Repe*Step))*Step
FreqCount_var.description="number of base frequencies"
FreqCount_var.units="count"

Log_step_var=groop_root.createVariable('Log_step','f4')
Log_step_var[:]=Repe
Log_step_var.description="Logarithmic tuning step"
Log_step_var.units="percent"

Rx_count_var=groop_root.createVariable('Rx_count','u2')
Rx_count_var[:]=2
Rx_count_var.description="Number of receiver antennas"

Rx_antenna_type_var=groop_root.createVariable('Rx_antenna_type','S1',('DIM4'))
Rx_antenna_type_var[0]='L'
Rx_antenna_type_var[1]='O'
Rx_antenna_type_var[2]='O'
Rx_antenna_type_var[3]='P'
Rx_antenna_type_var.description="Receiver antennas type"

Rx_height_var=groop_root.createVariable('Rx_height','u2')
Rx_count_var[:]=3
Rx_height_var.description="Receiver antenna height above ground"
Rx_height_var.units="meters"

Rx_height_var=groop_root.createVariable('Rx_cable_length','u2')
Rx_count_var[:]=39
Rx_height_var.description="Lenght of the receiver cables"
Rx_height_var.units="meters"

Clock_type_var=groop_root.createVariable('Clock_type','S1',('DIM5'))
Clock_type_var[0]='G'
Clock_type_var[1]='P'
Clock_type_var[2]='S'
Clock_type_var[3]='D'
Clock_type_var[4]='O'
Clock_type_var.description="Source of the time for the receiver"

Pri_count_var=groop_root.createVariable('Pri_count','u2')
Pri_count_var[:]=len(f)
Pri_count_var.description="Number of pulse repetition intervals"

Holdoff_var=groop_root.createVariable('Holdoff','u2')
Holdoff_var[:]=HoldOff
Holdoff_var.description="Time between Tx GPS reference and the transmition pulse"
Holdoff_var.units="microseconds"

Pulse_width_var=groop_root.createVariable('Pulse_width','u2')
Pulse_width_var[:]=width
Pulse_width_var.description="Width of the frecuency pulse transmitted (pure signal)"
Pulse_width_var.units="microseconds"

Table_freq_var=groop_root.createVariable('Table_freq','f4',('FreqsTable'))
Table_freq_var[:]=ArrayFreqT
Table_freq_var.description="Table frequency"
Table_freq_var.units="units"

Nomin_freqs_var=groop_root.createVariable('Nomin_freqs','f4',('Freqs'))
Nomin_freqs_var[:]=ArrayFreq
Nomin_freqs_var.description="Nominal frequencies"
Nomin_freqs_var.units="units"

#******Resolution
High_resolution_var=groop_root.createVariable('High_resolution','f4')
High_resolution_var[:]=Resolucionkm
High_resolution_var.description="High resolution"
High_resolution_var.units="kilometers"

Freq_step_var=groop_root.createVariable('Freq_step','u2')
Freq_step_var[:]=Step
Freq_step_var.description="Frequency step"
Freq_step_var.units="units"

Freq_rep_var=groop_root.createVariable('Freq_rep','u2')
Freq_rep_var[:]=Repe
Freq_rep_var.description="Frequency repetition"
Freq_rep_var.units="units"

#Tx_Rx_DifTime_var=groop_root.createVariable('Tx_Rx_DifTime','u1')
#Tx_Rx_DifTime_var[:]=1
#Tx_Rx_DifTime_var.description="Time difference between transmition and reception"
#Tx_Rx_DifTime_var.units="seconds"

Rx_chan_var=groop_root.createVariable('Rx_chan','u1')
Rx_chan_var[:]=2
Rx_chan_var.description="Number de reception channels"
Rx_chan_var.units="units"

Acq_freq_var=groop_root.createVariable('Acq_freq','f4')
Acq_freq_var[:]=sampRate
Acq_freq_var.description="Acquisition Frequency"
Acq_freq_var.units="megaHertz"

Center_freq_var=groop_root.createVariable('Cent_freq_NW45','f4')
Center_freq_var[:]=centFreq
Center_freq_var.description="Center Frequency of acquisition (fc) for the NW45° direction"
Center_freq_var.units="megaHertz"

Center_freq_var_1=groop_root.createVariable('Cent_freq_NE45','f4')
Center_freq_var_1[:]=centFreq_1
Center_freq_var_1.description="Center Frequency of acquisition (fc) for the NE45° direction"
Center_freq_var_1.units="megaHertz"

Bandwidth_var=groop_root.createVariable('Bandwidth','u2')
Bandwidth_var[:]=bandwidth
Bandwidth_var.description="Frequency bandwidth([-WB/2-fc-WB/2])"
Bandwidth_var.units="megaHertz"

Decimation_var=groop_root.createVariable('Decimation','u2')
Decimation_var[:]=decimation
Decimation_var.description="Decimation"
Decimation_var.units="units"

Storage_freq_var=groop_root.createVariable('Storage_freq','f4')
Storage_freq_var[:]=storFreq
Storage_freq_var.description="Storage frequency"
Storage_freq_var.units="megaHertz"

j=0
Number_taps_var=groop_root.createVariable('Number_taps','u2',('DIM_FiltTap'))
for i in filtTap:
    Number_taps_var[j]=i
    j=j+1
Number_taps_var.description="Taps number"
Number_taps_var.units="units"

Has_NW_45_power=groop_root.createVariable('Has_NW_45_power','u1')
Has_NW_45_power[:]=1
Has_NW_45_power.description="Flag indicating presence of NW45° power data"
Has_NW_45_power.flag_values="[0 1]"
Has_NW_45_power.flag_meanings="0 = data_absent, 1 = data_present"

NW_45_power_var=groop_root.createVariable('NW_45_power','f4',('DIM_Freq','DIM_Height'))
NW_45_power_var[:]=PloteoCh0
NW_45_power_var.description="Profile power in the NW45° direction"
NW_45_power_var.units="Decibel"

Has_NE_45_power=groop_root.createVariable('Has_NE_45_power','u1')
Has_NE_45_power[:]=1
Has_NE_45_power.description="Flag indicating presence of NE45° power data"
Has_NE_45_power.flag_values="[0 1]"
Has_NE_45_power.flag_meanings="0 = data_absent, 1 = data_present"

NE_45_power_var=groop_root.createVariable('NE_45_power','f4',('DIM_Freq','DIM_Height'))
NE_45_power_var[:]=PloteoCh1
NE_45_power_var.description="Profile power in the NE45° direction"
NE_45_power_var.units="Decibel"

Has_NW_45_SNR=groop_root.createVariable('Has_NW_45_SNR','u1')
Has_NW_45_SNR[:]=1
Has_NW_45_SNR.description="Flag indicating presence of NW45° SNR power data"
Has_NW_45_SNR.flag_values="[0 1]"
Has_NW_45_SNR.flag_meanings="0 = data_absent, 1 = data_present"

NW_45_SNR_var=groop_root.createVariable('NW_45_SNR','f4',('DIM_Freq','DIM_Height'))
NW_45_SNR_var[:]=PloteoSNRCh0
NW_45_SNR_var.description="Profile SNR in the NW45° direction"
NW_45_SNR_var.units="Decibel"

Has_NE_45_SNR=groop_root.createVariable('Has_NE_45_SNR','u1')
Has_NE_45_SNR[:]=1
Has_NE_45_SNR.description="Flag indicating presence of NE45° SNR power data"
Has_NE_45_SNR.flag_values="[0 1]"
Has_NE_45_SNR.flag_meanings="0 = data_absent, 1 = data_present"

NE_45_SNR_var=groop_root.createVariable('NE_45_SNR','f4',('DIM_Freq','DIM_Height'))
NE_45_SNR_var[:]=PloteoSNRCh1
NE_45_SNR_var.description="Profile SNR in the NE45° direction"
NE_45_SNR_var.units="Decibel"


'''
Has_O_mode_power_var=groop_root.createVariable('Has_NO_mode_power','u1')
Has_O_mode_power_var[:]=1
Has_O_mode_power_var.description="Flag indicating presence of O power data"
Has_O_mode_power_var.flag_values="[0 1]"
Has_O_mode_power_var.flag_meanings="0 = data_absent, 1 = data_present"

O_mode_power_var=groop_root.createVariable('O_mode_power','f4',('DIM_Freq','DIM_Height'))
O_mode_power_var[:]=PloteoCoherente
O_mode_power_var.description="Ordinary mode power data"
O_mode_power_var.units="Decibel"'''

#Has_X_mode_power_var=groop_root.createVariable('Has_X_mode_power','u1')
#Has_X_mode_power_var[:]=1
#Has_X_mode_power_var.description="Flag indicating presence of X power data"
#Has_X_mode_power_var.flag_values="[0 1]"
#Has_X_mode_power_var.flag_meanings="0 = data_absent, 1 = data_present"

#X_mode_power_var=groop_root.createVariable('X_mode_power','f4',('DIM_Freq','DIM_Height'))
#X_mode_power_var[:]=
#X_mode_power_var.description="Extraordinary mode power data"
#X_mode_power_var.units="Decibel"

#Has_total_power_var=groop_root.createVariable('Has_total_power','u1')
#Has_total_power_var[:]=1
#Has_total_power_var.description="Flag indicating presence of power data"
#Has_total_power_var.flag_values="[0 1]"
#Has_total_power_var.flag_meanings="0 = data_absent, 1 = data_present"

Has_doopler_var=groop_root.createVariable('Has_doopler','u1')
Has_doopler_var[:]=0
Has_doopler_var.description="Flag indicating presence of doopler data"
Has_doopler_var.flag_values="[0 1]"
Has_doopler_var.flag_meanings="0 = data_absent, 1 = data_present"

Has_coherence_var=groop_root.createVariable('Has_coherence','u1')
Has_coherence_var[:]=1
Has_coherence_var.description="Flag indicating presence of coherence data"
Has_coherence_var.flag_values="[0 1]"
Has_coherence_var.flag_meanings="0 = data_absent, 1 = data_present"

print(groop_root)
print("************************************")
Var_Dim=groop_root.dimensions
for dim in groop_root.dimensions.values():
    print(dim)
print("Las cantidad de dimensiones son:\n",len(Var_Dim))

Var_variable=groop_root.variables
for dim in groop_root.variables.values():
    print(dim)
#print("Las variables son:\n",Var_variable)

print("************************************")
Variale_pri=groop_root['NW_45_power']
print(Variale_pri)
#Variale_pri=groop_root['Has_total_power'][:]
#print(Variale_pri)
print("Se creo el archivo NGI")
#************************************************Cerramos Files**************************************************************
#plt.show()

file0.close()
file1.close()
file2.close()
groop_root.close()
