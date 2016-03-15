# Delphi-IDE
Some functions to make your life a little easy programming delphi on ST. 
This plugin will have a lot of basic functions. 

## Installation
The recommended method of installation is via [Package Control](https://packagecontrol.io/). It will download upgrades to your packages automatically.

### Package Control

* Follow instructions on [https://packagecontrol.io/installation](https://packagecontrol.io/installation)
* Install using Package Control: Install > Delphi-IDE

### Using Git

Go to your Sublime Text Packages directory and clone the repository using the command below:

git clone [https://github.com/JeisonJHA/Delphi-IDE](https://github.com/JeisonJHA/Delphi-IDE) "Delphi IDE"

## Goto Definition

Go to method definition.

* ctrl+leftclick**(THIS OVERRIDE ST MOUSE BINDING)**

## Delphi method navigation

Navigate between method interface and implementation like Delphi IDE.

* ctrl+shift+up**(THIS OVERRIDE ST KEY BINDING)**
    
## Formatter

File formats that use the theme "Pascal" or "Delphi".
It uses the [jedi formatter](http://jedicodeformat.sourceforge.net/), but you can change to use the one of your preference.
Configurations:

* "path_formatter": "C:\MyFormatter.exe"
* "other_params": ""
* "auto_format": true
* "encode": "'Western (Windows 1252)'"
* "validate_encode": false

## Doc

Now you can doc yours methods, propertys, classes, interfaces and records.

To use put the cursor on the scope of what you want to doc and push the trigger.

You can choose XML or JAVADOC.

Method Ex:
```
/// <summary>
/// 
/// </summary>
/// <remarks>
/// Owner: Jeison.Azevedo Date: March 10, 2016
/// </remarks>
/// <param name="ParamName">
/// </param>
/// <exception>
/// 
/// </exception>
```

* ctrl + shift + m 

## Add TAG

This insert the user TAG in the line of the cursor

Ex:
```
// Jeison.Azevedo - March 10, 2016
```

* ctrl + shift + g

## Limitations

Except the formatter all other plugins of this pack is based on this syntax: [sublime-delphi-language](https://bitbucket.org/JeisonJHA/sublime-delphi-language).
    
## Next steps
    ## Declare Method
    
    This works like the "Ctrl+Shift+C" of the Delphi, the diference is that this works only
    for the method that is in scope.
    
    ## Extract Method
    
    You select the snippet you want to extract and the plugin will identify which parameters
     are required for the new method and includes in the new method. 
    The new method will be inserted with the name "ExtractedMethod" you just need to write the
     name you want to change the declaration will use and implementation of the method.
    
    ## Exchange method return
    
    Changes the return of the method, for procedure if you do not inform a return type or function if you do.
    
    ## Syncronize method declaration
    
    Syncronize the parameters of the method of implementation and interface with the method that is in scope.
