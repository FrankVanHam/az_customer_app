SET EMACSROOT=D:\Emacs\emacs
SET SMALLWORLD_GIS=%~dp0\SW\core
SET SW_GIS_ALIAS_FILE=D:\Emacs\emacs\config\gis_aliases
SET SW_GIS_ENVIRONMENT_FILE=%SMALLWORLD_GIS%\config\environment.bat
SET JAVA_HOME=D:\jdk-17
SET PATH=D:\jdk-17\bin;%PATH%

CALL %~dp0set_base_dir.bat
%SMALLWORLD_GIS%\bin\x86\runalias -a %SW_GIS_ALIAS_FILE% -e %SW_GIS_ENVIRONMENT_FILE% emacs