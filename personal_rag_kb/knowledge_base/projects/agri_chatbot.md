# Farm AI Assistant

An AI-powered farming helper for African farmers.

##  What It Does

1. **AI Chatbot** - Ask farming questions
2. **📊 Live Data** - Weather & crop prices  
3. **🐛 Pest Info** - Learn about pests/diseases

## 🚀 Quick Start

### 1. Setup Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

Create `.env` file:
```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/agriculture_db
OPENAI_API_KEY=sk-your-key-here
```

### 2. Setup Frontend
```bash
cd frontend
npm install
```

### 3. Run
```bash
# Terminal 1 - Backend
cd backend
python main.py  # Runs on http://localhost:8000

# Terminal 2 - Frontend  
cd frontend
npm run dev  # Runs on http://localhost:3000
```

## 📁 Files

```
backend/
├── main.py          # Server start
├── database.py      # Database connection
├── models.py        # Database tables
├── routers/         # API routes
│   ├── chat.py      # AI chatbot
│   ├── live_data.py # Weather/prices
│   └── pests.py     # Pest info
└── .env             # Your keys/passwords

frontend/
├── src/
│   ├── App.jsx      # Main app
│   ├── pages/       # 3 main pages
│   └── index.css    # Styling
└── package.json     # Frontend dependencies
```

## 🌐 API Endpoints

- `POST /api/chat` - Ask farming questions
- `GET /api/live-data` - Get weather & prices
- `POST /api/pests` - Get pest information

## 🔧 Troubleshooting

**Database error?**
```sql
CREATE DATABASE agriculture_db;
```

**No styling?**
```bash
cd frontend
npm install tailwindcss postcss autoprefixer
```

**OpenAI error?**
Get API key from: https://platform.openai.com/api-keys

## 📞 Support

Check `http://localhost:8000/docs` for API details.

---

**Simple farming advice for African farmers** 🌱