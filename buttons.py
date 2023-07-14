from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
import database


def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('Добавить объявления')
    kb.add('Удалить объявления')
    kb.add('Меню клиента')
    kb.add('/show_users', '/broadcast')

    return kb

def models_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add = ('iPhone', 'Samsung')
    kb.add = ('POCO', 'Google')
    kb.add = ('realme', 'Oppo')
    kb.add = ('Xiaomi', 'vivo')
    kb.add = ('LG', 'OnePlus')

    return kb

def phone_number_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Отправить номер телефона', request_contact=True)
    kb.add(button)

    return kb


def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add('Я покупатель', 'Я продавец')
    kb.add('Контакты☎️', 'О нас')

    return kb




def accessories_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button = KeyboardButton('Назад')
    all_products = database.accessories_product()

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)

    return kb



def product_name_kb(category_id):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Назад')
    all_products = database.get_name_product(category_id)

    buttons = [KeyboardButton(i[0]) for i in all_products]
    kb.add(*buttons, button)



def search_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    search = KeyboardButton('Поиск')
    back = KeyboardButton('Назад⬅️')

    kb.add(search, back)

    return kb


def sub_model_kb(products_from_db):
    # Создаем пространство для кнопок
    kb = InlineKeyboardMarkup(row_width=2)

    # создаем кнопки (несгораемые)
    nextt = InlineKeyboardButton(text='Следующая', callback_data='next')
    down = InlineKeyboardButton(text='Предыдущая', callback_data='down')
    back = InlineKeyboardButton(text='Назад', callback_data='back')

    # Генерация кнопок с товарами(берем из базы)
    # создаем кнопки с продуктами
    all_products = [InlineKeyboardButton(text=f'{i[0]}', callback_data=i[0])
                    for i in products_from_db]

    # Обеденить пространство с кнопками
    kb.add(*all_products)
    kb.row(nextt)
    kb.row(down)
    kb.row(back)

    # Возвращаем кнопки
    return kb

