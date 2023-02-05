import telebot
import requests
import random
bot=telebot.TeleBot('5897261595:AAGTJX0TOAAtWZVM13-QjpCcAdZZyb1LZBU', parse_mode=None)
command_list=['/start', '/help', '/hello', '/goodbye', '/calc', '/number']
game = False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, f"Введите команды \
         {command_list}")


@bot.message_handler(commands=['calc'])
def start_calc(message):
    bot.reply_to(message, f'Введите математическое выражение: \
        чтобы выключить бота введите "хватит"')
    bot.register_next_step_handler(message, calc)
def calc(message):
        if message.text!='хватит':
            bot.send_message(message.from_user.id, f'{message.text}={eval(str(message.text))}')
            bot.register_next_step_handler(message, calc)
        else:
            return
            
@bot.message_handler(commands=['number'])
def send_game(message):    
    bot.reply_to(message, f'Сыграем в угадай число от 1 до 1000 \
        введите число')  
    right_number=random.randint(1,1000)  
    bot.register_next_step_handler(message, start_guess_the_number, 0, right_number)
def start_guess_the_number(message, try_number:int, right_number:int):
    game=True 
    if game==True:
        if message.text.isdigit():
            if int(message.text)==right_number:
                bot.send_message(message.from_user.id, f'Вы отгадали число!, чило попыток= {try_number}')
                game=False
                return
            elif int(message.text) > right_number:
                bot.send_message(message.from_user.id, f'я загадал число меньше {right_number}')
            elif int(message.text) < right_number:
                bot.send_message(message.from_user.id, 'я загадал число больше')
            bot.register_next_step_handler(message, start_guess_the_number, try_number + 1, right_number)
        elif message.text.isdigit()==False:
            bot.send_message(message.from_user.id, 'Вы ввели не число')
            bot.register_next_step_handler(message, start_guess_the_number, try_number, right_number)

@bot.message_handler(content_types=['text'])
def echo_all(message):
    if message.text=='Погода':
        data=requests.get('https://wttr.in/?0T')
        bot.reply_to(message,data.text)
    elif 'привет' in message.text:
        bot.reply_to(message, f'Привет, {message.from_user.first_name}')
    elif message.text=='кот':
        cat=open('C:/Users/user/Pictures/Фоновые изображения рабочего стола/3. Леопард.jpg','rb')
        bot.send_photo(message.from_user.id,cat )
    else:
        print(f'{message.from_user.first_name}{message.from_user.last_name}:{message.text}')

bot.infinity_polling()