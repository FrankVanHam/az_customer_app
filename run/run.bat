SET PATH="C:\jdk-17\bin";%PATH%
SET JAVA_HOME=C:\jdk-17

SET SMALLWORLD_GIS=C:\Smallworld\core
SET CUSTOMER_APP_BASE_DIR=C:\SW-app\
SET SMALLWORLD_REGISTRY=C:\SW-app\smallworld_registry
%SMALLWORLD_GIS%\bin\x86\runalias.exe -a C:\SW-app\customer_app\config\gis_aliases -e %SMALLWORLD_GIS%\config\environment.bat customer_app_open
