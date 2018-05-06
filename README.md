# Kraken-MD
View markdown on your computer with ease, launch Kraken MD from command line or open a file!

> **Note:** Only basic markdown capability is present, if you wish to render more advanced markdown, download another renderer, this program is a work in progress and is *not* yet fully capable. Updates are being worked on.

*Kraken MD* is a markdown renderer for the Windows operating system. Its purpose is to display formatted markdown.

To begin, open Kraken MD and go to `File > Open` or press CTRL+O and select a `.md` file. Your file will be displayed in the window.

You can also open a file immediately via the command line. Simply enter `python index.py <filepath>` where `<filepath>` is an absolute or relative path to the file.

To run an unbuilt version, you must have installed:
- wxPython `($ pip install -U wxPython)`
- beautifulSoup `($ pip install beautifulsoup4)`
- [python 3.6+](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe)
