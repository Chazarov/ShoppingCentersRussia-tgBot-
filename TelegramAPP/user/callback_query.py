from aiogram import F, types, Router
from aiogram.methods.edit_message_media import EditMessageMedia
from aiogram.types import FSInputFile, InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession

from TelegramAPP.user.kbds.inline import Center_item_callback_data, City_navigation_callback_data
from TelegramAPP.user.kbds.inline import shopping_center_item_buttoms, city_navigation_buttons
from Database.orm_query import get_center, get_centers_in_city


callback_query_router = Router()

@callback_query_router.callback_query(Center_item_callback_data.filter())
async def center_change_info_items(callback: types.CallbackQuery, callback_data: Center_item_callback_data, session: AsyncSession):
    center_id = callback_data.center_id
    center = await get_center(session, center_id = center_id)
    if(callback_data.action == "description"):
        await callback.message.edit_media(media = InputMediaPhoto(media = FSInputFile(path = center.image, filename = f"myPhoto{center.id}"),caption = center.name + "  \n" + center.description[:1000] + "..."), reply_markup = shopping_center_item_buttoms(callback_data.center_id))
    if(callback_data.action == "contacts"):
        await callback.message.edit_media(media = InputMediaPhoto(media = FSInputFile(path = center.image, filename = f"myPhoto{center.id}"),caption = center.name + "  \n" + center.contacts), reply_markup = shopping_center_item_buttoms(callback_data.center_id))
    if(callback_data.action == "location"):
        await callback.message.edit_media(media = InputMediaPhoto(media = FSInputFile(path = center.image, filename = f"myPhoto{center.id}"),caption = center.name + "  \n" + center.location), reply_markup = shopping_center_item_buttoms(callback_data.center_id))

@callback_query_router.callback_query(City_navigation_callback_data.filter())
async def change_center_item(callback: types.CallbackQuery, callback_data: City_navigation_callback_data, session: AsyncSession):
    city_item_message_id = callback.message.message_id - 1
    chat_id = callback.message.chat.id
    center_index = int(callback_data.current_center_index)
    bot = callback.bot

    centers = await get_centers_in_city(session, callback_data.city)
    
    current_center_index = center_index

    if(callback_data.action == "next"):
        if(center_index < len(centers) - 1):
            current_center_index = center_index + 1

    if(callback_data.action == "previous"):
        if(center_index > 0):
            current_center_index = center_index - 1
    
    if(current_center_index == center_index): return

    center = centers[current_center_index]
        
    reply_markup = shopping_center_item_buttoms(center.id)
    await bot(EditMessageMedia(media = InputMediaPhoto(media = FSInputFile(path = center.image, filename = f"myPhoto{center.id}"), caption = center.name), chat_id = chat_id, message_id = city_item_message_id, reply_markup = reply_markup))
    
    city_name = callback_data.city
    reply_markup_city_navigation = city_navigation_buttons(city_name, str(current_center_index))
    await callback.message.edit_text(text = "Торговые центры в городе: " + city_name + "\n" + f"{current_center_index + 1}/{len(centers)}", reply_markup = reply_markup_city_navigation)