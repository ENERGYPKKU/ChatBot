from django.contrib import admin

from main.forms import ProfileForm
from main.models import Game, Message, UserProfile, Form, Contact
from django import forms
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_id",
        "name",
        "main_game",
        "steam_nickname",
        "about",
        "in_search",
    )
    form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "text", "created_at")


class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'phone_number': PhoneNumberInternationalFallbackWidget(attrs={
                'class': 'form-control'
            })
        }


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactModelForm


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "gamename")


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("name", "file")
