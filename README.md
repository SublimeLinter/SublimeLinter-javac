SublimeLinter-javac
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-javac.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-javac)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [javac](http://docs.oracle.com/javase/6/docs/technotes/tools/solaris/javac.html).
It will be used with files that have the "Java" syntax.

Please note that because `javac` requires a complete directory context in order to work, this linter plugin currently will only lint a file **when it has been saved**.


## Installation
SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before using this plugin, ensure that `javac` (JDK 1.7+) is installed on your system.
`javac` is part of the `java` developer SDK, which can be downloaded [here](http://www.oracle.com/technetwork/java/javase/downloads/index.html).

Please make sure that the path to `javac` is available to SublimeLinter.
The docs cover [troubleshooting PATH configuration](http://sublimelinter.com/en/latest/troubleshooting.html#finding-a-linter-executable).


## Settings
- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html

Additional SublimeLinter-javac settings:

|Setting|Description|
|:------|:----------|
|lint|A comma-delimited list of rules to apply.|

Valid rule names are: all, cast, classfile, deprecation, dep-ann, divzero, empty, fallthrough, finally, options, overrides, path, processing, rawtypes, serial, static, try, unchecked, varargs, -cast, -classfile, -deprecation, -dep-ann, -divzero, -empty, -fallthrough, -finally, -options, -overrides, -path, -processing, -rawtypes, -serial, -static, -try, -unchecked, -varargs, none.

For example, to ignore deprecation warnings for all files in a project, you would add this to the linter settings:

```
"javac": {
    "lint": "all,-deprecation"
}
```

### Passing options to `javac`

In order to configure `javac` options like the class path, source path, or file encoding,
the `args` setting can be used.

|Setting|Description|
|:------|:----------|
|`args`|An array of strings, alternating between an option and the corresponding value.|

A full list of available options is given [here][1].

For example, the following configuration defines the source file encoding,
includes the two libraries `lib/some_lib.jar` and `lib/some_other_lib.jar`
in the classpath,
and defines `src/` as the project's source path:

```
"args": [
    "-encoding", "UTF8",
    "-cp", "${folder}/lib/some_lib.jar:${folder}/lib/some_other_lib.jar",
    "-sourcepath", "${folder}/src/"
]
```

Note that options and their values must be separate elements in the array
(i.e. `"args": ["-sourcepath", "/path/to/src"]` does work, while
`"args": ["-sourcepath /path/to/src"]` does not work).

#### Project-specific options

Settings like the class path often only apply to one specific project.
The general SublimeLinter documentation also [explains][3] how to specify
project-specific settings in the `sublime-project` file.

For the example above, such a project file could look like this:
```
{
    "folders":
    [
        {
            "path": "."
        }
    ],
    "SublimeLinter":
    {
        "linters":
        {
            "javac": {
                "lint": "all",
                "args": [
                    "-encoding", "UTF8",
                     "-cp", "${folder}/lib/some_lib.jar:${folder}/lib/some_other_lib.jar",
                    "-sourcepath", "${folder}/src/"
                ]
            }
        }
    }
}
```


[1]:http://docs.oracle.com/javase/7/docs/technotes/tools/windows/javac.html
[2]:http://sublimelinter.com/en/latest/settings.html#settings
[3]:http://sublimelinter.com/en/latest/settings.html#project-settings
