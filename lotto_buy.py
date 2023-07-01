from lib2to3.pgen2 import driver
import os
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from lotto_gen import LottoGen, parse_weights


class Lotto:
    def __init__(self):
        self.init_chrome_driver()

    def login(self, id, pw):
        login_url = "https://www.dhlottery.co.kr/user.do?method=loginm"
        self.driver.get(login_url)

        id_box = self.driver.find_element(value="userId")
        id_box.send_keys(id)

        pw_box = self.driver.find_element(value="password")
        pw_box.send_keys(pw)

        self.driver.execute_script("loginpage()")

    def init_chrome_driver(self):
        chromedriver_path = chromedriver_autoinstaller.install()

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        self.driver = webdriver.Chrome(
            executable_path=str(chromedriver_path), options=options
        )

    def buy(self, lotto_nums: list):
        buy_url = "https://ol.dhlottery.co.kr/olotto/game/game645.do"
        self.driver.get(buy_url)

        for num in lotto_nums:
            checkbox = self.driver.find_element(value=f"check645num{num}")
            self.driver.execute_script("arguments[0].click();", checkbox)

        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element(value="btnSelectNum"),
        )
        self.driver.execute_script(
            "arguments[0].click();",
            self.driver.find_element(value="btnBuy"),
        )

        self.driver.execute_script("closepopupLayerConfirm(true)")

    def deposit(self):
        deposit_url = "https://m.dhlottery.co.kr/payment.do?method=payment"
        self.driver.get(deposit_url)
        select = Select(self.driver.find_element(value="Amt"))
        select.select_by_value("30000")
        self.driver.execute_script("nicepayStart()")


if __name__ == "__main__":

    lotto_nums = LottoGen(parse_weights()).gen()
    # lotto_nums = LottoGen().gen()

    id = os.environ["LOTTO_ID"]
    pw = os.environ["LOTTO_PW"]

    l = Lotto()
    l.login(id, pw)
    l.deposit()
    l.buy(lotto_nums)
    print(lotto_nums)
