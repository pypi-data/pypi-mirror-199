# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import logging
import sys

from pyAyiin.config import Var as Variable

from ..methods.helpers import Helpers
from ..methods.hosting import where_hosted

from .client import *


logs = logging.getLogger(__name__)
HOSTED_ON = where_hosted()
Var = Variable()
Xd = Helpers()


async def ayiin_client(client):
    try:
        await client.join_chat("AyiinChat")
        await client.join_chat("AyiinSupport")
        await client.join_chat("StoryAyiin")
    except Exception:
        pass


clients = []
client_id = []


async def StartPyrogram():
    try:
        bot_plugins = Xd.import_module(
            "assistant/",
            display_module=False,
            exclude=Var.NO_LOAD,
        )
        logs.info(f"{bot_plugins} Total Plugins Bot")
        plugins = Xd.import_module(
            "AyiinXd/",
            display_module=False,
            exclude=Var.NO_LOAD,
        )
        logs.info(f"{plugins} Total Plugins User")
    except BaseException as e:
        logs.info(e)
        sys.exit()
    if tgbot:
        await tgbot.start()
        me = await tgbot.get_me()
        tgbot.id = me.id
        tgbot.mention = me.mention
        tgbot.username = me.username
        if me.last_name:
            tgbot.name = me.first_name + " " + me.last_name
        else:
            tgbot.name = me.first_name
        logs.info(
            f"TgBot in {tgbot.name} | [ {tgbot.id} ]"
        )
        client_id.append(tgbot.id)
    if AYIIN1:
        try:
            await AYIIN1.start()
            clients.append(1)
            await ayiin_client(AYIIN1)
            me = await AYIIN1.get_me()
            AYIIN1.id = me.id
            AYIIN1.mention = me.mention
            AYIIN1.username = me.username
            if me.last_name:
                AYIIN1.name = me.first_name + " " + me.last_name
            else:
                AYIIN1.name = me.first_name
            #AYIIN1.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN1 in {AYIIN1.name} | [ {AYIIN1.id} ]"
            )
            client_id.append(AYIIN1.id)
        except Exception as e:
            logs.info(f"[STRING_1] ERROR: {e}")
    if AYIIN2:
        try:
            await AYIIN2.start()
            clients.append(2)
            await ayiin_client(AYIIN2)
            me = await AYIIN2.get_me()
            AYIIN2.id = me.id
            AYIIN2.mention = me.mention
            AYIIN2.username = me.username
            if me.last_name:
                AYIIN2.name = me.first_name + " " + me.last_name
            else:
                AYIIN2.name = me.first_name
            #AYIIN2.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN2 in {AYIIN2.name} | [ {AYIIN2.id} ]"
            )
            client_id.append(AYIIN2.id)
        except Exception as e:
            logs.info(f"[STRING_2] ERROR: {e}")
    if AYIIN3:
        try:
            await AYIIN3.start()
            clients.append(3)
            await ayiin_client(AYIIN3)
            me = await AYIIN3.get_me()
            AYIIN3.id = me.id
            AYIIN3.mention = me.mention
            AYIIN3.username = me.username
            if me.last_name:
                AYIIN3.name = me.first_name + " " + me.last_name
            else:
                AYIIN3.name = me.first_name
            #AYIIN3.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN3 in {AYIIN3.name} | [ {AYIIN3.id} ]"
            )
            client_id.append(AYIIN3.id)
        except Exception as e:
            logs.info(f"[STRING_3] ERROR: {e}")
    if AYIIN4:
        try:
            await AYIIN4.start()
            clients.append(4)
            await ayiin_client(AYIIN4)
            me = await AYIIN4.get_me()
            AYIIN4.id = me.id
            AYIIN4.mention = me.mention
            AYIIN4.username = me.username
            if me.last_name:
                AYIIN4.name = me.first_name + " " + me.last_name
            else:
                AYIIN4.name = me.first_name
            #AYIIN4.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN4 in {AYIIN4.name} | [ {AYIIN4.id} ]"
            )
            client_id.append(AYIIN4.id)
        except Exception as e:
            logs.info(f"[STRING_4] ERROR: {e}")
    if AYIIN5:
        try:
            await AYIIN5.start()
            clients.append(5)
            await ayiin_client(AYIIN5)
            me = await AYIIN5.get_me()
            AYIIN5.id = me.id
            AYIIN5.mention = me.mention
            AYIIN5.username = me.username
            if me.last_name:
                AYIIN5.name = me.first_name + " " + me.last_name
            else:
                AYIIN5.name = me.first_name
            #AYIIN5.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN5 in {AYIIN5.name} | [ {AYIIN5.id} ]"
            )
            client_id.append(AYIIN5.id)
        except Exception as e:
            logs.info(f"[STRING_5] ERROR: {e}")
    if AYIIN6:
        try:
            await AYIIN6.start()
            clients.append(6)
            await ayiin_client(AYIIN6)
            me = await AYIIN6.get_me()
            AYIIN6.id = me.id
            AYIIN6.mention = me.mention
            AYIIN6.username = me.username
            if me.last_name:
                AYIIN6.name = me.first_name + " " + me.last_name
            else:
                AYIIN6.name = me.first_name
            #AYIIN1.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN6 in {AYIIN6.name} | [ {AYIIN6.id} ]"
            )
            client_id.append(AYIIN6.id)
        except Exception as e:
            logs.info(f"[STRING_6] ERROR: {e}")
    if AYIIN7:
        try:
            await AYIIN7.start()
            clients.append(7)
            await ayiin_client(AYIIN7)
            me = await AYIIN7.get_me()
            AYIIN7.id = me.id
            AYIIN7.mention = me.mention
            AYIIN7.username = me.username
            if me.last_name:
                AYIIN7.name = me.first_name + " " + me.last_name
            else:
                AYIIN7.name = me.first_name
            #AYIIN7.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN7 in {AYIIN7.name} | [ {AYIIN7.id} ]"
            )
            client_id.append(AYIIN7.id)
        except Exception as e:
            logs.info(f"[STRING_7] ERROR: {e}")
    if AYIIN8:
        try:
            await AYIIN8.start()
            clients.append(8)
            await ayiin_client(AYIIN8)
            me = await AYIIN8.get_me()
            AYIIN8.id = me.id
            AYIIN8.mention = me.mention
            AYIIN8.username = me.username
            if me.last_name:
                AYIIN8.name = me.first_name + " " + me.last_name
            else:
                AYIIN8.name = me.first_name
            #AYIIN8.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN8 in {AYIIN8.name} | [ {AYIIN8.id} ]"
            )
            client_id.append(AYIIN8.id)
        except Exception as e:
            logs.info(f"[STRING_8] ERROR: {e}")
    if AYIIN9:
        try:
            await AYIIN9.start()
            clients.append(9)
            await ayiin_client(AYIIN9)
            me = await AYIIN9.get_me()
            AYIIN9.id = me.id
            AYIIN9.mention = me.mention
            AYIIN9.username = me.username
            if me.last_name:
                AYIIN9.name = me.first_name + " " + me.last_name
            else:
                AYIIN9.name = me.first_name
            #AYIIN9.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN9 in {AYIIN9.name} | [ {AYIIN9.id} ]"
            )
            client_id.append(AYIIN9.id)
        except Exception as e:
            logs.info(f"[STRING_9] ERROR: {e}")
    if AYIIN10:
        try:
            await AYIIN10.start()
            clients.append(10)
            await ayiin_client(AYIIN10)
            me = await AYIIN10.get_me()
            AYIIN10.id = me.id
            AYIIN10.mention = me.mention
            AYIIN10.username = me.username
            if me.last_name:
                AYIIN10.name = me.first_name + " " + me.last_name
            else:
                AYIIN10.name = me.first_name
            #AYIIN10.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN10 in {AYIIN10.name} | [ {AYIIN10.id} ]"
            )
            client_id.append(AYIIN10.id)
        except Exception as e:
            logs.info(f"[STRING_10] ERROR: {e}")
    if AYIIN11:
        try:
            await AYIIN11.start()
            clients.append(11)
            AYIIN11.me = await AYIIN11.get_me()
            #AYIIN11.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN11 in {AYIIN11.me.first_name} | [ {AYIIN11.me.id} ]"
            )
            client_id.append(AYIIN11.id)
        except Exception:
            pass
    if AYIIN12:
        try:
            await AYIIN12.start()
            clients.append(12)
            AYIIN12.me = await AYIIN12.get_me()
            #AYIIN12.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN12 in {AYIIN12.me.first_name} | [ {AYIIN12.me.id} ]"
            )
            client_id.append(AYIIN12.id)
        except Exception:
            pass
    if AYIIN13:
        try:
            await AYIIN13.start()
            clients.append(13)
            AYIIN13.me = await AYIIN13.get_me()
            #AYIIN13.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN13 in {AYIIN13.me.first_name} | [ {AYIIN13.me.id} ]"
            )
            client_id.append(AYIIN13.id)
        except Exception:
            pass
    if AYIIN14:
        try:
            await AYIIN14.start()
            clients.append(14)
            AYIIN14.me = await AYIIN14.get_me()
            #AYIIN14.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN14 in {AYIIN14.me.first_name} | [ {AYIIN14.me.id} ]"
            )
            client_id.append(AYIIN14.id)
        except Exception:
            pass
    if AYIIN15:
        try:
            await AYIIN15.start()
            clients.append(15)
            AYIIN15.me = await AYIIN15.get_me()
            #AYIIN15.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN15 in {AYIIN15.me.first_name} | [ {AYIIN15.me.id} ]"
            )
            client_id.append(AYIIN15.id)
        except Exception:
            pass
    if AYIIN16:
        try:
            await AYIIN16.start()
            clients.append(16)
            AYIIN16.me = await AYIIN16.get_me()
           # AYIIN16.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN16 in {AYIIN16.me.first_name} | [ {AYIIN16.me.id} ]"
            )
            client_id.append(AYIIN16.id)
        except Exception:
            pass
    if AYIIN17:
        try:
            await AYIIN17.start()
            clients.append(17)
            AYIIN17.me = await AYIIN17.get_me()
            #AYIIN17.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN17 in {AYIIN17.me.first_name} | [ {AYIIN17.me.id} ]"
            )
            client_id.append(AYIIN17.id)
        except Exception:
            pass
    if AYIIN18:
        try:
            await AYIIN18.start()
            AYIIN18.me = await AYIIN18.get_me()
            clients.append(18)
            #AYIIN18.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN18 in {AYIIN18.me.first_name} | [ {AYIIN18.me.id} ]"
            )
            client_id.append(AYIIN18.id)
        except Exception:
            pass
    if AYIIN19:
        try:
            await AYIIN19.start()
            clients.append(19)
            AYIIN19.me = await AYIIN19.get_me()
            #AYIIN19.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN19 in {AYIIN19.me.first_name} | [ {AYIIN19.me.id} ]"
            )
            client_id.append(AYIIN19.id)
        except Exception:
            pass
    if AYIIN20:
        try:
            await AYIIN20.start()
            clients.append(20)
            AYIIN20.me = await AYIIN20.get_me()
            #AYIIN20.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN20 in {AYIIN20.me.first_name} | [ {AYIIN20.me.id} ]"
            )
            client_id.append(AYIIN20.id)
        except Exception:
            pass
    if AYIIN21:
        try:
            await AYIIN21.start()
            clients.append(21)
            AYIIN21.me = await AYIIN21.get_me()
            #AYIIN21.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN21 in {AYIIN21.me.first_name} | [ {AYIIN21.me.id} ]"
            )
            client_id.append(AYIIN21.id)
        except Exception:
            pass
    if AYIIN22:
        try:
            await AYIIN22.start()
            clients.append(22)
            AYIIN22.me = await AYIIN22.get_me()
            #AYIIN22.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN22 in {AYIIN22.me.first_name} | [ {AYIIN22.me.id} ]"
            )
            client_id.append(AYIIN22.id)
        except Exception:
            pass
    if AYIIN23:
        try:
            await AYIIN23.start()
            clients.append(23)
            AYIIN23.me = await AYIIN23.get_me()
            #AYIIN23.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN23 in {AYIIN23.me.first_name} | [ {AYIIN23.me.id} ]"
            )
            
            client_id.append(AYIIN23.id)
        except Exception:
            pass
    if AYIIN24:
        try:
            await AYIIN24.start()
            clients.append(24)
            AYIIN24.me = await AYIIN24.get_me()
            #AYIIN24.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN24 in {AYIIN24.me.first_name} | [ {AYIIN24.me.id} ]"
            )
            
            client_id.append(AYIIN24.id)
        except Exception:
            pass
    if AYIIN25:
        try:
            await AYIIN25.start()
            clients.append(25)
            AYIIN25.me = await AYIIN25.get_me()
            #AYIIN25.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN25 in {AYIIN25.me.first_name} | [ {AYIIN25.me.id} ]"
            )
            client_id.append(AYIIN25.id)
        except Exception:
            pass
    if AYIIN26:
        try:
            await AYIIN26.start()
            clients.append(26)
            AYIIN26.me = await AYIIN26.get_me()
            #AYIIN26.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN26 in {AYIIN26.me.first_name} | [ {AYIIN26.me.id} ]"
            )
            client_id.append(AYIIN26.id)
        except Exception:
            pass
    if AYIIN27:
        try:
            await AYIIN27.start()
            clients.append(27)
            AYIIN27.me = await AYIIN27.get_me()
            #AYIIN27.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN27 in {AYIIN27.me.first_name} | [ {AYIIN27.me.id} ]"
            )
            client_id.append(AYIIN27.id)
        except Exception:
            pass
    if AYIIN28:
        try:
            await AYIIN28.start()
            clients.append(28)
            AYIIN28.me = await AYIIN28.get_me()
            #AYIIN28.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN28 in {AYIIN28.me.first_name} | [ {AYIIN28.me.id} ]"
            )
            client_id.append(AYIIN28.id)
        except Exception:
            pass
    if AYIIN29:
        try:
            await AYIIN29.start()
            AYIIN29.me = await AYIIN29.get_me()
            clients.append(29)
            #AYIIN29.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN29 in {AYIIN29.me.first_name} | [ {AYIIN29.me.id} ]"
            )
            client_id.append(AYIIN29.id)
        except Exception:
            pass
    if AYIIN30:
        try:
            await AYIIN30.start()
            clients.append(30)
            AYIIN30.me = await AYIIN30.get_me()
            #AYIIN30.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN30 in {AYIIN30.me.first_name} | [ {AYIIN30.me.id} ]"
            )
            client_id.append(AYIIN30.id)
        except Exception:
            pass
    if AYIIN31:
        try:
            await AYIIN31.start()
            clients.append(31)
            AYIIN31.me = await AYIIN31.get_me()
            #AYIIN31.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN31 in {AYIIN31.me.first_name} | [ {AYIIN31.me.id} ]"
            )
            client_id.append(AYIIN31.id)
        except Exception:
            pass
    if AYIIN32:
        try:
            await AYIIN32.start()
            clients.append(32)
            AYIIN32.me = await AYIIN32.get_me()
            #AYIIN32.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN32 in {AYIIN32.me.first_name} | [ {AYIIN32.me.id} ]"
            )
            client_id.append(AYIIN32.id)
        except Exception:
            pass
    if AYIIN33:
        try:
            await AYIIN33.start()
            clients.append(33)
            AYIIN33.me = await AYIIN33.get_me()
            #AYIIN33.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN33 in {AYIIN33.me.first_name} | [ {AYIIN33.me.id} ]"
            )
            client_id.append(AYIIN33.id)
        except Exception:
            pass
    if AYIIN34:
        try:
            await AYIIN34.start()
            clients.append(34)
            AYIIN34.me = await AYIIN34.get_me()
            #AYIIN34.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN34 in {AYIIN34.me.first_name} | [ {AYIIN34.me.id} ]"
            )
            client_id.append(AYIIN34.id)
        except Exception:
            pass
    if AYIIN35:
        try:
            await AYIIN35.start()
            clients.append(35)
            AYIIN35.me = await AYIIN35.get_me()
            #AYIIN35.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN35 in {AYIIN35.me.first_name} | [ {AYIIN35.me.id} ]"
            )
            client_id.append(AYIIN35.id)
        except Exception:
            pass
    if AYIIN36:
        try:
            await AYIIN36.start()
            clients.append(36)
            AYIIN36.me = await AYIIN36.get_me()
            #AYIIN36.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN36 in {AYIIN36.me.first_name} | [ {AYIIN36.me.id} ]"
            )
            client_id.append(AYIIN36.id)
        except Exception:
            pass
    if AYIIN37:
        try:
            await AYIIN37.start()
            clients.append(37)
            AYIIN37.me = await AYIIN37.get_me()
            #AYIIN37.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN37 in {AYIIN37.me.first_name} | [ {AYIIN37.me.id} ]"
            )
            client_id.append(AYIIN37.id)
        except Exception:
            pass
    if AYIIN38:
        try:
            await AYIIN38.start()
            clients.append(38)
            AYIIN38.me = await AYIIN38.get_me()
            #AYIIN38.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN38 in {AYIIN38.me.first_name} | [ {AYIIN38.me.id} ]"
            )
            client_id.append(AYIIN38.id)
        except Exception:
            pass
    if AYIIN39:
        try:
            await AYIIN39.start()
            clients.append(39)
            AYIIN39.me = await AYIIN39.get_me()
            #AYIIN39.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN39 in {AYIIN39.me.first_name} | [ {AYIIN39.me.id} ]"
            )
            client_id.append(AYIIN39.me.id)
        except Exception:
            pass
    if AYIIN40:
        try:
            await AYIIN40.start()
            clients.append(40)
            AYIIN40.me = await AYIIN40.get_me()
            #AYIIN40.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN40 in {AYIIN40.me.first_name} | [ {AYIIN40.me.id} ]"
            )
            client_id.append(AYIIN40.me.id)
        except Exception:
            pass
    if AYIIN41:
        try:
            await AYIIN41.start()
            clients.append(41)
            AYIIN41.me = await AYIIN41.get_me()
            #AYIIN41.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN41 in {AYIIN41.me.first_name} | [ {AYIIN41.me.id} ]"
            )
            client_id.append(AYIIN41.me.id)
        except Exception:
            pass
    if AYIIN42:
        try:
            await AYIIN42.start()
            clients.append(42)
            AYIIN42.me = await AYIIN42.get_me()
            #AYIIN42.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN42 in {AYIIN42.me.first_name} | [ {AYIIN42.me.id} ]"
            )
            client_id.append(AYIIN42.me.id)
        except Exception:
            pass
    if AYIIN43:
        try:
            await AYIIN43.start()
            clients.append(43)
            AYIIN43.me = await AYIIN43.get_me()
            #AYIIN43.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN43 in {AYIIN43.me.first_name} | [ {AYIIN43.me.id} ]"
            )
            client_id.append(AYIIN43.me.id)
        except Exception:
            pass
    if AYIIN44:
        try:
            await AYIIN44.start()
            clients.append(44)
            AYIIN44.me = await AYIIN44.get_me()
            #AYIIN44.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN44 in {AYIIN44.me.first_name} | [ {AYIIN44.me.id} ]"
            )
            client_id.append(AYIIN44.me.id)
        except Exception:
            pass
    if AYIIN45:
        try:
            await AYIIN45.start()
            clients.append(45)
            AYIIN45.me = await AYIIN45.get_me()
            #AYIIN45.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN45 in {AYIIN45.me.first_name} | [ {AYIIN45.me.id} ]"
            )
            client_id.append(AYIIN45.me.id)
        except Exception:
            pass
    if AYIIN46:
        try:
            await AYIIN46.start()
            clients.append(46)
            AYIIN46.me = await AYIIN46.get_me()
            #AYIIN46.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN46 in {AYIIN46.me.first_name} | [ {AYIIN46.me.id} ]"
            )
            client_id.append(AYIIN46.me.id)
        except Exception:
            pass
    if AYIIN47:
        try:
            await AYIIN47.start()
            clients.append(47)
            AYIIN47.me = await AYIIN47.get_me()
            #AYIIN47.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN47 in {AYIIN47.me.first_name} | [ {AYIIN47.me.id} ]"
            )
            client_id.append(AYIIN47.me.id)
        except Exception:
            pass
    if AYIIN48:
        try:
            await AYIIN48.start()
            clients.append(48)
            AYIIN48.me = await AYIIN48.get_me()
            #AYIIN48.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN48 in {AYIIN48.me.first_name} | [ {AYIIN48.me.id} ]"
            )
            client_id.append(AYIIN48.me.id)
        except Exception:
            pass
    if AYIIN49:
        try:
            await AYIIN49.start()
            clients.append(49)
            AYIIN49.me = await AYIIN49.get_me()
            #AYIIN49.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN49 in {AYIIN49.me.first_name} | [ {AYIIN49.me.id} ]"
            )
            client_id.append(AYIIN49.me.id)
        except Exception:
            pass
    if AYIIN50:
        try:
            await AYIIN50.start()
            clients.append(50)
            AYIIN50.me = await AYIIN50.get_me()
            #AYIIN50.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN50 in {AYIIN50.me.first_name} | [ {AYIIN50.me.id} ]"
            )
            client_id.append(AYIIN50.me.id)
        except Exception:
            pass
    logs.info(
        f"Connect On [ {HOSTED_ON} ]\n"
    )
