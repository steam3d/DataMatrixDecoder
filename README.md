# DataMatrixDecoder
 Decode Data Matrix .eps files

# Необходимый софт

1. [Python 3.7 и выше](https://www.python.org/downloads/)
2. [pylibdmtx](https://pypi.org/project/pylibdmtx/) 
   >Установка через консоль после установки Python `pip install pylibdmtx`
3. [ghostscript](https://www.ghostscript.com/download/gsdnld.html)
4. Добавить путь до ghostscript `C:\Program Files\gs\gs9.54.0\bin` в `Переменные среды` раздел `Path`. Для пользователя и системы.
# Как использовать
## Обычный вариант
1. Скопировать файл `decoder.py` в любую папку. Двойным нажатием запустить.
2. Скопировать файлы .eps с DataMatrix в только что созданную папку input
3. Повторно запустить `decoder.py`
4. Дождаться завершения. Файл с извлеченными данные находится в `output/output.txt`

## Через консоль
`cd "путь до папки с decoder.py"`

`python3 decoder.py`

>Если произошла ошибка связання с PIL `pip install Pillow`