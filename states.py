from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    getting_name_state = State()
    getting_phone_number = State()



class Add_phone(StatesGroup):
    get_name_end_model = State()
    get_photo = State()
    get_stated = State()
    get_color = State()
    get_storage = State()
    get_docs = State()
    get_price = State()
    get_address = State()
    get_number = State()
    get_telegram = State()




class Search(StatesGroup):
    search_product = State()


class Admin(StatesGroup):
    get_status = State()


class GetProduct(StatesGroup):
    getting_pr_name = State()
    getting_category = State()






