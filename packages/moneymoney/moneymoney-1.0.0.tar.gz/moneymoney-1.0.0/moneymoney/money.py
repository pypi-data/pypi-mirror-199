from moneymoney.currency_codes import CurrencyCodes


class CurrencyCodeIsNoneException(Exception):
    """Exception thrown when CurrencyCode is None."""


class CurrencyIsNotTheSameException(Exception):
    """Exception thrown when currencies are different."""


class OtherIsNotMoneyInstanceException(Exception):
    """Exception thrown when the other compared is not of Money instance."""


class Money:
    """Class representing an amount with a currency.

    Money of different currency cannot operate between them, they need
    to be of the same currency.
    """

    def __init__(self, currency_code: str, amount: float = 0.0):
        if currency_code is None:
            raise CurrencyCodeIsNoneException()
        self._amount = amount
        self._currency_code = currency_code

    @property
    def amount(self) -> float:
        """Property amount of this object."""
        return self._amount

    @property
    def currency_code(self):
        """Property currency_code of this object."""
        return self._currency_code

    @staticmethod
    def __assert_other_is_instance_money(other):
        if not isinstance(other, Money):
            raise OtherIsNotMoneyInstanceException()

    def __assert_currencies_are_the_same(self, other):
        if other.currency_code.lower() != self.currency_code.lower():
            raise CurrencyIsNotTheSameException()

    def __add__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        amount = self.amount + other.amount
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __sub__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        amount = self.amount - other.amount
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __eq__(self, other):
        if isinstance(other, Money):
            return (self._amount == other.amount) and (self._currency_code.lower() == other.currency_code.lower())
        return False

    def __lt__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        return self._amount < other.amount

    def __le__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        return self._amount <= other.amount

    def __gt__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        return self._amount > other.amount

    def __ge__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        return self._amount >= other.amount

    def __str__(self):
        rounded_amount = round(self.amount, 2)
        return f"{rounded_amount}{self.currency_code}"


DEFAULT_MONEY = Money(currency_code=CurrencyCodes.EUR)
