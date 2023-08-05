"""
API Navigation
==============

API Navigation is made to purely interact with the api and scrape the meal off the web.
For examples and in depth usage, take a look at our documentation.
<https://dasadweb.com/documentation/eAwaiter#API-Navigation>
"""

from bs4 import BeautifulSoup
from bs4.element import Tag

from datetime import datetime, timedelta
import requests

from .dataclasses import eAsistentMeal



HTML_ID = "ednevnik-seznam_ur_teden"


class ApiNavigator:
    session = requests.Session()
    def login(self, username: str, password: str) -> requests.models.Response:
        login_url = "https://www.easistent.com/p/ajax_prijava"
        data = {
            "uporabnik": username,
            "geslo": password,
            "pin": "",
            "captcha": "",
            "koda": "",
        }
        login = self.session.post(login_url, data=data)
        return login

    def get_menu_ids(self) -> list:
        meals_url = "https://www.easistent.com/dijaki/ajax_prehrana_obroki_seznam"
        response = self.session.get(meals_url)
        soup = BeautifulSoup(response.content, "html.parser")
        meal_types = soup.find(class_=HTML_ID).find_all("tr")
        meal_types.pop(0)
        meal_types.pop(-1)

        meal_ids = []
        for meal_type in meal_types:
            meal_id_full = meal_type.find_all("td")[1].get("id")
            meal_id = meal_id_full.split("-")[4]
            meal_ids.append(meal_id)

        return meal_ids

    def get_meal_data(self, week_num: int, monday: datetime, meals: list) -> list:
        data = {
            "qversion": 1,
            "teden": week_num,
            "smer": "naprej",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        meals_url = "https://www.easistent.com/dijaki/ajax_prehrana_obroki_seznam"
        site = self.session.post(meals_url, data=data, headers=headers)
        soup = BeautifulSoup(site.content, "html.parser")

        work_days = 5
        week_data = []
        for i in range(work_days):
            date = monday + timedelta(days=i)

            day_data = self.get_daily_meals(soup, meals, date)
            week_data.append(day_data)

        return week_data

    def get_daily_meals(self, soup: BeautifulSoup, meals: list, date: datetime) -> list:
        date_str = date.strftime("%Y-%m-%d")
        day_data = []
        for meal_id in meals:
            meal_html_id = f"{HTML_ID}-td-malica-{meal_id}-{date_str}-0"  # html class
            meal_container = soup.find("td", id=meal_html_id).find("div")

            check_first = self.check_single_div(meal_container, meal_id, date_str)
            if check_first[0]:
                day_data.append(
                        check_first[1]
                        )
                continue

            check_second = self.check_double_div(meal_container, meal_id, date, date_str)
            if check_second[0]:
                day_data.append(
                        check_second[1]
                        )
                continue

            check_third = self.check_tripple_div(meal_container, meal_id, date, date_str)
            if check_third[0]:
                day_data.append(
                        check_third[1]
                        )
                continue

        return day_data

    def check_single_div(self, container: Tag, meal_id: str, date_str: str) -> [bool, dict]:
        """
        Only in past meals without meal_text
        """
        if not len(container.find_all("div")) == 1:
            return False, {}
        return True, eAsistentMeal("", meal_id, date_str, False, False)

    def check_double_div(self, container: Tag, meal_id: str, date: datetime, date_str: str) -> [bool, dict]:
        """
        Either: past (not selected),
                past (selected),
                future (not loaded)
        """
        if not len(container.find_all("div")) == 2:
            return False, {}

        selected = False
        changable = False
        second_div = container.find_all("div")[1]

        if len(list(container.findChildren(recursive=False))) > 2:
            # selected or signed off
            selected = True \
                    if container.find("span").text == "Prijavljen" \
                    else False

        meal_text = second_div.text.strip()
        if meal_text.split(" ")[0] in ["Prijava", "Naročen"]:
            # future
            today = datetime.today()
            changable = True \
                    if (date - today).days > 9 \
                    else False
            selected = True \
                    if meal_text.split(" ")[0] == "Naročen" \
                    else False
            meal_text = ""

        return True, eAsistentMeal(meal_text, meal_id, date_str, changable, selected)

    def check_tripple_div(self, container: Tag, meal_id: str, date: datetime, date_str: str) -> [bool, dict]:
        """
        Either: future (not selected),
                future (selected),
                present (selected),
                present (unable to change)
        """
        second_div = container.find_all("div")[1]
        third_div = container.find_all("div")[2]
        third_div_children = third_div.findChildren(recursive=False)
        meal_text = second_div.text.strip()
        selected = False

        if len(list(third_div_children)) > 2:
            selected = True \
                    if third_div.find("span").text == "Naročen" \
                    else False

        today = datetime.today()
        changable = False \
                if third_div_children[0].text == "Izbira menija ni več mogoča" \
                or (date - today).days < 9 \
                else True

        return True, eAsistentMeal(meal_text, meal_id, date_str, changable, selected)

    def prijava_odjava(self, action: str, meal_id: str, date: str) -> requests.models.Response:
        url = "https://www.easistent.com/dijaki/ajax_prehrana_obroki_prijava"
        data = {
            "tip_prehrane": "malica",
            "id_lokacija": "0",
            "akcija": f"{action}",
            "id_meni": f"{meal_id}",
            "datum": f"{date}",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest",
        }
        response = self.session.post(url, data=data, headers=headers)
        return response


    def send_mail(self, message: str):
        print(message)

"""
Created By:

|~| ._ _'|
_)|<| (_ |
"""

