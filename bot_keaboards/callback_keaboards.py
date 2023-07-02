from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from game_data import states


class GameBoardCallbackFactory(CallbackData, prefix='field'):
    x: int
    y: int



def get_field_keyboard(text, status) -> InlineKeyboardMarkup:
    array_buttons: list[list[InlineKeyboardButton]] = []
    menu_buttons = [InlineKeyboardButton(text='New game', callback_data='new_game'),
                    InlineKeyboardButton(text='Stat', callback_data='stats')]
    exit_button = [InlineKeyboardButton(text='exit', callback_data="exit")]
    record = [InlineKeyboardButton(text='Records', callback_data='records')]
    for i in range(3):
        array_buttons.append([])
        for j in range(3):
            array_buttons[i].append(InlineKeyboardButton(
                text=states[text['game_board'][i][j]],
                callback_data=GameBoardCallbackFactory(x=i, y=j).pack()))
    if not status:
        array_buttons.append(menu_buttons)
        array_buttons.append(record)
    else:
        array_buttons.append(exit_button)

    markup: InlineKeyboardMarkup = InlineKeyboardMarkup(inline_keyboard=array_buttons)
    return markup


menu_buttons = [
    [InlineKeyboardButton(text='New game', callback_data='new_game'),
     InlineKeyboardButton(text='Stat', callback_data='stats'),
     InlineKeyboardButton(text='Records', callback_data='records')]
]
menu_buttons = InlineKeyboardMarkup(inline_keyboard=menu_buttons)


cross_or_toe = [[InlineKeyboardButton(text='❌', callback_data='cross')]]
cross_or_toe_buttons = InlineKeyboardMarkup(inline_keyboard=cross_or_toe)

new_game_button = [
                    [InlineKeyboardButton(text='New game', callback_data='new_game'),
                     InlineKeyboardButton(text='Records', callback_data='records')]
                   ]

new_game_button = InlineKeyboardMarkup(inline_keyboard=new_game_button)


new_game_button_2 = [
                    [InlineKeyboardButton(text='New game', callback_data='new_game'),
                     InlineKeyboardButton(text='Stat', callback_data='stats')]
                   ]
new_game_button_2 = InlineKeyboardMarkup(inline_keyboard=new_game_button_2)
