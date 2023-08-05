"""
eAsistentUser
=============

eAsistentUser class is used for creating and accessing uer's data.
For examples and in depth usage, take a look at our documentation.
<https://dasadweb.com/documentation/eAwaiter#Waiter>
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class eAsistentUser():
    username: str
    password: str

    disliked_foods: list
    favourite_foods: list

    preferred_menu: int
    default_menu: int

    overwrite_unchangable: bool

@dataclass
class eAsistentMeal():
    meal_text: str
    meal_id: str
    date: datetime
    changable: bool
    selected: bool

"""
Created By:

|~| ._ _'|
_)|<| (_ |
"""

