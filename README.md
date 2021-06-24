# DataMatrixDecoder
 Decode Data Matrix .eps files

# Необходимый софт

1. [Python 3.7 и выше](https://www.python.org/downloads/)
2. [pylibdmtx](https://pypi.org/project/pylibdmtx/)
3. [ghostscript](https://www.ghostscript.com/download/gsdnld.html)

# Подготовка
Установить Python и выполнить

`pip install pylibdmtx`

Если произошла ошибка связання с PIL:

`pip install Pillow`

# Как использовать
## Обычный вариант
1. Скопировать файл `decoder.py` в любую папку. Двойным нажатием запустить.
2. Скопировать файлы .eps с DataMatrix в папку input
3. Повторно запустить `decoder.py`
4. Дождаться завершения. Файл с извлеченными данные находится в `output/output.txt`

## Через консоль

`python3 decoder.py`