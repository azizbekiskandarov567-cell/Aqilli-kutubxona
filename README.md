# Smart Library Management & Recommendation System (SLMRS)

Aqlli kutubxonani boshqarish va tavsiya berish tizimi.

**Mualliflar:** Iskandarov Azizbek, Mamajonov Jaloliddin

## Imkoniyatlar
- Kitoblar katalogi va nusxalarni hisobga olish
- Kitob berish / qaytarish / band qilish / jarimalar
- Baho va sharhlar
- Gibrid tavsiya tizimi (content-based + collaborative filtering)
- Rollar: reader, librarian, admin (JWT)

## Texnologiyalar
FastAPI, PostgreSQL, SQLAlchemy, scikit-learn, React, Docker, Google Cloud Platform (Cloud Run, Cloud SQL, Cloud Storage)

## Lokal ishga tushirish
```bash
cp backend/.env.example backend/.env
docker compose up --build
```
API hujjatlari: http://localhost:8000/docs

## Tuzilma
- `backend/` - REST API va tavsiya moduli
- `database/schema.sql` - baza sxemasi
- `frontend/` - React ilovasi (keyingi bosqich)
- `docs/diagrams/` - PlantUML diagrammalar
