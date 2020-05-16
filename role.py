import discord
from discord import utils
import os

POST_ID = 672160421368561667

ROLES = {
    '💛': 711203435915116607,
    '💙': 711203740752805968,
    '🧡': 711203932822700082,
    '💚': 711204030503845898,
    '💜': 711204257809956944,
    '🤎': 711204334142095420
}

EXCROLES = ()

MAX_ROLES_PER_USER = 15


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        channel = self.get_channel(payload.channel_id)  # получаем объект канала
        message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
        member = utils.get(message.guild.members,
                           id=payload.user_id)  # получаем объект пользователя который поставил реакцию

        try:
            emoji = str(payload.emoji)  # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=ROLES[emoji])  # объект выбранной роли (если есть)

            if (len([i for i in member.roles if i.id not in EXCROLES]) <= MAX_ROLES_PER_USER):
                await member.add_roles(role)
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
            else:
                await message.remove_reaction(payload.emoji, member)
                print('[ERROR] Too many roles for user {0.display_name}'.format(member))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)  # получаем объект канала
        message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
        member = utils.get(message.guild.members,
                           id=payload.user_id)  # получаем объект пользователя который поставил реакцию

        try:
            emoji = str(payload.emoji)  # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=ROLES[emoji])  # объект выбранной роли (если есть)

            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


# RUN
client = MyClient()
token = os.environ.get('TOKEN')
client.run(str(token))

