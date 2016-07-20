Wanxin Tools
===============

A toolset for STUPID wanxin client in Alfred workflow.

Download and Install
---------------------

Goto [release](https://github.com/slawdan/wxcontact_workflow/releases) to download the packaged workflow.


Requirements
----------------

- Mac
- Alfred Powerpack
- Wanxin Client (>= 0.98.037) for Mac installed.
- Python 2.6+


Usages
-----------

### Start wanxin client

`wanxin`

    Quick start wanxin client by Pinyin.

#### Actions

 - `Enter`: start wanxin client.


### Search wanxin contacts

`wx {keyword}`

    Keyword could be contact's Chinese name, English name, email, mobile or telephone.

#### Actions

 - `Enter`: copy the contact to clipboard, and show on fullscreen. 

### Search wanxin chat logs

`wxchat {keyword} ...`

    Keywords will be used in fuzzy search.

#### Actions

 - `Enter`: copy the chat log to clipboard.
 - `⌘+Enter`: show the chat log on fullcreen.

### Browse wanxin automatically downloaded files

`wxfile [filename]`

    Filename is optional and would be used in fuzzy match.

#### Actions

 - `Enter`: open the file.
 - `⌘+C`: copy file full path.
 - `⌘+Enter`: reveal the file in Finder.

### Clean wanxin automatically generated files

`wxclear`

    Clean wanxin automatically downloaded images and duplicated files.


    - Images include `png`, `jpg`, `gif`, `bmp` files.
    - Duplicated files are calculated by file's md5.

`wxclearall`

    Clean wanxin automatically downloaed files, and also wanxin client's logs.

#### Actions

 - `Enter`: do clean.


ICONS
----------

The logo is extract from Wanxin client for Mac.

Others were fetched from "www.iconsfind.com":

 - Male icon: http://www.iconsfind.com/wp-content/uploads/2015/10/20151012_561baed03a54e.png

 - Female icon: http://www.iconsfind.com/wp-content/uploads/2015/10/20151012_561bae5f0713e.png


Author
--------

 - slawdan <schludern@gmail.com>
 - shiluodan@wanxin

