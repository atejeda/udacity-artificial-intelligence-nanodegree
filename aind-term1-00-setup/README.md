# udacity-aind conda setup

*Uses python3.6, jupyter is moving exclusively to py3.*

## Anaconda

Setup and cheat sheet

- download
    - https://www.continuum.io/downloads#osx
    - add the conda path to your environment, follow instructions
- create environment
    - conda create -n <environment_name>  python=3.6  [package list] # python version
- activate the environment
    - source activate <environment_name>
- deactivate environment
    - source deactivate
- export environment
    - conda env export > environment.yaml
- restore the environment
    - conda env create -f environment.yaml
- removing environment
    - conda env remove -n <environment_name>
- update conda
    - conda upgrade conda
    - conda upgrade --all
- install needed packages
    - conda install numpy pandas matplotlib
- jupyter notebook to developed code
    - conda install jupyter notebook
- list packages installed
    - conda list
- Others
    - https://docs.continuum.io/mkl-optimizations/
    - conda install, update, remove, search <name>

Mac OS X and Linux

- Download the aind-environment-unix.yml file at the bottom of this page (right click, save file).
- conda env create -f aind-environment-unix.yml to create the environment.
- then source activate aind to enter the environment.
- Install the development version of hmmlearn 0.2.1 with a source build: pip install git+https://github.com/hmmlearn/hmmlearn.git. If you are having trouble on this step feel free to skip ahead. You'll only need this for hmmlearn in the very last project.

Optional: Install Pygame
Through this Nanodegree, we'll use pygame to help you visualize your programs so that you have beautiful visualizations of AI you can share with others in your portfolio. However, pygame is optional as it can be tricky to install. If you'd like to install it, here are the steps:

Mac OS X

- Install homebrew
- brew install sdl sdl_image sdl_mixer sdl_ttf portmidi mercurial
- source activate aind
- pip install pygame
- Some users have reported that pygame is not properly initialized on OSX until you also run python -m pygame.tests.

Windows and Linux

- pip install pygame
- In Windows, an alternate method is to install a precompiled binary wheel:
    - download the appropriate pygame-1.9.3-yourpythonwindows.whl file from here
    - install with pip install pygame-1.9.3-yourpythonwindows.whl.