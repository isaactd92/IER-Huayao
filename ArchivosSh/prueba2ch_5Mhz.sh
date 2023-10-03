#!/bin/bash

#****** 2 Canales 5MHz
#timeout 93s /usr/bin/python3.8 /home/soporte/Isaac/CodeDemodV2/FlowGraphGNURadio/Adq2Ch_5MHz/Prueb_2canales_5MHz.py #IPP=40ms
#timeout 43s /usr/bin/python3.8 /home/soporte/Isaac/CodeDemodV2/FlowGraphGNURadio/Adq2Ch_5MHz/Prueb_2canales_5MHz.py #IPP=10ms Antiguo

#timeout 43s /usr/bin/python3.8 /home/soporte/Isaac/CodeDemodV2/FlowGraphGNURadio/Adq2Ch_5MHz/Prueb_2canales_5MHz.py #IPP=10ms Antiguo
#timeout 42s /usr/bin/python3.8 /home/soporte/Isaac/CodeDemodV2/FlowGraphGNURadio/Adq2Ch_5MHz/Prueb_2canales_5MHz.py #IPP=12.5ms
#timeout 37s /usr/bin/python3.8 /home/soporte/Isaac/CodeDemodV2/FlowGraphGNURadio/Adq2Ch_5MHz/Prueb_2canales_5MHz.py #IPP=10ms 1min/5min
timeout 58s /usr/bin/python3.8 /home/soporte/Isaac/CodeDemodV2/FlowGraphGNURadio/Adq2Ch_5MHz/Prueb_2canales_5MHz.py #IPP=20ms

mv /home/soporte/Isaac/AdquIonoSDR/DataAdquirida/2Canales/Canal0 /home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal0

mv /home/soporte/Isaac/AdquIonoSDR/DataAdquirida/2Canales/Canal1 /home/soporte/Isaac/AdquIonoSDR/DataAlmacenada/DataCanal1

/usr/bin/python3.8 /home/soporte/Isaac/workspace-eclipse/python/DataDate/__init__.py

#****Poner adelante timeout 8s si se quiere ver ionogramas para mas de 1min
/usr/bin/python3.8 /home/soporte/Isaac/workspace-eclipse/python/IonoIntCohDbCh0/__init__.py

/usr/bin/python3.8 /home/soporte/Isaac/workspace-eclipse/python/IonoIntCohDbCh1/__init__.py

/usr/bin/python3.8 /home/soporte/Isaac/workspace-eclipse/python/IonoSNRdBCh0/__init__.py

/usr/bin/python3.8 /home/soporte/Isaac/workspace-eclipse/python/IonoSNRdBCh1/__init__.py

/usr/bin/python3.8 /home/soporte/Isaac/workspace-eclipse/python/NGIDbSNR/__init__.py > /home/soporte/Isaac/log/NGI.txt

#/usr/bin/python3.8 /home/soporte/Isaac/workspace-eclipse/python/UploadServer2/UploadServer2/__init__.py > /home/soporte/Isaac/log/Upload.txt 

/usr/bin/python3.8 /home/soporte/Isaac/workspace-eclipse/python/MoveFiles/__init__.py > /home/soporte/Isaac/log/movefiles.txt




