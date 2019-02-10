from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from io import BytesIO
import requests
import re
from PIL import Image


class SlideCaptcha():
    def __init__(self):
        self.url = "https://www.huxiu.com"
        option = self.set_start_option()
        self.driver = webdriver.Chrome(chrome_options=option)#, executable_path='chromedriver.exe'
        self.wait = WebDriverWait(self.driver, 10)
        pass

    def set_start_option(self):
        option = Options()
        option.add_argument('--window-size=1900,1000')
        option.add_argument('--disable-infobars')
        # option.add_argument('--headless')
        return option
    def get_first_page(self):
        self.driver.get(self.url)
        login_button = self.driver.find_element_by_xpath('//a[@class="js-login"]')
        # login_button = self.driver.find_element_by_xpath('//a[@class="transition msubstr-row2"][1]')
        login_button.click()
    def get_image(self):
        image_tag_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="gt_cut_bg gt_show"]/div')))
        no_image_tag_list = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="gt_cut_fullbg gt_show"]/div')))
        gap_image = self.get_image_list(image_tag_list)
        no_gap_image = self.get_image_list(no_image_tag_list)
        distance = self.get_move_distance(gap_image, no_gap_image)
        self.slide_button(distance - 5)

    def slide_button(self,distance):
        # 需要一个滑动轨迹
        button = self.driver.find_element_by_xpath('//div[@class="gt_slider_knob gt_show"]')
        ActionChains(self.driver).click_and_hold(button).perform()
        ActionChains(self.driver).move_by_offset(distance, 0).perform()
        ActionChains(self.driver).release().perform()

    def get_move_distance(self, gap, no_gap):
        def compare_pixel(p1, p2):
            for i in range(3):
                if abs(p1[i] - p2[i]) > 50:
                    return False
        for x in range(260):
            for y in range(116):
                if compare_pixel(gap.getpixel((x, y)), no_gap.getpixel((x, y))) is False:
                    return x

    def get_image_list(self, image_tag_list):
        image_url = re.findall(r'url\("(.*?)"\)', image_tag_list[0].get_attribute("style"))[0]
        style_list = [i.get_attribute("style")for i in image_tag_list]
        position_list = [re.findall(r'background-position: -?(.*?)px -?(.*?)px;', i)[0][0] for i in style_list]
        image = requests.get(image_url).content
        image_file = BytesIO(image)
        old_image = Image.open(image_file)
        new_image = Image.new('RGB', (260, 116))
        up_count = 0
        down_count = 0
        for i in position_list[:26]:
            crop_image = old_image.crop((int(i), 58, int(i)+10, 116))
            new_image.paste(crop_image, (up_count, 0))
            up_count += 10
        for i in position_list[26:]:
            crop_image = old_image.crop((int(i), 0, int(i)+10, 58))
            new_image.paste(crop_image, (down_count, 58))
            down_count += 10
        return new_image
    def run(self):
        try:
            self.get_first_page()
            self.get_image()
        finally:
            time.sleep(5)
            self.driver.quit()

if __name__=="__main__":
    huxiu = SlideCaptcha()
    huxiu.run()