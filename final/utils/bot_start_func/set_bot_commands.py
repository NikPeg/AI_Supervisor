from constants import commands


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        commands.START,
        commands.HELP,
        commands.NEW_CASE,
    ])
