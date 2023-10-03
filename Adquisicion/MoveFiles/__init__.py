import shutil
import os, time,glob
from datetime import datetime
import netCDF4 as nc
'''
now = datetime.utcnow()

current_time = now.strftime("%d/%m/%Y-%H:%M:%S")

year=int(now.strftime("%Y"))
month=int(now.strftime("%m"))
day=int(now.strftime("%d"))
hour0=int(now.strftime("%H"))
minute=int(now.strftime("%M"))
second=int(now.strftime("%S"))'''

parent="/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal1"
parent0="/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal0"

subdr=max(glob.glob(os.path.join(parent,'*')),key=os.path.getmtime)
subdr0=max(glob.glob(os.path.join(parent0,'*')),key=os.path.getmtime)

print(subdr)
print(subdr0)

listOfFiles = list()
for (dirpath, dirnames, filenames) in os.walk(subdr):  #Crea una lista de archivos en todos los subdirectorios bajo de "parent"
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]

#print("The time to move files is :", str(month)+"/"+str(day)+"/"+str(year)+"-"+str(hour0)+":"+str(minute)+":"+str(second))

NumElem=len(listOfFiles)
print("La longitud de ListPath es:",NumElem)
print(listOfFiles)
listOfFiles.sort()
print(listOfFiles)


if(NumElem<=3):
    shutil.rmtree(subdr, ignore_errors=False)
    shutil.rmtree(subdr0, ignore_errors=False)
    print("NumElem es menor que 3")
else:    
    path_metadata=listOfFiles[(NumElem-2)] # Direcction donde se encuntra la metadata del Epoch
    print("La metadata del epoch es:",path_metadata)

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

    print("The storage time is :", str("%02d" %month)+"/"+str("%02d" %day)+"/"+str(year)+"-"+str("%02d" %hour0)+":"+str("%02d" %minute)+":"+str("%02d" %second))

    if month == 1 or month == 2 or month == 3:
        season = "Winter-EEUU"

    elif month == 4 or month == 5 or month == 6:
        season = "Spring-EEUU"

    elif month == 7 or month == 8 or month == 9:
        season = "Summer-EEUU"

    elif month == 10 or month == 11 or month == 12:
        season = "Fall-EEUU"

    src="/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Canal0"
    dst=os.path.join("/media/soporte/HardDisk/Ionogramas/Ionograms_NO45","Ionograms"+"-"+str("%02d" %month)+"-"+str("%02d" %day)+"-"+str("%02d" %year))
    #dst=os.path.join("/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Ionograms_O","Ionograms"+"-"+str(month)+"-"+str(day)+"-"+str(year))

    dir_list=os.listdir(src)

    #print("La lista es:",dir_list)

    src2="/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Canal1"
    dst2=os.path.join("/media/soporte/HardDisk/Ionogramas/Ionograms_NE45","Ionograms"+"-"+str("%02d" %month)+"-"+str("%02d" %day)+"-"+str("%02d" %year))
    #dst2=os.path.join("/home/soporte/Isaac/AdquIonoSDR/Ionogramas/Ionograms_X","Ionograms"+"-"+str(month)+"-"+str(day)+"-"+str(year))

    dir_list2=os.listdir(src2)

    #print("La lista2 es:",dir_list2)

    src3="/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal0"
    dst3=os.path.join("/media/soporte/HardDisk/DataAlmacenada/Data_NO45","Data"+"-"+str("%02d" %month)+"-"+str("%02d" %day)+"-"+str("%02d" %year))
    #dst3=os.path.join("/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/Data_O","Data"+"-"+str(month)+"-"+str(day)+"-"+str(year))

    dir_list3=os.listdir(src3)

    #print("La lista2 es:",dir_list3)

    src4="/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal1"
    dst4=os.path.join("/media/soporte/HardDisk/DataAlmacenada/Data_NE45","Data"+"-"+str("%02d" %month)+"-"+str("%02d" %day)+"-"+str("%02d" %year))
    #dst4=os.path.join("/home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/Data_X","Data"+"-"+str(month)+"-"+str(day)+"-"+str(year))
    dir_list4=os.listdir(src4)

    #print("La lista2 es:",dir_list4)

    src5="/media/soporte/HardDisk/DataNGI/DataNow"
    dst5=os.path.join("/media/soporte/HardDisk/DataNGI","DataNGI"+"-"+str("%02d" %month)+"-"+str("%02d" %day)+"-"+str("%02d" %year))
    dst5f=os.path.join(dst5,"NGI")
    dir_list5=os.listdir(src5)
    
    print("************************dst5",dst5)

    if ((hour0 == 23) and (minute==58)): #5min
    #if ((hour0 == 23) and (minute==59)): #1min
    #if (1):
        print("****Estoy dentro****")
        os.mkdir(dst)
        os.mkdir(dst2)
        os.mkdir(dst3)
        os.mkdir(dst4)
        os.mkdir(dst5)
        os.mkdir(dst5f)

        for fname in dir_list:
            shutil.move(os.path.join(src,fname),dst)

        for fname in dir_list2:
            shutil.move(os.path.join(src2,fname),dst2)
       
        for fname in dir_list3:
            shutil.move(os.path.join(src3,fname),dst3)
       
        for fname in dir_list4:
            shutil.move(os.path.join(src4,fname),dst4)        
   
        for fname in dir_list5:
            shutil.move(os.path.join(src5,fname),dst5f)
   
        #    os.mkdir(os.path.join(src,"IntegrCoher")) # Nombre de archivo donde guarda ionogramas el programa
        #    os.mkdir(os.path.join(src2,"IntegrCoher"))
        #    os.mkdir(os.path.join(src,"IntegrIncoher"))
        #    os.mkdir(os.path.join(src2,"IntegrIncoher"))
        os.mkdir(os.path.join(src,"DB"))
        os.mkdir(os.path.join(src2,"DB"))
        os.mkdir(os.path.join(src,"SNR"))
        os.mkdir(os.path.join(src2,"SNR"))    

print("Terminado")
