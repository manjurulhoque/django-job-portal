from .base import ProviderBase


class Telegram(ProviderBase):
    code = "telegram"

    def _publish(self, tpl: str):
        pass
