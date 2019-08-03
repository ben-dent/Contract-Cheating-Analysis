Installation
=============

Make sure you have Python installed. It can be found here:

https://www.python.org

You will also need PyPi, which is usually installed by default with Python on version 3.4 onwards.
If you need to install it:

**Debian/Ubuntu:**
::

    sudo apt-get install python-pip

**Fedora:**
::

    sudo yum install python-pip

**MacOS:**
::

    sudo easy_install pip

**Windows:**\
It is recommended that you use a Linux Virtual Machine if your Python distribution does not contain the 'pip' command.

Once you have PyPi installed, make sure you have Git installed from here:

https://git-scm.com/downloads

Now you can install the project files with:
::

    git clone https://github.com/ben-dent/Contract-Cheating-Analysis.git

Next, install all project requirements by executing:
::

    pip install -r requirements.txt

OR
::

    pip3 install -r requirements.txt

The relevant instruction to use will depend on your PyPi distribution.

Now make sure you install the gecko driver.

Users on Windows are directed to the instructions at this link if they wish to continue on Windows:

https://selenium-python.readthedocs.io/installation.html#detailed-instructions-for-windows-users

Users on all other Operating Systems can install the drivers here:

https://github.com/mozilla/geckodriver/releases

This needs to be installed in usr/lib or usr/local/bin

# Program Execution

The program can be executed (within the directory) by running:
::

    python3 Main.py