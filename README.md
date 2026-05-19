# 🌍 Climate Goal CMS

An academic and public advocacy content management system designed to drive climate action, share research insights, and empower youth across sub-Saharan Africa and beyond. Built with Django, MySQL, and Tailwind CSS.

---

## 🚀 Key Features

*   **📰 70/30 Editorial Grid Layout:** A newspaper-style editorial split highlighting a primary featured story and a rolling feed of the latest insights.
*   **📱 Fully Responsive Mobile Navigation:** Adaptive design fitted with a sleek glassmorphic slide-out vertical navigation drawer for mobile and tablet devices.
*   **🎥 Multi-Format Video Integration:** Custom-engineered portrait video frames for **TikTok embeds** (aspect `9:16`) and widescreen landscape players for **YouTube embeds** (aspect `16:9`).
*   **🗂️ Dynamic Academic Experts Directory:** Author detail panels showcasing experts' short-form biographies and a filtered catalog of their publications.
*   **📥 Digital Inbox Management:** A staff-only dashboard metric to manage received inquiries with active "unread bounce badges," details modals, and confirmation dialogues.
*   **🌱 Automatic Database Seeding:** Custom Django management commands to populate your database with ready-to-test mock profiles, articles, and research databases.
*   **🛡️ Production-Grade Cloud Configurations:** Optimized for one-click, zero-downtime deployment on Render via Blueprints, Gunicorn, and WhiteNoise static compression.

---

## 🛠️ Technology Stack

*   **Core Framework:** Django 6.0+
*   **Primary Database:** MySQL (Optimized for **Aiven Cloud Databases**)
*   **Fallback Database:** SQLite3 (Local development fallback)
*   **WSGI Server:** Gunicorn (Production concurrency)
*   **Static Asset Delivery:** WhiteNoise (Compressed & cached assets delivery)
*   **Front End styling:** Tailwind CSS, Playfair Display (Typography) & FontAwesome

---

## ⚙️ Environment Variables

Create a `.env` file in the root folder of your project to store local configurations:

```env
# Optional Remote MySQL (Aiven) connection details.
# If omitted, Django will fallback seamlessly to local SQLite3.
DB_HOST=your-aiven-mysql-hostname.aivencloud.com
DB_PORT=14498
DB_NAME=defaultdb
DB_USER=avnadmin
DB_PASSWORD=your_aiven_password

# Django Configurations
DEBUG=True
SECRET_KEY=your-django-secret-key
```

---

## 💻 Local Quickstart

Follow these instructions to run the application on your computer:

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/climate_cms.git
cd climate_cms
```

### 2. Configure Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Mac/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run Migrations & Default Administrative Setup
Django will automatically apply table schemas and inject a programmatic default superuser:
*   **Username**: `admin`
*   **Password**: `password`
```bash
python manage.py migrate
```

### 4. Seed the Database
Seed the database with 5 distinct authors, 10 detailed climate change articles, and 10 external research resource links:
```bash
python manage.py seed_data
```

### 5. Launch the Development Server
```bash
python manage.py runserver
```
Visit the local server in your browser at `http://127.0.0.1:8000/`.

---

## 🚀 One-Click Deployment to Render

This project is preconfigured with a `render.yaml` Blueprint and an automated `build.sh` pipeline for seamless, zero-downtime cloud hosting:

1.  Log in to your **Render Dashboard**.
2.  Click **New +** -> **Blueprint**.
3.  Connect your GitHub repository.
4.  Input the required environment variables:
    *   `DB_HOST` (Aiven Host)
    *   `DB_PORT` (Aiven Port)
    *   `DB_NAME` (e.g. `defaultdb`)
    *   `DB_USER` (e.g. `avnadmin`)
    *   `DB_PASSWORD` (Your Aiven MySQL Password)
5.  Click **Approve**. Render will run dependencies installation, compress assets via WhiteNoise, execute database migrations to Aiven, and boot Gunicorn automatically!

---

## 📁 Repository Directory Structure

```text
climate_cms/
│
├── articles/                   # Django App core
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py    # Custom seeding command
│   ├── migrations/             # Table schema history
│   ├── templates/              # HTML layout and dashboard pages
│   ├── models.py               # Database schemas (Author, Article, Message)
│   ├── urls.py                 # Endpoint routes
│   └── views.py                # Dashboard & main logic controllers
│
├── config/                     # Django project settings
│   ├── settings.py             # Security, static, & MySQL integrations
│   └── urls.py                 # Top-level routing
│
├── .gitignore                  # Git tracking exclusions
├── build.sh                    # Automated cloud build pipeline
├── render.yaml                 # Render infrastructure Blueprint
├── requirements.txt            # Production dependencies list
└── manage.py                   # Django CLI utility
```

---

## 📄 License
This project is open-source and free to distribute under the terms of the MIT License.
