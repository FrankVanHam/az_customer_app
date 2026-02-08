@ECHO OFF

SET PATH="D:\jdk-17\bin";%PATH%
SET JAVA_HOME=D:\jdk-17

SET SMALLWORLD_GIS=%~dp0..\..\SW\core
SET CUSTOMER_PRD_BASE_DIR=%~dp0..
%SMALLWORLD_GIS%\bin\x86\runalias.exe -a %CUSTOMER_PRD_BASE_DIR%\customer_prd\config\gis_aliases -e %CUSTOMER_PRD_BASE_DIR%\customer_prd\config\environment.bat customer_prd_open
