from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


def validate_superusers(value):
    User = get_user_model()
    if User.objects.filter(is_superuser=True).count() > 1:
        raise ValidationError('There can be only one superuser.')


class User(AbstractUser):
    validators = [validate_superusers]

    def save(self, *args, **kwargs):
        if User.objects.all().count() == 1:
            raise ValidationError('There can be only one superuser.')
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
