'''
Простой сприпт для декодирования .eps файлов содержаших DataMatrix штрихкод.
При первом запуске скрипт создаст необходимые директории.
Затем файлы eps скопируйте в папку input и запустите скрипт
Дождитесь окончания результата. Извлеченные данные находятся в файле output.txt в папке output
'''

from PIL import Image
from pylibdmtx.pylibdmtx import decode
from datetime import datetime
from io import BytesIO
import os

# Конвертировать изображение и получить данные
def extract_data(file):
    eps_image = Image.open(os.path.join(pathin, file))
    eps_image.load(scale=10)
    tmp_file = BytesIO()
    eps_image.save(tmp_file, format("png"))
    tmp_file.seek(0)
    data = decode(Image.open(tmp_file))
    return data[0].data.decode("utf-8")


if __name__ == '__main__':

    # Путь до текущей дериктории
    path = os.path.dirname(__file__)

    # Создать папки для файлов, если они отсуствуют
    for folder in ('input', 'output'):
        if not os.path.isdir(folder):
            os.mkdir(folder)
            print("Папки input и output созданы. Добавьте файлы eps со штрихкодами в папку input и перезапустите скрипт.")

    # Путь до папки с eps штрихкодами
    pathin = os.path.join(path, 'input')

    # Путь до файла куда сохранять декодированные данные
    file_object = open(os.path.join(path, 'output', 'output.txt'), 'a+')

    # Добавить переход на новую строку, если файл не пуст
    file_object.seek(0)
    file_data = file_object.read(100)
    if len(file_data) > 0:
        file_object.write("\n")

    file_counter = 0
    start_time = datetime.now()

    # Получить список файлов
    files = os.listdir(os.path.join(path, 'input'))

    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".eps":
            file_counter += 1
            print('({0} / {1}) Декодируем: {2}'.format(file_counter, len(files), os.path.basename(file)))
            code_data = extract_data(file)
            file_object.write(code_data + "\n")

    file_object.close()
    print("Завершено за", datetime.now() - start_time)