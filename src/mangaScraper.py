import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os

def vol_my_hero(vol, current_chapter,last_chapter,url_manga_name, manga_name):
    page_counter = 1
    while current_chapter <= last_chapter:
        # https://mangaseeonline.us/read-online/Onepunch-Man-chapter-1-page-1.html
        main_website = f'https://mangaseeonline.us/read-online/{url_manga_name}-{current_chapter}-page-1.html'
        json_png_url = get_info(main_website)
        initial_page = 1 
        while initial_page < len(json_png_url):
            current_page_url = json_png_url[f'{initial_page}']
            save_page(vol,current_chapter,current_page_url,initial_page,page_counter, manga_name)

            initial_page += 1
            page_counter += 1
        current_chapter += 1


def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
    page = requests.get(url, headers=headers)

    return page


def get_info(main_site):
    page = get_page(main_site)
    soup = BeautifulSoup(page.content, 'html.parser')

    scripts = soup.find_all('script')
    json_soup = json.loads(scripts[17].string.split(';')[1].strip().split('=')[1])

    return json_soup


def save_page(vol,chapter,png_url,page_num,page_counter, manga_name):
    page = get_page(png_url)
    
    try:
        path = f'../volumes/{manga_name}/{manga_name} v{vol:02d}'
        os.makedirs(path)
    except FileExistsError:
        pass
    
    file = open(f"../volumes/{manga_name}/{manga_name} v{vol:02d}/{manga_name} v{vol}-{page_counter:03d}.png","wb")
    file.write(page.content)
    
    file.close()


if __name__ == '__main__':
    manga_name = 'My Hero Academia'
    df = pd.read_excel (r'/home/tepocate/projects/comicScraper/code/MangaVolumes.xlsx',sheet_name= manga_name)
    url_manga_name = 'Boku-No-Hero-Academia-chapter'
    i=0
    while i < len(df):
        current_vol = df.loc[i,'currentVol']
        start_chapter = df.loc[i,'startChapter']
        end_chapter = df.loc[i,'endChapters']
        vol_my_hero(current_vol, start_chapter, end_chapter, url_manga_name, manga_name)

        i += 1

