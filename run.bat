@echo off
@REM REM Start the Flask app in a new command prompt window
start /b cmd /c "cd TLM2008_Project && flask --app chat run -h localhost -p 4000"

@REM REM Change directory back and start the virtual environment
@REM cd /d ..
echo running virtual environment...
call env\Scripts\activate & python -m flask --app TLM2008_Project --debug run

@REM REM Once the Flask app terminates, kill the command prompt process
taskkill /fi "imagename eq cmd.exe" /fi "windowtitle eq Administrator:*"
