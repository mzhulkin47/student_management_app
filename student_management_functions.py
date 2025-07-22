import time
import json 
import psycopg2 # Импортируем библиотеку для работы с PostGreSQL
from psycopg2 import Error  # Импортируем класс Error для работы с ошибками


# --- Данные для подключения к базе данных PostgreSQL ---
DB_HOST = 'localhost'            # адрес сервера базы данных (мой ноутбук)
DB_NAME = 'student_db'           # Имя базы данных, которую мы создали
DB_USER = 'student_user'         # Имя пользователя, которого мы создали
DB_PASSWORD = 'rvvdkdku2010'     # Пароль для польователя student_user
DB_PORT = '5432'                 # Порт, на котором слушает PostgreSQL
# --------------------------------------------------------------------------


def get_db_connection():
    """
    Устанавливает и возвращает соединение с базой данных PostgreSQL.
    В случае ошибки подключения выводит сообщение и возвращает None.
    """
    connection = None
    try:
        # Пытаемся установить соединение с БД, используя импортированную библиотеку "psycopg2"
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        # Если соединение успешно установлено, то выводим об этом сообщение
        print('Соединение с базой данных PostgreSQL успешно установлено!')
        return connection # возвращает объект соединения
    except Error as e:
        # Если произошла ошибка, выводим ее
        print(f"Произошла ошибка: {e}.")
        return None # В случае ошибки возвращает None
    
    
def create_students_table():
    """
    Создает таблицу 'students' в базе данных, если она еще не существует.
    """
    connection = get_db_connection()  # Получаем объект соединения с БД
    if connection: # Проверяем, удалось ли установить соединение
        cursor = connection.cursor()  # Создаем объект курсора
        try:
            # SQL-запрос для создания таблицы students
            # IF NOT EXISTS: предотвращает ошибку, если таблица уже существует
            # student_id: SERIAL PRIMARY KEY - автоматически увеличивающийся уникальный ID
            # VARCHAR(50): строка до 50 символов
            # NOT NULL: поле не может быть пустым
            # INTEGER: целое число
            create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                last_name VARCHAR(50) NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                patronymic VARCHAR(50),
                age INTEGER,
                course INTEGER
            );
            """
            cursor.execute(create_table_query) # Выполняет SQL-запрос через курсор
            connection.commit() # Подтверждаем изменения в базе данных (сохраняем)
            print("Таблица 'students' успешно создана или уже существует.")
        
        except Error as e:
            print(f"Ошибка при создании таблицы 'students': {e}")
            connection.rollback()  # Откатываем изменения, если произошла ошибка
        
        finally:
            if cursor:
                cursor.close()  # Всегда закрываем курсор
            if connection:
                connection.close()  # Всегда закрываем соединение с БД
                print('Соединение с БД закрыто.')
                
    
    
     

# ==================== Определение класса Student ====================
# Мы определяем новый КЛАСС с именем 'Student'.
# Это как ЧЕРТЕЖ или ШАБЛОН для создания КОНКРЕТНЫХ ОБЪЕКТОВ-студентов.
# Каждый ОБЪЕКТ-студент будет иметь характеристики (АТРИБУТЫ)
# и сможет выполнять действия (МЕТОДЫ), определенные в этом КЛАССЕ.
class Student:
    """
    Класс Student представляет собой шаблон для создания объектов студентов.
    Каждый объект студента будет иметь АТРИБУТЫ (данные)
    и сможет выполнять МЕТОДЫ (действия).
    """
    # --- Конструктор (метод __init__) ---
    # Это специальный МЕТОД, называемый КОНСТРУКТОРОМ.
    # Он автоматически вызывается КАЖДЫЙ РАЗ, когда вы создаете новый
    # ЭКЗЕМПЛЯР (или ОБЪЕКТ) класса Student.
    # Например, когда мы пишем `Student("Иванов", "Иван", ...)`
    # 'self' - это ОБЯЗАТЕЛЬНЫЙ первый параметр в любом методе класса.
    # Он является ссылкой на ТОТ КОНКРЕТНЫЙ ОБЪЕКТ, который сейчас создается
    # или с которым мы работаем. Через 'self' мы присваиваем данные
    # АТРИБУТАМ ЭТОГО КОНКРЕТНОГО ОБЪЕКТА.
    def __init__(self, last_name, first_name, patronymic, age, course):
        self.last_name = last_name    # АТРИБУТ фамилия
        self.first_name = first_name  # АТРИБУТ имя
        self.patronymic = patronymic  # АТРИБУТ отчество
        self.age = age                # АТРИБУТ возраст
        self.course = course          # АТРИБУТ курс
        
    
    # --- Специальный метод __str__() ---
    # Этот специальный МЕТОД определяет, как ОБЪЕКТ класса Student
    # должен быть представлен в виде СТРОКИ, когда вы используете
    # функцию `print()` для этого ОБЪЕКТА или преобразуете его к строке (`str()`).
    # Это очень удобно для "человекочитаемого" вывода информации о студенте.
    def __str__(self):
        return (f"ФИО: {self.last_name} {self.first_name} {self.patronymic} "
                f"| Возраст: {self.age} | Курс: {self.course}")
        
# ==================== Конец определения класса Student ====================


students = []



# функция вызова меню
def display_menu():
    '''
        Выводит главное меню системы управления студентами на экран
    '''
    print('<><><><><> СИСТЕМА УПРАВЛЕНИЯ СПИСКОМ СТУДЕНТОВ <><><><><>')
    time.sleep(0.2)
    print()
    print('<< 1 >> Добавить нового студента')
    time.sleep(0.2)
    print('<< 2 >> Посмотреть список студентов')
    time.sleep(0.2)
    print('<< 3 >> Найти студента по фамилии')
    time.sleep(0.2)
    print('<< 4 >> Удалить студента из списка')
    time.sleep(0.2)
    print('<< 5 >> Редактировать студента')
    time.sleep(0.2)
    print('<< 6 >> Выход из программы')
    print('\n***********************************************************')
    print() # пустая строка для отделения меню
    
    
'''
добавляю функции для обработки данных ввода ФИО
'''
# проверяет корректность части ФИО
def validate_name(name, name_type):
    if not name:
        print(f'Ошибка: **{name_type}** не может быть пустым.')
        return False
    
    if not name.isalpha():
        print(f'Ошибка: **{name_type}** должен содержать только буквы.')
        return False
    return True

'''
функция запрашивает у пользователя часть ФИО с валидацией
'''
def get_valid_name(name_type):
    while True:
        name = input(f'Введите {name_type} студента: ').title().strip()
        if validate_name(name, name_type):
            return name
    
        
        
        
        
# определение функции добавить студента  add_student()
def add_student(students_list):
    '''
    Добавляем нового студента (фамилия, имя, отчество, возраст, курс)
    
    Аргументы:
        students_list (list): Список, в который будет добавлен новый студент.
    '''
    print('\n---------- Добавляем нового студента ----------') # вывод для ясности, что сейчас мы добавляем нового студента
    '''
    здесь будет весь код для вызова "пункта меню << 1 >>"
    '''
    time.sleep(0.5)
    print('\n***Введите данные студента***')
    time.sleep(0.2)
    print('-----------------------------')
    last_name = get_valid_name('фамилию')
    first_name = get_valid_name('имя')
    patronymic = get_valid_name('отчество')
    
    # ввод и валидация возраста студента
    while True:
        student_age_str = input('Введите возраст студента: ').strip()
        # валидация на пустой ввод
        if not student_age_str:
            print('Возраст не может быть пустой строкой')
            continue
        
        # валидация на число
        if not student_age_str.isdigit():
            print('Возраст надо вводить числом')
            continue
        student_age = int(student_age_str)
        # проверка диапазона возраста(в нашем ввузе можно обучаться с 16 до 65 лет (включительно))
        if not 16 <= student_age <= 65:
            print('В нашем ВУЗе можно учиться с 16 лет до 65(включительно)')
            continue
        break # выход из цикла валидации **возраста**
        
        # ввод и валидация курса студента
    while True:
        student_course_str = input('Введите курс студента: ').strip()
        if not student_course_str:
            print('Вы не ввели курс')
            continue
        if not student_course_str.isdigit():
            print('Курс надо вводить числом')
            continue
        student_course = int(student_course_str)
        if not 1 <= student_course <= 6:
            print('В нашем ВУЗе есть только курсы с 1-го по 6-ой(включительно)')
            continue
        break
            
    # создаю объект (экземпляр) класса Student
    # Раньше здесь создавался словарь, а теперь вызываем конструктор __init__
    new_student = Student(
        last_name,
        first_name,
        patronymic,
        student_age,
        student_course
    )
    
    # ----- код для сохранения в БД -----
    connection = get_db_connection()   # Получаю соиденение с БД
    if connection: # Если соединение установленно
        cursor = connection.cursor() # Создаю курсор
        try:
            # SQL-запрос для вставки данных. Используем %s для параметров,
            # чтобы избежать SQL-инъекций и корректно передавать данные.
            insert_query = """
            INSERT INTO students (last_name, first_name, patronymic, age, course)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """
            # выполняю запрос, передавая данные ввиде кортежа
            cursor.execute(insert_query, (
                new_student.last_name,
                new_student.first_name,
                new_student.patronymic,
                new_student.age,
                new_student.course
            ))
            # Получаем ID только что вставленной записи (если нужно, для подтверждения)
            student_id = cursor.fetchone()[0]
            connection.commit()  # Подтверждаю изменения в БД
            
    
            # добаляю словарь на нового студента в список
            # students_list.append(new_student)
            # вывод подтверждения о добавлении студента
            print(f'\nСтудент **{new_student.last_name} {new_student.first_name} {new_student.patronymic}**  (ID: {student_id}) добавлен в список студентов.')
        except Error as e:
            print(f"Произошла ошибка при добавлении студента в БД: {e}")
            connection.rollback() # Откатываю изменения, если произошла ошибка.
        # Закрываю курсор и закрываю соединение
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
                print("Соелинение с БД закрыто.")
    else:
        print("Не удалось добавить студента: нет соединения с БД.")
    # ------ тут код для сохранения студента в БД заканчивается ------    
    
 
# определение функции вывода списка студентов
def view_students(students_list):
    """
    Отображает список всех студентов, находящихся в системе.

    Аргументы:
        students_list (list): Список студентов для отображения.
    """
    print('\n<<<<<<<<<<<<<<<<<<<<< СПИСОК СТУДЕНТОВ >>>>>>>>>>>>>>>>>>>>>')
    time.sleep(0.2)
    print()
    if not students_list:
        print('\nСписок студентов пуст.')
    else:
        for i, student_data in enumerate(students_list):
            time.sleep(0.2)
            print(    
                f'{i + 1}. ФИО: {student_data.last_name.ljust(15, ' ')}'
                f'{student_data.first_name.ljust(15, ' ')}'
                f'{student_data.patronymic.ljust(15, ' ')} '
                f'| Возраст: {student_data.age} '
                f'| Курс: {student_data.course}'
            )
    print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print()
    
    
# определение функции "найти студента" def find_student()
def find_student(students_list):
    """
    Ищет студентов по фамилии и выводит информацию о найденных студентах.

    Аргументы:
        students_list (list): Список студентов, в котором осуществляется поиск.
    """
    print('\n------------------- ПОИСК СТУДЕНТА ПО ФАМИЛИИ --------------------')
    time.sleep(0.2)
    search_last_name = input('Введите начало фамилии для поиска: ').strip().title()
    print()
    if not search_last_name:
        print('Ошибка: фамилия не может быть пустой.')
        return
    found_students = []
    for i, student_data in enumerate(students_list):
        if student_data.last_name.startswith(search_last_name):
            found_students.append((i, student_data))
    if not found_students:
        print(f'Студент(ы) с фамилией **{search_last_name}* не найден(ы)')
    else:
        print(f'Найдены следующие студенты с фамилией *{search_last_name}*:')
        time.sleep(0.4)
        print()
        for i, (original_index, student_data) in enumerate(found_students):
            print(
                f'{i + 1}. (ID: {original_index + 1}) ФИО: {student_data.last_name.ljust(15, ' ')}'
                f'{student_data.first_name.ljust(15, ' ')}'
                f'{student_data.patronymic.ljust(15, ' ')} '
                f'| Возраст: {student_data.age} '
                f'| Курс: {student_data.course}'
            )
    print('\n--------------------------------------------------')
    
    
# определение функции "удалить студента"  def delete_student()
def delete_student(students_list):
    print('\n-------------------- УДАЛЕНИЕ СТУДЕНТА --------------------')
    if not students_list:
        print('Список студентов пуст, удалять некого.')
        return
    view_students(students_list)
    print('\nПожалуйста, используйте ID студента из списка выше для удаления.')
    
    while True:
        student_id_str = input('Введите *ID* студента для его удаления или *0* для выхода: ').strip()
        if not student_id_str.isdigit():
            print('\nОшибка: *ID* должен быть числом')
            continue
        student_id = int(student_id_str)
        if student_id == 0:
            print('Удаление отменено.')
            return
        index_to_delete = student_id - 1
        if 0 <= index_to_delete < len(students_list):
            deleted_student = students_list.pop(index_to_delete)
            print(f'Студент: **{deleted_student.last_name} {deleted_student.first_name} {deleted_student.patronymic}** успешно удаленю')
            break
        else:
            print(f'Ошибка: Студент с ID *{student_id}* не найден.')
            print('Попробуйте еще раз.')
    print('\n-----------------------------------------------------------')
    print()
    
    
# определение функции "изменить студента"  def edit_student()
def edit_student(students_list):
    print('\n*************** РЕДАКТИРОВАНИЕ СТУДЕНТА ***************')
    time.sleep(0.5)
    print()
    if not students_list:
        print('Список студентов пуст. Изменить в пустом списке ниего нельзя.')
        return
    view_students(students_list)
    print('\nИспользуйте *ID* студента из списка выше для его редактирования.') 
    while True:
        student_id_str = input('\nВведите из списка выше *ID* студента, которого хотите редактировать (или 0 для отмены)').strip()
        if not student_id_str.isdigit():
            print('\nОшибка: *ID* студента должно быть числом.')
            continue
        student_id = int(student_id_str)
        if student_id == 0:
            print('Редактирование отменено.')
            return
        index_to_edit = student_id - 1
        # проверка, что ввели коректный ID
        if 0 <= index_to_edit < len(students_list):
            student_to_edit = students_list[index_to_edit]
            print(f"\nРедактирование студента: **{student_to_edit.last_name} {student_to_edit.first_name} {student_to_edit.patronymic}**")
            print('Оставте поле пустым, если не хотите его менять.')
            
            # Теперь запрашиваем новые данные, используя существующие функции и логику
            # Запрашиваем новую фамилию, имя, отчество
            new_last_name = input(f'Новая фамилия (текущая фамилия: {student_to_edit.last_name}): ').strip().title()
            if new_last_name: # если пользователь что-то ввел, проверяем и обновляем
                if validate_name(new_last_name, 'фамилия'): # переипользуем функцию validate_name()
                    student_to_edit.last_name = new_last_name
                else:
                    print('Фамилия неизменена из-за неверного формата ввода.')
            new_first_name = input(f"Новое имя (текущее имя **{student_to_edit.first_name}**): ").strip().title()
            if new_first_name:
                if validate_name(new_first_name, 'имя'):
                    student_to_edit.first_name = new_first_name
                else:
                    print('Имя неизменено из-за неверного формата ввода.')
            new_patronymic = input(f"Новое отчество (текущее отчество **{student_to_edit.patronymic}**): ").strip().title()
            if new_patronymic:
                if validate_name(new_patronymic, 'отчество'):
                    student_to_edit.patronymic = new_patronymic
                else:
                    print('Отчество неизменено из-за неверного формата ввода.')
            while True:
                new_age_str = input(f"Новый возраст (текущий возраст **{student_to_edit.age}** (16-65 или пусто для пропуска)): ").strip()
                if not new_age_str:
                    break
                if not new_age_str.isdigit():
                    print('Ошибка: Возраст должен быть числом.')
                    continue
                new_age = int(new_age_str)
                if not 16 <= new_age <= 65:
                    print('В нашем ВУЗе можно учиться с 16 до 65 лет (включительно).')
                    continue
                student_to_edit.age = new_age
            while True:
                new_course_str = input(f"Новый курс (текущий курс **{student_to_edit.course}** (1-6 или пусто для пропуска)): ").strip()
                if not new_course_str:
                    break
                if not new_course_str.isdigit():
                    print('Ошибка: Курс должен быть числом.')
                    continue
                new_course = int(new_course_str)
                if not 1 <= new_course <= 6:
                    print('В нашем ВУЗе курсы с 1-го по 6 (включительно)')
                    continue
                student_to_edit.course = new_course
                break
            print(f"\nИнформация о студенте **{student_to_edit.first_name} {student_to_edit.last_name} {student_to_edit.patronymic}** успешно обновлена.")
            break
        else:
            print(f"Ошибка: Студент с ID **{student_id}** не найден. Попробуйте еще раз.")
    print('********************************************************************')
    print()


# Определение функции для сохранения списков студентов в файл JSON
def save_students_to_file(students_list, filename = 'students.json'):
    '''
    Сохраняем список студентов в файл JSON
    
    Аргументы:
        students_list (list) список словарей студентов.
        filename (str) файл для сохранения словарей студентов в файл JSON.
    '''
    data_to_save = []
    
    for student_obj in students_list:
        data_to_save.append({
            'фамилия': student_obj.last_name,
            'имя': student_obj.first_name,
            'отчество': student_obj.patronymic,
            'возраст': student_obj.age,
            'курс': student_obj.course     
        })

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        print(f'\nДанные успешно сохранены в файл: "{filename}"')
    except IOError:
        print(
            f'\nОшибка: Не удалось сохранить данные в файл {filename}.'  
            f'Проверьте права доступа или место на диске.'
            )
    except Exception as e:
        print(f'\nПроизошла непредвиденная ошибка "{e}"')


# Определение функции для загрузки списка студентов из файла JSON
def load_students_from_file(filename = 'students.json'):
    '''
    Загружает список студентов из JSON-файла.
    
    Аргументы:
        filename (str) файл из которого производим загрузку (students.json)
    Возвращает:
        list: список словарей, представляющий студентов или пустой список,
        print(f'\nФайл данных "{filename}" не найден. Начинаем с пустого списка студентов.')
        если файл не найден/поврежден
    '''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        students_objects = []
        for student_dict in loaded_data:
            students_objects.append(Student(
                student_dict['фамилия'],
                student_dict['имя'],
                student_dict['отчество'],
                student_dict['возраст'],
                student_dict['курс'],
            ))
            
        print(f'\nДанные студентов успешно загружены из файла "{filename}".')
        return students_objects
    except FileNotFoundError:
        # Бывает при первом запуске программы
        print(f'\nФайл данных "{filename}" не найден. Начинаем с пустого списка студентов.')
        return [] # возвращает пустой список, если файла нет
    except json.JSONDecodeError:
        # Ловит ошибку, если файл сущетвует, но он не корректен (JSON)
        print(
            f'\nОшибка: файл "{filename}" поврежден или содержит некорректные данные.'
            f'\nНачинаем с нового списка.'
            )
        return [] # Возвращаем пустой список, чтобы программа могла продолжить работать
    except Exception as e:
        # ловим любые другие ошибки, которые могут возникнуть
        print(f'\nПроизошла непредвиденная ошибка "{e}".')
        return [] # Возвращаем пустой список
        
        
   
# определение главной функции main()
def main():
    '''
    Главная функция программы, управляющая основным циклом меню и выбором действия пользователя
    '''
    global students
    students = load_students_from_file() # <<- Загружает данные при старте
    # здесь начинается главный цикл while True
    while True:
        display_menu() # вызываем функцию, которая теперь отображает меню
        
        # Ниже будет весь код, который был в твоем главном цикле while True
        # (запрос ввода, валидация, if/elif для выбора пунктов)
        menu_choice_str = input('Выберите пункт меню: 1 - 6:>> ')
        try:
            menu_choice = int(menu_choice_str)
        except ValueError:
            print('Ошибка: Введите числовое значение для выбора пункта меню.')
            time.sleep(0.5)
            continue
        if not 1 <= menu_choice <= 6:
            print(f'Меню с номером << {menu_choice} >> нет в списке.')
            continue
        
        # -------------------- выбор меню << 6 >> --------------------
        if menu_choice == 6:
            print('Вы вышли из программы.')
            save_students_to_file(students) # Сохранение данных перед выходом 
            print('До свидания!')
            break # выход из пронраммы
        
        # -------------------- выбор меню << 1 >> --------------------
        elif menu_choice == 1:
            print('Вы выбрали пункт меню << 1 >>: "Добавить студента"')
            add_student(students)
        
        elif menu_choice == 2:
            print('Вы выбрали пункт меню << 2 >>: "Посмотреть список студентов"')
            view_students(students) 
        
        elif menu_choice == 3:
            print('Вы выбрали пункт меню << 3 >>: "Найти студента по фамилии"')
            find_student(students)
        
        elif menu_choice == 4:
            print('Вы выбрали пункт меню << 4 >>: "Удалить студента из списка"')
            delete_student(students)
        
        elif menu_choice == 5:
            print('Вы выбрали пункт меню << 5 >>: "Редактировать студента"')
            edit_student(students)
            
            
if __name__ == '__main__':
    # Этот блок кода будет выполнен только тогда, когда файл запущен напрямую (не импортирован как модуль)
    create_students_table()
    main()
    
    