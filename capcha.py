import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Конфигурация
TARGET_CHANNEL_ID = 1393283447400697856  # ID чата, за которым следим
ROLE_TO_REMOVE = 1393282494446698647     # Роль для удаления (замени на свою)
ROLE_TO_ADD = 1393281376773603491        # Роль для выдачи (замени на свою)

@bot.event
async def on_message(message):
    # Игнорируем сообщения не из нужного чата или от других ботов
    if message.channel.id != TARGET_CHANNEL_ID or message.author.bot:
        return

    member = message.author
    guild = message.guild

    # Получаем объекты ролей
    role_to_remove = guild.get_role(ROLE_TO_REMOVE)
    role_to_add = guild.get_role(ROLE_TO_ADD)

    if not (role_to_remove and role_to_add):
        print("Ошибка: Роли не найдены!")
        return

    try:
        # Удаляем старую роль (если есть)
        if role_to_remove in member.roles:
            await member.remove_roles(role_to_remove)
            print(f"У {member.display_name} убрана роль {role_to_remove.name}")

        # Выдаём новую роль
        await member.add_roles(role_to_add)
        print(f"У {member.display_name} выдана роль {role_to_add.name}")

        # Удаляем сообщение пользователя
        await message.delete()
        print(f"Сообщение от {member.display_name} удалено.")

    except discord.Forbidden:
        print("Ошибка: Недостаточно прав! (управление ролями/удаление сообщений)")
    except Exception as e:
        print(f"Ошибка: {e}")

    await bot.process_commands(message)  # Важно для других команд

# Запуск бота
TOKEN = "MTM5OTg5NTk2NzExNjgyMDU0MQ.G6Uupf.Pfb9t5LdpaiPRHbzaYLnaLdqywRRpNiYHbAidU"  # Замени на свой токен
bot.run(TOKEN)
