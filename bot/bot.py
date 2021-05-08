import logging
import typing
import re

from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

API_TOKEN = '1636384341:AAFm2WJcfNaa9bQWAMYdjNXFN4fozr9dq28'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

get_cb = CallbackData('item', 'action')
order = {}


async def generate_menu(message_or_query: typing.Union[types.Message, types.CallbackQuery], edit_msg=False):
    text = 'Ты можешь приобрести:'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.add(
        types.InlineKeyboardButton('лайки', callback_data=get_cb.new(action='get_likes')),
        types.InlineKeyboardButton('просмотры', callback_data=get_cb.new(action='get_views')),
        types.InlineKeyboardButton('подписчиков', callback_data=get_cb.new(action='get_followers')),
        types.InlineKeyboardButton('комментарии', callback_data=get_cb.new(action='get_comments')),
        types.InlineKeyboardButton('статистику', callback_data=get_cb.new(action='get_statistics')),
        types.InlineKeyboardButton('жалобы', callback_data=get_cb.new(action='get_reports')),
    )
    if not edit_msg:
        await bot.send_message(chat_id=message_or_query.chat.id, text=text, reply_markup=keyboard_markup)
    else:
        await bot.edit_message_text(text,
                                    message_or_query.from_user.id,
                                    message_or_query.message.message_id,
                                    reply_markup=keyboard_markup)


def generate_name(callback_data_action: str):
    if 'likes' in callback_data_action:
        return re.findall(r'\d+_[a-z]+', callback_data_action)[0].replace('_likes', ' лайков')
    if 'views' in callback_data_action:
        return re.findall(r'\d+_[a-z]+', callback_data_action)[0].replace('_views', ' просмотров')
    if 'followers' in callback_data_action:
        return re.findall(r'\d+_[a-z]+', callback_data_action)[0].replace('_followers', ' подписчиков')
    if 'comments' in callback_data_action:
        return re.findall(r'\d+_[a-z]+', callback_data_action)[0].replace('_comments', ' комментариев')
    if 'stat' in callback_data_action:
        return re.findall(r'\d+_[a-z]+', callback_data_action)[0].replace('_stat', ' статы')
    if 'rempost' in callback_data_action:
        return re.findall(r'[a-z]+', callback_data_action)[0].replace('rempost', ' удаление поста')
    if 'remacc' in callback_data_action:
        return re.findall(r'[a-z]+', callback_data_action)[0].replace('remacc', ' удаление аккаунта')


def generate_go_back_action(callback_data_action: str):
    if 'likes' in callback_data_action:
        return 'get_likes'
    if 'views' in callback_data_action:
        return 'get_views'
    if 'followers' in callback_data_action:
        return 'get_followers'
    if 'comments' in callback_data_action:
        return 'get_comments'
    if 'stat' in callback_data_action:
        return 'get_statistics'
    if 'rem' in callback_data_action:
        return 'get_reports'


@dp.message_handler(commands=['start', 'restart'])
@dp.message_handler(text_contains=['меню'])
async def start_cmd_handler(message: types.Message):
    logger.debug(f'{message.from_user.mention} started bot or called menu.')
    await generate_menu(message)


@dp.callback_query_handler(get_cb.filter(action='menu'))
async def menu_handler(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logger.debug(f'{query.from_user.mention} called menu.')
    await query.answer()
    await generate_menu(query, edit_msg=True)


@dp.callback_query_handler(get_cb.filter(action='get_likes'))
async def callback_likes_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    text = 'Купить лайки:'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard_markup.add(
        types.InlineKeyboardButton('100', callback_data=get_cb.new(action='100_likes_50')),
        types.InlineKeyboardButton('250', callback_data=get_cb.new(action='250_likes_100')),
        types.InlineKeyboardButton('500', callback_data=get_cb.new(action='500_likes_200')),
        types.InlineKeyboardButton('1.000', callback_data=get_cb.new(action='1000_likes_350')),
        types.InlineKeyboardButton('2.500', callback_data=get_cb.new(action='2500_likes_500')),
        types.InlineKeyboardButton('5.000', callback_data=get_cb.new(action='5000_likes_650')),
        types.InlineKeyboardButton('10.000', callback_data=get_cb.new(action='10000_likes_750')),
        types.InlineKeyboardButton('15.000', callback_data=get_cb.new(action='15000_likes_1500')),
        types.InlineKeyboardButton('25.000', callback_data=get_cb.new(action='25000_likes_2000')),
        types.InlineKeyboardButton('50.000', callback_data=get_cb.new(action='50000_likes_2500')),
        types.InlineKeyboardButton('100.000', callback_data=get_cb.new(action='100000_likes_3500')),
        types.InlineKeyboardButton('1.000.000', callback_data=get_cb.new(action='1000000_likes_35000')),
    )
    keyboard_markup.row(types.InlineKeyboardButton('назад', callback_data=get_cb.new(action='menu')))
    await bot.edit_message_text(text, query.from_user.id, query.message.message_id, reply_markup=keyboard_markup)


likes_actions = ['100_likes_50', '250_likes_100', '500_likes_200', '1000_likes_350', '2500_likes_500', '5000_likes_650',
                 '10000_likes_750', '15000_likes_1500', '25000_likes_2000', '50000_likes_2500',
                 '100000_likes_3500', '1000000_likes_35000']


@dp.callback_query_handler(get_cb.filter(action='get_views'))
async def callback_views_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    text = 'Купить просмотры (шт.):'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard_markup.add(
        types.InlineKeyboardButton('10.000', callback_data=get_cb.new(action='10000_views_250')),
        types.InlineKeyboardButton('50.000', callback_data=get_cb.new(action='50000_views_500')),
        types.InlineKeyboardButton('100.000', callback_data=get_cb.new(action='100000_views_600')),
        types.InlineKeyboardButton('500.000', callback_data=get_cb.new(action='500000_views_1500')),
    )
    keyboard_markup.row(types.InlineKeyboardButton('назад', callback_data=get_cb.new(action='menu')))
    await bot.edit_message_text(text, query.from_user.id, query.message.message_id, reply_markup=keyboard_markup)


views_actions = ['10000_views_250', '50000_views_500', '100000_views_600', '500000_views_1500']


@dp.callback_query_handler(get_cb.filter(action='get_followers'))
async def callback_followers_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    text = 'Купить подписчиков:'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard_markup.add(
        types.InlineKeyboardButton('100', callback_data=get_cb.new(action='100_followers_100')),
        types.InlineKeyboardButton('250', callback_data=get_cb.new(action='250_followers_150')),
        types.InlineKeyboardButton('1.000', callback_data=get_cb.new(action='1000_followers_300')),
        types.InlineKeyboardButton('2.500', callback_data=get_cb.new(action='2500_followers_500')),
        types.InlineKeyboardButton('5.000', callback_data=get_cb.new(action='5000_followers_900')),
        types.InlineKeyboardButton('10.000', callback_data=get_cb.new(action='10000_followers_1800')),
        types.InlineKeyboardButton('15.000', callback_data=get_cb.new(action='15000_followers_2000')),
        types.InlineKeyboardButton('25.000', callback_data=get_cb.new(action='25000_followers_2500')),
        types.InlineKeyboardButton('50.000', callback_data=get_cb.new(action='50000_followers_4500')),
        types.InlineKeyboardButton('100.000', callback_data=get_cb.new(action='100000_followers_8500')),
        types.InlineKeyboardButton('1.000.000', callback_data=get_cb.new(action='1000000_followers_75000')),
    )
    keyboard_markup.row(types.InlineKeyboardButton('назад', callback_data=get_cb.new(action='menu')))
    await bot.edit_message_text(text, query.from_user.id, query.message.message_id, reply_markup=keyboard_markup)


followers_actions = ['100_followers_100', '250_followers_150', '1000_followers_300', '2500_followers_500',
                     '5000_followers_900', '10000_followers_1800', '15000_followers_2000', '25000_followers_2500',
                     '50000_followers_4500', '100000_followers_8500', '1000000_followers_75000']


@dp.callback_query_handler(get_cb.filter(action='get_comments'))
async def callback_comments_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    text = 'Купить комментарии:'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
    keyboard_markup.add(
        types.InlineKeyboardButton('10', callback_data=get_cb.new(action='10_comments_100')),
        types.InlineKeyboardButton('25', callback_data=get_cb.new(action='25_comments_150')),
        types.InlineKeyboardButton('50', callback_data=get_cb.new(action='50_comments_200')),
        types.InlineKeyboardButton('100', callback_data=get_cb.new(action='100_comments_250')),
        types.InlineKeyboardButton('500', callback_data=get_cb.new(action='500_comments_300')),
    )
    keyboard_markup.row(types.InlineKeyboardButton('назад', callback_data=get_cb.new(action='menu')))
    await bot.edit_message_text(text, query.from_user.id, query.message.message_id, reply_markup=keyboard_markup)


comments_actions = ['10_comments_100', '25_comments_150', '50_comments_200', '100_comments_250', '500_comments_300']


@dp.callback_query_handler(get_cb.filter(action='get_statistics'))
async def callback_statistics_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    text = 'Купить статистику (показы и сохранения):'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard_markup.add(
        types.InlineKeyboardButton('10.000', callback_data=get_cb.new(action='10000_stat_500')),
        types.InlineKeyboardButton('25.000', callback_data=get_cb.new(action='25000_stat_700')),
        types.InlineKeyboardButton('50.000', callback_data=get_cb.new(action='100000_stat_2500')),
    )
    keyboard_markup.row(types.InlineKeyboardButton('назад', callback_data=get_cb.new(action='menu')))
    await bot.edit_message_text(text, query.from_user.id, query.message.message_id, reply_markup=keyboard_markup)


stat_actions = ['10000_stat_500', '25000_stat_700', '100000_stat_2500']


@dp.callback_query_handler(get_cb.filter(action='get_reports'))
async def callback_reports_action(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    text = 'Купить жалобы:'
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard_markup.add(
        types.InlineKeyboardButton('удаление публикации', callback_data=get_cb.new(action='rempost_3000')),
        types.InlineKeyboardButton('удаление аккаунта', callback_data=get_cb.new(action='remacc_7000')),
    )
    keyboard_markup.row(types.InlineKeyboardButton('назад', callback_data=get_cb.new(action='menu')))
    await bot.edit_message_text(text, query.from_user.id, query.message.message_id, reply_markup=keyboard_markup)


reports_actions = ['rempost_3000', 'remacc_7000']

all_actions = likes_actions + views_actions + followers_actions + comments_actions + stat_actions + reports_actions


@dp.callback_query_handler(get_cb.filter(action=all_actions))
async def proceed_with_chosen(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    callback_data_action = callback_data['action']
    order_item = order.get(query.from_user.id, {})
    order_item['action'] = callback_data_action
    order_item['name'] = generate_name(callback_data_action)
    order_item['price'] = int(re.findall(r'_\d+', callback_data_action)[0].replace('_', ''))
    order[query.from_user.id] = order_item
    text = f"Купить {order_item['name']} за {order_item['price']} рублей?"
    go_back_action = generate_go_back_action(callback_data_action)
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard_markup.add(
        types.InlineKeyboardButton('купить', callback_data=get_cb.new(action='order_continue')),
        types.InlineKeyboardButton('назад', callback_data=get_cb.new(action=go_back_action)),
    )
    await bot.edit_message_text(text, query.from_user.id, query.message.message_id, reply_markup=keyboard_markup)


@dp.callback_query_handler(get_cb.filter(action='order_continue'))
async def order_continue(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    text = f'Отправьте ссылку на пост или аккаунт чтобы продолжить.'
    await bot.edit_message_text(text, query.from_user.id, query.message.message_id)


@dp.message_handler(text_contains=['inst'])
async def get_url(message: types.Message):
    logging.info(f'{message.from_user.mention} gave link {message.text}')
    order_item = order.get(message.from_user.id, {})
    if 'action' in order_item:
        order_item['url'] = message.text
        order[message.from_user.id] = order_item
        price = order_item['price']
        text = f"Ваша ссылка - {order_item['url']}.\n" \
               f"Чтобы изменить ссылку отправьте её повторно.\n" \
               f"Перейти к оплате ({price} руб)?"
        keyboard_markup = types.InlineKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard_markup.add(
            types.InlineKeyboardButton('оплатить', callback_data=get_cb.new(action='pay')),
            types.InlineKeyboardButton('отмена', callback_data=get_cb.new(action='menu')),
        )
        await bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard_markup)
    else:
        await start_cmd_handler(message)


@dp.callback_query_handler(get_cb.filter(action='pay'))
async def pay(query: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    logging.info('Got this callback data: %r from %s', callback_data, query.from_user.mention)
    await query.answer()
    order_item = order.get(query.from_user.id, {})
    if 'action' in order_item:
        text = f"Чтобы оплатить заказ переведите {order_item['price']} рублей по данной ссылке: <тут ссылка>\n" \
               f"Заказ будет выполнен в течении одного рабочего дня. \n"
        admin_text = f"‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️‼️\n" \
                     f"Новый заказ от {query.from_user.mention}\n" \
                     f"{order_item['name']} за {order_item['price']} рублей по ссылке {order_item['url']}\n" \
                     f"Коля купи энергетик!!!"
        logging.info(f"{query.from_user.mention}: "
                     f"{order_item['name']} за {order_item['price']} рублей по ссылке {order_item['url']}")
        await bot.send_message(chat_id='483693812', text=admin_text)
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        keyboard_markup.row(types.KeyboardButton('меню'))
        order_item.clear()
        await bot.send_message(chat_id=query.from_user.id, text=text, reply_markup=keyboard_markup)
    else:
        await menu_handler(query)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
