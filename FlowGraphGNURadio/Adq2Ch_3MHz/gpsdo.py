# this module will be imported in the into your flowgraph
f=open("/home/soporte/Isaac/AdquisIonosOblic/gpsdo.txt","r")
Latitud=float(f.readline())
Lat_ind=f.readline()
Longitud=float(f.readline())
Long_ind=f.readline()
f.close
#print("LA LISTA ES:",ListFile)
