import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import shutil
import re


class web_scrape:
    def __init__(self, manga_name, url_manga_name, current_vol, start_chapter, end_chapter):
        self.manga_name = manga_name
        self.url_manga_name = url_manga_name
        self.vol = current_vol
        self.start_chapter = start_chapter
        self.end_chapter = end_chapter
        self.info = self.get_info(f'https://mangasee123.com/read-online/{self.url_manga_name}-chapter-{self.start_chapter}-page-1.html')

    def vol_scrape(self):
        page_counter = 0
        index = 0
        vol_df = self.info[0]

        first_chapter = (self.start_chapter * 10) + 100000
        last_chapter = (self.end_chapter * 10) + 100000

        chapter_df = vol_df[vol_df['Chapter'].between(first_chapter,last_chapter)]

        for i in chapter_df.index:
            first_page = 1
            last_page = chapter_df['Page'][i] # Last page for the current chapter i
            current_chapter = (chapter_df['Chapter'][i] - 100000)/10 # Does math to get the num of current chapter
            while first_page <= last_page:
                if current_chapter.is_integer():
                    first_page_url = f"https://{self.info[1]}/manga/{self.url_manga_name}/{current_chapter:04.0f}-{first_page:03d}.png"
                else:
                    first_page_url = f"https://{self.info[1]}/manga/{self.url_manga_name}/{current_chapter:06.1f}-{first_page:03d}.png"
                self.save_page(first_page_url,page_counter)
                print(f"Volume: {self.vol} Chapter: {current_chapter} Page {page_counter} extracted")
                first_page += 1
                page_counter += 1
        self.archive()

    # Save the pages into volume folder
    def save_page(self, png_url,page_counter):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
        page = requests.get(png_url, headers=headers)
        
        try:
            path = f'{os.getcwd()}/volumes/{self.manga_name}/{self.manga_name} v{self.vol:02d}'
            os.makedirs(path)
        except FileExistsError:
            pass
        
        file = open(f"{path}/{self.manga_name} v{self.vol}-{page_counter:03d}.png","wb")
        file.write(page.content)
        
        file.close()

    # Scrape the info needed form the page
    def get_info(self, site):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
        page = requests.get(site, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        scripts = soup.find_all('script')

        json_chapter = json.loads(scripts[15].string.split('\r\n\t\t\t')[7].split(';')[0].split('=')[1])

        png_path = scripts[15].string.split('\r\n\t\t\t')[6].split(';')[0].split('=')[1].strip().split('"')[1]

        df = pd.DataFrame(json_chapter)
        df = df.drop(columns=['Directory','ChapterName','Date','Type'])
        df = df.astype(str).astype(int)

        return df, png_path

    # zip up to a cbr archive
    def archive(self):
        print("Archiving files to cbr")
        path = f'{os.getcwd()}/volumes/{self.manga_name}/{self.manga_name} v{self.vol:02d}'
        shutil.make_archive(path, 'zip', path)

        os.rename(f'{path}.zip',f'{path}.cbr')
        print(f"cbr located {path}.cbr")
        shutil.rmtree(f'{path}')

# Asking the questions to get the detials of what manga you are trying to extract
def ask():
    manga_name = input("What is the name of the excel sheet you have created that "\
                        "contains the columns currentVol|startChapter|endChapter in "\
                        "that order: ")# A valid response would be: My Hero Academia
    
    url_manga_name = input("What is the name with of the manga you want to download "\
                            "form https://mangasee123.com/directory/ make sure you "\
                            "include a - between every word: ") # A valid answer would be: Boku-No-Hero-Academia

    single_multiple = input('Will you be dowloand:\n(1)A single chapter\n(2)Mutliple volumes\nEnter 1 or 2: ')
    if single_multiple == '2':
        volumes = input('What are the volumes you wish to collect in a list? Ex: [1,2,3,4,5,6,7,8] : ')
        volumes_list = re.split('\[|\]|,',volumes)
        while ("" in volumes_list): volumes_list.remove("")
        # OUTPUT: ['1', '2', '3', '4', '5', '6', '7', '8']

        chapters = input('What are the chapters in each volume listed? Ex: [1-7,8-17,18-26,27-35,36-44,45-53,54-62,63-71] :')
        Chapters_list = re.split('\[|\]|,',Chapters)
        while("" in Chapters_list): Chapters_list.remove("")
        # OUTPUT: ['1-7', '8-17', '18-26', '27-35', '36-44', '45-53', '54-62', '63-71']

        if len(Chapters_list) == len(volumes_list):
            i=0
            while i < len(volumes_list):
                current_vol = volumes[i]
                start_chapter = Chapters_list[i].split('-')[0]
                end_chapter = Chapters_list[i].split('-')[1]
                manga = web_scrape(manga_name, url_manga_name, current_vol, start_chapter, end_chapter)
                manga.vol_scrape()

                i += 1

            print(f"Finish Extracting.\nYour volumes are located: {os.getcwd()}/volumes")
        else:
            print(f'Chapters list length, {Chapter_list}, isn\'t the same as the list length for Volumes, {volumes}')
            print('Please make sure you are not missing any chapters or volumes in your list')

    else:
        current_vol = 0
        chapters = input('What chapter do you want to download? ')
        start_chapter = int(chapters)
        end_chapter = int(chapters)
        manga = web_scrape(manga_name, url_manga_name, current_vol, start_chapter, end_chapter)
        manga.vol_scrape()


if __name__ == '__main__':
    ask()

