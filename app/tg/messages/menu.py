from telegram import InlineKeyboardMarkup

from app.crud import crud_language
from app.tg.messages.base import BaseMessageParams
from app.tg.messages.base import CallbackData
from app.tg.messages.base import factory_btn_close
from app.tg.messages.base import InlineButtonFactory


class MessageParamsMainMenu(BaseMessageParams):
    _key_message_text = "/menu/main"

    callback_entry = CallbackData("/menu/main")
    factory_settings_btn = InlineButtonFactory(
        db_key="/buttons/settings", callback_data=CallbackData("/settings")
    )

    @classmethod
    async def async_build(cls, language_code: str):
        text_db_obj = await crud_language.get(
            key=cls._key_message_text, language_code=language_code
        )

        settings_button = await cls.factory_settings_btn.get_button(language_code)
        close_button = await factory_btn_close.get_button(language_code)

        reply_markup = InlineKeyboardMarkup([[settings_button], [close_button]])
        return cls(text=str(text_db_obj), reply_markup=reply_markup)


class MessageParamsMenuSettings(BaseMessageParams):
    _key_message_text = "/menu/settings"

    cd_event = CallbackData(
        MessageParamsMainMenu.factory_settings_btn.callback_data, event_channel="switch"
    )
    factory_btn_event_enable = InlineButtonFactory(
        "/buttons/settings/event_channel/enable", callback_data=cd_event
    )

    factory_btn_event_disable = InlineButtonFactory(
        "/buttons/settings/event_channel/disable", callback_data=cd_event
    )

    factory_btn_language = InlineButtonFactory(
        "/buttons/settings/change_language",
        CallbackData(
            path="/change_language",
            base_callback_data=(
                MessageParamsMainMenu.factory_settings_btn.callback_data
            ),
        ),
    )

    factory_btn_back = InlineButtonFactory(
        "/buttons/back", MessageParamsMainMenu.callback_entry
    )

    @classmethod
    async def async_build(cls, language_code: str, action: bool):
        text_db_obj = await crud_language.get(
            key=cls._key_message_text, language_code=language_code
        )

        # Enable
        if action:
            event_button = await cls.factory_btn_event_enable.get_button(language_code)
        # Disable
        else:
            event_button = await cls.factory_btn_event_disable.get_button(language_code)

        language_button = await cls.factory_btn_language.get_button(language_code)

        back_btn = await cls.factory_btn_back.get_button(language_code)
        reply_markup = InlineKeyboardMarkup(
            [[event_button], [language_button], [back_btn]]
        )
        return cls(text=str(text_db_obj), reply_markup=reply_markup)


class MessageParamsSettingLanguage(BaseMessageParams):
    _key_message_text = "/menu/settings/change_language"

    factory_buttons_language = InlineButtonFactory(
        "/buttons/settings/select_language/",
        CallbackData(
            path=MessageParamsMenuSettings.factory_btn_language.callback_data,
            language_code="",
        ),
    )

    factory_btn_back = InlineButtonFactory(
        "/buttons/back", MessageParamsMainMenu.factory_settings_btn.callback_data
    )

    @classmethod
    async def async_build(cls, language_code: str):
        text_db_obj = await crud_language.get(
            key=cls._key_message_text, language_code=language_code
        )
        language_codes: list = await crud_language.get_language_codes()

        keyboard = []
        row = []
        for lg_code in language_codes:
            cls.factory_buttons_language.callback_data.change_parameter(
                "language_code", lg_code
            )
            button = await cls.factory_buttons_language.get_button(lg_code)
            row.append(button)
            if len(row) == 5:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        cls.factory_buttons_language.callback_data.change_parameter("language_code", "")
        back_btn = await cls.factory_btn_back.get_button(language_code)
        keyboard.append([back_btn])

        reply_markup = InlineKeyboardMarkup(keyboard)
        return cls(text=str(text_db_obj), reply_markup=reply_markup)
