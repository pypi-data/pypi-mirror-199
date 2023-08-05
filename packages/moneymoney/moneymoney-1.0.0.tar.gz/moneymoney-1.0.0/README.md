# moneymoney

Money package for Python

[![PyPI](https://img.shields.io/pypi/v/moneymoney)](https://pypi.org/project/moneymoney/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/moneymoney)](https://github.com/w0rmr1d3r/moneymoney/releases)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/moneymoney)
[![PyPi downloads](https://img.shields.io/pypi/dm/moneymoney?label=PyPi%20downloads)](https://pypistats.org/packages/moneymoney)

## Installation

```bash
pip install moneymoney
```

## Usage

```python
from moneymoney.currency_codes import CurrencyCodes
from moneymoney.money import Money

# using a string as currency code
quantity = Money(amount=1000, currency_code="EUR")

# using currency codes from this package
quantity_two = Money(amount=1000, currency_code=CurrencyCodes.EUR)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Sponsors

Become a sponsor [here](https://github.com/sponsors/w0rmr1d3r)

## License

[GPLv3](LICENSE)
