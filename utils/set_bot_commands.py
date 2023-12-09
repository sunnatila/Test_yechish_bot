from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("info", "Profilim haqida malumot"),
            types.BotCommand("set_email", "Emailni o'zgartirish"),
            types.BotCommand("set_number", "Telefon nomerni o'zgartirish"),
            types.BotCommand("set_fullname", "Ism-Familiyani o'zgartirish"),
            types.BotCommand("all_users", "Hamma foydalanuvchilarni ko'rish. Faqat admin uchun!"),
            types.BotCommand("send_post", "Hamma foydalanuvchilarga habar yuborish. Faqat admin uchun!"),
            types.BotCommand("del_users", "Foydalanuvchilarni ochirish. Faqat admin uchun!"),
            types.BotCommand("del_tests", "Testlarni ochirish. Faqat admin uchun!"),
        ]
    )
