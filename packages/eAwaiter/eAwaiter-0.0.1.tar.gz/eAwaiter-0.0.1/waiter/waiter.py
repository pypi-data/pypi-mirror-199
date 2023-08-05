"""
Waiter
======

Waiter class is used for easy interaction with the user.
For examples and in depth usage, take a look at our documentation.
<https://dasadweb.com/documentation/eAwaiter#Waiter>
"""

from bs4 import BeautifulSoup

from datetime import datetime, timedelta
import json
import os

from .api_navigator import ApiNavigator
from .dataclasses import eAsistentUser
from .exceptions import UserLoginException, MealFetchingException, ChangingMealsException
from .helpers import *


FORMAT = "%Y-%m-%d %H:%M:%S"


class Waiter:
    def __init__(
            self,
            username: str="",
            password: str="",
            disliked_foods: list=[],
            favourite_foods: list=[],
            default_menu: int=1,
            preferred_menu: int=1,
            overwrite_unchangable: bool=False
            ) -> None:

        self.failed_login: bool = False
        self.api: ApiNavigator = ApiNavigator()
        self.user: eAsistentUser = eAsistentUser(
                username=username,
                password=password,
                disliked_foods=disliked_foods,
                favourite_foods=favourite_foods,
                default_menu=default_menu,
                preferred_menu=preferred_menu,
                overwrite_unchangable=overwrite_unchangable
                )

        self.login()

    def login(self) -> None:
        if not self.user.username and not self.user.password:
            raise UserLoginException("Please fill in the Login form!")

        login = self.api.login(
                self.user.username,
                self.user.password
                )

        if login.json()["status"] in ["", "hide_pin"]:
            self.failed_login = True
            # captcha => make them login on web
            if list(login.json()["errfields"].keys())[0] == "captcha":
                raise UserLoginException(
                    "Login failed too many times, please try logging in on the web!"
                )
            raise UserLoginException("Check your credentials and try again!")

        (
            self.meals,
            self.first_week_school
        ) = self.get_school_info()

    def get_school_info(self) -> [list, datetime]:
        date_today = datetime.now()
        curr_month = int(date_today.strftime("%m"))
        curr_year = int(date_today.strftime("%Y"))
        meal_ids = self.api.get_menu_ids()

        school_start_year = curr_year \
                if curr_month >= 9 \
                else curr_year - 1

        first_day_school = datetime(school_start_year, 9, 1)
        first_week_school = get_monday(first_day_school)

        return meal_ids, first_week_school
    
    def prijava_odjava(self, action: str, meal_id: str, date: str):
        result = self.api.prijava_odjava(
            action,
            meal_id,
            date
            )
        if not result.json()["status"]:
            result = self.api.prijava_odjava(
                "odjava",
                meal_id,
                date
                )
        return True if result.json()["status"] else False

    def change_disliked(self, week: int) -> list:
        changes = []
        next_week_num, monday = weeks_in_advance(week, self.first_week_school)
        meals_data = get_selected(
            self.api.get_meal_data(next_week_num, monday, self.meals)
        )

        check_odjava = False
        if int(self.user.preferred_menu) == 0:
            check_odjava = True
        selected_menu = self.meals[int(self.user.preferred_menu) - 1]

        for meal_data in meals_data:
            for disliked_food in self.user.disliked_foods:
                if not meal_data.changable and not self.user.overwrite_unchangable:
                    break
                if disliked_food.upper() in meal_data.meal_text:
                    if check_odjava: 
                        self.api.prijava_odjava(
                            "odjava", meal_data.meal_id, meal_data.date
                        )
                        changes.append(f"Meal changed for {meal_data.date} (sigend off)!")
                        break

                    response = self.api.prijava_odjava(
                        "prijava", selected_menu, meal_data.date
                    )
                    change = f"Meal changed for {meal_data.date} (to {selected_menu})!"
                    if not response.json()["status"]:
                        response = self.api.prijava_odjava(
                            "odjava", meal_data.meal_id, meal_data.date
                        )
                        change = f"Meal signed off for {meal_data.date}!"
                    changes.append(change)
                    break
        return changes

    def change_favourites(self) -> list:
        changes = []
        next_week_num, monday = weeks_in_advance(2, self.first_week_school)
        meals_data = self.api.get_meal_data(next_week_num, monday, self.meals)

        check_odjava = False
        if int(self.user.default_menu) == 0:
            check_odjava = True
        selected_menu = self.meals[int(self.user.default_menu) - 1]

        for i in range(5):
            is_subbed = False
            for meal_data in meals_data[i]:
                for favourite_food in self.user.favourite_foods:
                    if (
                        not meal_data.changable
                        and not self.user.overwrite_unchangable
                        ):
                        break
                    if favourite_food.upper() in meal_data.meal_text:
                        response = self.api.prijava_odjava(
                            "prijava", meal_data.meal_id, meal_data.date
                        )
                        if response.json()["status"]:
                            is_subbed = True
                            changes.append(
                                f"Favourite meal found ({meal_data.date})!"
                                )
                        break
                if is_subbed:
                    break
            if is_subbed:
                continue
            if check_odjava:
                response = self.api.prijava_odjava(
                    "odjava", meal_data[i][0].meal_id, meals_data[i][0].date
                )
                continue
            response = self.api.prijava_odjava(
                "prijava", selected_menu, meals_data[i][0].date
            )
            if not response.json()["status"]:
                response = self.api.prijava_odjava(
                    "odjava", meal_data[i][0].meal_id, meals_data[i][0].date
                )
        return changes

    def get_meals(self, week_num: int = 0, date: datetime = datetime.today()) -> list:
        if week_num:
            print(week_num)
            date = get_monday(self.first_week_school + timedelta(days=7*week_num))
            return self.api.get_meal_data(week_num, date, self.meals)
        monday = get_monday(date)
        week_num = int(str((monday - self.first_week_school) / 7).split(" ")[0])
        return self.api.get_meal_data(week_num, monday, self.meals)

    def service(self) -> None:
        self.api.send_mail("Service started!")
        changes = []

        if self.failed_login:
            raise UserLoginException("Failed to login!")

        try:
            if not self.meals:
                raise MealFetchingException("No meals' ids!")

            if self.user.disliked_foods and self.user.preferred_menu:
                changes += self.change_disliked(1)

            if self.user.favourite_foods and self.user.default_menu:
                changes += self.change_favourites()

            if self.user.disliked_foods:
                changes += self.change_disliked(2)

            self.api.send_mail("service did well")

        except Exception as e:
            self.api.send_mail(e)
        
        return changes

"""
Created By:

|~| ._ _'|
_)|<| (_ |
"""

