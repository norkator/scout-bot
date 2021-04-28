# Scout Bot

RuneScape scout bot machine vision project.


Table of contents
=================
* [Documents](#documents)
* [Infrastructure](#infrastructure)
* [Install](#install)
* [Samples](#samples)
* [Troubleshooting](#troubleshooting)
* [Hints](#hints)



Documents
============
Documents for development.

* Project Google Drive folder:
    https://drive.google.com/drive/folders/1Bjp6M0aU6s2qkTvNfAAzTgtLijzt2ykQ?usp=sharing
* Random mouse curve possibility
    https://stackoverflow.com/questions/44467329/pyautogui-mouse-movement-with-bezier-curve

Infrastructure
============
Infra...


Install
============

Get game window position with `Mouse.py` script. Positions are left top and bottom right corners.

```text
0,0       X increases -->
+---------------------------+
|                           | Y increases
|                           |     |
|   1920 x 1080 screen      |     |
|                           |     V
|                           |
|                           |
+---------------------------+ 1919, 1079
```

Define configuration separating them by `;` and defining target strategy.

```ini
[bot]
game_frames=0,80,1100,700;0,80,1100,700
strategies=scout;scout
```

1. ...
2. ...



Samples
============
Running program sample

```python
...
```

Troubleshooting
============

1. Screen capture does not capture window
    * See system security and privacy settings for possible permissions.  
2. Mouse does not move automatically
    * See system security and privacy settings for possible permissions.  


Hints
============
Some command hints for python

See installed libraries and their version.
```shell script
pip freeze
```
