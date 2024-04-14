from aiogram import F, types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from sqlalchemy.ext.asyncio import AsyncSession

from TelegramAPP.user.kbds.inline import shopping_center_item_buttoms, city_navigation_buttons
from TelegramAPP.user.callback_query import callback_query_router
from Database.orm_query import get_center_by_name, get_centers_in_city

user_dialogues_router = Router()
user_dialogues_router.include_router(callback_query_router)

class CenterSearch(StatesGroup):
    city_name = State()
    center_name = State()
    center_get_additional_info = State()


@user_dialogues_router.message(Command("find_by_name"))
@user_dialogues_router.message(F.text == "Поиск по названию")
async def center_name_request(message: types.Message, state: FSMContext):
    await state.set_state(CenterSearch.center_name)
    await message.answer("Введите название центра")

@user_dialogues_router.message(CenterSearch.center_name, F.text)
async def center_item(message: types.Message, state: FSMContext, session:AsyncSession):
    await state.clear()
    center = await get_center_by_name(session, center_name = message.text)
    if(center):
        reply_markup = shopping_center_item_buttoms(center.id)
        await message.answer_photo(FSInputFile(path = center.image, filename = f"myPhoto{center.id}"), center.name, reply_markup = reply_markup)
    else: await message.answer("Простите, торгового центра с таким названием нет в базе(")


@user_dialogues_router.message(StateFilter(None), Command("find_in_city"))
@user_dialogues_router.message(F.text == "Поиск в городе")
async def city_request(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.set_state(CenterSearch.city_name)
    await message.answer("Введите город")

@user_dialogues_router.message(CenterSearch.city_name, F.text)
async def find_in_city(message: types.Message, state: FSMContext, session:AsyncSession):
    await state.clear()

    centers = await get_centers_in_city(session, message.text)
    if(centers):
        center_index = 0
        center = centers[center_index]
        
        reply_markup_city_navigation = city_navigation_buttons(message.text, center_index = str(center_index))
        reply_markup_center_data_actions = shopping_center_item_buttoms(center.id)
        await message.answer_photo(FSInputFile(path = center.image, filename = f"myPhoto{center.id}"), center.name, reply_markup = reply_markup_center_data_actions)
        await message.answer("Торговые центры в городе: " + message.text + f"\n1/{len(centers)}", reply_markup = reply_markup_city_navigation)
    else: await message.answer("Простите, города с таким названием нет в базе(")

        

