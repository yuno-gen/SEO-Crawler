# 🚀 SEO Crawler Platform

A scalable, open-source platform to **crawl any website**, store raw HTML in Supabase Storage, and index page metadata in a Supabase Postgres table. Built for extensibility, automation, and easy cloud deployment.

---

## 🌐 **Features**

* **Automated web crawling** using Scrapy
* **Airflow orchestration**: schedule and monitor crawls via UI
* **Raw HTML storage** in Supabase Buckets
* **Metadata indexing** in Supabase Postgres (`pages` table)
* **Easy configuration** with Airflow Variables and JSON
* **Completely containerized** with Docker Compose

---

## ⚡️ **Quick Start**

### 1. **Clone the Repository**

```bash
git clone <your-repo-url>
cd <project-directory>
```

---

### 2. **Set Up Environment Variables & Supabase**

* Create a **Supabase project** at [supabase.com](https://supabase.com).
* Obtain your `SUPABASE_URL` and `SUPABASE_KEY` (Service Role recommended for backend/server use).
* Create a **storage bucket** called `raw-html`.

---

### 3. **Create the `pages` Table**

Paste this SQL in Supabase's SQL Editor:

```sql
create table public.pages (
    id uuid primary key default gen_random_uuid(),
    url text not null,
    title text,
    crawled_at timestamp with time zone default now(),
    storage_path text,
    status integer,
    content_hash text
);
```

---

### 4. **Enable Read/Write Policies for Dev**

**WARNING:** This makes your table readable/writable by anyone for dev/testing only!
Paste in SQL editor:

```sql
-- Read
create policy "Allow read for all users"
on public.pages
for select
using (true);

-- Write
create policy "Allow insert for all users"
on public.pages
for insert
with check (true);
```

---

### 5. **Configure Airflow Variables**

Create a `variables.json` file in your project root:

```json
{
  "START_URL": "https://example.com",
  "PROJECT_ID": "example_com",
  "SUPABASE_URL": "https://your-project.supabase.co",
  "SUPABASE_KEY": "your-service-role-key"
}
```

Import variables into Airflow:

```bash
docker compose exec airflow airflow variables import /opt/airflow/variables.json
```

---

### 6. **Install & Run**

**Build and start everything:**

```bash
docker compose down
docker compose up -d --build
```

Access Airflow UI at [http://localhost:8080](http://localhost:8080)

---

### 7. **Run Your Crawler**

* In Airflow UI, **unpause** and **trigger** the DAG (e.g., `seo_example_com`).
* Monitor logs and results in Airflow.

---

### 8. **See Your Data**

* **HTML files**: Supabase Storage → `raw-html` bucket
* **Metadata**: Supabase Database → `pages` table

---

## 🛠️ **Project Structure**

```
.
├── dags/                   # Airflow DAG definitions
├── crawler/                # Scrapy spiders and runner scripts
│   └── spiders/
│       └── generic_site.py
├── requirements.txt        # Python dependencies (for Airflow + Crawler)
├── Dockerfile              # Airflow custom image build
├── docker-compose.yml      # Container orchestration
├── variables.json          # Airflow Variables import (SEO config)
└── README.md
```

---

## 🧰 **Tech Stack**

* **Airflow**: Scheduling/orchestration
* **Scrapy**: Crawling
* **Supabase**: Cloud storage + Postgres DB
* **Docker Compose**: Easy deployment

---

## ✨ **Customization**

* Add new spiders under `crawler/spiders/`.
* Edit DAGs in `dags/` for scheduling, notification, or custom logic.
* Store additional metadata by expanding the `pages` table and spider output.

---

## 🛡️ **Security**

* Dev policies are open for demo!
  For production, set **proper Row Level Security (RLS)** on your tables and use secure API keys.

---

## 📄 **License**

MIT (or your preferred license).

---

## 🏁 **Troubleshooting**

* **404 errors**: Table does not exist or permissions misconfigured in Supabase.
* **File not found**: Ensure correct volume mounting in `docker-compose.yml`.
* **ModuleNotFoundError**: Rebuild Docker image, check `requirements.txt`.
* **Variables not showing**: Check path and re-import with `airflow variables import`.

---

## 🙋 **Contributions & Support**

Open issues or submit PRs—let’s make this platform better together!

---

**Happy crawling! 🚀**
Let me know if you need a ready-to-use repo, extra features, or help deploying to the cloud.
