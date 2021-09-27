<h1 align="center">
  ariadne-django-ext
</h1>

<p align="center">
  <a href="https://github.com/dulmandakh/ariadne-django-ext/">
    <img src="https://img.shields.io/github/workflow/status/dulmandakh/ariadne-django-ext/CI?label=Test&logo=github&style=for-the-badge" alt="ci status">
  </a>
  <a href="https://pypi.org/project/ariadne-django-ext/">
    <img src="https://img.shields.io/pypi/v/ariadne-django-ext?style=for-the-badge" alt="pypi link">
  </a>
  <a href="https://codecov.io/github/dulmandakh/ariadne-django-ext">
    <img src="https://img.shields.io/codecov/c/github/dulmandakh/ariadne-django-ext?logo=codecov&style=for-the-badge" alt="codecov">
  </a>
  <br>
  <a>
    <img src="https://img.shields.io/pypi/pyversions/ariadne-django-ext?logo=python&style=for-the-badge" alt="supported python versions">
  </a>
  <a>
    <img src="https://img.shields.io/pypi/djversions/ariadne-django-ext?logo=django&style=for-the-badge" alt="supported django versions">
  </a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

<p align="center">Custom, simple Django User model with email as username</p>

## Installation

```sh
pip install ariadne-django-ext
```

**cache** decorator will cache a result returned from resolver using Django cache framework. You can it accepts **timeout** and **version** parameters and passed down.

Cache key must be either str or callable. Callable must accept parent, info as argument then return cache key.

```python
from ariadne_django_ext import cache

@cache(key='cache_key')
def resolver(parent, info):
    ...
    return 'result'

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT License](https://choosealicense.com/licenses/mit/)
