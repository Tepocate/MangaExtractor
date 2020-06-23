import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os

index = 1
class web_scrape:
    def __init__(self,manga_name,url_manga_name,current_vol, end_chapter):
        self.manga_name = manga_name
        self.url_manga_name =url_manga_name
        self.manga_name = manga_name
        self.vol = current_vol
        self.last_chapter = end_chapter

    def vol_scrape(self):
        page_counter = 0
        global index
        chapter_df = self.get_dataframe(f'https://mangaseeonline.us/read-online/{self.url_manga_name}-chapter-1-page-1.html')
        while float(chapter_df.loc[index]['ChapterDisplay']) < self.last_chapter:
            main_website = f"https://mangaseeonline.us/read-online/{self.url_manga_name}-chapter-{chapter_df.loc[index]['ChapterDisplay']}-page-1.html"
            json_vol = self.get_info(main_website)
            initial_page = 1 
            while initial_page < len(json_vol):
                current_page_url = json_vol[f'{initial_page}']
                self.save_page(current_page_url,page_counter)
                print(f"Volume {self.vol} page {page_counter} extracted")

                initial_page += 1
                page_counter += 1
            index += 1


    def get_page(self,url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
        page = requests.get(url, headers=headers)

        return page


    def get_info(self,main_site):
        page = self.get_page(main_site)
        soup = BeautifulSoup(page.content, 'html.parser')

        scripts = soup.find_all('script')

        json_page = json.loads(scripts[17].string.split(';')[1].strip().split('=')[1])

        return json_page


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

    def get_dataframe(self, site):
        page = self.get_page(site)
        soup = BeautifulSoup(page.content, 'html.parser')

        scripts = soup.find_all('script')

        json_chapter = json.loads(scripts[17].string.split(';')[0].strip().split('=')[1])

        chapter_df = pd.DataFrame(json_chapter)
        chapter_df = chapter_df.T.iloc[1:].drop(columns=['Chapter','ChapterIndex','ChapterName','Date','Type'])
        chapter_df = chapter_df.set_index('ChapterDisplay').reset_index()
        chapter_df.index = chapter_df.index + 1

        return chapter_df
    
def ask():
    manga_name = input("What is the name of the excel sheet you have created that "\
                       "contains the columns currentVol|startChapter|endChapter in "\
                       "that order: ")# A valid response would be: My Hero Academia

    xlsx = input(f"What is the name of the excel workbook file in {os.getcwd()}, "\
                  "include the file extension in the name: ") # A valid input would be: MangaVolumes.xlsx
    
    url_manga_name = input("What is the name with of the manga you want to download "\
                           "form https://mangaseeonline.us/directory/ make sure you "\
                           "include a - between every word: ") # A valid answer would be: Boku-No-Hero-Academia
    df = pd.read_excel (f'{os.getcwd()}/{xlsx}',sheet_name= manga_name,dtype=object) 
    
    print("Extracting volumes now")
    i=0
    while i < (len(df)-1):
        current_vol = df.loc[i,'currentVol']
        end_chapter = df.loc[i+1,'startChapter']
        my_hero = web_scrape(manga_name, url_manga_name, current_vol, end_chapter)
        my_hero.vol_scrape()

        i += 1
    print(f"Finish Extracting.\nYour volumes are located: {os.getcwd()}/volumes")



if __name__ == '__main__':
    ask()
    
    



