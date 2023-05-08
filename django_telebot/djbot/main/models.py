from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import datetime


def validate_superusers(value):
    User = get_user_model()
    if User.objects.filter(is_superuser=True).count() > 1:
        raise ValidationError(
            'Был создан новый пользователь, хотя этого не должно быть. Необходимо срочно связаться с администратором проекта. Возможна угроза безопасности.')


class User(AbstractUser):
    validators = [validate_superusers]

    def save(self, *args, **kwargs):
        if User.objects.all().count() > 1:
            raise ValidationError(
                'Был создан новый пользователь, хотя этого не должно быть. Необходимо срочно связаться с администратором проекта. Возможна угроза безопасности.')
        else:
            super(User, self).save(*args, **kwargs)


class Form(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, verbose_name="Название формы")
    file = models.FileField(
        verbose_name="Файл, который содержит информацию о форме")
    is_entry = models.BooleanField(verbose_name="Является ли файл стартовым?")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Форма 🧥"
        verbose_name_plural = "Форма 🧥"


class Contact(models.Model):
    name = models.TextField(
        verbose_name="Как обращаться? Можно указать дополнительную информацию", max_length=255)
    phone_number = PhoneNumberField(
        verbose_name="Номер телефона", help_text="Формат телефона +79123456789")

    def __str__(self):
        return f"{self.name}: {self.phone_number}"

    class Meta:
        verbose_name = "Контакт 🗒️"
        verbose_name_plural = "Контакты 🗒️"


button_choices = [
    ("Домой", "Домой"),
    ("Информация", "Информация"),
    ("Вопрос", "Вопрос"),
    ("Контакты", "Контакты"),
    ('Назад', 'Назад'),
    ('Остановить диалог', 'Остановить диалог'),
    ("Форма", "Форма"),
    ("Специальности", "Специальности")
]


class Button(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    name = models.CharField(max_length=255, verbose_name="Текст кнопки",
                            help_text="Текст кнопки, который будет отображаться в самом телеграм боте")
    role = models.CharField(choices=button_choices,
                            verbose_name="Роль кнопки",
                            max_length=50)

    def __str__(self):
        return f"Кнопка '{self.name}' с ролью {self.role}"

    class Meta:
        verbose_name = "Кнопка 🔘"
        verbose_name_plural = "Кнопки 🔘"


class Specialisation(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(
        max_length=255, verbose_name="Название специальности")
    file = models.FileField(
        verbose_name="Файл, который содержит информацию о специальности")
    is_entry = models.BooleanField(verbose_name="Является ли файл стартовым?")

    class Meta:
        verbose_name = "Специальность 🌐"
        verbose_name_plural = "Специальности 🌐"

    def __str__(self):
        return f"Специальность: {self.name}"


message_choices = (
    ('Привет', "Привет"),
    ("Вернуться домой", "Вернуться домой"),
    ("О чем рассказать", "О чем рассказать"),
    ("Как звучит вопрос", "Как звучит вопрос"),
    ("Остановка диалога", "Остановка диалога"),
    ("Переотправка сообщения специалисту", "Переотправка сообщения специалисту"),
    ("Доступные контакты", "Доступные контакты"),
    ("Нет контактов", "Нет контактов"),
    ("Доступная информация о специальностях",
     "Доступная информация о специальностях"),
    ("Доступная информация о форме", "Доступная информация о форме"),
    ("Сообщение отправителя", "Сообщение отправителя"),
    ("Сообщение специалиста", "Сообщение специалиста")
)


class BotMessage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.TextField(
        max_length=1000, verbose_name="Содержимое сообщения")
    role = models.CharField(choices=message_choices,
                            max_length=200, verbose_name="Роль сообщения")

    class Meta:
        verbose_name = "Сообщение бота 🤖"
        verbose_name_plural = "Сообщения бота 🤖"

    def __str__(self):
        return f"Сообщение {self.name}"


class UserMessage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    date_timestamp = models.BigIntegerField(
        verbose_name="Дата сообщения в виде timestamp")
    username = models.CharField(
        max_length=255, verbose_name="Имя пользователя в телеграме @Test123")
    content = models.TextField(
        max_length=5000, verbose_name="Содержимое сообщения")
    date = models.CharField(
        max_length=1000, verbose_name="Дата в нормальном виде", editable=False, blank=True, null=True)
    user_id = models.CharField(
        max_length=255, verbose_name="Идентификатор пользователя в телеграме")

    def save(self, *args, **kwargs):
        self.date = datetime.fromtimestamp(self.date_timestamp)
        super(UserMessage, self).save(*args, **kwargs)

    def __str__(self):
        return f"Сообщение {self.username}: {self.content}

    class Meta:
        verbose_name = "Пользовательское сообщение 📔"
        verbose_name_plural = "Пользовательские сообщения 📔"


class BotConfiguration(models.Model):
    bot_token = models.TextField(
        max_length=1000,
        verbose_name="Токен для бота")
    admin_chat_id = models.TextField(max_length=50,
                                     verbose_name="Id админ чата для бота",
                                     help_text="Чат бот изначально должен быть добавлен в чат"
                                     )
    is_in_use = models.BooleanField(
        verbose_name="Используется ли данная конфигурация в боте?")

    def __str__(self):
        return f"Конфигурация бота {self.id}"

    class Meta:
        verbose_name = "Конфигурация бота 🤖"
        verbose_name_plural = "Конфигурации бота 🤖"
