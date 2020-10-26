Anaconda Tips & Tricks
======================

Thank you to `SoundSpinning <https://github.com/SoundSpinning>` over on Github for these fantastic notes! A direct link to the thread is here <https://github.com/JackMcKew/pandas_alive/issues/11>.

Note: these comments refer to an installation on a Windows 10 PC.

Preamble:
Anaconda is a great starter program to learn Python for Data Science and others. With a single install you get hundreds of packages which will allow you to follow most tutorials while learning. This, most likely, will be via the Jupyter notebook app already included in the main install.
Anaconda will install a default Python environment called base, and may be at least 3GB large on your PC. The main package & environment manager is called conda. However, once you start working in collaboration with other Python projects, it is not recommended to continue with the base (default environment). This is because project authors will be careful to stick to specific package versions for development. To be able to work with these projects you'll need to create new conda environments for each project, and then install those specific package versions under your new Python project environment.
Therefore, to simply copy (clone) your (large) base environment into a new one is not a good idea. It'll over time eat disc space, but also conda may become slow. Worst of all, you won't guarantee that your setup will work with the package versions for that specific project.

So, what to do next? This is what it worked for me and keeps disc size to a minimum and allows for many conda environments to work fine (so far) with other projects.

1.- I uninstalled the whole of the Anaconda program from my PC, including deleting manually any anaconda entries anywhere on my machine.

2.- I installed Miniconda3 under C:\miniconda3. Make sure you do not install it under a path with spaces in it, or else things may break later on and cause hassles.
Miniconda installs only conda, python and pip in the base (default) environment and a very small number of dependencies.

3.- Set up conda & the conda-forge channel:
In order to use conda (as the general package & environment manager) from base for all other conda environments without having to install it on each of them, all you need to do is to make sure you add to the (Windows) PATH the path to the conda main installation folders. It should look something like this in your PATH: C:\miniconda3;C:\miniconda3\condabin;C:\miniconda3\Scripts ... (your other PATH entries).
Once this is done you can then call (use) the conda command from any other environment while keeping a single install of conda in the base env only.

conda-forge is a community driven conda packages repository, which is recommended as your main channel for installs. pandas_alive was recently added to this channel, neat. You'll need to execute these commands once in an Anaconda terminal to set this up permanently:
conda config --add channels conda-forge
conda config --set channel_priority strict
After the above, each time you do conda install package-name on any environment it'll look 1st into the conda-forge channel.

4.- Set up a new conda env example:
conda create -n py38 python=3.8
conda activate py38
conda install pandas matplotlib notebook pandas-alive ffmpeg xlrd jupyter_contrib_nbextensions tqdm
This example will install the above main packages and (many) dependencies. To keep track of what's installed in each env, conda can export YAML files so that they can later be used to create/update an env. You can create a *.yml for your new env like this:
conda env export --from-history > env-name.yml
Note the --from-history flag. This is very handy as it'll list only the main packages versions without their dependencies. This allows for a safer cross-platform install minimising breaks from dependencies. You can then continue hand editing this file when you add any main package and its version, without having to list all dependencies.

Attached is a (small) .yml file which worked for me setting/updating a conda environment to work with the pandas_alive project.
py38-pandas_alive.zip:
conda create -f py38-pandas_alive.yml
or after hand editing the file adding new main packages:
conda update -f py38-pandas_alive.yml

NOTE: I found a gotcha in Windows where conda will write the 1st .yml file encoded as UTF-16. This file will not work later on with conda create/update. The trick is to open the .yml file in your text editor, change the encoding to UTF-8 and save the file. Then continue editing it if required in your text editor and should work fine from there onwards.

5.- Some recommended setting in Windows:
If you've come this far here, you most likely have played with GIT and have git for windows installed. From my experience I also recommend to install MINGW64 on your Windows setup. Both combined and set up properly will bring all the useful Linux tools you may need, not only on the git bash terminal, but also across the Windows Powershell command window too.

The above is useful with Python via conda, because you need to use the Anaconda command window. In Windows when you 1st search for this you'll most likely be confronted with two options: usual CMD style prompt, and the Powershell prompt version. I suggest you use the latter and pin it to your task bar for future easy access. If all set up properly then you will have access to the history of commands from all windows and with Linux commands.

A very useful shortcut is Ctrl+r. This will allow you to search back in the history of commands as you type a string. Repeat the same shortcut if the 1st search is not the command you want and it'll search back further. It saves a lot of time when trying to remember and/or go back to long or unusual commands without having to google them again.

Another useful conda command when you need to clean up your overall python set up is:
conda clean -a

6.- IDE (code editor choice):
I used for years Sublime Text. However, I recently switched to VS code and it seems brilliant, free and with monthly updates. It has an instant and excellent integration with GIT and Python environments, including conda. Well worth a try.

Please add to this thread any other tips and tricks from your experience with conda installs.
