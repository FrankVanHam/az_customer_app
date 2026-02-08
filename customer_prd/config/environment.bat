REM
REM Smallworld Product Windows Environment
REM Windows version of environment
REM
REM This file should not normally need to be edited by hand.
REM In any case, do not add anything other than simple SET, REM and
REM CALL lines, as it is read by the 'gis' command, not just by cmd.exe.
REM Note that the CALL statement can be used to call other batch files.
REM However these have the same restrictions on their contents. Also
REM the gis launcher program limits the CALL stack to be a maximum of 32
REM levels deep.
REM

set SW_PRODUCTS_PATH=

REM the current 
CALL %SMALLWORLD_GIS%\..\..\set_base_dir.bat

set SW_MESSAGE_DB_DIR=D:\SW530\smallworld_registry
set SW_ACE_DB_DIR= D:\SW530\cambridge_db\ds\ds_admin
SET SMALLWORLD_REGISTRY=%CUSTOMER_PRD_BASE_DIR%\smallworld_registry

set SW_GIS_PATTERN_DIR=%SMALLWORLD_GIS%\data\xview_patterns
set SW_FONT_CONFIG=%SMALLWORLD_GIS%\config\font
set SW_CODE_TABLES=%SMALLWORLD_GIS%\data\code_tables
set SW_GIS_TEMPLATE_DIR=%SMALLWORLD_GIS%\data\template
set SW_MDB_TRANSPORTS=tcpip
set SW_MDB_KEEPALIVE=60,10
set SW_ACP_PATH=%SMALLWORLD_GIS%\etc\x86
set PATH=%SMALLWORLD_GIS%\bin\x86;%PATH%

REM Launcher related default settings for SW5 Java startup 
set SW_LAUNCH_JAVA_MEMORY=-Xmx1g 
set SW_LAUNCH_JAVA_ARGS=-Xss3m -XX:ReservedCodeCacheSize=256m -Djdk.lang.Process.allowAmbigousCommands=true -Djava.lang.invoke.MethodHandle.COMPILE_THRESHOLD=3 -Djava.locale.providers=COMPAT -Dnashorn.args="--no-deprecation-warning" -XX:-TieredCompilation -XX:MaxTrivialSize=8 -XX:MinInliningThreshold=1000 -Dorg.osgi.framework.os.name=win32 -Dsun.java2d.uiScale.enabled=false -Dorg.ops4j.pax.logging.DefaultServiceLog.level=ERROR
rem Crash reporting options have changed at Java 9. To enable crash dumps, uncomment one of the following lines:
rem On Java 8:
rem  set SW_LAUNCH_JAVA_ARGS=%SW_LAUNCH_JAVA_ARGS% -XX:+CreateMinidumpOnCrash
rem On Java 9 and above:
rem  set SW_LAUNCH_JAVA_ARGS=%SW_LAUNCH_JAVA_ARGS% -XX:+CreateCoredumpOnCrash
rem Street View Java JDK-17 Compatibility
set SW_LAUNCH_JAVA_ARGS=%SW_LAUNCH_JAVA_ARGS% --add-exports=java.base/java.lang=ALL-UNNAMED --add-exports=java.desktop/sun.awt=ALL-UNNAMED --add-exports=java.desktop/sun.java2d=ALL-UNNAMED
set SW_LAUNCH_OSGI_JAR=%SMALLWORLD_GIS%/libs/org.eclipse.osgi-3.13.100.jar

REM For Java 13 tweak to improve font rendering
set FREETYPE_PROPERTIES=interpreter-version

REM Double percent characters delay the expansion until the command line is constructed. 
REM SW_LAUNCH_OSGI_CONFIG_DIR is concocted by the launcher.
set SW_LAUNCH_JAVA_LOG=%%SW_LAUNCH_OSGI_CONFIG_DIR%%/magik_on_java.log

REM For GDAL
set PROJ_LIB=%SMALLWORLD_GIS%\sw_core\libs
