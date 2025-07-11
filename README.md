# 🧩 Django Project

This is a Django-based web application using Django 5.2 and Python 3.11. It includes custom apps and a selection of third-party libraries for extended functionality.

---

## 🚀 Features

- Custom user and admin modules (`customadmin`, `docmodify`)
- Admin panel (default `django.contrib.admin` commented out)
- `django-extensions` for shell, management commands, and debugging
- `rolepermissions`, `djangorestframework`, and others available in the environment
- Supports static file serving, session management, and authentication

---

## 📁 Project Structure

```
project_root/
├── customadmin/
├── docmodify/
├── manage.py
├── requirements.txt
└── ...
```

---

## ⚙️ Requirements

- Python 3.11
- pip (latest recommended)
- Virtualenv (recommended)

---

## 📦 Required Packages (from `requirements.txt`)

```
asgiref==3.8.1
Django==5.2
sqlparse==0.5.3
tzdata==2025.2
```

### 🧩 Additional Installed Packages (via `pip list`)
Here are some other important packages already installed in your environment:

- **django-extensions==4.1**
- **django-role-permissions==3.2.0**
- **django-tinymce==4.1.0**
- **django-widget-tweaks==1.5.0**
- **djangorestframework==3.16.0**
- **openpyxl==3.1.5**
- **pandas==2.3.0**
- **pdfkit==1.0.0**
- **weasyprint==65.1**
- **faker==37.3.0**
- **psycopg2-binary==2.9.10**

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Shakil1081/craftdoc.git
cd your-project-directory
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> ⚠️ If you’re missing any packages from your dev environment (like `django-extensions`, `rest_framework`, etc.), install them manually or update `requirements.txt` using `pip freeze > requirements.txt`.

---

## 🗃️ Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🧪 Run Development Server

```bash
python manage.py runserver 8003
```

---

## ⚙️ Environment Notes

- Django version mismatch was fixed: the project now uses **Django 5.2**
- Some built-in apps like `django.contrib.admin` are currently disabled in `INSTALLED_APPS` — enable as needed.
- The project contains two custom apps: `customadmin` and `docmodify`.

---

## 📌 Troubleshooting

### Migration Error: Missing `auth.0012`
If you encounter:
```
Migration customadmin.0007... reference nonexistent parent node ('auth', '0012...')
```

Make sure your Django version is **>= 4.0**, or manually fix the migration dependency in:
```
customadmin/migrations/0007_*.py
```

---

## 👨‍💻 Developer Notes

- For shell_plus and model visualizations, use:
```bash
python manage.py shell_plus
python manage.py graph_models -a -o models.png
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) — feel free to customize.

---

## 🤝 Contribution

Pull requests and feedback are welcome. Make sure to format code using PEP8 and follow Django best practices.
