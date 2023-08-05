from django.contrib import admin
from .models import Finance , FinanceAccounting , Exchangerate , Interestaccount , Loanaccount , FinanceAccounting , FloatingInterestRate , Currency

from django import forms


# class AuthorForm(forms.ModelForm):

#     def __init__(self, *args, **kwargs):
#         print("My custom admin Form")
#         super().__init__(*args, **kwargs)

#     class Meta:
#         fields = ('currency', 'period')


# class AuthorAdmin(admin.ModelAdmin):
#     form = AuthorForm



# Register your models here.
admin.site.register(Finance)
admin.site.register(FinanceAccounting)
admin.site.register(Exchangerate)
admin.site.register(Interestaccount)
admin.site.register(Loanaccount)
admin.site.register(FloatingInterestRate )
admin.site.register(Currency)