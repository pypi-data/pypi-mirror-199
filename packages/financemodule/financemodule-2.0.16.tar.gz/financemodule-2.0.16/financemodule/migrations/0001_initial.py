from django.db import migrations, models
import django.db.models.deletion
from django.core.management import call_command




def create_fixtures(apps, schema_editor):
    call_command('loaddata', 'fixtures.json')  

class Migration(migrations.Migration):

    initial = True
    dependencies = [
    ]
    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=10)),
                ('days_in_year', models.IntegerField(blank=True, null=True)),
                ('rounding_units', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finance_date', models.DateTimeField(auto_now_add=True)),
                ('finance_request_id', models.IntegerField(blank=True, null=True)),
                ('program_type', models.CharField(blank=True, max_length=255, null=True)),
                ('anchor_party', models.IntegerField(blank=True, null=True)),
                ('counterparty', models.IntegerField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('loan_account', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_currency', models.CharField(blank=True, max_length=255, null=True)),
                ('invoice_amount', models.IntegerField(blank=True, null=True)),
                ('finance_currency', models.CharField(blank=True, max_length=255, null=True)),
                ('finance_amount', models.IntegerField(blank=True, null=True)),
                ('settlement_currency', models.CharField(blank=True, max_length=255, null=True)),
                ('settlement_amount', models.IntegerField(blank=True, null=True)),
                ('repayment_currency', models.CharField(blank=True, max_length=255, null=True)),
                ('repayment_account', models.CharField(blank=True, max_length=255, null=True)),
                ('interest_type', models.CharField(blank=True, max_length=255, null=True)),
                ('interest_rate_type', models.CharField(blank=True, max_length=255, null=True)),
                ('margin', models.FloatField(blank=True, null=True)),
                ('interest_rate', models.FloatField(blank=True, null=True)),
                ('interest_amount', models.IntegerField(blank=True, null=True)),
                ('interest_paid_by', models.CharField(blank=True, max_length=255, null=True)),
                ('own_party_account_info', models.JSONField(blank=True, null=True)),
                ('remittance_info', models.JSONField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loanaccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_entity', models.CharField(blank=True, max_length=255, null=True)),
                ('customer', models.CharField(blank=True, max_length=255, null=True)),
                ('program_type', models.CharField(blank=True, max_length=255, null=True)),
                ('account', models.CharField(blank=True, max_length=255, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financemodule.currency')),
            ],
        ),
        migrations.CreateModel(
            name='Interestaccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_entity', models.CharField(blank=True, max_length=255, null=True)),
                ('program_type', models.CharField(blank=True, max_length=255, null=True)),
                ('account', models.CharField(blank=True, max_length=255, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financemodule.currency')),
            ],
        ),
        migrations.CreateModel(
            name='FloatingInterestRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_entity', models.CharField(blank=True, max_length=255, null=True)),
                ('rate_date', models.DateField(blank=True, null=True)),
                ('interest_rate_type', models.CharField(blank=True, choices=[('LIBOR', 'LIBOR'), ('EURIBOR', 'EURIBOR'), ('SOFR', 'SOFR')], max_length=255, null=True)),
                ('period', models.JSONField(blank=True, null=True)),
                ('currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='floating_currency', to='financemodule.currency')),
            ],
        ),
        migrations.CreateModel(
            name='FinanceAccounting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_ref', models.CharField(blank=True, max_length=155, null=True)),
                ('stage', models.CharField(blank=True, max_length=155, null=True)),
                ('type', models.CharField(blank=True, max_length=155, null=True)),
                ('currency', models.CharField(blank=True, max_length=155, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('account', models.CharField(blank=True, max_length=255, null=True)),
                ('interest_paid_by', models.CharField(blank=True, max_length=255, null=True)),
                ('account_type', models.CharField(blank=True, max_length=155, null=True)),
                ('base_currency', models.CharField(blank=True, max_length=155, null=True)),
                ('base_currency_amount', models.IntegerField(blank=True, null=True)),
                ('exch_rate', models.FloatField(blank=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('finance_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finance_account', to='financemodule.finance')),
            ],
        ),
        migrations.CreateModel(
            name='Exchangerate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_entity', models.IntegerField(blank=True, null=True)),
                ('rate_base_currency', models.CharField(blank=True, max_length=255, null=True)),
                ('rate_date', models.DateField(blank=True, null=True)),
                ('rate_previous_day', models.DateField(blank=True, null=True)),
                ('rate_buy', models.FloatField(blank=True, null=True)),
                ('rate_sell', models.FloatField(blank=True, null=True)),
                ('rate_mid', models.FloatField(blank=True, null=True)),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('rate_currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financemodule.currency')),
            ],
        ),
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('base_currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financemodule.currency')),
            ],
        ),
        migrations.RunPython(create_fixtures),
    ]
    