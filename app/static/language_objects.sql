insert into language_objects (id, language_code, key, value)
values

--      # Events
        (1, 'ru', '/event/channel/joined_user', 'Пользователь {user_link} присоединился к каналу {channel_title} '),
        (2, 'en', '/event/channel/joined_user', 'User {user_link} joined the channel {channel_title}'),
        (3, 'ru', '/event/channel/left_user', 'Пользователь {user_link} покинул канал {channel_title} '),
        (4, 'ru', '/event/channel/left_bot', 'Бот удалён из канала {channel_title}'),
        (5, 'en', '/event/channel/left_bot', 'Bot removed from channel {channel_title}'),
        (6, 'en', '/event/channel/left_user', 'User {user_link} has left the channel {channel_title}'),

--      Commands
        (7, 'ru', '/commands/start', 'Привет! Я бот для частных каналов. Если хочешь узнать что я умею, просто отправь /help'),
        (8, 'en', '/commands/start', 'Hi! I am a bot for private channels. If you want to know what I can do, just send /help'),
        (9, 'ru', '/commands/help', 'Я могу уведомлять вас, когда пользователи присоединяются к каналу или покидают его. Для этого добавьте меня в свой канал в качестве администратора.'),
        (10, 'en', '/commands/help', 'I can notify you when users join or leave a channel. To do this, add me to your channel as an administrator.'),

--      Main menu
        (11, 'en', '/menu/main', 'Main menu'),
        (12, 'ru', '/menu/main', 'Основное меню'),
        (13, 'en', '/buttons/settings', '⚙ My Settings'),
        (14, 'ru', '/buttons/settings', '⚙ Мои настройки'),

--      Settings menu
        (15, 'en', '/menu/settings', '⚙ My Settings'),
        (16, 'ru', '/menu/settings', '⚙ Мои настройки'),

        (17, 'en', '/buttons/settings/event_channel/enable', '🔔 Enable notifications from channels'),
        (18, 'ru', '/buttons/settings/event_channel/enable', '🔔 Включить уведомдения из каналов'),
        (19, 'en', '/buttons/settings/event_channel/disable', '🔕 Turn off notifications from channels'),
        (20, 'ru', '/buttons/settings/event_channel/disable', '🔕 Выключить уведомления из каналов'),

        (21, 'en', '/buttons/settings/change_language', '🔁 Change the language'),
        (22, 'ru', '/buttons/settings/change_language', '🔁 Сменить язык'),
        (23, 'ru', '/menu/settings/change_language', 'Выбирете язык интерфейса'),
        (24, 'en', '/menu/settings/change_language', 'Select the interface language'),
        (25, 'ru', '/buttons/settings/select_language/', '🇷🇺'),
        (26, 'en', '/buttons/settings/select_language/', '🇺🇸'),

--      Other
        (27, 'ru', '/event/error', 'Во время выполнения запроса возникла непредвединная ошибка! Попробуйте позже.'),
        (28, 'en', '/event/error', 'An unexpected error occurred during the execution of the request! Try again later.'),
        (29, 'en', '/buttons/back', '↩ Go back'),
        (30, 'ru', '/buttons/back', '↩ Вернуться назад'),
        (31, 'en', '/buttons/close', '🚪 Close the menu'),
        (32, 'ru', '/buttons/close', '🚪 Закрыть меню')

ON CONFLICT (id) DO UPDATE SET language_code = EXCLUDED.language_code, key = EXCLUDED.key, value = EXCLUDED.value;
