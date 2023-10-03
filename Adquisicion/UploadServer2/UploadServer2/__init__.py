#!/usr/bin/python

import os, shutil, time, glob, ftplib
#import time

URSI="HY0JM"

pathIonoNE = "/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Canal1"
pathIonoNW = "/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Canal0"
pathNGI="/media/soporte/HardDisk/DataNGI/DataNow"

pathComprPWR="/home/soporte/Isaac/AdquIonoSDR/DatosComprPWR"
pathComprNGI="/home/soporte/Isaac/AdquIonoSDR/DatosComprNGI"

dataNE=glob.glob(os.path.join(pathIonoNE,'*'))
dataNW=glob.glob(os.path.join(pathIonoNW,'*'))

lendata=len(dataNW)

IonoPNG_NE=[0,0]
HeaderPNG_NE=[0,0]

IonoPNG_NW=[0,0]
HeaderPNG_NW=[0,0]

TailDataNE=[0,0]
TailDataNW=[0,0]

i=0
j=0

ftp_host="lisn.igp.gob.pe"
ftp_user="itupac"
ftp_password="1pIzfK97EPbeXjnwEsiR"

path_list="/home/soporte/Isaac/DatosCompr/HY0JM_2023222040805.ngi.tar.gz"
path_download="/home/soporte/Isaac/DatosCompr/FTPDownload"

print("***********************************************************")
#Canal NE .png
for n in range(lendata):
    if os.path.exists(dataNE[n]) and os.path.isdir(dataNE[n]):
        print ("Buscando ionogramas en "+dataNE[n])
        IonogPWR=max(glob.glob(os.path.join(dataNE[n],'*')),key=os.path.getmtime) # List of files
        #print(len(IonogSNR))
        print("El archivo es:",IonogPWR)
        shutil.copy(IonogPWR,pathComprPWR)
                
        IonoPNG_NE[i]=IonogPWR
        print("El valor de IonoPNG_NE es:",IonoPNG_NE)
        
        ext=IonogPWR[-3:]  # file extension
        print("El valor de ext es:", ext)
                
        header=IonogPWR[-27:-8]  # first 19 characters e. JME1J_yyyydoyhhmmss
        print("El valor de header es",header)        
        
        HeaderPNG_NE[j]=header      
        print("El valor de HeaderPNG_NE es",HeaderPNG_NE)
               
        head_tail=os.path.split(IonoPNG_NE[i])
        
        tail=head_tail[1]
        print("El valor de tail es:",tail)
        
        TailDataNE[i]=tail
        print("El valor del arreglo de tails es:",TailDataNE)
                 
        i=i+1
        j=j+1
     
        print(i)
                
        if(i==2):
            i=0;
            j=0;
            
    else:
        print("No existe el directorio"+dataNE[n])
              

if(HeaderPNG_NE[0]!=HeaderPNG_NE[1]):
    print("Los archivos PNG no tienen la misma fecha")
    exit()
    
#Canal NW .png
for n in range(lendata):
    if os.path.exists(dataNW[n]) and os.path.isdir(dataNW[n]):
        print ("Buscando ionogramas en "+dataNW[n])
        IonogPWR=max(glob.glob(os.path.join(dataNW[n],'*')),key=os.path.getmtime) # List of files
        #print(len(IonogSNR))
        print("El archivo es:",IonogPWR)
        shutil.copy(IonogPWR,pathComprPWR)
        
        IonoPNG_NW[i]=IonogPWR
        print("El valor de IonoPNG_NW es:",IonoPNG_NW)
        
        ext=IonogPWR[-3:]  # file extension
        print("El valor de ext es:",ext)
        
        header=IonogPWR[-22:-8]  # first 19 characters e. _yyyydoyhhmmss
        print("El valor de header es",header)
        
        HeaderPNG_NW[j]=header
        print("El valor de HeaderPNG_NW es",HeaderPNG_NW)
        
        head_tail=os.path.split(IonoPNG_NW[i])
        
        tail=head_tail[1]
        print("El valor de tail es:",tail)
        
        TailDataNW[i]=tail
        print("El valor del arreglo de tails es:",TailDataNW)
              
        i=i+1
        j=j+1
     
        print(i)
        
        if(i==2):
            i=0;
            j=0;
            
    else:
        print("No existe el directorio"+dataNW[n])
                

if(HeaderPNG_NW[0]!=HeaderPNG_NW[1]):
    print("Los archivos PNG no tienen la misma fecha")
    exit()


#Se creará el archivo comprimido tar en /Canal1/DB     
os.system("cd "+pathComprPWR+" && tar -czf "+URSI+header+".png.tar.gz "+TailDataNE[0]+" "+TailDataNE[1]+" "+TailDataNW[0]+" "+TailDataNW[1])    
print("Se ejecuto la compresion .tar en:",pathComprPWR)
#print("Archivo tar es:",URSI+header+".png.tar.gz "+TailDataNE[0]+" "+TailDataNE[1]+" "+TailDataNW[0]+" "+TailDataNW[1])

#Se eliminarán los png movidos
os.remove(os.path.join(pathComprPWR,TailDataNE[0]))
os.remove(os.path.join(pathComprPWR,TailDataNE[1]))
os.remove(os.path.join(pathComprPWR,TailDataNW[0]))
os.remove(os.path.join(pathComprPWR,TailDataNW[1]))

print("Se termino",os.path.join(pathComprPWR,TailDataNE[0]) )

print("***********************************************************")    
#NGI    
IonogSNR=max(glob.glob(os.path.join(pathNGI,'*')),key=os.path.getmtime) # List of files
print("El archivo ngi es:",IonogSNR)
shutil.copy(IonogSNR,pathComprNGI)

head_tail_ngi=os.path.split(IonogSNR)
print("El valor de head_tail[1] es:",head_tail_ngi[1])

#Se creará el archivo comprimido tar en /Canal1/DB     
os.system("cd "+pathComprNGI+" && tar -czf "+head_tail_ngi[1]+".tar.gz "+head_tail_ngi[1])    
print("Se ejecuto la compresion .tar en:",pathComprNGI)
#print("Archivo tar es:",head_tail_ngi[1]+".tar.gz "+head_tail_ngi[1])

#Se eliminará el ngi movido

os.remove(os.path.join(pathComprNGI,head_tail_ngi[1]))

#startTime=time.time()


print("***********************************************************")
ftp=ftplib.FTP(ftp_host,ftp_user,ftp_password)

print("Conectandose al servidor ...")

print(ftp.getwelcome())
#print(ftp.pwd())
print("Las carpetas son:",ftp.dir())

ftp.cwd("huancayo")
print("Estamos en:",ftp.pwd())

print("Los files antes del upload son:",ftp.nlst())

#Updload tar
print("Uploading PWR and NGI...")

path_list_compr_PWR=os.path.join(pathComprPWR,URSI+header+".png.tar.gz")
path_list_compr_NGI=os.path.join(pathComprNGI,head_tail_ngi[1]+".tar.gz")

print("El valor de path_list_compr_PWR es:",path_list_compr_PWR)
print("El valor de path_list_compr_NGI es:",path_list_compr_NGI)

parentPWR=pathComprPWR
parentNGI=pathComprNGI

subdrPWR=glob.glob(os.path.join(parentPWR,'*'))
subdrNGI=glob.glob(os.path.join(parentNGI,'*'))

print("el valor de subdrPWR es:",subdrPWR)
print("el valor de subdrNGI es:",subdrNGI)

if(len(subdrPWR)>1):
    print("Hay archivos comprimidos no almacenados en el servidor")
    
    for t in subdrPWR:
        fil_PWR= open(t,'rb')
        path_tail=os.path.split(t)
        
        tailPWR=path_tail[1]
        print("El valor de tail es:",tailPWR)
        
        ftp.storbinary('STOR '+tailPWR, fil_PWR)
                
    for g in subdrNGI:     
        fil_NGI= open(g,'rb') 
        path_NGI=os.path.split(g)
        
        tailNGI=path_NGI[1]
        print("El valor de tail es:",tailNGI)
        
        ftp.storbinary('STOR '+tailNGI, fil_NGI)
    
    arrayFiles=ftp.nlst()

    print("Los files subidos son:",arrayFiles)

    print(ftp.quit())

    print("Se termino el uploading")
    #print("El tiempo transcurrido en segundo para subir al servidor es:",entTime-startTime)
           
else:      
    fil_PWR= open(path_list_compr_PWR,'rb') 
    fil_NGI= open(path_list_compr_NGI,'rb') 

    ftp.storbinary('STOR '+URSI+header+".png.tar.gz", fil_PWR)
    ftp.storbinary('STOR '+head_tail_ngi[1]+".tar.gz", fil_NGI)

    #entTime=time.time()

    arrayFiles=ftp.nlst()

    print("Los files subidos son:",arrayFiles)

    print(ftp.quit())

    print("Se termino el uploading")
    #print("El tiempo transcurrido en segundo para subir al servidor es:",entTime-startTime)

if(len(arrayFiles)<2):
    print("No se subió correctamente los ionogramas al servidor. Problemas con la red")
else:   
    print("Se subio correctamente ...")
    
    if(len(subdrPWR)>1):
        for rm in subdrPWR:
            os.remove(rm)  
        for rm2 in subdrNGI:
            os.remove(rm2)             
    else:    
        #Se eliminarán los archivos comprimidos .tar
        os.remove(os.path.join(pathComprNGI,head_tail_ngi[1]+".tar.gz"))
        os.remove(os.path.join(pathComprPWR,URSI+header+".png.tar.gz"))
    
    print("Se elimino los .tar.gz locales")

#print("Se ejecuto la compresion .tar en:",os.path.join(pathComprNE,header+".png.tar.gz"))
#print("Se ejecuto la compresion .tar en:",os.path.join(pathComprNW,header+".png.tar.gz"))
#print("Se ejecuto la compresion .tar en:",os.path.join(pathComprNGI,head_tail[1]+".tar.gz"))
