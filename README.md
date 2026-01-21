# 🎟 Booking Platform API

Booking Platform — это backend-платформа для управления событиями и бронирования билетов.  
Проект реализован на Django + Django REST Framework с поддержкой аутентификации, ролей пользователей, фильтрации, пагинации и фоновых задач.

---

## Features

-  Пользователи с ролями: **User / Organizer / Admin**
-  Аутентификация по токену (DRF TokenAuth)
-  Управление событиями (Events)
-  Типы билетов (Ticket Types)
-  Корзина и бронирование билетов
-  Проверка доступного количества билетов
-  Фильтрация и пагинация
-  Сброс пароля через email (Celery + Redis)
-  Swagger / OpenAPI документация
-  Docker + Docker Compose

---

##  Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL / SQLite (dev)
- **Auth:** Token Authentication
- **Async Tasks:** Celery + Redis
- **Docs:** drf-yasg (Swagger)
- **Containerization:** Docker, Docker Compose

---

##  Project Structure

```text
core/
├── settings.py
├── celery.py
├── urls.py
accounts/
├── models.py
├── managers.py
├── serializers.py
├── generic_api.py
main/
├── models.py
├── tasks.py
api/
├── auth/
│   ├── serializers.py
│   ├── generic_api.py
│   └── endpoints.py
├── main/
│   ├── viewsets.py
│   ├── serializers.py
│   ├── filters.py
│   ├── permissions.py
│   └── paginations.py
docker-compose.yml
Dockerfile
requirements.txt
