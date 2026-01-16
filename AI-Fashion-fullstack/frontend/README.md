# 🎨 AI Fashion Assistant - Frontend

React-based frontend with authentication and search functionality.

## ✅ Features

- 🔐 JWT Authentication (Login/Register)
- 🔍 Text, Image & Multimodal Search
- 💬 AI Chat Interface
- ❤️ Favorites Management
- 👤 User Profile & Preferences
- ✨ Personalized Results

## 🚀 Quick Start

### Windows

```cmd
REM Setup (first time)
setup_windows.bat

REM Run
run_frontend.bat
```

### Manual Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

## 📂 Project Structure

```
src/
├── components/          # Reusable components
│   └── ProtectedRoute.jsx
├── contexts/           # React contexts
│   └── AuthContext.jsx
├── pages/              # Page components
│   ├── LoginPage.jsx
│   ├── RegisterPage.jsx
│   ├── SearchPage.jsx
│   ├── ChatPage_updated.jsx
│   ├── FavoritesPage.jsx
│   └── ProfilePage.jsx
├── services/           # API services
│   └── api.js
├── App.jsx             # Main app component
└── main.jsx            # Entry point
```

## 🔧 Configuration

Create `.env` file:

```env
VITE_API_URL=http://localhost:8000/api
```

## 📦 Dependencies

- React 18.2
- React Router DOM 6.20
- Axios 1.6
- Lucide React (icons)
- Vite 5.0

## 🎯 Available Pages

- `/` - Home
- `/login` - Login
- `/register` - Register
- `/search` - Product Search
- `/chat` - AI Chat
- `/favorites` - My Favorites
- `/profile` - User Profile

## 🔐 Authentication

JWT tokens are stored in `localStorage`:
- `access_token` - Main token (30min)
- `refresh_token` - Refresh token (7 days)

Auto-refresh on 401 errors.

## 🎨 Styling

Uses inline styles with CSS variables from `index.css`.

Dark mode by default, light mode responsive.

## 🚀 Build for Production

```bash
npm run build
```

Output in `dist/` folder.

## 🆘 Troubleshooting

### Port already in use
```bash
# Change port in vite.config.js
server: { port: 3000 }
```

### API connection error
Check `VITE_API_URL` in `.env` and ensure backend is running.

### Dependencies error
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📞 Support

Check backend logs for API errors.
Use browser DevTools Console for frontend errors.

---

**Made with ❤️ for AI Fashion Assistant v2.5**
