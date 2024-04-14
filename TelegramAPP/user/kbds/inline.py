from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData


class Center_item_callback_data(CallbackData, prefix = "center_item"):
    center_id:str
    action:str

class City_navigation_callback_data(CallbackData, prefix = "city_navigation"):
    current_center_index:str
    city:str
    action:str

class City_info_items(CallbackData, prefix = "center_info_items"):
    info_item:str

def shopping_center_item_buttoms(id:str):
    kbd = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text = "Описание", callback_data = Center_item_callback_data(center_id=id, action = "description").pack()),
                InlineKeyboardButton(text = "Контакты", callback_data = Center_item_callback_data(center_id=id, action = "contacts").pack()),
                InlineKeyboardButton(text = "Расположение", callback_data = Center_item_callback_data(center_id=id, action = "location").pack()),
            ],
        ]
    )

    return kbd

def city_navigation_buttons(city_name:str, center_index:str):
    kbd = InlineKeyboardMarkup(inline_keyboard = [
            [   
                InlineKeyboardButton(text = "Предыдущий", callback_data = City_navigation_callback_data(city = city_name, action = "previous", current_center_index = center_index).pack()),
                InlineKeyboardButton(text = "Следующий", callback_data = City_navigation_callback_data(city = city_name, action = "next", current_center_index = center_index).pack()),
            ],
        ]
    )

    return kbd