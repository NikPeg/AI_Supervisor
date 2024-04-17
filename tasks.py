import asyncio

from config import ADMIN_ID

import messages
import payments
from database.feedback_db import delete_user_from_feedback, get_all_feed_back_users
from database.feedback_db import get_all_subscriptions
from database.payment_db import subscribe, unsubscribe
from keyboards.keyboards import feedback_markup
from loader import bot, client

FEEDBACK_PERIOD = 24 * 60 * 60


async def start_feed_back():
    while True:
        all_users = get_all_feed_back_users()
        for user in all_users:
            try:
                await bot.send_message(user[0], text=messages.FEEDBACK_ASK, reply_markup=feedback_markup())
                await bot.send_message(ADMIN_ID, text=messages.FEEDBACK_ASKED.format(user[0]))
                delete_user_from_feedback(user[0])
            except Exception as e:
                await bot.send_message(ADMIN_ID, text=e)
                continue
        await asyncio.sleep(FEEDBACK_PERIOD)


async def check_subscriptions():
    await bot.send_message(ADMIN_ID, text=messages.CHECK_SUBSCRIPTION)
    while True:
        all_users = get_all_subscriptions()
        for user_id, username, subscribed in all_users:
            try:
                for sub in client.list_subscriptions(user_id):
                    if sub.status == payments.SubscriptionStatus.ACTIVE.value and not subscribed:
                        await bot.send_message(
                            ADMIN_ID,
                            messages.SUBSCRIPTION_ERROR.format(user_id, username),
                        )
                        subscribe(user_id)
                        break
                    if sub.status == payments.SubscriptionStatus.CANCELLED.value and subscribed:
                        await bot.send_message(
                            ADMIN_ID,
                            messages.SUBSCRIPTION_ENDED.format(user_id, username),
                        )
                        unsubscribe(user_id)
                        break
            except Exception as e:
                await bot.send_message(ADMIN_ID, text=e)
                continue
        await asyncio.sleep(FEEDBACK_PERIOD)
