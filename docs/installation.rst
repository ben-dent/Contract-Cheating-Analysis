Installation
=============

Make sure you have Python installed. It can be found here:

https://www.python.org

You will also need PyPi (which must be pip3), which is usually installed by default with Python on version 3.4 onwards.
There is currently a problem with the default on MacOS so if you do need to install it:

**Debian/Ubuntu:**
::

    sudo apt-get install python-pip

**Fedora:**
::

    sudo yum install python-pip

**MacOS:**

First you must install HomeBrew by running:
.. code-block::

  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Then, once Homebrew is installed, run:

.. code-block::

   brew install python


**Windows:**

It is recommended that you use a Linux Virtual Machine if your Python distribution does not contain the 'pip' command.

Once you have PyPi installed, make sure you have Git installed. It should come pre-installed on Linux.

If you want to check if you have Git installed, open up a command line terminal and execute this command:
::

   git

If you get a lengthy output, telling you how to use the command then it is installed.

If not, you can install it from here:
https://git-scm.com/downloads

Now you can install the project files with:
::

    git clone https://github.com/ben-dent/Contract-Cheating-Analysis.git

Next, install all project requirements by executing:
::

    pip install -r requirements.txt

OR:
::

    pip3 install -r requirements.txt

The relevant instruction to use will depend on your PyPi distribution.

Now make sure you install the gecko driver.

The driver can be installed from here here:

https://github.com/mozilla/geckodriver/releases

This needs to be installed in /usr/bin or /usr/local/bin

Program Execution
------------------

The program can be executed (within the directory) by running:
::

    python3 Main.py