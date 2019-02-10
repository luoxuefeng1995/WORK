#encode:utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from chaojiying import Chaojiying_Client
import time
from io import BytesIO
from PIL import Image


class Click_Capture():
    def __init__(self, un, pw, soft_id):
        self.un = un
        self.pw = pw
        self.soft_id = soft_id
        self.url = 'http://dun.163.com/trial/picture-click'
        option = self.set_start_option()
        self.driver = webdriver.Chrome(chrome_options=option)
        self.wait = WebDriverWait(self.driver, 10)

    def set_start_option(self):
        option = Options()
        option.add_argument('--window-size=1300,900')
        option.add_argument('--disable-infobars')
        # option.add_argument('--headless')
        return option
    def get_first_page(self):
        self.driver.get(self.url)
        self.driver.execute_script("window.scrollTo(0,200)")
        capture_po = self.wait.until(EC.presence_of_element_located((By.XPATH,
            '//div[@data-type="click_float"]//div[@class="yidun_tips"]')))
        ActionChains(self.driver).move_to_element(capture_po).perform()

    def get_captcha_image(self):
        image_loc = self.wait.until(EC.visibility_of_element_located((By.XPATH,
        '//div[@data-type="click_float"]//*[@class="yidun_bg-img"]'))).location
        print(image_loc)
        image = BytesIO(self.driver.get_screenshot_as_png())
        im = Image.open(image)
        # im.show()
        new_image = im.crop((image_loc['x'], image_loc['y']-200, image_loc['x']+400, image_loc['y']+70))
        # new_image.show()
        captcha = BytesIO()
        new_image.save(captcha, format('png'))
        return captcha.getvalue()


    def post_captcha(self,captcha):
        cjy = Chaojiying_Client(self.un, self.pw, self.soft_id)
        result = cjy.PostPic(captcha, 9103).get('pic_str')
        print(result)
        position = [i.split(',')for i in result.split('|')]

        return position
    def click_words(self, position):
        #还差一个点击轨迹。
        im = self.wait.until(EC.visibility_of_element_located((By.XPATH,
        '//div[@data-type="click_float"]//*[@class="yidun_bg-img"]')))
        for x, y in position:
            print(x,y)
            ActionChains(self.driver).move_to_element_with_offset(im, int(x), int(y)).perform()
            ActionChains(self.driver).click().perform()

    def run(self):
        try:
            self.get_first_page()
            captcha = self.get_captcha_image()
            position = self.post_captcha(captcha)
            self.click_words(position)
        finally:
            # pass
            time.sleep(5)

            self.driver.quit()

if __name__=="__main__":
    yidun = Click_Capture('qq849885277', 'luoxuefeng520', '896547')
    yidun.run()