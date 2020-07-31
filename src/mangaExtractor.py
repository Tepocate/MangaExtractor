import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os

index = 1
class web_scrape:
    def __init__(self,manga_name,url_manga_name,current_vol, end_chapter):
        self.manga_name = manga_name
        self.url_manga_name = url_manga_name
        self.manga_name = manga_name
        self.vol = current_vol
        self.last_chapter = end_chapter
        self.info = self.get_info(f'https://mangasee123.com/read-online/{self.url_manga_name}-chapter-1-page-1.html')

    def vol_scrape(self):
        page_counter = 0
        global index
        vol_df = self.info[0]
        while (int(vol_df.loc[index]['Chapter'])-100000)/10 < self.last_chapter:
            current_chapter = (int(vol_df.loc[index]['Chapter'])-100000)/10
            current_page = int(vol_df.loc[index]['Page'])
            initial_page = 1 
            while initial_page < (current_page + 1):
                if current_chapter.is_integer():
                    initial_page_url = f"https://{self.info[1]}/manga/{self.url_manga_name}/{int(current_chapter):04d}-{initial_page:03d}.png"
                else: 
                    initial_page_url = f"https://{self.info[1]}/manga/{self.url_manga_name}/{current_chapter:06.1f}-{initial_page:03d}.png"
                print(f"page url = {initial_page_url}") # Testing
                self.save_page(initial_page_url,page_counter)
                print(f"Volume {self.vol} page {page_counter} extracted")

                initial_page += 1
                page_counter += 1
            index += 1
        print(f'global index = {index}')


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
        df.index = df.index + 1

        return df, png_path



def ask():
    # enable after testing
    # manga_name = input("What is the name of the excel sheet you have created that "\
    #                     "contains the columns currentVol|startChapter|endChapter in "\
    #                     "that order: ")# A valid response would be: My Hero Academia

    # xlsx = input(f"What is the name of the excel workbook file in {os.getcwd()}, "\
    #                 "include the file extension in the name: ") # A valid input would be: MangaVolumes.xlsx

    # url_manga_name = input("What is the name with of the manga you want to download "\
    #                         "form https://mangasee123.com/directory/ make sure you "\
    #                         "include a - between every word: ") # A valid answer would be: Boku-No-Hero-Academia

    manga_name = 'Onepunch Man'
    xlsx = 'MangaVolumes.xlsx'
    url_manga_name = 'Onepunch-Man'

    df = pd.read_excel (f'{os.getcwd()}/{xlsx}',sheet_name= manga_name,dtype=object) 
    # print("Extracting volumes now")
    i=0
    while i < len(df):
        current_vol = df.loc[i,'currentVol']
        end_chapter = df.loc[i+1,'startChapter']
        my_hero = web_scrape(manga_name, url_manga_name, current_vol, end_chapter)
        my_hero.vol_scrape()

        i += 1

    print(f"Finish Extracting.\nYour volumes are located: {os.getcwd()}/volumes")



if __name__ == '__main__':
    ask()




