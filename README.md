# MangaExtractor

MangaExtractor is a python script that will allow the user to extract manga volumes/chapters.

## **Installation - Prerequisites**

You will have to first download Python 3.7.3 or earlier from https://www.python.org/downloads/

You will also need to download a few python dependencies before running the script for the first time. I would suggest installing these dependencies in a virtual environment. I will be using pipenv, you can install pipenv by doing the following:

```bash
pip install pipenv
```

to create a new environment in the current working directory run the following:

```bash
pipenv --three
```

This will allow you to create a python virtual environment --three signifies the version of python to use

THe following dependencies will need to be downloaded:

```
bs4==0.0.1
  - beautifulsoup4 [required: Any, installed: 4.9.1]
    - soupsieve [required: >1.2, installed: 2.0.1]
pandas==1.0.5
  - numpy [required: >=1.13.3, installed: 1.18.5]
  - python-dateutil [required: >=2.6.1, installed: 2.8.1]
    - six [required: >=1.5, installed: 1.15.0]
  - pytz [required: >=2017.2, installed: 2020.1]
requests==2.24.0
  - certifi [required: >=2017.4.17, installed: 2020.4.5.2]
  - chardet [required: <4,>=3.0.2, installed: 3.0.4]
  - idna [required: <3,>=2.5, installed: 2.9]
  - urllib3 [required: !=1.25.1,<1.26,>=1.21.1,!=1.25.0, installed: 1.25.9]
xlrd==1.2.0
```

There is a requirements.txt file in the repository that will make downloading the dependencies easier. To download follow the following command:

```bash
pipenv install -r requirements.txt
```

OR

if you are in the same directory ad the pipenvFiles from the repo then you can just do the following command

```Bash
pipenv install
```

This will install all the dependencies you need from my pipfile.

To learn more about pip you can visit these helpful links:

- https://pipenv-fork.readthedocs.io/en/latest/basics.html
- https://pipenv.kennethreitz.org/en/latest/cli/
- https://pipenv.pypa.io/en/latest/

## **Usage - Running the script**

Once all the dependencies have been downloaded then you will now be able to run the following command to start the script:

```bash
pipenv run python mangaExtractor.py
```

OR

```bash
pipenv shell # This allows you to open the virtual environment in that directory
python mangaExtractor.py # Within the virtual environment run the script
```

Once ran you will be asked 2 questions. The first question asks:

```
What is the name of the excel sheet you have created that contains the columns currentVol|startChapter|endChapter in that order:
```

You will need to create or add to an excel workbook. There is an example in the repository in case you don not know what is needed. You will then enter the sheet name for this question. Make sure you save this document in the same directory as the python script.

The 2nd question states:

```
What is the name of the excel workbook file in {os.getcwd()}, include the file extension in the name:
```

This is basically asking for the file name you must include the file extension when entering the name "EXAMPLE.xlsx" for example.

The 3rd and last question asked is:

```
What is the name with of the manga you want to download form https://mangasee123.com/directory/ make sure you include a - between every word:
```

So basically you will have to get the name of the manage you want and enter it exactly how you see.

## Example

This is how the line of code will look like when you run everything in linux bash:

```Bash
tepocate:{~}$ cd projects/mangaExtractor/src/
tepocate:{~/projects/mangaExtractor/src}$ pipenv run python mangaExtractor.py
What is the name of the excel sheet you have created that contains the columns currentVol|startChapter|endChapter in that order: Onepunch Man
What is the name of the excel workbook file in /home/tepocate/projects/mangaExtractor/src, include the file extension in the name: MangaVolumes.xlsx
What is the name with of the manga you want to download form https://mangasee123.com/directory/ make sure you include a - between every word: Onepunch-Man
Extracting volumes now
Volume 1 page 0 extracted
Volume 1 page 1 extracted
Volume 1 page 2 extracted
Volume 1 page 3 extracted
Volume 1 page 4 extracted
Volume 1 page 5 extracted
Volume 1 page 6 extracted
Volume 1 page 7 extracted
Volume 1 page 8 extracted
Volume 1 page 9 extracted
Volume 1 page 10 extracted
Volume 1 page 11 extracted
```

This is how the line of code will look like when you run everything in windows PowerShell:

```PowerShell
PS A:\Shared Folder> cd ~
PS C:\Users\Christian> cd 'A:\Shared Folder\src\'
PS A:\Shared Folder\src> pipenv run python .\mangaExtractor.py
What is the name of the excel sheet you have created that contains the columns currentVol|startChapter|endChapter in that order: My Hero Academia
What is the name of the excel workbook file in A:\Shared Folder\src, include the file extension in the name: MangaVolumes.xlsx
What is the name with of the manga you want to download form https://mangasee123.com/directory/ make sure you include a - between every word: Boku-No-Hero-Academia
Extracting volumes now
Volume 1 page 0 extracted
Volume 1 page 1 extracted
Volume 1 page 2 extracted
Volume 1 page 3 extracted
Volume 1 page 4 extracted
Volume 1 page 5 extracted
Volume 1 page 6 extracted
Volume 1 page 7 extracted
Volume 1 page 8 extracted
Volume 1 page 9 extracted
Volume 1 page 10 extracted
Volume 1 page 11 extracted
```
