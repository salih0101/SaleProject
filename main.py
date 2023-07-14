from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import Registration, Add_phone, Admin, GetProduct
from aiogram import Dispatcher, executor, Bot, types
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
import buttons as btns
import database
import logging
import states
import csv
import os

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

about = f''

@dp.message_handler(commands=['start'])
async def start_message(message):
    start_txt = f'{message.from_user.first_name}\nПриветствуем в боте'
    start_reg = f'Для начала пройдите простую регистрацию, чтобы в дальнейшем не было проблем с доставкой\n\nВведите Ваше имя или выберите поделиться👇:'

    user_id = message.from_user.id
    checker = database.check_user(user_id)

    if user_id == 5928000362 or 316233843:
        await message.answer('Приветствую Администратор',
                             reply_markup=btns.admin_kb())
        await states.Admin.get_status.set()

    elif checker:
        await message.answer('Выберите категорию',
                             reply_markup=btns.main_menu())
        await states.Admin.get_status.set()

    else:
        await message.answer(start_txt)
        await message.answer(start_reg,
                             reply_markup=btns.ReplyKeyboardMarkup())

        await states.Registration.getting_name_state.set()



@dp.message_handler(commands=['show_users'])
async def show_users(message: types.Message):
    admin_id = 1186132006

    if message.from_user.id != admin_id:
        response = "Команда доступна только администратору."
        await message.answer(response)
        return

    users = database.get_users()

    if users:

        with open('users.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Username"])

            for user in users:
                writer.writerow([user[0], user[1]])

        with open('users.csv', 'rb') as file:
            await message.bot.send_document(admin_id, file)

        response = "Список пользователей сохранен в файле users.csv и отправлен администратору."

    else:
        response = "Список пользователей пуст."

    await message.answer(response)



@dp.message_handler(commands=['search'])
async def search(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()

    if not args:
        await message.reply('Вы не указали название товара.')
        return

    products = database.search_product(args)

    if not products:
        await message.reply('Товары не найдены.')

    else:

        for product in products:
            await dp.current_state(user=user_id).update_data(pr_name=product[0], pr_count=1, price=product[2])

            await bot.send_photo(user_id,
                                 photo=product[4],
                                 caption=f'{product[0]}\n\nЦена: {product[2]} $\n\nОписание:\n {product[3]}',
                                 reply_markup=btns.choose_product_count())

        await states.GetProduct.getting_pr_count.set()


@dp.message_handler(state=states.Admin.get_status)
async def get_name(message, state=states.Admin.get_status):
    if message.text == 'Добавить объявления':

        await message.answer('Введите название телефона и модель(Iphone 13pro)')
        await states.Add_phone.get_name_end_model.set()

    elif message.text == 'Меню клиента':

        user_id = message.from_user.id
        checker = database.check_user(user_id)

        if checker:

            await state.finish()
            await message.answer('Выберите продукт',
                                 reply_markup=btns.main_menu())

        else:

            start_txt = f'{message.from_user.first_name}\nПриветствуем в боте'
            start_reg = f'Для начала пройдите простую регистрацию, чтобы в дальнейшем не было проблем с доставкой\n\nВведите Ваше имя или выберите поделиться👇:'

            await message.answer(start_txt)
            await message.answer(start_reg)

            await states.Registration.getting_name_state.set()


@dp.message_handler(state=Registration.getting_name_state)
async def get_name(message, state=Registration.getting_name_state):
    user_answer1 = message.text

    await state.update_data(name=user_answer1)
    await message.answer('Имя сохранил!\nОтправьте номер телефона!',
                         reply_markup=btns.phone_number_kb())

    await Registration.getting_phone_number.set()


@dp.message_handler(state=Registration.getting_phone_number, content_types=['text', 'contact'])
async def get_phone_number(message: types.Message, state=Registration.getting_phone_number):
    global user_answer

    if message.content_type == 'text':
        user_answer = message.text

        if not user_answer.replace('+', '').isdigit():
            await message.answer('Отправьте номер телефона')
            return

    elif message.content_type == 'contact':
        user_answer = message.contact.phone_number

    await state.update_data(number=user_answer)
    await message.answer('Номер сохранил!\n\nВы успешно прошли регистрацию!\n\nВыберите категорию.', reply_markup=btns.main_menu())


    all_info = await state.get_data()
    user_id = message.from_user.id
    name = all_info.get('name')
    phone_number = all_info.get('number')
    time_sub = all_info.get('time_sub')
    end_sub = all_info.get('end_sub')
    status = all_info.get('status')
    amount_sub = all_info.get('amount_sub')

    database.add_user(user_id,
                      name, phone_number,
                      time_sub, end_sub,
                      status, amount_sub)

    await state.finish()


@dp.message_handler(state=states.Add_phone.get_name_end_model)
async def get_name_model(message, state=states.Add_phone.get_name_end_model):
    model = message.text

    await state.update_data(model=model)
    await message.answer(f'Напишите состояние телефона\n(Пример: Отлично, Хорошее, Плохое) \n{model}:>>')
    await states.Add_phone.get_stated.set()


@dp.message_handler(state=states.Add_phone.get_stated)
async def get_stated(message, state=states.Add_phone.get_stated):
    stated = message.text

    await state.update_data(stated=stated)
    await message.answer(f'Напишите цвет устройства:')
    await states.Add_phone.get_color.set()


@dp.message_handler(state=states.Add_phone.get_color)
async def get_color(message, state=states.Add_phone.get_color):
    color = message.text

    await state.update_data(color=color)
    await message.answer('Напишите память устройства:')
    await states.Add_phone.get_storage.set()


@dp.message_handler(state=states.Add_phone.get_storage)
async def get_storage(message, state=states.Add_phone.get_storage):
    storage = message.text

    await state.update_data(storage=storage)
    await message.answer('Есть ли документы устройства(Да, Нет или Паспорт копия):')
    await states.Add_phone.get_docs.set()


@dp.message_handler(state=states.Add_phone.get_docs)
async def get_docs(message, state=states.Add_phone.get_docs):
    docs = message.text

    await state.update_data(docs=docs)
    await message.answer('Отправьте цену\n(Цена в долларах):')
    await states.Add_phone.get_price.set()


@dp.message_handler(state=states.Add_phone.get_price)
async def get_price(message, state=states.Add_phone.get_price):
    price = message.text

    await state.update_data(price=price)
    await message.answer('Отправьте город:')
    await states.Add_phone.get_address.set()


@dp.message_handler(state=states.Add_phone.get_address)
async def get_address(message, state=states.Add_phone.get_address):
    address = message.text

    await state.update_data(address=address)
    await message.answer('Отправьте номер телефона:')
    await states.Add_phone.get_number.set()


@dp.message_handler(state=states.Add_phone.get_number)
async def get_number(message, state=states.Add_phone.get_number):
    number = message.text

    await state.update_data(number=number)
    await message.answer('Отправьте Username\n(@test):')
    await states.Add_phone.get_telegram.set()


@dp.message_handler(state=states.Add_phone.get_telegram)
async def get_telegram(message, state=states.Add_phone.get_telegram):
    telegram = message.text

    await state.update_data(telegram=telegram)
    await message.answer('Отправьте фотографию устройства\n(Пожалуйста отправьте одну фотографию телефона):')
    await states.Add_phone.get_photo.set()


@dp.message_handler(content_types=['photo'], state=states.Add_phone.get_photo)
async def product_photo(message, state=states.Add_phone.get_photo):
    # user_answer = message.text

    all_info = await state.get_data()
    model = all_info.get('model')
    stated = all_info.get('stated')
    color = all_info.get('color')
    storage = all_info.get('storage')
    docs = all_info.get('docs')
    price = all_info.get('price')
    address = all_info.get('address')
    number = all_info.get('number')
    user_id = message.from_user.id
    picture = message.photo[-2].file_id
    telegramm = all_info.get('telegram')
    await state.update_data(picture=picture)



    database.add_products_to_db(user_id,
                                model,
                                stated,
                                color,
                                storage,
                                docs,
                                price,
                                address,
                                number,
                                telegramm,
                                picture)

    await message.answer('Ваша заявка принята!', reply_markup=btns.main_menu())
    await states.Admin.get_status.set()



@dp.message_handler(content_types=['text'])
async def models(message):
    user_answer = message.text
    user_id = message.from_user.id

    if user_answer == 'Я покупатель':
        await message.answer('Выберите бренд', reply_markup=btns.models_kb())

    




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
