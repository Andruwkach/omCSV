import csv


def request_and_do_command():
    """ Функция запрашивает команду и выполняет её """

    needed_comand = input('''Выберите действие:
    1. Вывести иерархию команд;
    2. Вывести сводный отчёт по департмаентам;
    3. Сохранить сводный отчёт по департмаентам.
    ''')
    assert needed_comand in ('1', '2', '3'), 'доступны только команды 1, 2 и 3'
    [print_teams_hierarchy, print_teams_info, create_report][
        int(needed_comand) - 1](departments)


def convert_csv_to_dict(path: str) -> dict:
    """ принимает на вход путь к CSV, читает файл,
    преобазует в словарь, где ключ - название департамента"""
    with open(path, newline='', encoding='utf-8') as csvfile:
        spam_reader = csv.reader(csvfile)
        departments = {}
        for row in spam_reader:
            name, department, team, position, mark, salary = row[0].split(';')
            if departments.get(department):
                departments[department]['Сотрудники'].append(name)
                departments[department]['Отделы'].add(team)
                departments[department]['Должности'].add(position)
                departments[department]['Оценки'].append(float(mark))
                departments[department]['Оклады'].append(int(salary))
            elif department != 'Департамент':
                departments[department] = {
                    'Сотрудники': [name], 'Отделы': set([team]),
                    'Должности': set([position]), 'Оценки': [float(mark)],
                    'Оклады': [int(salary)]
                }
    return departments


def print_teams_hierarchy(departments: dict) -> None:
    for department, information in departments.items():
        print(department, end=': ')
        print(*information['Отделы'], sep=', ')


def print_teams_info(departments: dict) -> None:
    for department, information in departments.items():
        count = len(information['Оклады'])
        min_salary = min(information['Оклады'])
        max_salary = max(information['Оклады'])
        average_salary = sum(information['Оклады']) / count
        print(f'{department}: численность - {count}, мин арплата - {min_salary}, '
              f'макс зарплата - {max_salary}, ср зарплата - {round(average_salary, 2)}')


def create_report(departments: dict) -> None:
    with open('report.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Департамент', 'Численность',
                      'Мин зарпалата', 'Макс зарплата', 'Ср зарплата']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for department, information in departments.items():
            count = len(information['Оклады'])
            min_salary = min(information['Оклады'])
            max_salary = max(information['Оклады'])
            average_salary = sum(information['Оклады']) / count
            writer.writerow(
                {'Департамент': department, 'Численность': count, 'Мин зарпалата': min_salary,
                 'Макс зарплата': max_salary, 'Ср зарплата': round(average_salary, 2)})


if __name__ == '__main__':
    departments = convert_csv_to_dict(input('укажите абсолютный путь к CSV файлу\n'))
    request_and_do_command()
