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


class UserProfile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name="Внешний ID пользователя",
        unique=True,
    )
    name = models.TextField(
        null=True,
        verbose_name="Имя пользователя",
    )
    main_game = models.TextField(
        null=True,
        verbose_name="Основная игра",
    )
    steam_nickname = models.TextField(
        null=True,
        verbose_name="Никнейм в Steam",
    )
    about = models.TextField(
        null=True,
        verbose_name="О пользователе",
    )

    in_search = models.BooleanField(
        null=True,
        verbose_name="Статус в поиске",
    )

    def __str__(self):
        return f"#{self.external_id} {self.name}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Message(models.Model):
    profile = models.ForeignKey(
        to="main.UserProfile",
        verbose_name="Профиль",
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    created_at = models.DateTimeField(
        verbose_name="Время получения",
        auto_now_add=True,
    )

    def __str__(self):
        return f"Сообщение {self.pk} от {self.profile}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Form(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, verbose_name="Название формы")
    file = models.FileField(verbose_name="Файл, который содержит форму")

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
    ("Контакты", "Контакты")
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

    class Meta:
        verbose_name = "Кнопка 🔘"
        verbose_name_plural = "Кнопки 🔘"


class Specialization(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    name = models.CharField(
        max_length=255, verbose_name="Название специальности")
    study_date = models.CharField(
        max_length=255, verbose_name="Время обучения")
    study_objects = models.ManyToManyField("StudyObject")
    description = models.CharField(
        max_length=1024, verbose_name="Описание специальности")

    class Meta:
        verbose_name = "Специальность 🌐"
        verbose_name_plural = "Специальности 🌐"


class StudyObject(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    name = models.CharField(
        max_length=255, verbose_name="Название специальности")
    code = models.CharField(
        max_length=255, verbose_name="Код предмета", blank=True)

    class Meta:
        verbose_name = "Предмет специальности 🌐"
        verbose_name_plural = "Предметы специальности 🌐"


class UserMessage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    date_timestamp = models.BigIntegerField(
        editable=False, verbose_name="Дата сообщения в виде timestamp")
    username = models.CharField(
        max_length=255, verbose_name="Имя пользователя в телеграме @Test123")
    content = models.CharField(
        max_length=5000, verbose_name="Содержимое сообщения")
    date = models.CharField(
        max_length=1000, verbose_name="Дата в нормальном виде", editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.date = datetime.fromtimestamp(self.date_timestamp)
        super(UserMessage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользовательское сообщение 📔"
        verbose_name_plural = "Пользовательские сообщения 📔"


class BotConfiguration(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    bot_token = models.CharField(
        max_length=1000,
        verbose_name="Токен для бота")
    admin_chat_id = models.TextField(max_length=50,
                                     verbose_name="Id админ чата для бота",
                                     help_text="Чат бот изначально должен быть добавлен в чат"
                                     )
    is_in_use = models.BooleanField(
        verbose_name="Используется ли данная конфигурация в боте?")

    class Meta:
        verbose_name = "Конфигурация бота 🤖"
        verbose_name_plural = "Конфигурации бота 🤖"
