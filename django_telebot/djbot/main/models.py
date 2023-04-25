from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class Game(models.Model):
    gamename = models.TextField(
        verbose_name="Название игры",
    )

    def __str__(self):
        return f"{self.gamename}"

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"


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
