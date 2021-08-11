from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import numpy
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    parsed_html = soup(html, 'html.parser')

    first_div = parsed_html.select_one('div.list_text')
    content_title = first_div.find('div', class_='content_title')
    Get_title_text = content_title.get_text()
    body_text = first_div.find('div', class_='article_teaser_body')
    Get_body_text = body_text.get_text()


    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    second_button = browser.find_by_tag('button')[1]
    second_button.click()
    html = browser.html
    parsed_html = soup(html, 'html.parser')
    img_url = parsed_html.find('img', class_='fancybox-image').get('src')
    full_img_url = f'https://spaceimages-mars.com/{img_url}'

    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['Properties', 'Mars', 'Earth']
    df.set_index('Properties', inplace=True)
    html_table = df.to_html()


    url = 'https://marshemispheres.com/'
    browser.visit(url)
    html = browser.html
    parsed_html = soup(html, 'html.parser')
    hemisphere_image_urls = []
    links = parsed_html.find_all('img', class_='thumb')


    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_tag('img.thumb')[i].click()
        new_link = browser.links.find_by_text('Sample').first['href']    
        hemisphere['img_url'] = new_link
        new_headline = parsed_html.find_all('h3')[i].get_text()
        hemisphere['title'] = new_headline
        
        hemisphere_image_urls.append(hemisphere)
        browser.back()
        

    data = {
        "news_title": Get_title_text,
        "news_paragraph": Get_body_text,
        "featured_image": full_img_url,
        "Ttable": html_table,
        "hemispheres": hemisphere_image_urls,
        }
    browser.quit()
    return data

if __name__ == "__main__":
    print(scrape())