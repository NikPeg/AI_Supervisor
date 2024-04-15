from cloudpayments import CloudPayments, Currency, Interval, Order
import config
import datetime


client = CloudPayments(config.PAYMENTS_ID, config.PAYMENTS_TOKEN)
print(client.create_order(100, Currency.RUB, "Бот", email=None,
                          send_email=True, require_confirmation=None,
                          invoice_id=None, account_id=None, phone=None,
                          send_sms=None, send_whatsapp=None, culture_info=None))
# Order(id='hYcYnX5XYg84hdfa', number=1, amount=100, currency='RUB', currency_code=0, email='peganov.nik@gmail.com', description='Бот', require_confirmation=False, url='https://orders.cloudpayments.ru/d/hYcYnX5XYg84hdfa')
# print(client.create_subscription(token, account_id, 100, Currency.RUB,
#                           "Подписка на бота", "peganov.nik@gmail.com", datetime.datetime.now(), Interval.MONTH, 1,
#                           require_confirmation=False, max_periods=None))
print(Order.mro())
