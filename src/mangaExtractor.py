import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
import shutil


class web_scrape:
    def __init__(self,manga_name,url_manga_name,current_vol, start_chapter, end_chapter):
        self.manga_name = manga_name
        self.url_manga_name = url_manga_name
        self.manga_name = manga_name
        self.vol = current_vol
        self.start_chapter = start_chapter
        self.end_chapter = end_chapter
        self.info = self.get_info(f'https://mangasee123.com/read-online/{self.url_manga_name}-chapter-{self.start_chapter}-page-1.html')

    def vol_scrape(self):
        page_counter = 0
        index = 0
        vol_df = self.info[0]

        first_chapter = ((self.start_chapter + index) * 10)+100000
        last_chapter = (self.end_chapter * 10) + 100000
        
        while first_chapter <= last_chapter:
            first_page = 1
            last_page = vol_df.loc[((self.start_chapter + index)*10)+100000]['Page']
            while first_page <= last_page:
                first_page_url = f"https://{self.info[1]}/manga/{self.url_manga_name}/{self.start_chapter + index:04d}-{first_page:03d}.png"
                self.save_page(first_page_url,page_counter)
                print(f"Volume {self.vol} page {page_counter} extracted")

                first_page += 1
                page_counter += 1
            index += 1
            first_chapter = ((self.start_chapter + index) * 10)+100000
        self.archive()

    def get_page(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
        page = requests.get(url, headers=headers)

        return page

    def save_page(self,png_url,page_counter):
        page = self.get_page(png_url)
        
        try:
            path = f'{os.getcwd()}/volumes/{self.manga_name}/{self.manga_name} v{self.vol:02d}'
            os.makedirs(path)
        except FileExistsError:
            pass
        
        file = open(f"{path}/{self.manga_name} v{self.vol}-{page_counter:03d}.png","wb")
        file.write(page.content)
        
        file.close()

    def get_info(self, site):

        page = self.get_page(site)
        soup = BeautifulSoup(page.content, 'html.parser')

        scripts = soup.find_all('script')

        json_chapter = json.loads(scripts[14].string.split('\r\n\t\t\t')[7].split(';')[0].split('=')[1])

        png_path = scripts[14].string.split('\r\n\t\t\t')[6].split(';')[0].split('=')[1].strip().split('"')[1]

        df = pd.DataFrame(json_chapter)
        df = df.drop(columns=['Directory','ChapterName','Date','Type'])
        df = df.astype(str).astype(int).set_index('Chapter')
        #df.index = df.index + 1

        return df, png_path

    def archive(self):
        print("Archiving files to cbr")
        path = f'{os.getcwd()}/volumes/{self.manga_name}/{self.manga_name} v{self.vol:02d}'
        shutil.make_archive(path, 'zip', path)

        os.rename(f'{path}.zip',f'{path}.cbr')
        print(f"cbr located {path}.cbr")
        shutil.rmtree(f'{path}')


def ask():
    # manga_name = input("What is the name of the excel sheet you have created that "\
    #                     "contains the columns currentVol|startChapter|endChapter in "\
    #                     "that order: ")# A valid response would be: My Hero Academia

    # xlsx = input(f"What is the name of the excel workbook file in {os.getcwd()}, "\
    #                 "include the file extension in the name: ") # A valid input would be: MangaVolumes.xlsx
    
    # url_manga_name = input("What is the name with of the manga you want to download "\
    #                         "form https://mangasee123.com/directory/ make sure you "\
    #                         "include a - between every word: ") # A valid answer would be: Boku-No-Hero-Academia

    manga_name = 'My Hero Academia' # testing

    xlsx = 'MangaVolumes.xlsx' # testing
    
    url_manga_name = 'Boku-No-Hero-Academia' # testing
    

    df = pd.read_excel (f'{os.getcwd()}/{xlsx}',sheet_name= manga_name,dtype=object) 

    i=0
    while i < len(df):
        current_vol = df.loc[i,'currentVol']
        start_chapter = df.loc[i,'startChapter']
        end_chapter = df.loc[i,'endChapter']
        my_hero = web_scrape(manga_name, url_manga_name, current_vol, start_chapter, end_chapter)
        my_hero.vol_scrape()

        i += 1

    print(f"Finish Extracting.\nYour volumes are located: {os.getcwd()}/volumes")


if __name__ == '__main__':
    ask()

