from enum import Enum
from django.db.models import TextChoices
from django.utils.translation import ugettext_lazy as _



class ExchangeRateCurrency(Enum):
    SGD = "SGD"
    HKD = "HKD"
    CNY = "CNY"
    AED = "AED"
    EUR = "EUR"
    USD = "USD"
 





class ExchangeMidrate(Enum):
    SGD_RATE = 0.016
    HKD_RATE = 0.095
    CNY_RATE = 0.083
    AED_RATE = 0.045
    EUR_RATE = 0.011
    USD_RATE = 0.012


class StatusChoices(Enum):
    FINANCED = "FINANCED"
    PARTIALLY_SETTLED = "PARTIALLY SETTLED"
    SETTLED = "SETTLED"


class UserTypeChoices(TextChoices):
    CUSTOMER = 'CUSTOMER', _('CUSTOMER')
    NON_CUSTOMER = 'NON_CUSTOMER',_('NON_CUSTOMER')
    INTERNAL = 'INTERNAL',_('INTERNAL')


class AccountTypeChoice(TextChoices):
    DEBIT = 'D', _('D')
    CREDIT = 'C',_('C')



class ModelTypeChoices(TextChoices):
    FINANCING = 'FINANCING', _('FINANCING')
    REPAYMENT = 'REPAYMENT',_('REPAYMENT')


class InterestTypeChoices(TextChoices):
    FIXED = 'FIXED', _('FIXED')
    FLOATING = 'FLOATING',_('FLOATING')


class InterestRateTypeChoices(TextChoices):
    LIBOR = 'LIBOR', _('LIBOR')
    EURIBOR = 'EURIBOR',_('EURIBOR')
    SOFR = 'SOFR',_('SOFR')



class ProgramTypeChoices(TextChoices):
    APF = 'APF',_('APF')
    RF = 'RF',_('RF')
    DF = 'DF',_('DF')



class InterestPaidByChoices(TextChoices):
    OWNPARTY = 'OWNPARTY', _('OWNPARTY')
    COUNTERPARTY = 'COUNTERPARTY',_('COUNTERPARTY')


