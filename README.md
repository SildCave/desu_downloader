# desu_downloader

## description
Simple tool for easy downloadig series from desu-online.pl

## requirements

- python 3.6 or later



## installation
No installation required, just download the script and vuala

## usage

The downloader will create a new folder for the episodes and then download them from cda.pl

#### examples
- ```python downloader.py --link https://desu-online.pl/anime/spy-x-family/```
- ```python downloader.py --link https://desu-online.pl/anime/spy-x-family/ --path C:\Users\xyz\Videos``` 

> Downloader will download 8 episodes at once by default, you can change that by using for example "--at_once 5"
> Downloader will download all episodes by default, but you can specify episodes that u want to download by --episodes, exaple: --episodes 3-8"

> Use "" if your path contains spaces, example: --path "C:\Users\xyz\My beloved videos"
