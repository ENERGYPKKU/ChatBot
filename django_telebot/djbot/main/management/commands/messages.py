from main.models import BotMessage

try:
    hello_msg = BotMessage.objects.get(role="Привет").name
except BotMessage.DoesNotExist:
    hello_msg = "Привет я - Подручник, телеграм бот ПК Энергии"

try:
    go_home_msg = BotMessage.objects.get(role="Вернуться домой").name
except BotMessage.DoesNotExist:
    go_home_msg = "Вернулись домой 🏚️"

try:
    what_tell_about_msg = BotMessage.objects.get(role="О чем рассказать").name
except BotMessage.DoesNotExist:
    what_tell_about_msg = "О чем мне рассказать? 🤗"

try:
    question_get_msg = BotMessage.objects.get(role="Как звучит вопрос").name
except BotMessage.DoesNotExist:
    question_get_msg = "Как звучит вопрос? 🤔"

try:
    stop_dialog_msg = BotMessage.objects.get(role="Остановка диалога").name
except BotMessage.DoesNotExist:
    stop_dialog_msg = "Диалог был остановлен 🛑"

try:
    send_message_to_specialist_msg = BotMessage.objects.get(
        role="Переотправка сообщения специалисту").name
except BotMessage.DoesNotExist:
    send_message_to_specialist_msg = "Сообщение было перенаправлено специалисту 🖊️"

try:
    available_contacts_msg = BotMessage.objects.get(
        role="Доступные контакты").name
except BotMessage.DoesNotExist:
    available_contacts_msg = "Доступные контакты ☎️"

try:
    no_contacts_msg = BotMessage.objects.get(role="Нет контактов").name
except BotMessage.DoesNotExist:
    no_contacts_msg = "На данный момент нет доступных контактов 😅"

try:
    available_info_about_spec_msg = BotMessage.objects.get(
        role="Доступная информация о специальностях").name
except BotMessage.DoesNotExist:
    available_info_about_spec_msg = "Вот вся доступная информация о специальностях 🌐"

try:
    available_info_about_form_msg = BotMessage.objects.get(
        role="Доступная информация о форме").name
except BotMessage.DoesNotExist:
    available_info_about_form_msg = "Вот вся доступная информация о форме для разных специальностей 🧥"

try:
    user_request_msg = BotMessage.objects.get(
        role="Сообщение отправителя").name
except BotMessage.DoesNotExist:
    user_request_msg = "Сообщение отправителя ❓"

try:
    specialist_response_msg = BotMessage.objects.get(
        role="Сообщение специалиста").name
except BotMessage.DoesNotExist:
    specialist_response_msg = "Сообщение специалиста 🖊️"
