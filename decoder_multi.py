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
from zipfile import ZipFile
import os
import threading
import tempfile

from multiprocessing.pool import ThreadPool


# Конвертировать изображение и получить данные
def extract_data(file):
    eps_image = Image.open(file)
    eps_image.load(scale=10)
    tmp_file = BytesIO()
    eps_image.save(tmp_file, format("png"))
    tmp_file.seek(0)
    data = decode(Image.open(tmp_file))
    return data[0].data.decode("utf-8")


def extract_zip(input_zip):
    """Extract zip to RAM memory and return eps files list"""
    input_zip = ZipFile(input_zip)

    # List eps files from zip
    zip_files_list = []

    for name in input_zip.namelist():
        if is_file_extension(name):
            zip_files_list.append(input_zip.read(name))
    return zip_files_list


def is_file_extension(file_name, extension=".eps"):
    """Check if file extension *.eps or other if set"""
    filename, file_extension = os.path.splitext(file_name)
    return file_extension.lower() == extension


def save_data(file, out_file, counter):
    global threadLock

    if is_file_extension(file):
        code_data = extract_data(file)

    threadLock.acquire()
    counter[0] -= 1
    print("    Осталось:", counter[0], "Обработан:", get_file_name(file))
    out_file.write(code_data + "\n")
    threadLock.release()


def find_eps_files(path_to_folder):
    files_list = []

    for file in os.listdir(path_to_folder):
        if is_file_extension(file):
            files_list.append(os.path.join(path_to_folder,file))
    return files_list


def find_files_folder(path):
    """
    Find files and folder that will be user to extract data
    :param path: path to filder where stored files to extract
    :return: list with full path to file or folder
    """
    temp_list = []
    for file in os.listdir(path):
        full_path = os.path.join(path, file)

        if os.path.isdir(full_path):
            temp_list.append(full_path)
        else:
            if os.path.isfile(full_path) and is_file_extension(file, ".zip"):
                temp_list.append(os.path.join(full_path))

    # Also search eps files in root folder
    temp_list.append(path)

    return temp_list


def create_pool(files_list, output_file_path):
    """
    files_list - full path to file
    output_file - file where save extracted data

    """

    # Add extention to file
    output_file_path += ".txt"

    # Check file if it exist remove it
    if os.path.isfile(output_file_path):
        os.remove(output_file_path)

    with open(output_file_path, 'a+') as out_file:

        print("Переходим к", get_file_name(path))

        pool = ThreadPool(processes=8)
        files_count = [len(files_list)]

        for file in files_list:
            pool.apply_async(save_data, args=(file, out_file, files_count))
        pool.close()
        pool.join()

def get_file_name(path):
    return os.path.basename(os.path.normpath(path))

if __name__ == '__main__':

    threadLock = threading.Lock()

    # Путь до текущей дериктории
    path = os.path.dirname(__file__)

    # Создать папки для файлов, если они отсуствуют
    for folder in ('input', 'output'):
        if not os.path.isdir(folder):
            os.mkdir(folder)
            print("Папки input и output созданы. Добавьте файлы eps со штрихкодами в папку input и перезапустите скрипт.")

    # Путь до папки с eps штрихкодами
    pathin = os.path.join(path, 'input')
    pathout = os.path.join(path, 'output')

    start_time = datetime.now()

    # Contains files or folder to extract data
    file_folder_list = find_files_folder(pathin)

    for path in file_folder_list:

        if os.path.isdir(path):
            input_files = find_eps_files(path)
            create_pool(input_files, os.path.join(pathout, get_file_name(path)))

        if os.path.isfile(path):
            # Create temp dir to extract .zip
            with tempfile.TemporaryDirectory() as tmpdirname:
                with ZipFile(path, 'r') as zipObj:
                    zipObj.extractall(tmpdirname)
                    input_files = find_eps_files(tmpdirname)
                    create_pool(input_files, os.path.join(pathout, get_file_name(path)))

    print("Завершено за", datetime.now() - start_time)
