import asyncio
import logging
from typing import Any
from uuid import uuid4
from datetime import datetime, timezone

import psycopg

from config import config


loger = logging.getLogger(__name__)


class DataForTestsGen:
    """Класс для генерации тестовых данных."""

    @property
    def insert_user(self) -> str:
        return (
            "INSERT INTO public.auth_user "
            "(id, password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

    @property
    def insert_status(self) -> str:
        return (
            "INSERT INTO cash_manager.cash_flow_status "
            "(id, title, alias) "
            "VALUES (%s, %s, %s)"
        )

    @property
    def insert_type(self) -> str:
        return (
            "INSERT INTO cash_manager.cash_flow_type "
            "(id, title, alias) "
            "VALUES (%s, %s, %s)"
        )

    @property
    def insert_subcategory(self) -> str:
        return (
            "INSERT INTO cash_manager.cash_flow_subcategory "
            "(id, title, alias) "
            "VALUES (%s, %s, %s)"
        )

    @property
    def insert_category(self) -> str:
        return (
            "INSERT INTO cash_manager.cash_flow_category "
            "(id, title, alias) "
            "VALUES (%s, %s, %s)"
        )

    @property
    def insert_category_by_type(self) -> str:
        return (
            "INSERT INTO cash_manager.cash_flow_category_by_type "
            "(id, category_id, type_id) "
            "VALUES (%s, %s, %s)"
        )

    @property
    def insert_category_by_subcategory(self) -> str:
        return (
            "INSERT INTO cash_manager.cash_flow_category_by_subcategory "
            "(id, category_id, subcategory_id) "
            "VALUES (%s, %s, %s)"
        )

    @staticmethod
    def gen_data() -> dict[str, dict[str, Any]]:
        subcategory = {
            "vps": {"id": str(uuid4()), "ru": "ВПС"},
            "proxy": {"id": str(uuid4()), "ru": "Прокси"},
            "farpost": {"id": str(uuid4()), "ru": "Фарпост"},
            "avito": {"id": str(uuid4()), "ru": "Авито"},
        }
        category = {
            "marketing": {
                "id": str(uuid4()),
                "ru": "Маркетинг",
            },
            "infrastructure": {
                "id": str(uuid4()),
                "ru": "Инфраструктура",
            },
        }
        types = {
            "replenishment": {
                "id": str(uuid4()),
                "ru": "Пополнение",
            },
            "write_off": {
                "id": str(uuid4()),
                "ru": "Списание",
            },
        }

        return {
            "user": {
                "id": 1,
                "password": "pbkdf2_sha256$1000000$I3LHT9frvDavKqeKGYrwcT$ykEI0fQT7WhkWxhrbGecxSPM3eHcrzqgYkWsvmmtssM=",
                "is_superuser": True,
                "username": "admin",
                "first_name": "test",
                "last_name": "test",
                "email": "test@gmail.com",
                "is_staff": True,
                "is_active": True,
                "date_joined": datetime.now(timezone.utc).isoformat(),
            },
            "statuses": {
                "business": {"id": str(uuid4()), "ru": "Бизнес"},
                "self": {"id": str(uuid4()), "ru": "Личное"},
                "tax": {"id": str(uuid4()), "ru": "Налог"},
            },
            "types": types,
            "subcategory": subcategory,
            "category": category,
            "category_by_type": {
                str(uuid4()): {
                    "category_id": category["marketing"]["id"],
                    "type_id": types["write_off"]["id"],
                },
                str(uuid4()): {
                    "category_id": category["infrastructure"]["id"],
                    "type_id": types["replenishment"]["id"],
                },
            },
            "category_by_subcategory": {
                str(uuid4()): {
                    "category_id": category["marketing"]["id"],
                    "subcategory_id": subcategory["farpost"]["id"]
                },
                str(uuid4()): {
                    "category_id": category["marketing"]["id"],
                    "subcategory_id": subcategory["avito"]["id"],
                },
                str(uuid4()): {
                    "category_id": category["infrastructure"]["id"],
                    "subcategory_id": subcategory["vps"]["id"],
                },
                str(uuid4()): {
                    "category_id": category["infrastructure"]["id"],
                    "subcategory_id": subcategory["proxy"]["id"],
                },
            },
        }

    async def gen(self) -> None:
        async with await psycopg.AsyncConnection.connect(
            config.pg_url_connection
        ) as pg_connect:
            try:
                async with pg_connect.cursor() as cursor:
                    data = self.gen_data()
                    await self._insert_user_data(cursor, data)
                    await self._insert_status_data(cursor, data)
                    await self._insert_type_data(cursor, data)
                    await self._insert_subcategory_data(cursor, data)
                    await self._insert_category_data(cursor, data)

                    await pg_connect.commit()

                    await self._insert_category_by_type_data(cursor, data)
                    await self._insert_category_by_subcategory_data(
                        cursor,
                        data,
                    )

                await pg_connect.commit()

            except Exception as ex:
                loger.error(f"Error gen test data: {ex}")

    loger.info("All test data was gen")

    async def _insert_user_data(self, cursor, data) -> None:
        user_data = data["user"]
        await cursor.execute(
            self.insert_user,
            (
                user_data["id"],
                user_data["password"],
                user_data["is_superuser"],
                user_data["username"],
                user_data["first_name"],
                user_data["last_name"],
                user_data["email"],
                user_data["is_staff"],
                user_data["is_active"],
                user_data["date_joined"],
            ),
        )

    async def _insert_status_data(self, cursor, data) -> None:
        for s_name, s_data in data["statuses"].items():
            await cursor.execute(
                self.insert_status,
                (
                    s_data["id"],
                    s_data["ru"],
                    s_name,
                ),
            )

    async def _insert_type_data(self, cursor, data) -> None:
        for t_name, t_data in data["types"].items():
            await cursor.execute(
                self.insert_type,
                (
                    t_data["id"],
                    t_data["ru"],
                    t_name,
                ),
            )

    async def _insert_subcategory_data(self, cursor, data) -> None:
        for sc_name, sc_data in data["subcategory"].items():
            await cursor.execute(
                self.insert_subcategory,
                (
                    sc_data["id"],
                    sc_data["ru"],
                    sc_name,
                ),
            )

    async def _insert_category_data(self, cursor, data) -> None:
        for c_name, c_data in data["category"].items():
            await cursor.execute(
                self.insert_category,
                (
                    c_data["id"],
                    c_data["ru"],
                    c_name,
                ),
            )

    async def _insert_category_by_type_data(self, cursor, data) -> None:
        for cbt_id, cbt_data in data["category_by_type"].items():
            await cursor.execute(
                self.insert_category_by_type,
                (
                    cbt_id,
                    cbt_data["category_id"],
                    cbt_data["type_id"],
                ),
            )

    async def _insert_category_by_subcategory_data(self, cursor, data) -> None:
        category_by_subcategories = data["category_by_subcategory"]

        for cbs_id, cbs_data in category_by_subcategories.items():
            await cursor.execute(
                self.insert_category_by_subcategory,
                (
                    cbs_id,
                    cbs_data["category_id"],
                    cbs_data["subcategory_id"],
                ),
            )

if __name__ == "__main__":
    asyncio.run(DataForTestsGen().gen())
