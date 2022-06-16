from psycopg2 import DatabaseError
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from imdb.services.telegram.user_shows import get_user_shows, check_show_is_seen, get_user_rating, get_seasons, is_subscribed_on_updates, get_episodes, get_episode_info
from imdb.services.shows_add_utils import check_usershow_exists
from imdb.services.kinopoisk_api import KP_API
from collections import namedtuple


def default_keyboard_markup() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    schedule_button = KeyboardButton('Список к просмотру')
    my_films_button = KeyboardButton('Мои фильмы')
    my_series_button = KeyboardButton('Мои cериалы')
    search_button = KeyboardButton('Искать')
    markup.add(schedule_button)
    markup.row(my_films_button, my_series_button)
    markup.add(search_button)
    return markup


def find_results_markup(message) -> InlineKeyboardMarkup:
    target = message.text
    markup = InlineKeyboardMarkup()
    shows = KP_API.parse_response(target, 'keyword')
    for show in shows:
        details_button = InlineKeyboardButton(
            text=f'{show.title_ru} | {show.title_en}: {show.year}', callback_data=f'show_details {show.kinopoisk_id}')
        markup.add(details_button)
    return markup


def delete_confirmation_markup(show_id, original_message_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    confirm_button = InlineKeyboardButton(
        text='Да', callback_data=f'delete {show_id} confirmed  {original_message_id}')
    descline_button = InlineKeyboardButton(
        text='Нет', callback_data=f'delete {show_id} desclined')
    markup.add(confirm_button, descline_button)
    return markup


def details_inline_markup(user_id, show_id, is_series: bool = False):
    markup = InlineKeyboardMarkup()
    delete_button = InlineKeyboardButton(
        'Удалить из списка', callback_data=f'delete {show_id}')
    seasons_button = InlineKeyboardButton(
        'Сезоны', callback_data=f'seasons {show_id}')
    rating_button = InlineKeyboardButton(
        text=f'Твоя оценка: {get_user_rating(user_id, show_id)}', callback_data=f'change rating')
    updates_on_button = InlineKeyboardButton(
        text='Отслеживать новые серии', callback_data=f'subscribe {show_id} on')
    updates_off_button = InlineKeyboardButton(
        text='Не отслеживать', callback_data=f'subscribe {show_id} off')
    if check_show_is_seen(user_id, show_id):
        markup.add(rating_button)
        if is_series:
            markup.add(seasons_button)
            if is_subscribed_on_updates(user_id, show_id):
                markup.add(updates_off_button)
            else:
                markup.add(updates_on_button)
        markup.add(delete_button)
        return markup

    if check_usershow_exists(user_id, show_id):
        action_button = InlineKeyboardButton(
            'Посмотрел!', callback_data=f'mark_seen {show_id}')
        markup.add(action_button)
        if is_series:
            markup.add(seasons_button)
            if is_subscribed_on_updates(user_id, show_id):
                markup.add(updates_off_button)
            else:
                markup.add(updates_on_button)
        markup.add(delete_button)
        return markup

    action_button = InlineKeyboardButton(
        'Хочу посмотреть!', callback_data=f'add {show_id}')
    markup.add(action_button)
    return markup


def list_inline_markup(user_id, current_page: int, filter: str) -> InlineKeyboardMarkup:
    '''
    Return inline markup page by page
    '''
    def get_page(shows: list, num_on_page: int, start: int, end: int) -> namedtuple:
        shows_length = len(shows)
        result = namedtuple('result', 'shows remaining')
        if shows_length <= num_on_page:
            return result(shows, 0)
        return result(shows[start:end], shows_length - end)
    try:
        all_user_shows = get_user_shows(
            user_id, filter=filter)
    except:
        raise DatabaseError

    if all_user_shows == None:
        return None

    shows_to_print = get_page(
        all_user_shows, 5, ((current_page - 1) * 5), ((current_page - 1) * 5) + 5)
    pages = ((len(all_user_shows)) // 5) + 1
    markup = InlineKeyboardMarkup()
    next_button = InlineKeyboardButton(
        text=f'>>> Вперед: {current_page + 1} из {pages}', callback_data=f'next_page {current_page + 1} {filter}')
    prev_button = InlineKeyboardButton(
        text=f'<<< Назад: {current_page - 1} из {pages}', callback_data=f'next_page {current_page - 1} {filter}')
    for show in shows_to_print.shows:
        details_button = InlineKeyboardButton(
            text=f'{show.show.title}: {show.show.year}', callback_data=f'show_details {show.show.id}')
        markup.add(details_button)

    if shows_to_print.remaining == 0:
        return markup

    if current_page == 1 and shows_to_print.remaining > 0:
        markup.add(next_button)
    elif 1 < current_page < pages:
        markup.row_width = 2
        markup.row(prev_button, next_button)
    else:
        markup.add(prev_button)

    return markup


def seasons_inline_markup(show_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    seasons = get_seasons(show_id)
    if not seasons:
        return None
    for season in seasons:
        markup.add(InlineKeyboardButton(
            text=f'Сезон {season.season_number}{"(" + str(season.air_date.year) + ")" if season.air_date else ""}', callback_data=f'season_info {season.id} pass {show_id}'))
    markup.add(InlineKeyboardButton(text='<<< НАЗАД',
               callback_data=f'seasons {show_id} back'))
    return markup


def episodes_inline_markup(season_id, show_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    episodes = get_episodes(season_id)
    if not episodes:
        return None
    for episode in episodes:
        markup.add(InlineKeyboardButton(
            text=f'{episode.episode_number}', callback_data=f'episode_info {episode.id} pass {season_id} {show_id}'))
    markup.add(InlineKeyboardButton(text='<<< НАЗАД',
               callback_data=f'season_info {show_id} back'))
    return markup


def episode_info_inline_markup(episode_id, season_id, show_id) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='<<< НАЗАД',
               callback_data=f'episode_info {season_id} back {show_id}'))
    return markup
