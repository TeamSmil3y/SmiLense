# SmiLense
[![Pigeon](https://img.shields.io/badge/Pigeon-8A2BE2)](https://docs.pigeon.teamsmiley.org) ![VSCode](https://img.shields.io/badge/VSCode-8A2BE2) 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

Smilense (Smile+License) is a solution to fix the mess licensing has become nowadays.
Wanna use a really hacky library but you fear there's gonna be legal consequences due too teeny tiny dependencies all the way down the dependency tree with custom and complicated licenses?
Worry no more, because SmiLense is here!
## Disclaimer
This project is not actively maintained and was devleoped as a project for the [HackBay](https://www.hackbay.de/) hackathon.
## What it does
SmiLense scans for licenses of packages on PiPy and furthermore probe all dependencies in the further dependency tree to examine compatability with your projects requirements.
## Usage
To use SmiLense, either install the provided VSCode extension or any other frontend that calls upon the API. SmiLense will automatically scan for all dependencies and warn you if any licenese collisions emerge.

