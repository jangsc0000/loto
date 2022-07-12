import requests
import random
from bs4 import BeautifulSoup


class LottoGen:
    candidates = list(range(1, 46))

    def __init__(self, weight=None):
        self.weight = weight
        pass

    def gen(self):
        weights = []
        if self.weight:
            weights = self.weight
        else:
            weights = [1] * 45

        lotto_nums = set()
        while len(lotto_nums) < 6:
            lotto_nums.add(random.choices(self.candidates, weights=weights, k=1).pop())

        return lotto_nums


def parse_weights():
    url = "https://www.dhlottery.co.kr/gameResult.do?method=statByNumber"

    try:
        content = requests.get(url).content
    except Exception as e:
        print(e)
        print("error")
        exit(1)

    weights = (
        BeautifulSoup(content, features="html.parser")
        .find(attrs={"class": "tbl_data_col"})
        .find("tbody")
        .find_all("tr")
    )
    return list(map(lambda x: int(x.find_all("td")[-1].text), weights))


if __name__ == "__main__":

    lotto_generator = LottoGen(parse_weights())
    print(lotto_generator.gen())
