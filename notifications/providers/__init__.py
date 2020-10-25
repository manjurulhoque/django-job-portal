from .telegram import Telegram
from .twitter import Twitter

PROVIDERS = {
    Telegram.code: Telegram,
    Twitter.code: Twitter,
}
