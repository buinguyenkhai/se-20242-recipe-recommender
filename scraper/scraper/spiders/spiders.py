import scrapy
from scrapy.selector import Selector
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
from scraper.spiders.utils import *

class FrameworkSpider(scrapy.Spider):
    name = None
    url = None
    
    def start_requests(self):
        category = getattr(self, "category", None)       # for testing
        print(self.url)
        if category is not None:
            yield scrapy.Request(self.url + "/" + category, callback=self.parse_recipe)
        else:
            yield scrapy.Request(self.url, callback=self.parse_category)
            
    def parse_recipe(self):
        pass
    
    def parse_category(self):
        pass
    
    def parse(self):
        pass
        

class VaobepSpider(FrameworkSpider):
    name = "vaobep"
    url = "https://www.dienmayxanh.com/vao-bep"
    '''
    start_urls = ["https://www.dienmayxanh.com/vao-bep/3-cong-thuc-lam-ginger-shot-dep-da-moi-ngay-voi-may-ep-cham-22592/",
                  "https://www.dienmayxanh.com/vao-bep/cach-lam-dua-mam-mien-tay-chua-chua-ngot-ngot-dam-vi-que-nha-14413/",
                  "https://www.dienmayxanh.com/vao-bep/3-cach-lam-banh-flan-tra-xanh-khong-can-lo-nuong-mem-muot-14059/",
                  "https://www.dienmayxanh.com/vao-bep/2-cach-lam-che-sau-rieng-da-nang-va-che-sau-rieng-04610/",
                  "https://www.dienmayxanh.com/vao-bep/danh-gia-bep-tu-kaff-chi-tiet-va-tim-hieu-uu-nhuoc-diem-22399/",
                  "https://www.dienmayxanh.com/vao-bep/3-cach-don-gian-lam-mon-thit-bo-xao-ngon-la-mieng-01751/"]
    '''
    def __init__(self, *args, **kwargs):
        super(VaobepSpider, self).__init__(*args, **kwargs)
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')  
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=chrome_options)

    def closed(self, reason):
        self.driver.quit()
    
    def parse_category(self, response):
        for href in response.css("div[class='menu-cooking topmenu'] > ul > li > a::attr(href)").re("^/\S+/\S+$"):
            yield response.follow(href, callback=self.parse_recipe)

    def parse_recipe(self, response):
        self.driver.get(response.url)
        sleep(3)  

        while True: 
            try:
                show_more = self.driver.find_element(By.CSS_SELECTOR, 'a.seemore-cook')
                show_more.click()
                sleep(1)
            except Exception as e:
                self.logger.info(f"No more 'Show more' button or error: {e}")
                break

        sel = Selector(text=self.driver.page_source).css("ul.cate-cook > li > a::attr(href)").getall()
        yield from response.follow_all(sel, callback=self.parse)

    def parse(self, response):
        recipes = response.css("div.box-recipe")
        if len(recipes) == 0:
            recipes = response.css("div.detail")
            
        for recipe in recipes:
            # if len(step_titles) == 0 and len(step_detail) == 0: continue
            # itemPipeline
            yield {
                "title": recipe.css("h2::text").get().strip() if len(recipes) > 1 
                         else recipe.css("h1::text").get().strip(),
                # add img instead of video
                "image": recipe.css("div.video > img::attr(data-src)").get() if len(recipes) > 1 
                         else recipe.css("div.video > img::attr(src)").get(),
                "ingredients": clean_text(recipe.css("div.staple > span").getall()),
                "step-detail": "\n".join([" ".join(clean_text(step.css("p").getall())) for step in recipe.css("div.text-method")]),
                "tags": [response.css("div.breadcrum > a::text")[-1].get()],
                "date": response.css("div[class~='txtAuthor']").re("[0-9]{2}/[0-9]{2}/[0-9]{4}")[0],
                "source": "Vào bếp (Điện máy Xanh)",
                "url": response.url
            }
            
'''
class CandyCanCookSpider(scrapy.Spider):
    name = "candycancook"
    """
    start_urls = ["https://candycancook.com/2010/10/nam-tok-moo-thai-spicy-pork-salad/",
                  "https://candycancook.com/2019/04/nam-tok-moo-salad-thit-lon-kieu-thai/",
                  "https://candycancook.com/2019/11/an-o-new-york-pancake-va-waffles-o-clinton-street-co-restaurant/",
                  "https://candycancook.com/2017/08/hat-sen-bot-loc-long-nhan/",
                  "https://candycancook.com/2013/07/cach-lam-tom-cuon-thit-xong-khoi/",
                  "https://candycancook.com/2010/10/cach-lam-caramel-popcorn-bap-rang-bo/"]
    """
    def start_requests(self):
        yield scrapy.Request("https://candycancook.com/", callback=self.parse_category)
        
    def parse_category(self, response):
        yield from response.follow_all(css="aside[class='widget widget_categories'] > ul > li > a",
                                       callback=self.parse_recipe)
        
        #yield scrapy.Request("https://candycancook.com/category/cac-loai-banh/banh-viet/", callback=self.parse_recipe)
            
    def parse_recipe(self, response):
        yield from response.follow_all(css="div.thumbnail > a", callback=self.parse)
        
        next_button_url = response.css("a[class='next page-numbers']::attr(href)").get()
        if next_button_url is not None:
            yield response.follow(next_button_url, callback=self.parse_recipe)
   
    def parse(self, response):
        recipe = response.css("#penci-post-entry-inner").get()
        soup = BeautifulSoup(recipe, 'html.parser')
        
        def get_attr(text):
            res = []
            attr_text = soup.find(name="strong", string=re.compile(text)).find_parent()
            
            for _ in range(3):
                attrs = attr_text.find_next_siblings("ul")
                if len(attrs) > 0: break
                attr_text = attr_text.find_parent()
            
            for small_attrs in attrs:
                res.extend([attr.get_text() for attr in small_attrs.find_all("li")])    
                
            return res
        
        step_detail = clean_text(get_attr("Cách làm"))
        ingredients = get_attr("Nguyên liệu")
        ingredients = ingredients[:len(ingredients) - len(step_detail)]
        
        yield {
                "title": response.css("h1::text").get(),
                "image": response.css("div[id^='attachment'] > a::attr(href)").get(), #####################
                "ingredients": ingredients,
                "step-title": None,
                "step-detail": step_detail,
                "tags": None,
                "url": response.url
            }
        # remove null if needed
        
class SoTayNauAnSpider(scrapy.Spider):
    name = "sotaynauan"
    """
    start_urls = ["https://sotaynauan.com/cach-lam-soda-chanh/",
                  "https://sotaynauan.com/cach-lam-ga-hap-hanh/",
                  "https://sotaynauan.com/huong-dan-lam-banh-dua-dai-loan-ngon-ngat-ngay/",
                  "https://sotaynauan.com/banh-tart-chanh-leo-ban-thu-chua/"]
    """
    
    def start_requests(self):
        yield scrapy.Request("https://sotaynauan.com/chuyen-muc/mon-ngon-moi-ngay/", callback=self.parse_category)
        
    def parse_category(self, response):
        yield from response.follow_all(css="#sidebar > div > ul > li > a", callback=self.parse_recipe)
        
    def parse_recipe(self, response):
        yield from response.follow_all(css="div.category-2 > a", callback=self.parse)
        
        next_button_url = response.css("a.nextpostslink::attr(href)").get()
        if next_button_url is not None:
            yield response.follow(next_button_url, callback=self.parse_recipe)
    
    def parse(self, response):
        yield {
                "title": response.css("h2.entry-title > a::text").get(),
                "image": response.css("div.thumb > img::attr(src)").get(), #####################
                "ingredients": clean_text(response.css("ul.ingredients > li").getall()),
                "step-title": None,
                "step-detail": [text for text in clean_text(response.css("div.instructions > p, div.instructions > ul > li").getall())
                                if not re.match(r'^\w*$', text)],
                "tags": None,
                "url": response.url
            }
        # remove null if needed
            
    
    
    
    
class DaubepGiaDinhSpider(scrapy.Spider):
    name = "daubepgiadinh"
    start_urls = ["https://daubepgiadinh.vn/cach-nau-lau-de"]
    
    def parse(self, response):
        yield {'html': response.css("#tab-description").get()}
        
class WebnauanSpider(scrapy.Spider):
    name = "webnauan"

    start_urls = ["https://trangnauan.com/cach-nau-bun-ca-loc.html",
                  "https://trangnauan.com/cach-luoc-oc-ngon.html",
                  "",
                  "",
                  ""]

    def parse(self, response):
        article = response.css("article")
        yield {
            "url": None,
            "title": article.css("h1::text").get(),
            "ingredient": response.css('article h3 ~ ul:first-of-type').getall(),
        }
'''    
