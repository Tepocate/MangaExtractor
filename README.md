# MangaExtractor

MangaExtractor is a python script that will allow the user to extract manga volumes/chapters.

## **Installation - Prerequisites**

You will have to first download Python 3.9 or earlier from https://www.python.org/downloads/

You will also need to download a few python dependencies before running the script for the first time. I would suggest installing these dependencies in a virtual environment. I will be using venv, To create a new environment in the current working directory run the following:

```bash
$ python --three -m venv {MY_VENV_NAME}
```

This will allow you to create a python virtual environment --three signifies the version of python to use.

The following dependencies will need to be downloaded:

```
certifi==2022.6.15
chardet==4.0.0
idna==2.10
numpy==1.23.1
pandas==1.2.0
python-dateutil==2.8.2
pytz==2022.1
requests==2.25.1
six==1.16.0
urllib3==1.26.10
```

There is a requirements.txt file in the repository that will make downloading the dependencies easier. To download run the following commands:

```bash
$ source {MY_VENVV_NAME}/bin/activate
$ pip install -r requirements.txt
```

This will install all the dependencies you need from the requirements.txt.

## **Usage - Running the script**

Once all the dependencies have been downloaded and your venv is activated then you will now be able to run the following command to start the script:

```bash
$ python mangaExtractor.py
```

Once ran you will be asked a question:

```
What is the name of the manga you want to extract:
```
After you input the name of the anime you want to extact the program will display a directoy of similar animes and will ask you:

```
What number from the list is the anime you want to extract?
```

This will display a list manga that you can select from by inputing the number that coincides with the manga. Next you will be asked:

```
Will you be dowloand:
(1) Chapter
(2) volume(s)
Enter 1 or 2:
```

If you select 1 then you be asked which chapter you would like to extact and it will extract that chapter ONLY. If number 2 is selected then you will be asked 2 more questions:

```
What are the volumes you wish to collect in a list? Ex: [1,2,3,4,5,6,7,8]: 
```

This is where you would enter the list of volumes you would like to download. Then the program will ask:

```
What are the chapters in each volume listed? Ex: [1-7,8-17,18-26,27-35,36-44,45-53,54-62,63-71]:
```

Here you will have to enter for each volume in the list from the question before which chapters match to that volume. for example volume 1 would have chpters 1-7, volume 2 will have chapters 8-7, etc. Once this is selected the program will check the length of the list and see if they are equal if not then this means the lists are uneven, meaning for ever volume you want the matching chapters are missing. If everything is correct then the process of extracting the volumes will begin.


## Example

This is how the line of code will look like when you run everything in linux bash:

```Bash
tepocate:[~}]$ cd projects/mangaExtractor/
tepocate:[~/projects/mangaExtractor]$ source {MY_VENVV_NAME}/bin/activate
(MY_VENVV_NAME) tepocate:[~/projects/mangaExtractor/src]$ python mangaExtractor.py

What is the name of the manga you want to extract: my hero academia


659: Boku no Hero Academia
660: Boku no Hero Academia Smash!!
2094: I Was Dismissed from the Heroâ€™s Party Because They Don't Need My Training Skills
2097: I was Told to Relinquish My Fiance to My Little Sister
2299: It's Not My Fault That My Friend's Not Popular
3449: My Hero!
3450: My Home Hero
3454: My Lover Was Stolen, and I Was Kicked Out of the Hero's Party
3455: My Mysterious Girlfriend X
3465: Mysteries, Maidens, And Mysterious Disappearances
5494: Vigilante: Boku no Hero Academia Illegals
5570: When I Was Reincarnated in Another World, I Was a Heroine and He Was a Hero

What number from the list is the anime you want to extract? 659

Will you be dowloand:
(1) Chapter
(2) volume(s)
Enter 1 or 2: 1

What chapter do you want to download? 297

Extracting  Chapter: 1 Page: 22... [■■■■■■■■■■]Done

Archiving files to cbr... [■■■■■■■■■■]Done

cbr located /home/tepocate/projects/MangaExtractor/src/chapters/my hero academia/my hero academia c297.cbr

```