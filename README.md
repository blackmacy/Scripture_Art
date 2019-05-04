# Scripture_Art

This project is developed for the [2019 Seattle Code for the Kingdom (C4TK) hackathon](https://codeforthekingdom.org/seattle-hackathon-2019.html). 

This repository contains our Python implementation with Tk GUI that randomly generates scripture art, i.e., images with Bible verse(s), for the user. 

## Introduction

This package is designed for random generation of scripture art. The input is a scripture quote, such as John 3:16 and Jeremiah 29:11-13, in the GUI panel. Then the user can generate any number of random scripture art, and save their favorite one(s). To ensure that the color of the scripture text has high contrast against the background, we compute the mean color of the background, and find the complement color in the HSV color space for the text. There is also an iterative scheme that automatically searches for the most suitable font size for the scripture. 

## Coding Structure
1. `./create_scripture_art.py`: The main Python code of our app
2. `./bible/` folder: Bible database with csv files (from [bible_databases](https://www.google.com)) and the default Bible version is ASV
3. `./font/` folder: Default fonts to be randomly chosen from
3. `./bg/` folder: Default backgrounds to be randomly chosen from
3. `./output/` folder: Folder for image output

## How to Build
1. Install required Python packages. 
```pip install python-scriptures```
```pip install pillow```
2. Change directory to the cloned repository.
```cd <Scripture_Art>```
3. (Option) Add your own images or fonts in the corresponding folders
4. Run the Python script. 
```python create_scripture_art.py```

## How to Use
1. Input the scripture quote at "Scripture quote:", such as John 3:16 and Jeremiah 29:11-13. 
2. Click the "Create" button and then a scripture art will be automatically generated. 
3. Click the "Next" button to generate a new scripture art.
4. Click the "Save" button to save your scripture art, which will be saved in the output folder. 

<div align="center">
    <img src="/example.jpg", width="640">
</div>

## Demonstration of Output
<div align="center">
    <img src="/output0.jpg", width="320">
</div>

<div align="center">
    <img src="/output1.jpg", width="640">
</div>

<div align="center">
    <img src="/output2.jpg", width="640">
</div>

<div align="center">
    <img src="/output3.jpg", width="640">
</div>

## Disclaimer
For any question you can contact [Yijin (Macy) Lee](https://github.com/blackmacy).
