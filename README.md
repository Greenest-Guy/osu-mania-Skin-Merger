# osu!mania Skin Merger
osu!mania Skin Merger is a tool designed to merge keycounts from two different osu!mania skins into one. Making skinning easier, so you don't have to read through long skin.ini config files, or search for images in large folders!

![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/Greenest-Guy/osu-mania-Skin-Merger/total?style=for-the-badge&color=%2389CFF0)
![GitHub Release](https://img.shields.io/github/v/release/Greenest-Guy/osu-mania-Skin-Merger?style=for-the-badge&color=029cff)



## :telescope: Preview
https://github.com/user-attachments/assets/a44d55a8-0b71-4629-9b4b-fb92003da497



## :gear: Options
### :bricks: Base Skin
  The base skin is where the majority of the files are drawn from, e.g., menu layout, hitsounds, and the rest of the keycounts, excluding the merging one.

### :heavy_plus_sign: Merge Skin
  The merge skin is where the files for the selected keycount are drawn from. E.g., if you selected 7k, the 7k skin files from the merge file will be added to the base skin.

### :1234: Keycount
  The keycount is taken from the merge skin and added to the base skin.



## :exclamation: Issues & Suggestions
  Please report any issues and or suggestions [here on GitHub](https://github.com/Greenest-Guy/osu-mania-Skin-Merger/issues) or message me on Discord ```rh7thm```



## :toolbox: How the Program Works
1. Creates a directory within the user's downloads folder (product folder), in which the merged skin will be created.

2. Copies all files from the base skin into the product folder.

3. Creates another directory within the product folder named "merge_files"

4. Copies the image files specified inside the merge skin's skin.ini config file into the "merge_files" folder. (specifically the images specified within the [mania] section for the selected keycount)

5. Reports any potentially missing files. (Still finishes the merge)

6. skin.ini config file is edited so that the new keycount has the correct image paths, settings, and adds both authors to the authors section



## :arrow_heading_down: Download Options
### :octocat: GitHub
- [Download v0.2.0-beta (EXE)](https://github.com/Greenest-Guy/osu-mania-Skin-Merger/releases/download/v0.2.0-beta/osu.mania.Skin.Merger.v0.2.0b0.exe)
### :cloud: Google Drive
- [Download via Google Drive](https://drive.google.com/drive/folders/1PNMQrJlja3rPaYmGyrkOC8eXjCaQexuF?usp=sharing)
### :snake: Source Code
1. Clone the repository and install all dependencies
2. Run main.py using Python version 3.7+
