from django.contrib import admin

from main.models import (
    Form,
    Contact,
    Button,
    Specialisation,
    UserMessage,
    BotConfiguration,
    BotMessage
)
from django import forms
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


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


@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ("name", "role")


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("name", "file")


admin.site.register(Specialisation)
admin.site.register(UserMessage)
admin.site.register(BotConfiguration)
admin.site.register(BotMessage)
