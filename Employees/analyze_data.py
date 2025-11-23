import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter

# Налаштування для коректного відображення українських символів
plt.rcParams['font.family'] = 'DejaVu Sans'

def calculate_age(birth_date_str):
    try:
        birth_date = datetime.strptime(birth_date_str, '%d.%m.%Y')
        today = datetime.now()
        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    except:
        return None

def categorize_age(age):
    if age is None:
        return None
    if age < 18:
        return 'younger_18'
    elif age <= 45:
        return '18-45'
    elif age <= 70:
        return '45-70'
    else:
        return 'older_70'

def get_category_label(category):
    labels = {
        'younger_18': 'Молодше 18',
        '18-45': '18-45',
        '45-70': '45-70',
        'older_70': 'Старше 70'
    }
    return labels.get(category, category)

def read_csv_data(filename='employees.csv'):
    if not os.path.exists(filename):
        print(f"Помилка: файл {filename} не знайдено!")
        return None
    
    try:
        employees = []
        with open(filename, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                age = calculate_age(row['Дата народження'])
                category = categorize_age(age)
                employees.append({
                    'gender': row['Стать'],
                    'age': age,
                    'category': category,
                    'data': row
                })
        
        if not employees:
            print(f"Помилка: файл {filename} порожній!")
            return None
        
        print("Ok")
        return employees
        
    except Exception as e:
        print(f"Помилка при відкритті файлу CSV: {e}")
        return None

def analyze_gender(employees):
    print("\n" + "="*50)
    print("АНАЛІЗ ЗА СТАТТЮ")
    print("="*50)
    
    gender_count = Counter(emp['gender'] for emp in employees)
    
    total = len(employees)
    for gender, count in gender_count.items():
        percentage = (count / total) * 100
        print(f"{gender}: {count} осіб ({percentage:.1f}%)")
    
    # Побудова діаграми
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = ['#FF69B4', '#4169E1']
    wedges, texts, autotexts = ax.pie(
        gender_count.values(),
        labels=gender_count.keys(),
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_weight('bold')
    
    ax.set_title('Розподіл співробітників за статтю', fontsize=14, weight='bold')
    plt.tight_layout()
    plt.savefig('gender_distribution.png', dpi=300, bbox_inches='tight')
    print("Діаграму збережено: gender_distribution.png")
    plt.close()

def analyze_age_categories(employees):
    print("\n" + "="*50)
    print("АНАЛІЗ ЗА ВІКОВИМИ КАТЕГОРІЯМИ")
    print("="*50)
    
    category_count = Counter(emp['category'] for emp in employees if emp['category'])
    
    # Упорядкування категорій
    ordered_categories = ['younger_18', '18-45', '45-70', 'older_70']
    ordered_data = {cat: category_count.get(cat, 0) for cat in ordered_categories}
    
    total = len(employees)
    for category, count in ordered_data.items():
        percentage = (count / total) * 100
        print(f"{get_category_label(category)}: {count} осіб ({percentage:.1f}%)")
    
    # Побудова діаграми
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
    
    bars = ax.bar(
        [get_category_label(cat) for cat in ordered_categories],
        ordered_data.values(),
        color=colors,
        edgecolor='black',
        linewidth=1.2
    )
    
    ax.set_xlabel('Вікова категорія', fontsize=12, weight='bold')
    ax.set_ylabel('Кількість співробітників', fontsize=12, weight='bold')
    ax.set_title('Розподіл співробітників за віковими категоріями', fontsize=14, weight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Додавання значень на стовпці
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=10, weight='bold')
    
    plt.tight_layout()
    plt.savefig('age_categories_distribution.png', dpi=300, bbox_inches='tight')
    print("Діаграму збережено: age_categories_distribution.png")
    plt.close()

def analyze_gender_by_age(employees):
    print("\n" + "="*50)
    print("АНАЛІЗ ЗА СТАТТЮ В КОЖНІЙ ВІКОВІЙ КАТЕГОРІЇ")
    print("="*50)
    
    ordered_categories = ['younger_18', '18-45', '45-70', 'older_70']
    
    data_by_category = {}
    for category in ordered_categories:
        cat_employees = [emp for emp in employees if emp['category'] == category]
        gender_count = Counter(emp['gender'] for emp in cat_employees)
        data_by_category[category] = gender_count
        
        print(f"\n{get_category_label(category)}:")
        total_cat = len(cat_employees)
        for gender, count in gender_count.items():
            percentage = (count / total_cat * 100) if total_cat > 0 else 0
            print(f"  {gender}: {count} осіб ({percentage:.1f}%)")
    
    # Побудова групованої стовпчикової діаграми
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = range(len(ordered_categories))
    width = 0.35
    
    male_counts = [data_by_category[cat].get('Чоловіча', 0) for cat in ordered_categories]
    female_counts = [data_by_category[cat].get('Жіноча', 0) for cat in ordered_categories]
    
    ax.bar([i - width/2 for i in x], male_counts, width, label='Чоловіча', 
           color='#4169E1', edgecolor='black', linewidth=1)
    ax.bar([i + width/2 for i in x], female_counts, width, label='Жіноча', 
           color='#FF69B4', edgecolor='black', linewidth=1)
    
    ax.set_xlabel('Вікова категорія', fontsize=12, weight='bold')
    ax.set_ylabel('Кількість співробітників', fontsize=12, weight='bold')
    ax.set_title('Розподіл за статтю в кожній віковій категорії', fontsize=14, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([get_category_label(cat) for cat in ordered_categories])
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig('gender_by_age_distribution.png', dpi=300, bbox_inches='tight')
    print("\nДіаграму збережено: gender_by_age_distribution.png")
    plt.close()
    
    # Побудова окремих кругових діаграм для кожної категорії
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    colors = ['#4169E1', '#FF69B4']
    
    for idx, category in enumerate(ordered_categories):
        gender_count = data_by_category[category]
        if sum(gender_count.values()) > 0:
            wedges, texts, autotexts = axes[idx].pie(
                gender_count.values(),
                labels=gender_count.keys(),
                autopct='%1.1f%%',
                colors=colors,
                startangle=90
            )
            
            for text in texts:
                text.set_fontsize(10)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(9)
                autotext.set_weight('bold')
        
        axes[idx].set_title(f'{get_category_label(category)}\n(всього: {sum(gender_count.values())})', 
                           fontsize=12, weight='bold')
    
    plt.suptitle('Розподіл за статтю в кожній віковій категорії', 
                 fontsize=14, weight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig('gender_by_age_pies.png', dpi=300, bbox_inches='tight')
    print("Діаграму збережено: gender_by_age_pies.png")
    plt.close()

def main():
    print("="*50)
    print("АНАЛІЗ ДАНИХ СПІВРОБІТНИКІВ")
    print("="*50)
    
    # Зчитування даних
    employees = read_csv_data('employees.csv')
    
    if employees is None:
        return
    
    print(f"\nВсього зчитано записів: {len(employees)}")
    
    # Виконання аналізу
    analyze_gender(employees)
    analyze_age_categories(employees)
    analyze_gender_by_age(employees)
    
    print("\n" + "="*50)
    print("АНАЛІЗ ЗАВЕРШЕНО")
    print("="*50)

if __name__ == "__main__":
    main()