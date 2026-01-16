@echo off
set /p OLD_PATH="Enter OLD PROJECT backend path: "
xcopy "%OLD_PATH%\data\embeddings\*.npy" "data\embeddings\" /Y /I
xcopy "%OLD_PATH%\data\*.csv" "data\" /Y
xcopy "%OLD_PATH%\data\models\*.pkl" "data\models\" /Y /S /I
echo Data copied! Run setup_backend.bat next
pause
