import asyncio
import aiofiles
import shutil
from pathlib import Path
import argparse
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


parser = argparse.ArgumentParser(description="Асинхронне сортування файлів за розширеннями")
parser.add_argument("source_folder", type=str, help="Шлях до вихідної папки")
parser.add_argument("output_folder", type=str, help="Шлях до папки призначення")
args = parser.parse_args()


source_path = Path(args.source_folder)
output_path = Path(args.output_folder)


async def read_folder(folder):
    for entry in folder.iterdir():
        if entry.is_dir():
            await read_folder(entry)
        elif entry.is_file():
            await copy_file(entry)

async def copy_file(file_path):
    try:
        ext = file_path.suffix[1:]  # отримуємо розширення файлу без точки
        target_folder = output_path / ext
        target_folder.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(file_path, 'rb') as src_file:
            async with aiofiles.open(target_folder / file_path.name, 'wb') as dst_file:
                while chunk := await src_file.read(1024):
                    await dst_file.write(chunk)
        logging.info(f"Файл {file_path} скопійовано до {target_folder}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні файлу {file_path}: {e}")



if __name__ == "__main__":
    if not source_path.exists():
        logging.error(f"Вихідна папка {source_path} не існує.")
    elif not output_path.exists():
        logging.error(f"Папка призначення {output_path} не існує.")
    else:
        asyncio.run(read_folder(source_path))



python script.py /шлях/до/вихідної/папки /шлях/до/цільової/папки
