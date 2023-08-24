insert into language_objects (id, language_code, key, value)
values  (1, 'ru', '/event/channel/joined_user', 'Пользователь {user_link} присоединился к каналу {channel_title} '),
        (2, 'en', '/event/channel/joined_user', 'User {user_link} joined the channel {channel_title}'),
        (3, 'ru', '/event/channel/left_user', 'Пользователь {user_link} покинул канал {channel_title} '),
        (4, 'ru', '/event/channel/left_bot', 'Бот удалён из канала {channel_title}'),
        (5, 'en', '/event/channel/left_bot', 'Bot removed from channel {channel_title}'),
        (6, 'en', '/event/channel/left_user', 'User {user_link} has left the channel {channel_title}');
