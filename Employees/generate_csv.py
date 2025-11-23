import csv
import random
from faker import Faker
from datetime import datetime

# Ініціалізація Faker з українською локалізацією
fake = Faker('uk_UA')

male_patronymics = [
    "Олександрович", "Іванович", "Петрович", "Михайлович", "Васильович",
    "Андрійович", "Сергійович", "Володимирович", "Дмитрович", "Миколайович",
    "Ігорович", "Юрійович", "Вікторович", "Анатолійович", "Григорович",
    "Олегович", "Степанович", "Романович", "Богданович", "Максимович"
]

female_patronymics = [
    "Олександрівна", "Іванівна", "Петрівна", "Михайлівна", "Василівна",
    "Андріївна", "Сергіївна", "Володимирівна", "Дмитрівна", "Миколаївна",
    "Ігорівна", "Юріївна", "Вікторівна", "Анатоліївна", "Григорівна",
    "Олегівна", "Степанівна", "Романівна", "Богданівна", "Максимівна"
]

positions = [
    "Менеджер", "Інженер", "Бухгалтер", "Програміст", "Аналітик",
    "Юрист", "Економіст", "Дизайнер", "Маркетолог", "HR-менеджер",
    "Адміністратор", "Консультант", "Координатор", "Спеціаліст", "Керівник відділу"
]

def generate_employee(gender):
    if gender == 'Жіноча':
        first_name = fake.first_name_female()
        last_name = fake.last_name_female()
        patronymic = random.choice(female_patronymics)
    else:
        first_name = fake.first_name_male()
        last_name = fake.last_name_male()
        patronymic = random.choice(male_patronymics)
    
    birth_date = fake.date_of_birth(minimum_age=16, maximum_age=86)
    
    return {
        'Прізвище': last_name,
        'Ім\'я': first_name,
        'По батькові': patronymic,
        'Стать': gender,
        'Дата народження': birth_date.strftime('%d.%m.%Y'),
        'Посада': random.choice(positions),
        'Місто проживання': fake.city(),
        'Адреса проживання': fake.street_address(),
        'Телефон': fake.phone_number(),
        'Email': fake.email()
    }

def create_csv_file(filename='employees.csv', total_records=500):
    try:
        female_count = int(total_records * 0.4)  # 40% жінок
        male_count = total_records - female_count  # 60% чоловіків
        
        # Створення списку статей у випадковому порядку
        genders = ['Жіноча'] * female_count + ['Чоловіча'] * male_count
        random.shuffle(genders)
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['Прізвище', 'Ім\'я', 'По батькові', 'Стать', 
                         'Дата народження', 'Посада', 'Місто проживання', 
                         'Адреса проживання', 'Телефон', 'Email']
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for gender in genders:
                employee = generate_employee(gender)
                writer.writerow(employee)
        
        print(f"Файл {filename} успішно створено!")
        print(f"Всього записів: {total_records}")
        print(f"Чоловіків: {male_count} ({male_count/total_records*100:.0f}%)")
        print(f"Жінок: {female_count} ({female_count/total_records*100:.0f}%)")
        
    except Exception as e:
        print(f"Помилка при створенні файлу: {e}")

if __name__ == "__main__":
    create_csv_file('employees.csv', 500)