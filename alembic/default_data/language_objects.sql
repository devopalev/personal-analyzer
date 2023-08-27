insert into language_objects (id, language_code, key, value)
values  (1, 'ru', '/event/channel/joined_user', 'Пользователь {user_link} присоединился к каналу {channel_title} '),
        (2, 'en', '/event/channel/joined_user', 'User {user_link} joined the channel {channel_title}'),
        (3, 'ru', '/event/channel/left_user', 'Пользователь {user_link} покинул канал {channel_title} '),
        (4, 'ru', '/event/channel/left_bot', 'Бот удалён из канала {channel_title}'),
        (5, 'en', '/event/channel/left_bot', 'Bot removed from channel {channel_title}'),
        (6, 'en', '/event/channel/left_user', 'User {user_link} has left the channel {channel_title}'),
        (7, 'ru', '/commands/start', 'Привет! Я бот для частных каналов. Если хочешь узнать что я умею, просто отправь /help'),
        (8, 'en', '/commands/start', 'Hi! I am a bot for private channels. If you want to know what I can do, just send /help'),
        (9, 'ru', '/commands/help', 'Я могу уведомлять вас, когда пользователи присоединяются к каналу или покидают его. Для этого добавьте меня в свой канал в качестве администратора.'),
        (10, 'en', '/commands/help', 'I can notify you when users join or leave a channel. To do this, add me to your channel as an administrator.');
