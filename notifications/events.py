from .providers.telegram import Telegram
from .providers.twitter import Twitter

EVENT_NEW_JOB = "new_job"

EVENTS = {
    EVENT_NEW_JOB: (Twitter.code, Telegram.code),
}
