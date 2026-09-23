from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from config import (
    MAX_API_BASE_URL,
    MAX_BOT_TOKEN,
    MAX_REQUIRED_CHANNEL_ID,
    MAX_REQUIRED_CHANNEL_URL,
)


class MaxApiError(RuntimeError):
    pass


@dataclass(frozen=True)
class SubscriptionStatus:
    required: bool
    subscribed: bool
    channel_url: str


class MaxBotClient:
    def __init__(self, token: str = MAX_BOT_TOKEN, base_url: str = MAX_API_BASE_URL):
        self.token = token
        self.base_url = base_url.rstrip("/")
        self._bot_id: int | None = None

    async def bot_id(self) -> int:
        if self._bot_id is None:
            bot = await self.request("GET", "/me")
            try:
                self._bot_id = int(bot["user_id"])
            except (KeyError, TypeError, ValueError) as exc:
                raise MaxApiError("MAX API did not return the bot user_id") from exc
        return self._bot_id

    def _request_sync(self, method: str, path: str, *, query=None, payload=None) -> dict:
        if not self.token:
            raise MaxApiError("MAX_BOT_TOKEN is not configured")
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query, doseq=True)}"
        body = json.dumps(payload, ensure_ascii=False).encode() if payload is not None else None
        request = Request(
            url,
            data=body,
            method=method,
            headers={
                "Authorization": self.token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        try:
            with urlopen(request, timeout=15) as response:
                raw = response.read()
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:500]
            raise MaxApiError(f"MAX API returned {exc.code}: {detail}") from exc
        except (URLError, TimeoutError) as exc:
            raise MaxApiError(f"MAX API is unavailable: {exc}") from exc
        return json.loads(raw) if raw else {}

    async def request(self, method: str, path: str, *, query=None, payload=None) -> dict:
        return await asyncio.to_thread(
            self._request_sync, method, path, query=query, payload=payload
        )

    async def send_message(self, user_id: int, text: str, *, button=None) -> dict:
        payload: dict = {"text": text[:4000], "notify": True}
        if button:
            if button.get("type") == "open_app":
                # MAX opens the bot's configured Mini App and supplies signed
                # WebAppData. A link button opens a regular browser tab.
                action = {
                    "type": "open_app",
                    "text": button["text"],
                    "contact_id": await self.bot_id(),
                    "payload": button.get("payload", ""),
                }
            else:
                action = {
                    "type": "link",
                    "text": button["text"],
                    "url": button["url"],
                }
            payload["attachments"] = [{
                "type": "inline_keyboard",
                "payload": {"buttons": [[action]]},
            }]
        return await self.request(
            "POST", "/messages", query={"user_id": int(user_id)}, payload=payload
        )

    async def is_channel_member(self, user_id: int) -> bool:
        if not MAX_REQUIRED_CHANNEL_ID:
            return True
        data = await self.request(
            "GET",
            f"/chats/{MAX_REQUIRED_CHANNEL_ID}/members",
            query={"user_ids": [int(user_id)]},
        )
        return any(int(item.get("user_id", 0)) == int(user_id) for item in data.get("members", []))

    async def subscription_status(self, user_id: int) -> SubscriptionStatus:
        required = bool(MAX_REQUIRED_CHANNEL_ID)
        return SubscriptionStatus(
            required=required,
            subscribed=(await self.is_channel_member(user_id)) if required else True,
            channel_url=MAX_REQUIRED_CHANNEL_URL,
        )


max_bot = MaxBotClient()
