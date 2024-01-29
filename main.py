import logging
import os
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import pathlib

logging.basicConfig(level=logging.INFO)

API_TOKEN = ''
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

questions = ["Where are you from?", "How old are you?", "Are you having a nice time?", "Could you pass the salt please?",
             "Yesterday I went __________ bus to the National Museum.", "Sue and Mike __________ to go camping.",
             "Who’s calling, please?", "They were __________ after the long journey, so they went to bed.",
             "Can you tell me the __________ to the bus station?", "__________ you remember to buy some milk?",
             "- Don’t forget to put the rubbish out. - I’ve __________ done it!",
             "You don’t need to bring __________ to eat.", "What about going to the cinema?",
             "- What would you like, Sue? - I’d like the same __________ Michael please.",
             "__________ people know the answer to that question.",
             "It’s not __________ to walk home by yourself in the dark.",
             "__________ sure all the windows are locked.", "I’ll go and __________ if I can find him.",
             "What’s the difference __________ football and rugby?", "My car needs __________ .",
             "Tim was too __________ to ask Monika for a dance.", "I haven’t had so much fun __________ I was a young boy!",
             "Sorry, I don’t know __________ you’re talking about.", "I’m afraid you __________ smoke in here."]


answers = [
    ["I’m France.", "I’m from France.", "French.", "I’m French."],
    ["I have 16.", "I am 16.", "I have 16 years.", "I am 16 years."],
    ["Yes, I’m nice.", "Yes, I’m having it.", "Yes, I am.", "Yes, it is."],
    ["Over there.", "I don’t know.", "Help yourself.", "Here you are."],
    ["on", "in", "by", "with"],
    ["wanted", "said", "made", "talked"],
    ["Just a moment.", "It’s David Parker.", "I’ll call you back.", "Speaking."],
    ["hungry", "hot", "lazy", "tired"],
    ["road", "way", "direction", "street"],
    ["Have", "Do", "Should", "Did"],
    ["yet", "still", "already", "even"],
    ["some", "a food", "many", "anything"],
    ["Good idea!", "Twice a month.", "It’s Star Wars.", "I think so."],
    ["that", "as", "for", "had"],
    ["Few", "Little", "Least", "A little"],
    ["sure", "certain", "safe", "problem"],
    ["Make", "Have", "Wait", "Take"],
    ["see", "look", "try", "tell"],
    ["from", "with", "for", "between"],
    ["repairing", "to repair", "to be repair", "repair"],
    ["worried", "shy", "selfish", "polite"],
    ["when", "for", "during", "since"],
    ["that", "what", "which", "why"],
    ["could not", "don’t have to", "are not allowed to", "can’t be"],
    ["apart", "unless", "however", "except"],
    ["having", "laughing", "making", "joking"],
]

correct_answers = [1, 2, 3, 2, 1, 4, 1, 2, 4, 3, 4, 1, 2, 1, 3, 4, 1, 4, 2, 1, 3, 2, 1, 3, 4]

user_levels = {
    'beginner': range(0, 8),
    'elementary': range(8, 14),
    'pre_intermediate': range(14, 20),
    'intermediate': range(20, 26)
}

async def start_test(user_id):
    user_data = get_user_data(user_id)
    user_data['in_test'] = True
    await ask_question(user_id, 0)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if 'in_test' in user_data and user_data['in_test']:
        # Пользователь уже в тесте, спрашиваем, хочет ли он начать заново
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Да", callback_data="retake_yes"))
        keyboard.add(InlineKeyboardButton("Нет", callback_data="retake_no"))

        await bot.send_message(user_id, "Вы уже проходите тест. Хотите начать заново?", reply_markup=keyboard)
    else:
        # Приветственное сообщение и кнопка "Пройти тест"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Пройти тест", callback_data="start_test"))
        
        await bot.send_message(user_id, "Спасибо за обращение в Slay English! Чем мы можем вам помочь?", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'start_test')
async def callback_start_test(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await start_test(user_id)

@dp.message_handler(content_types=['text'])
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if message.text == "Пройти тест":
        await start_test(user_id)
    else:
        await bot.send_message(user_id, "Спасибо за обращение в Slay English! Чем мы можем вам помочь?")

def save_results_to_file():
    with open("user_results.txt", "w", encoding="utf-8") as file:
        for user_id, user_data in dp.data.items():
            if 'level' in user_data and 'correct_answers' in user_data:
                level = user_data['level']
                correct_answers = user_data['correct_answers']
                file.write(f"{user_id}:{correct_answers}:{level}\n")

async def ask_question(user_id, question_number):
    question_text = f"{question_number + 1}. {questions[question_number]}"
    answer_options = answers[question_number]

    keyboard = InlineKeyboardMarkup()
    for idx, option in enumerate(answer_options, start=1):
        callback_data = f"q_{question_number}_{idx}"
        keyboard.add(InlineKeyboardButton(f"{idx}. {option}", callback_data=callback_data))

    message = await bot.send_message(user_id, question_text, reply_markup=keyboard)

    user_data = get_user_data(user_id)
    user_data['last_message_id'] = message.message_id
    user_data['current_question_id'] = callback_data
    dp.data[user_id] = user_data  # Добавлено обновление данных пользователя

def get_user_data(user_id):
    if user_id not in dp.data:
        dp.data[user_id] = {}
    return dp.data[user_id]

@dp.callback_query_handler(lambda c: c.data.startswith('q_'))
async def process_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data.split('_')

    if len(data) == 3:  # Изменено количество элементов
        question_number = int(data[1])
        chosen_answer = int(data[2])

        user_data = get_user_data(user_id)

        if question_number is not None:
            if chosen_answer == correct_answers[question_number]:
                if 'correct_answers' not in user_data:
                    user_data['correct_answers'] = 0
                user_data['correct_answers'] += 1

            await bot.delete_message(user_id, user_data['last_message_id'])

            if question_number < len(questions) - 1:
                await ask_question(user_id, question_number + 1)
            else:
                await finish_test(user_id)
        else:
            print(f"Ошибка: Не удалось найти номер вопроса для callback_data: {callback_query.data}")
            
@dp.callback_query_handler(lambda c: c.data.startswith('retake_'))
async def process_retake(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    retake_option = callback_query.data.split('_')[1]

    if retake_option == "yes":
        await start_test(user_id)
    elif retake_option == "no":
        await bot.send_message(user_id, "Хорошо, если вы передумаете, вы всегда можете начать тест позже.")

async def finish_test(user_id):
    user_data = get_user_data(user_id)
    correct_answers_count = user_data['correct_answers']
    level = next(level for level, value in user_levels.items() if correct_answers_count in value)

    dp.data[user_id] = {'in_test': False, 'correct_answers': correct_answers_count, 'level': level}
    save_results_to_file()

    if 'stop_words' not in user_data or not user_data['stop_words']:
        await send_words(user_id, level)

    await bot.send_message(user_id, f"Ваш уровень: {level}\nКоличество правильных ответов: {correct_answers_count}")

async def send_words(user_id, level):
    word_file_path = pathlib.Path(__file__).parent.absolute() / f"{level.lower()}.txt"
    if word_file_path.exists():
        with open(word_file_path, "r", encoding="utf-8") as word_file:
            words = [line.strip() for line in word_file.readlines()]
            chunk_size = 5
            chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
            for chunk in chunks:
                await bot.send_message(user_id, f"{chunk_size} новых слов этого дня\n" + "\n".join(chunk))
                await asyncio.sleep(10)
    else:
        print(f"Ошибка: Файл слов не найден для уровня: {level}")

@dp.message_handler(commands=['stop'])
async def stop_command(message: types.Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    user_data['stop_words'] = True

    await bot.send_message(user_id, "Остановка отправки слов. Вы можете возобновить в любое время командой /start_test")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop)
