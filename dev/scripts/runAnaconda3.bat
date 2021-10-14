set root=C:\ProgramData\Anaconda3
call %root%\Scripts\activate.bat %root%
rem call conda env create -f python\environment.yml
rem call activate sensitivity
jupyter notebook
rem call conda deactivate
rem pause