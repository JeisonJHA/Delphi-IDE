# Delphi-API
Some functions to make your life a little easy programming delphi on ST. 
This plugin will have a lot of basic functions. 

## Installation
The recommended method of installation is via [Package Control](https://packagecontrol.io/). It will download upgrades to your packages automatically. -->

### Package Control

* Follow instructions on [https://packagecontrol.io/installation](https://packagecontrol.io/installation)
* Install using Package Control: Install > Delphi API

### Using Git

Go to your Sublime Text Packages directory and clone the repository using the command below:

git clone [https://github.com/JeisonJHA/Delphi-API](https://github.com/JeisonJHA/Delphi-API) "Delphi API"

## Goto Definition

Go to method definition.
* ctrl+leftclick(this override ST mouse binding)

## Delphi method navigation

Navigate between method interface and implementation like Delphi IDE.
* ctrl+shift+up(this override ST key binding)

## Limitations

All plugins of this pack is based on this syntax: [sublime-delphi-language](https://bitbucket.org/JeisonJHA/sublime-delphi-language).
    
## Next steps
    ## Method Comment
  	
  	This insert the comment of the method that the cursor is on.
  
  	Ex:
  	/// <summary>
  	///  Comment of the method
  	/// </summary>
  	/// <param name="ParamName">
  	/// </param>
  	/// <returns>
  	///  Return type
  	/// </returns>
  	/// <remarks>
  	///  Author
  	/// </remarks>
  
    ## Add TAG
    
    This insert the user TAG in the line of the cursor
    
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
    
	## Formatter

		File formats that use the theme "Pascal" or "Delphi" and are with encoding 
		"Western (Windowns 1252)".
