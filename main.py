import requests
import json
from urllib.parse import quote

CATAAS_URL = "https://cataas.com/cat"  
YANDEX_BASE_URL = "https://cloud-api.yandex.net/v1/disk"


from urllib.parse import quote  

def get_cat_image_bytes(text: str) -> bytes:
    encoded_text = quote(text)
    url = f"https://cataas.com/cat/says/{encoded_text}"
    
    print(f"Запрос к cataas: {url}")  
    
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def create_folder_on_yandex(token: str, folder_name: str) -> None:
    url = f"{YANDEX_BASE_URL}/resources"
    headers = {
        "Authorization": f"OAuth {token}"
    }
    params = {
        "path": folder_name
    }
    response = requests.put(url, headers=headers, params=params)
    if response.status_code not in (201, 409):
        print("Не удалось создать папку на Яндекс.Диске")
        print("Статус:", response.status_code, response.text)


def get_upload_url(token: str, disk_path: str) -> str:
    url = f"{YANDEX_BASE_URL}/resources/upload"
    headers = {
        "Authorization": f"OAuth {token}"
    }
    params = {
        "path": disk_path,
        "overwrite": "true"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data["href"]


def upload_file_by_url(upload_url: str, file_bytes: bytes) -> None:
    response = requests.put(upload_url, data=file_bytes)
    response.raise_for_status()


def get_file_info(token: str, disk_path: str) -> dict:
    url = f"{YANDEX_BASE_URL}/resources"
    headers = {
        "Authorization": f"OAuth {token}"
    }
    params = {
        "path": disk_path
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    info = {
        "name": data.get("name"),
        "path": data.get("path"),
        "size": data.get("size")
    }
    return info


def save_result_to_json(info: dict, filename: str = "result.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)


def main():
    text_for_cat = input("Введите текст для картинки: ")
    yandex_token = input("Введите токен Яндекс.Диска: ")

    folder_name = "py-fpy-140"

    file_name = text_for_cat + ".jpg"
    disk_path = f"{folder_name}/{file_name}"

    print("Получаем котика ...")
    cat_bytes = get_cat_image_bytes(text_for_cat)

    print("Создаём папку на Яндекс.Диске (если её ещё нет)...")
    create_folder_on_yandex(yandex_token, folder_name)


    print("Получаем ссылку для загрузки файла...")
    upload_url = get_upload_url(yandex_token, disk_path)

 
    print("Загружаем файл на Яндекс.Диск...")
    upload_file_by_url(upload_url, cat_bytes)
    print("Файл загружен!")


    print("Получаем информацию о файле...")
    file_info = get_file_info(yandex_token, disk_path)

    print("Сохраняем информацию в result.json...")
    save_result_to_json(file_info)

    print("Готово! Проверяйте папку py-fpy-140 на Яндекс.Диске и файл result.json рядом с программой.")


if __name__ == "__main__":
    main()