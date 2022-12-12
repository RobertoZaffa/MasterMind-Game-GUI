# MasterMind Game GUI
Program to play Mastermind with the original vintage board game
# Dependencies
- pygame
- webbrowser  
- configparser
- distutils
- constants 
- Mastermind_Engine
# Screenshot
![VMM-1](https://user-images.githubusercontent.com/76481108/207011474-7158b25c-0f4f-495e-a0c5-1a81ee780c37.jpg)
# How to Install
- To run the game, download the zip file, unzip in a folder and run mm79.py from Python.
- mastermind_engine.py is external module/class that is imported by mm79.py
- mastermind_engine.pyd is mastermind_engine.py compiled with cython. If both files are present, the .pyd will be used. 
- constants is external module that is imported by mm79.py
- For some processes the use of mastermin_engine.pyd it is three times faster than mastermind_engine.py 
- To run the game without Python and/or Pygame library, download it from:
https://mastermind.altervista.org/
- **At https://mastermind.altervista.org/this you will find also all Mastermind related stuff include ZX Spectrum, Lego EV3 Mindstorm, Lego Robot Inventor, Arduino version of masterMind.**
