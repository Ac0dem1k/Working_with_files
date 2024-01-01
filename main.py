import operator
import os
import random
from csv import DictReader, DictWriter


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class SmallerThanMin(Exception):
    def __init__(self, txt):
        self.txt = txt


class BiggerThanMax(Exception):
    def __init__(self, txt):
        self.txt = txt


class FileNameLength(Exception):
    def __init__(self, txt):
        self.txt = txt


class WrongFileName(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_new_contact(edit, modifying_contact):
    if edit:
        first_name_old = modifying_contact["Имя"]
        second_name_old = modifying_contact["Отчество"]
        last_name_old = modifying_contact["Фамилия"]
        print("Чтобы сохранить текущее значение, оставьте строку пустой.")
        print("Для определения пустого значения введите один пробел")
        first_name = input(f"Введите имя ({first_name_old}): ")
        second_name = input(f"Введите отчество ({second_name_old}): ")
        last_name = input(f"Введите фамилию ({last_name_old}): ")
        if first_name == " ":
            first_name = ""
        elif first_name == "":
            first_name = first_name_old
        if second_name == " ":
            second_name = ""
        elif second_name == "":
            second_name = second_name_old
        if last_name == " ":
            last_name = ""
        elif last_name == "":
            last_name = last_name_old
    else:
        first_name = input("Введите имя: ")
        second_name = input("Введите отчество: ")
        last_name = input("Введите фамилию: ")
    phone_number = 0
    is_valid_phone = False
    while not is_valid_phone:
        try:
            if edit:
                phone_number_old = modifying_contact["Телефон"]
                phone_number_string = input(f"Введите номер ({str(phone_number_old)}): ")
                if phone_number_string == "":
                    phone_number_string = str(phone_number_old)
                phone_number = int(phone_number_string)
            else:
                phone_number = int(input("Введите номер: "))
            if len(str(phone_number)) != 11:
                raise LenNumberError("Неверная длина номера.")
        except ValueError:
            print("Номер должен состоять только из цифр.")
        except LenNumberError as error:
            print(error)
            continue
        is_valid_phone = True
    return {"Имя": first_name, "Отчество": second_name, "Фамилия": last_name, "Телефон": phone_number}


male_names = ["Иван", "Андрей", "Виталий", "Петр", "Павел", "Григорий"]
male_second_names = ["Иванович", "Андреевич", "Витальевич", "Петрович", "Павлович", "Григорьевич"]
male_last_names = ["Иванов", "Андреев", "Витальев", "Перов", "Павлов", "Григорьев"]

fem_names = ["Анна", "Анастасия", "Валерия", "Ольга", "Екатерина", "Виктория"]
fem_second_names = ["Ивановна", "Андреевна", "Витальевна", "Петровна", "Павловна", "Григорьевна"]
fem_last_names = ["Иванова", "Андреева", "Витальева", "Петрова", "Павлова", "Григорьева"]


def get_random_element(sequence):
    return sequence[random.randint(0, len(sequence) - 1)]


def get_random_contact():
    if random.randint(0, 1) == 0:
        name = get_random_element(male_names)
        second_name = get_random_element(male_second_names)
        last_name = get_random_element(male_last_names)
    else:
        name = get_random_element(fem_names)
        second_name = get_random_element(fem_second_names)
        last_name = get_random_element(fem_last_names)
    phone = '8'
    for i in range(10):
        phone += str(random.randint(0, 9))
    return {"Имя": name, "Отчество": second_name, "Фамилия": last_name, "Телефон": phone}


def create_file(file_name):
    # with - менеджер контекста
    with open(file_name, 'w', encoding="UTF-8") as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Отчество", "Фамилия", "Телефон"])
        f_writer.writeheader()
        print(f"Файл сохранен под именем {file_name}")


def read_file(file_name):
    with open(file_name, 'r', encoding="UTF-8") as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, contacts_list):
    with open(file_name, 'w', encoding="UTF-8", newline='') as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Отчество", "Фамилия", "Телефон"])
        f_writer.writeheader()
        f_writer.writerows(contacts_list)
        print(f"Файл {file_name} сохранен.")


def required_length_string(text, required_length):
    text = str(text)
    current_length = len(text)
    if current_length >= required_length:
        return text[0:required_length]
    else:
        return text + " " * (required_length - current_length)


def dictionaries_chars_count(dictionaries_list):
    result = {"Имя": 3, "Фамилия": 7, "Отчество": 8, "Телефон": 11, "№": len(str(len(dictionaries_list)))}
    for current_dictionary in dictionaries_list:
        for current_key in current_dictionary.keys():
            current_value = len(str(current_dictionary.get(current_key)))
            saved_value = result.get(current_key)
            if saved_value is None:
                result[current_key] = current_value
            elif current_value > saved_value:
                result[current_key] = current_value
    return result


def dictionaries_list_to_text(dictionaries_list, numerated, numbers_list):
    if len(dictionaries_list) > 0:
        chars_count = dictionaries_chars_count(dictionaries_list)
        slim_end = '|'
        wide_end = " | "
        # Шапка таблицы
        result = f"| {required_length_string('№', chars_count['№'])}" + wide_end
        for key in dictionaries_list[0].keys():
            result += (required_length_string(key, chars_count[key])) + wide_end
        result += '\n'
        # Разделитель шапки
        result += f"|-{'-' * (chars_count['№'] + 1)}|"
        for key in dictionaries_list[0].keys():
            result += ("-" * (chars_count[key] + 2) + slim_end)
        result += '\n'
        # Строки таблицы
        for i in range(len(dictionaries_list)):
            contact = dictionaries_list[i]
            index = numbers_list[i] if numerated else i + 1
            result += (f"| {required_length_string(index, chars_count['№'])}" + wide_end)
            for key in contact.keys():
                result += (required_length_string(contact[key], chars_count[key]) + wide_end)
            i += 1
            result += '\n'
        return result
    else:
        return "Список пустой."


def select_element_from_list(my_list, to_print_list, message):
    if len(my_list) == 0:
        return -1
    else:
        if to_print_list:
            print(f"{message}:")
            for i in range(len(my_list)):
                print(i + 1, end="\t")
                print(my_list[i])
        while True:
            try:
                number = int(input("Введите номер для выбор строки: "))
                if 0 < number <= len(my_list):
                    return number - 1
                else:
                    print("В списке нет строки с таким номером.")
            except ValueError:
                print("Необходимо ввести целое число из списка.")


def look_up_for_tables():
    files_list = list()
    for entry in os.scandir(os.getcwd()):
        if entry.is_file():
            if os.path.splitext(entry.path)[1] == ".csv":
                files_list.append(entry.name)
    return files_list


def enter_file_name():
    while True:
        try:
            result = input("Введите имя, под которым файл будет сохранен: ").replace("\r\n", " ") + ".csv"
            directory_path = os.getcwd()
            full_path = directory_path + result
            if (len(full_path)) > 255:
                raise FileNameLength("Путь к файлу не может быть длиннее 255 символов. Сократите имя файла.")
            else:
                for ch in result:
                    if ch in {"<", ">", ":", "\"", "/", "\\", "|", "?", "*"}:
                        raise WrongFileName("Имя файла не может содержать символы < > : \" / \\ | ? *")
            return result
        except FileNameLength as error:
            print(error)
        except WrongFileName as error:
            print(error)


def enter_list_length():
    while True:
        try:
            result = int(input("Введите длину списка контактов: "))
            if result < 1:
                raise SmallerThanMin("Длина списка должна быть больше нуля.")
            elif result > 1000:
                raise BiggerThanMax("Программа не предназначена для работы с более чем 1000 контактов.")
            return result
        except ValueError:
            print("Длина списка контактов должна быть целым числом.")
            continue
        except SmallerThanMin as error:
            print(error)
        except BiggerThanMax as error:
            print(error)


def create_new_file():
    file_name = enter_file_name()
    create_file(file_name)
    contacts_list = list()
    work_with_file(file_name, contacts_list)


def create_random_file():
    file_name = enter_file_name()
    list_length = enter_list_length()
    contacts_list = list()
    for i in range(list_length):
        contacts_list.append(get_random_contact())
    work_with_file(file_name, contacts_list)


def open_existing_file():
    files_list = look_up_for_tables()
    if len(files_list) > 0:
        file_name = files_list[select_element_from_list(files_list, True, "Список файлов")]
        contacts_list = read_file(file_name)
        work_with_file(file_name, contacts_list)
    else:
        print("В текущей директории нет подходящих файлов.")


def remove_contact(contacts_list):
    if len(contacts_list) == 0:
        print("Список контактов пуст.")
    else:
        index = select_element_from_list(contacts_list, False, "")
        contacts_list.pop(index)
        print(f"Контакт №{index + 1} удален.")


def edit_contact(contacts_list):
    if len(contacts_list) == 0:
        print("Список контактов пуст.")
    else:
        index = select_element_from_list(contacts_list, False, "")
        contacts_list[index] = get_new_contact(True, contacts_list[index])
        print(f"Контакт №{index + 1} изменен.")


def move_contact(contacts_list):
    if len(contacts_list) == 0:
        print("Список контактов пуст.")
    else:
        index = select_element_from_list(contacts_list, False, "")
        while True:
            print("Перенести контакт: \"n\" – в новый список, \"o\" – в существующий.")
            command = input("Введите команду: ").lower()
            if command == "n":
                file_name = enter_file_name()
                write_file(file_name, [contacts_list[index]])
                break
            elif command == "o":
                files_list = look_up_for_tables()
                if len(files_list) > 0:
                    file_name = files_list[select_element_from_list(files_list, True, "Список файлов")]
                    another_contacts_list = read_file(file_name)
                    another_contacts_list.append(contacts_list[index])
                    write_file(file_name, another_contacts_list)
                    break
                else:
                    print("В текущей директории нет подходящих файлов.")


def find_contacts(contacts_list):
    if len(contacts_list) > 0:
        scores = list()
        matches = list()
        indexes = list()
        keywords = input("Введите поисковый запрос: ").lower().split(" ")
        for i in range(len(contacts_list)):
            contact = contacts_list[i]
            index = i + 1
            score = 0
            for keyword in keywords:
                if keyword in contact["Имя"].lower():
                    score -= 1
                if keyword in contact["Отчество"].lower():
                    score -= 1
                if keyword in contact["Фамилия"].lower():
                    score -= 1
                if keyword in str(contact["Телефон"]).lower():
                    score -= 1
            if score < 0:
                scores.append(score)
                matches.append(contact)
                indexes.append(index)
        if len(matches) > 0:
            result = sorted(list(zip(scores, indexes, matches)), key=operator.itemgetter(0, 1))
            result_matches = list()
            result_indexes = list()
            for x in result:
                result_matches.append(x[2])
                result_indexes.append(x[1])
            print("Результаты поиска:")
            print(dictionaries_list_to_text(result_matches, True, result_indexes))
        else:
            print("Нет совпадений.")
    else:
        print("Список пустой.")


def work_with_file(file_name, contacts_list):
    print(f"Редактирование файла {file_name}:")
    while True:
        command = input("Введите команду или \"h\" для списка команд: ").lower()
        if command == "h":
            print("Список команд:")
            print("\"v\" – показать список контактов")
            print("\"a\" – добавить контакт")
            print("\"d\" – удалить контакт")
            print("\"e\" – редактировать контакт")
            print("\"f\" – найти контакт")
            print("\"m\" – перенести контакт в другой файл")
            print("\"s\" – сохранить файл")
            print("\"sa\" – сохранить файл под другим именем")
            print("\"b\" – вернуться в главное меню")
        elif command == "v":
            print(dictionaries_list_to_text(contacts_list, False, None))
        elif command == "a":
            contacts_list.append(get_new_contact(False, None))
            print("Контакт добавлен.")
        elif command == "d":
            remove_contact(contacts_list)
        elif command == "e":
            edit_contact(contacts_list)
        elif command == "f":
            find_contacts(contacts_list)
        elif command == "m":
            move_contact(contacts_list)
        elif command == "s":
            write_file(file_name, contacts_list)
        elif command == "sa":
            file_name = enter_file_name()
            write_file(file_name, contacts_list)
        elif command == "b":
            print("Возвращаемся в главное меню.")
            break
        else:
            print("Такой команды нет.")


def main():
    print("Добро пожаловать в программу \"Список контактов\".")
    while True:
        command = input("Введите команду или \"h\" для списка команд: ").lower()
        if command == 'h':
            print("Список команд:")
            print("\t\"n\" – создать новый файл")
            print("\t\"r\" – сгенерировать случайный список")
            print("\t\"o\" – открыть существующий файл")
            print("\t\"q\"– выйти из программы")
        elif command == 'q':
            break
        elif command == 'o':
            open_existing_file()
        elif command == 'r':
            create_random_file()
        elif command == 'n':
            create_new_file()
        else:
            print("Такой команды нет.")


main()
