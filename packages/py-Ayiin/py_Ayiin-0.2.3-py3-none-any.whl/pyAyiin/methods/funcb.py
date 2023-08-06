# py - Ayiin
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/pyAyiin >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/pyAyiin/blob/main/LICENSE/>.
#
# FROM py-Ayiin <https://github.com/AyiinXd/pyAyiin>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

from fipper.types import CallbackQuery, Message


class FuncBot(object):
    async def approve_pmpermit(
        self,
        cb,
        user_ids,
        OLD_MSG,
    ):
        from ..dB.pmpermit import approve_pmpermit, is_pmpermit_approved

        
        if isinstance(cb, CallbackQuery):
            if await is_pmpermit_approved(user_ids):
                await cb.answer("Pengguna Ini Sudah Ada Di Database.", show_alert=True)
                return
            await approve_pmpermit(user_ids)
            await cb.edit_message_text("Pesan Anda Diterima Tod")
            if str(user_ids) in OLD_MSG:
                await OLD_MSG[str(user_ids)].delete()
        elif isinstance(cb, Message):
            if await is_pmpermit_approved(user_ids):
                await cb.edit("Pengguna Ini Sudah Ada Di Database.", show_alert=True)
                return
            await approve_pmpermit(user_ids)
            await cb.edit("Pesan Anda Diterima Tod")
            if str(user_ids) in OLD_MSG:
                await OLD_MSG[str(user_ids)].delete()
        
    async def disapprove_pmpermit(
        self,
        cb,
        user_ids,
    ):
        from ..dB.pmpermit import disapprove_pmpermit, is_pmpermit_approved
        
        if isinstance(cb, CallbackQuery):
            if not await is_pmpermit_approved(user_ids):
                return await cb.answer("Pengguna Ini Tidak Ada Di Database")
            await disapprove_pmpermit(user_ids)
            await cb.edit_message_text("Pesan Anda Ditolak Tod")
        elif isinstance(cb, Message):
            if not await is_pmpermit_approved(user_ids):
                return await cb.edit("Pengguna Ini Tidak Ada Di Database")
            await disapprove_pmpermit(user_ids)
            await cb.edit("Pesan Anda Ditolak Tod")
