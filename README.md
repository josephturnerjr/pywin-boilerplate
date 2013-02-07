# pywin-boilerplate

This project provides boilerplate for a full build of a native Windows application in Python. It includes:

  * Sane requirements (pywin32, py2exe)
  * py2exe boilerplate (builds to single executable)
  * WiX boilerplate (builds an MSI)

The application itself can use a Windows resource template file as created by the Visual Studio dialog editor or a similar editor.

# Building

You can build the executable for the example application by running make from the root directory. The executable will be placed in the dist directory. To build the MSI, descend into the packaging directory and run:

    ?> bash ./build_all.sh 0.1.2

Of course, you can replace 0.1.2 with whatever version number you would like.
