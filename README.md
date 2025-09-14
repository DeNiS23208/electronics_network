# 📦 Electronics Network API

## 📌 Описание проекта
Онлайн-платформа торговой сети электроники.  
Реализована трёхуровневая иерархия сети:
- **Завод** (уровень 0)  
- **Розничная сеть** (уровень 1)  
- **Индивидуальный предприниматель (ИП)** (уровень 2)  

Каждое звено содержит контакты, список продуктов, задолженность перед поставщиком и автоматически определяется по уровню иерархии.

---

## ⚙️ Технологии
- Python 3.12  
- Django 4.2  
- Django REST Framework 3.14  
- PostgreSQL 15  
- django-filter  
- python-dotenv  

---

## 🚀 Запуск проекта (локально)

### 1. Клонировать репозиторий
```bash
git clone https://github.com/<твой-ник>/<название-репо>.git
cd <название-репо>
```

### 2. Создать и активировать виртуальное окружение
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Настроить переменные окружения
Создать файл `.env` в корне и заполнить по примеру:

```env
DEBUG=1
SECRET_KEY=your_secret_key
DB_NAME=electronics
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Применить миграции и создать суперпользователя
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Запустить сервер
```bash
python manage.py runserver
```

---

## 🛠 Возможности

### 🔹 Админка (`/admin/`)
- Управление объектами сети и продуктами.  
- Ссылка на поставщика прямо в карточке объекта.  
- Фильтр по городу (и стране).  
- Admin action: очистка задолженности у выбранных объектов.  

### 🔹 API (`/api/`)
**Эндпоинты:**
- `GET /api/suppliers/` — список звеньев сети  
- `POST /api/suppliers/` — создать новое звено  
- `GET /api/suppliers/{id}/` — получить звено  
- `PATCH /api/suppliers/{id}/` — обновить (кроме поля `debt`)  
- `DELETE /api/suppliers/{id}/` — удалить  
- `GET /api/suppliers/?country=Russia` — фильтрация по стране  
- `GET /api/products/` — список продуктов  

**Особенности:**
- Только активные сотрудники (`is_active=True, is_staff=True`) имеют доступ к API.  
- Поле `debt` нельзя изменить через API (только при создании или через админку).  
- Автоматическое вычисление уровня (0–2).  

---

## 📊 Пример работы API

Создать звено сети:
```json
POST /api/suppliers/
{
  "name": "DNS",
  "email": "dns@example.com",
  "country": "Russia",
  "city": "Moscow",
  "street": "Tverskaya",
  "house_number": "10",
  "supplier": 1,
  "debt": 10000.50
}
```

Ответ:
```json
{
  "id": 2,
  "name": "DNS",
  "email": "dns@example.com",
  "country": "Russia",
  "city": "Moscow",
  "street": "Tverskaya",
  "house_number": "10",
  "products": [],
  "supplier": 1,
  "debt": "10000.50",
  "created_at": "2025-09-13T10:00:00Z",
  "level": 1
}
```

---

## ✅ Статус выполнения задания
- [x] Модель сети (3 уровня)  
- [x] Контакты, продукты, задолженность, время создания  
- [x] Админка: вывод, ссылка на поставщика, фильтр, action очистки задолженности  
- [x] API: CRUD, запрет изменения `debt`, фильтрация по стране  
- [x] Доступ к API только активным сотрудникам  
