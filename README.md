# pywin-boilerplate

This project provides boilerplate for a full build of a native Windows application in Python, particularly for rapid prototyping of dialog-based applications. It includes:

  * Sane requirements (pywin32, py2exe)
  * Example application boilerplate (processes a Windows message loop)
  * py2exe boilerplate (builds to single executable)
  * WiX boilerplate (builds an MSI)

The application itself can use a Windows resource template file as created by the Visual Studio dialog editor or a similar editor.

# Building

_These instructions presume a working [Cygwin](http://cygwin.com/) installation; if you're not using Cygwin, you'll need to use the power of your superior primate brain to adapt these instructions and installation tools to your needs. The build infrastructure for this project uses both `bash` and `make`._

First, you'll need to install the requirements. From within the project directory:
 
    ?> pip install -r REQUIREMENTS

You can build the executable for the example application by running make from the root directory. The executable will be placed in the dist/ directory.

To build the MSI, descend into the packaging/ directory and run:

    ?> bash ./build_all.sh 0.1.2

Of course, you can replace 0.1.2 with whatever version number you would like.

# Customizing

### Naming

The first step is choosing a name for your application. The example application is called 'example', and files are named accordingly. awk/sed/search and replace the occurances with your chosen name.

### Application logic

The second step is to create an actual application of value. The example.py file in the top-level directory is a very, very simplistic application. For single-dialog application or prototype, it may be enough to get rolling. 

You can open the Visual Studio solution in the resources/ directory to edit the dialog or add new resources as you need.

Sometimes the py2exe build can become confused by some imports. You're mostly on your own here, but the py2exe documentation has a number of common problems resolved.

### Packaging

Finally, you can customize the installation by modifying the wxs file in the packaging/ directory. A discussion of how to do that is beyond the scope of this project, but again let the documentation be your guide.
