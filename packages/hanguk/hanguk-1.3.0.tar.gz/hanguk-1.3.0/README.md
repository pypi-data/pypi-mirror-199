# Revised Romanization of Korean

[![Made with Python](https://img.shields.io/badge/Python->=3.10-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage")
[![Python package](https://github.com/joumaico/hanguk/actions/workflows/python-package.yml/badge.svg)](https://github.com/joumaico/hanguk/actions/workflows/python-package.yml)
[![Upload Python Package](https://github.com/joumaico/hanguk/actions/workflows/python-publish.yml/badge.svg)](https://github.com/joumaico/hanguk/actions/workflows/python-publish.yml)

## Installation

```console
$ pip install hanguk
```

## Modules

### *class* hanguk.Hanguk(s)

#### .read()
↳ Transcribe Korean characters into Latin alphabet.
```powershell
>>> hanguk.Hanguk('나는 TV를 사랑').read()
naneun TVreul sarang
```

#### .stream()
↳ Generate in-memory file object.
```powershell
>>> hanguk.Hanguk('나는 TV를 사랑').stream()
<_io.StringIO object at memory_address>
```

## References
* https://web.archive.org/web/20070916025652/http://www.korea.net/korea/kor_loca.asp?code=A020303
* https://www.korean.go.kr/front_eng/roman/roman_01.do

## Links
* PyPI Releases: https://pypi.org/project/hanguk
* Source Code: https://github.com/joumaico/hanguk
