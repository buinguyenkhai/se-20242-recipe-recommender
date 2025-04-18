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
        sleep(0.01)
        recipes = response.css("div.box-recipe")
        if len(recipes) == 0:
            recipes = response.css("div.detail")
            
        for recipe in recipes:
            image = recipe.css("div.video > img::attr(data-src)").get()
            if not image:
                recipe.css("div.video > img::attr(src)").get()
            if not image:
                recipe.css("div.video-frame > img::attr(src)").get()
                
            lst = response.css("div.staple > h2 > small::text").re("\d.*")
            num_of_people = lst[0] if len(lst) > 0 else None
            
            yield {
                "title": recipe.css("h2::text").get().strip() if len(recipes) > 1 
                         else recipe.css("h1::text").get().strip(),
                "description": " ".join(response.css("div.leadpost ::text").re("\w.*\w")).replace("  ", " "),
                "image": image,
                "ingredients": seperate_ingredient(clean_text(recipe.css("div.staple > span").getall())),
                "step-detail": "\n".join([" ".join(clean_text(step.css("p").getall())) for step in recipe.css("div.text-method")]),
                "tags": [response.css("div.breadcrum > a::text")[-1].get()],
                "num_of_people": num_of_people,
                "date": response.css("script[type='application/ld+json']").re(time_reg)[0],
                "source": "Vào bếp (Điện máy Xanh)",
                "url": response.url
            }
            

class SoTayNauAnSpider(FrameworkSpider):
    name = "sotaynauan"
    url = "https://sotaynauan.com/chuyen-muc/phuong-phap-che-bien/"
    """
    start_urls = ["https://sotaynauan.com/cach-lam-soda-chanh/",
                  "https://sotaynauan.com/cach-lam-ga-hap-hanh/",
                  "https://sotaynauan.com/huong-dan-lam-banh-dua-dai-loan-ngon-ngat-ngay/",
                  "https://sotaynauan.com/banh-tart-chanh-leo-ban-thu-chua/"]
    """
        
    def parse_category(self, response):
        yield from response.follow_all(css="#sidebar a", callback=self.parse_recipe)
        
    def parse_recipe(self, response):
        yield from response.follow_all(css="div.category-2 > a", callback=self.parse)
        
        next_button_url = response.css("a.nextpostslink::attr(href)").get()
        if next_button_url is not None:
            yield response.follow(next_button_url, callback=self.parse_recipe)
    
    def parse(self, response):
        yield {
                "title": response.css("h2.entry-title > a::text").get(),
                "description": " ".join(response.css("#content > p")[1].css(" ::text").getall()).replace("  ", " "),
                "image": response.css("div.thumb > img::attr(src)").get(),
                "ingredients": seperate_ingredient(clean_text(response.css("ul.ingredients > li").getall())),
                "step-detail": "\n".join([text for text in clean_text(response.css("div.instructions > p, div.instructions > ul > li").getall())
                                if not re.match(r'^\w*$', text)]),
                "tags": response.css("#breadcrumbs > span > span > a::text").getall()[1:],
                "num_of_people": None,
                "date": response.css("script[type='application/ld+json']").re(time_reg)[0],
                "source": "Sổ tay nấu ăn",
                "url": response.url
            }
        # remove null if needed
        
        
class MonNgonMoiNgaySpider(FrameworkSpider):
    name = "monngonmoingay"
    url = "https://monngonmoingay.com/tim-kiem-mon-ngon/"
    """
    start_urls = ["https://monngonmoingay.com/bo-cuon-la-rong-bien/",
                  "https://monngonmoingay.com/com-nam-rong-bien-mayo/",
                  "https://monngonmoingay.com/banh-mi-xiu-mai-2/",
                  "https://monngonmoingay.com/tim-kiem-mon-ngon/"]
    """
    
    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse_recipe)
        
    def parse_recipe(self, response):
        css = "div.flex.gap-2.justify-between.group-has-\[\.group-1\]\:lg\:flex-col-reverse.items-center > h3 > a"
        yield from response.follow_all(css=css, callback=self.parse)
        
        next_page_link = response.css("a[class='next page-numbers']::attr(href)").get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse_recipe)
            
    def parse(self, response):
        yield {
                "title": response.css("h1 span::text").get(),
                "description": " ".join(response.css("[class~='section-tabs'] + div ::text").re("\w.*\w")),
                "image": response.css("div.main > div > div > div > img::attr(src)").get(),
                "ingredients": seperate_ingredient(response.css("#tab-gram ::text").re("\S.*\S")),
                "step-detail": "\n".join(response.css("#section-soche ::text, #section-thuchien ::text, #section-howtouse ::text").re("\w.*\w")),
                "tags": response.css("ul[class~='tags']")[-1].css("::text").getall(),
                "num_of_people": response.css("div.flex.justify-around > div > strong::text")[0].get(),
                "date": response.css("script[type='application/ld+json']").re(time_reg)[0],
                "source": "Món ngon mỗi ngày",
                "url": response.url
            }
        
'''        
class LanVaoBepSpider(FrameworkSpider):
    name = "lanvaobep"
    url = "https://lanvaobep.com/"
    """
    start_urls = ["https://lanvaobep.com/cach-lam-ca-tre-chien-gion-thom-ngon-gion-rum/",
                  "https://lanvaobep.com/page/3/",
                  "https://candycancook.com/2019/11/an-o-new-york-pancake-va-waffles-o-clinton-street-co-restaurant/",
                  "https://candycancook.com/2017/08/hat-sen-bot-loc-long-nhan/",
                  "https://candycancook.com/2013/07/cach-lam-tom-cuon-thit-xong-khoi/",
                  "https://candycancook.com/2010/10/cach-lam-caramel-popcorn-bap-rang-bo/"]
    """
    
    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse_recipe)
        
    def parse_recipe(self, response):
        css = "#main > article > a"
        yield from response.follow_all(css=css, callback=self.parse)
        
        next_page_link = response.css("a[class='next page-numbers']::attr(href)").get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse_recipe)
    
    def parse(self, response):
        yield {
                "title": response.css("h1.entry-title::text").get(),
                "description": " ".join(response.css("div.entry-content > p:first-of-type ::text").getall()).replace("  ", " "),
                "image": response.css("div.wp-block-image a::attr(href)").get(),
                "ingredients": seperate_ingredient(response.xpath("//h2[contains(., 'Nguyên liệu')]/following-sibling::*[1]")
                                                   .css(" ::text").re("\S.*\S")),
                "step-detail": response.xpath('//h2[contains(., "Cách")]/following-sibling::*[not(self::h2)][following-sibling::h2]')
                                        .css(" ::text").re("\w.*\w"),
                "tags": response.css("span.entry-category > a::text").getall(),
                "num_of_people": None,
                "date": response.css("time.entry-date.updated::attr(datetime)").get(),
                "source": "Lăn vào bếp",
                "url": response.url
            }
'''                
'''      
class CandyCanCookSpider(FrameworkSpider):
    name = "candycancook"
    url = "https://candycancook.com"
    """
    start_urls = ["https://candycancook.com/2010/10/nam-tok-moo-thai-spicy-pork-salad/",
                  "https://candycancook.com/2019/04/nam-tok-moo-salad-thit-lon-kieu-thai/",
                  "https://candycancook.com/2019/11/an-o-new-york-pancake-va-waffles-o-clinton-street-co-restaurant/",
                  "https://candycancook.com/2017/08/hat-sen-bot-loc-long-nhan/",
                  "https://candycancook.com/2013/07/cach-lam-tom-cuon-thit-xong-khoi/",
                  "https://candycancook.com/2010/10/cach-lam-caramel-popcorn-bap-rang-bo/"]
    """
        
    def parse_category(self, response):
        yield from response.follow_all(css="aside[class='widget widget_categories'] > ul > li > a",
                                       callback=self.parse_recipe)
            
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
                # fix bug
                "image": response.css("div[id^='attachment'] > a::attr(href)").get(), 
                "ingredients": ingredients,
                "step-detail": step_detail,
                "tags": response.css("span.cat > a > span::text").getall(),
                "date": response.css("time[class='entry-date published']::text").get(),
                "source": "Candy Can Cook",
                "url": response.url
            }
        # remove null if needed
'''       
'''

        
    
    
# https://monngonmoingay.com/
# https://lanvaobep.com/    
    
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
