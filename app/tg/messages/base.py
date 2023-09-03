import re
from abc import ABC
from abc import abstractmethod
from collections import UserDict

from telegram import InlineKeyboardButton
from telegram.constants import ParseMode

from app.crud import crud_language


class CallbackData:
    """
    callback_data consists of path (required) and params (optional), example: /settings?select_language=ru
        path consists of string separated "/", example: /settings/user
        One param consists of key and value separated "=", example: select_language=ru
        Multiple parameters are separated by "&", example: /settings?select_language=ru&action=1

    """

    _separator_path_and_params = "?"
    _separator_params = "&"
    _separator_param_key_and_value = "="
    _separator_path = "/"

    def __init__(
        self, path, base_callback_data=None, callback_data_str: str = None, **kwargs
    ):
        if base_callback_data:
            if self._separator_path_and_params in str(base_callback_data):
                raise ValueError(
                    "callback_data from base_builder already contains parameters"
                )
            if str(base_callback_data)[0] != self._separator_path:
                raise ValueError(
                    'The base_callback_data_str must start with the symbol "/"'
                )

        if str(path)[0] != self._separator_path:
            raise ValueError('The path must start with the symbol "/"')

        if base_callback_data:
            self.path = str(base_callback_data) + str(path)
        else:
            self.path = str(path)
        self.params = kwargs

        if callback_data_str:
            self.callback_data = callback_data_str
        else:
            self._build_callback_data()

    def __str__(self):
        return self.callback_data

    def __getattr__(self, item):
        if item in self.params:
            return self.params[item]
        return super().__getattr__(item)

    @classmethod
    def build_from_callback_data(cls, callback_data: str):
        if not callback_data:
            ValueError("Empty callback_data")
        split_cd = callback_data.split(cls._separator_path_and_params)

        if len(split_cd) > 1:
            path_str, params_str = split_cd
        else:
            path_str, params_str = *split_cd, None

        if params_str:
            params_list = params_str.split(cls._separator_params)
            params = dict(
                p.split(cls._separator_param_key_and_value) for p in params_list
            )
        else:
            params = {}
        return cls(path_str, callback_data_str=callback_data, **params)

    def _build_callback_data(self):
        params_list = [
            self._separator_param_key_and_value.join(map(str, p))
            for p in self.params.items()
        ]
        params_str = self._separator_params.join(params_list)
        text_params = (
            self._separator_path_and_params + params_str if self.params else ""
        )
        self.callback_data = self.path + text_params

    def change_parameter(self, key: str, value):
        self.params[key] = value
        self._build_callback_data()

    @property
    def re_callback_data(self):
        return re.escape(self.callback_data)

    @property
    def re_strict_callback_data(self):
        return f"^{re.escape(self.callback_data)}$"

    @property
    def re_path(self):
        return f"^{re.escape(self.path)}$"


class InlineButtonFactory:
    def __init__(self, db_key, callback_data: CallbackData, **kwargs):
        self.db_key = db_key

        self.callback_data = callback_data
        self.params = kwargs

    def _build_button_with_text(self, button_text: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            button_text, callback_data=str(self.callback_data), **self.params
        )

    async def get_button(self, language_code: str) -> InlineKeyboardButton:
        button_text = await crud_language.get(
            key=self.db_key, language_code=language_code
        )
        return self._build_button_with_text(str(button_text))


class BaseMessageParams(UserDict, ABC):
    """
    Params for send_message to telegram. Builds text and keyboard.

    Original parameters
        text: str,
        parse_mode: ODVInput[str] = DEFAULT_NONE,
        disable_web_page_preview: ODVInput[bool] = DEFAULT_NONE,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        entities: Optional[Sequence["MessageEntity"]] = None,
        *,
        read_timeout: ODVInput[float] = DEFAULT_NONE,
        write_timeout: ODVInput[float] = DEFAULT_NONE,
        connect_timeout: ODVInput[float] = DEFAULT_NONE,
        pool_timeout: ODVInput[float] = DEFAULT_NONE,
        api_kwargs: Optional[JSONDict] = None,
    """

    PARSE_MODE = ParseMode.MARKDOWN
    _key_message_text = "/example/example_key"
    _allowed_keys = ("text", "reply_markup", "parse_mode")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data["parse_mode"] = self.PARSE_MODE

    def __setitem__(self, key, value):
        if key in self.data:
            raise RuntimeError("This object is read-only")

        if key not in self._allowed_keys:
            raise KeyError(f"Invalid key <{key}>")

        super().__setitem__(key, value)

    @classmethod
    @abstractmethod
    async def async_build(cls, *args, **kwargs):
        raise NotImplementedError("Redefine async_build method")


class MessageTextSimpleBuilder(BaseMessageParams):
    @classmethod
    async def async_build(cls, language_code: str = None):
        if cls._key_message_text == BaseMessageParams._key_message_text:
            raise NotImplementedError("Redefine _key_message_text")
        text_db_obj = await crud_language.get(
            key=cls._key_message_text, language_code=language_code
        )
        return cls(text=str(text_db_obj))


factory_btn_close = InlineButtonFactory(
    "/buttons/close", CallbackData("/message/delete")
)
