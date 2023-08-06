from telegram import (
    ForceReply,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    ext,
)

Context = ext.ContextTypes.DEFAULT_TYPE
PTBHandler = ext.BaseHandler[Update, Context]  # type: ignore[misc]
KeyboardMarkup = ReplyKeyboardMarkup | InlineKeyboardMarkup
ReplyMarkup = KeyboardMarkup | ReplyKeyboardRemove | ForceReply
