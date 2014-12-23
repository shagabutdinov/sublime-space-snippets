# Sublime SpaceSnippets plugin

It inserts spaces instead of you where it assumed to be inserted. Requires a lot
of adaptation.

There is not much help from this plugin in writing code but when I personally
started to use it, I liked it and prefer to write code with this plugin rather
than without.


### Features

Provides spaces insertion for certain characters. Spaces style are adapted to my
personal coding style so it can be worthless for others.

Example:

```
    # type "myvar"
    myvar| # <- cursor is |

    # type "+"
    myvar+|

    # plugin will convert "+" to " + " (with spaces)
    myvar + |

    # some special cases are handled too:
    # type "myvar":
    myvar| # <- cursor is |

    # than type "+"
    MyClass + |

    # than type "=" (automatically removes space between "+" and "=")
    MyClass += |
```


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.

If you don't like fuzzy behavior you should rebind keyboard shortcuts after
installation in the "Autocompletion/Default (OSNAME).sublime-keymap" file
(non-fuzzy behavior are commented by default).


### Commands

| Description       | Keyboard shortcuts |
|-------------------|--------------------|
| Insert spaced "," | ,                  |
| Insert spaced ":" | :                  |
| Insert spaced ">" | >                  |
| Insert spaced "<" | <                  |
| Insert spaced "*" | *                  |
| Insert spaced "/" | /                  |
| Insert spaced "+" | +                  |
| Insert spaced "-" | -                  |
| Insert spaced "&" | &                  |
| Insert spaced "|" | |                  |
| Insert spaced "=" | =                  |
| Insert spaced "!" | !                  |
| Insert spaced "." | .                  |