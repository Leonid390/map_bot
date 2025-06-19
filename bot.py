import telebot
from config import *
from logic import *

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:  /show_city - показать город, /remember_city - сохранить город, /show_my_cities - отрисовать все города")
    # Допиши команды бота


@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Напиши название города")
        return
    city_name = ' '.join(parts[1:])  
    coords = manager.get_coordinates(city_name)
    if not coords:
        bot.send_message(message.chat.id, "Город не найден.")
        return
    path = f'{city_name}_map.png'
    manager.create_graph(path, [city_name])
    with open(path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    user_id = message.chat.id
    cities = manager.select_cities(user_id)
    if not cities:
        bot.send_message(message.chat.id, "Нет сохранённых городов")
        return
    path = 'my_cities_map.png'
    manager.create_graph(path, cities)
    with open(path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


if __name__=="__main__":
    manager = DB_Map(DATABASE)
    bot.polling()
