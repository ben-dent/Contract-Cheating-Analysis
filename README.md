# Contract Cheating Analysis
A tool for analysis of contract cheating sites. Designed by Ben Dent as part of an Undergraduate Research Opportunities Placement (UROP) at Imperial College London

**Full documentation can be seen <a href=https://contract-cheating-analysis.readthedocs.io/en/latest/index.html>here</a>**

**PLEASE NOTE - YOU WILL NEED TO INSTALL THE GECKO DRIVER LOCALLY FOR THIS TO WORK:**

https://github.com/mozilla/geckodriver/releases

Install this in /usr/bin or /usr/local/bin

All other requirements can be installed from the cloned directory with

```pip install -r requirements.txt```

OR

```pip3 install -r requirements.txt```

# Full installation instructions
Make sure you have Python installed. It can be found here:

https://www.python.org

You will also need PyPi, which is usually installed by default with Python on version 3.4 onwards.
If you need to install it:

**Debian/Ubuntu:**

```sudo apt-get install python-pip```

**Fedora:**

```sudo yum install python-pip```

**MacOS:**

```sudo easy_install pip```

**Windows:**\
It is recommended that you use a Linux Virtual Machine if your Python distribution does not contain the 'pip' command.

Once you have PyPi installed, make sure you have Git installed. It should come pre-installed on Linux.

If you want to check if you have Git installed, open up a command line terminal and execute this command:

```git```

If you get a lengthy output, telling you how to use the command then it is installed.

If not, you can install it from here:

https://git-scm.com/downloads

Now you can install the project files with:

```git clone https://github.com/ben-dent/Contract-Cheating-Analysis.git```

Next, install all project requirements by executing:

```pip install -r requirements.txt```

OR

```pip3 install -r requirements.txt```

The relevant instruction to use will depend on your PyPi distribution.

Now make sure you install the gecko driver.

The driver can be installed from here:

https://github.com/mozilla/geckodriver/releases

This needs to be installed in /usr/bin or /usr/local/bin

# Updates

This program may be updated periodically. To check for and install updates, you only need to open a command prompt terminal, change to the program directory (cd) and execute this command:

```git pull origin master```

If an update is available, it will be installed.

# Program Execution

The program can be executed (within the directory) by running:

```python3 Main.py```


