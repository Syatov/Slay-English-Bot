# Slay English Bot

Slay English Bot - это телеграм-бот для изучения английского языка с использованием тестов.

## Запуск бота

1. Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

2. Запустите бота:

    ```bash
    python main.py
    ```

## Команды бота

- `/start`: Начать общение с ботом.
- `/start_test`: Начать тест по английскому языку.
- `/stop`: Остановить отправку новых слов.

## Пример использования тестовых данных

1. Запустите бота с помощью команды `/start`.
2. Начните тест, введя команду `/start_test`.
3. Отвечайте на вопросы бота, выбирая варианты ответов.
4. Получайте уровень владения английским языком и новые слова каждые 10 секунд.

## Тестовые данные

### Вопросы

1. Where are you from?
2. How old are you?
3. Are you having a nice time?
4. Could you pass the salt please?
5. Yesterday I went __________ bus to the National Museum.

### Варианты ответов

1. ["I’m France.", "I’m from France.", "French.", "I’m French."]
2. ["I have 16.", "I am 16.", "I have 16 years.", "I am 16 years."]
3. ["Yes, I’m nice.", "Yes, I’m having it.", "Yes, I am.", "Yes, it is."]
4. ["Over there.", "I don’t know.", "Help yourself.", "Here you are."]
5. ["on", "in", "by", "with"]

### Правильные ответы

[1, 2, 3, 2, 1]
