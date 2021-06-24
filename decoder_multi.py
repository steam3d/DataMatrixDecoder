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
import threading
from multiprocessing.pool import ThreadPool


# Конвертировать изображение и получить данные
def extract_data(file):
    eps_image = Image.open(os.path.join(pathin, file))
    eps_image.load(scale=10)
    tmp_file = BytesIO()
    eps_image.save(tmp_file, format("png"))
    tmp_file.seek(0)
    data = decode(Image.open(tmp_file))
    return data[0].data.decode("utf-8")


def save_data(file):
    global file_counter
    code_data = extract_data(file)
    threadLock.acquire()
    file_counter -= 1
    print("Осталось:", file_counter, "Обработан:", file)
    file_object.write(code_data + "\n")
    threadLock.release()


def find_eps_files(files):
    files_list = []
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".eps":
            files_list.append(file)
    return files_list


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

    start_time = datetime.now()

    # Получить список файлов
    files = find_eps_files(os.listdir(os.path.join(path, 'input')))

    # Должен быть хотя бы 1 файл для работы
    if len(files) >= 1:
        file_counter = len(files)
        threadLock = threading.Lock()
        pool = ThreadPool(processes=8)
        results = pool.map_async(save_data, files)
        results.get()
    else:
        print("Файлы eps в папке input не найдены.")

    file_object.close()
    print("Завершено за", datetime.now() - start_time)
