# PTWordFinder
[![Build](https://github.com/DarekRepos/PanTadeuszWordFinder/actions/workflows/python-package.yml/badge.svg)](https://github.com/DarekRepos/PanTadeuszWordFinder/actions/workflows/python-package.yml)
[![Tests Status](https://github.com/DarekRepos/PanTadeuszWordFinder/blob/master/reports/coverage/coverage-unit-badge.svg)](./reports/junit/report.html)
[![Coverage Status](https://github.com/DarekRepos/PanTadeuszWordFinder/blob/master/reports/coverage/coverage-badge.svg)](./reports/coverage/index.html)
[![Flake8 Status](https://github.com/DarekRepos/PanTadeuszWordFinder/blob/master/reports/flake8/flake8-badge.svg)](./reports/flake8/index.html)

"What specific words would you like to read?"
Counting words in "Pan Tadeusz" poem

## Python version
tested with Python >= 3.10.6

## Why
It was started as a project to exercise python language. The code helped to find specific words in a selected file. It became command line tool that help find any word within any file. The files can be selected by command line

## how to use
you can installl this cmd tool from pip:
```
    pip install PTWordFinder
```
Usage: ptwordf calculate-words WORDS_INPUT_FILE SEARCHED_FILE

<strong>where:</strong>

WORDS_INPUT_FILE - is path to input file (.txt) that contain searched words 

SEARCHED_FILE - is path to file that program search for a specific word

Try 'ptwordf --help' for help

<strong>examples:</strong>

 ptwordf calculate-words words-list.txt test-file.txt

 ptwordf calculate-words srcfolder/words-list.csv newfolder/test-file.csv

## Features
- [x] lines counter
- [x] a specific word counter
- [x] tracking the script execution time
- [x] support csv files