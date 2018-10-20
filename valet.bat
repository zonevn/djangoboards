@echo off
setlocal enableDelayedExpansion
set args=%*
python valet.py %args%
exit /b 1