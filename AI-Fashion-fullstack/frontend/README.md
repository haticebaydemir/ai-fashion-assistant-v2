# 🎨 AI Fashion Assistant - Frontend

![Frontend Overview](../screenshots/Anasayfa.jpg)

Modern React-based frontend with authentication, search, and AI chat functionality.

---

## ✅ Features Overview

### 🏠 Landing & Home Pages

<table>
<tr>
<td width="50%">

**Landing Page (Logged Out)**
![Landing](../screenshots/Anasayfa.jpg)

Features showcase with call-to-action

</td>
<td width="50%">

**Personalized Home (Logged In)**
![Home Logged In](../screenshots/Anasayfa2.jpg)

Welcome message with active personalization

</td>
</tr>
</table>

### 🔐 Authentication System

<table>
<tr>
<td width="50%">

**Login Page**
![Login](../screenshots/LoginPage.jpg)

- JWT Authentication
- Email + Password
- "Remember Me" option
- Link to registration

</td>
<td width="50%">

**Registration Page**
![Register](../screenshots/CreateAccount.jpg)

- Full name validation
- Email verification
- Password strength check
- Confirm password

</td>
</tr>
</table>

**Authentication Features:**
- JWT token-based auth
- Access token (30 min lifetime)
- Refresh token (7 days)
- Auto-refresh on 401 errors
- Protected routes
- Persistent sessions in localStorage

---

### 🔍 Search Capabilities

#### Text Search
![Text Search](../screenshots/TextSearchWithResults.jpg)

**Features:**
- Semantic search powered by MPNet (768d embeddings)
- Real-time results as you type
- Personalization toggle
- Shows similarity scores
- Favorite button on each product
- Grid layout with product cards

**Example queries:**
- "red cap" - Color-based search
- "black dress" - Style search
- "running shoes" - Category search
- "formal evening wear" - Complex queries

#### Image Search

<table>
<tr>
<td width="50%">

**Upload Interface**
![Image Upload](../screenshots/İmageSearch.jpg)

- Drag & drop support
- File browser
- Image preview
- Personalization option

</td>
<td width="50%">

**Search Results**
![Image Results](../screenshots/İmageSearchResults.jpg)

- CLIP-powered similarity
- Visual similarity scores
- Similar product grid
- Quick add to favorites

</td>
</tr>
</table>

#### Multimodal Search
![Multimodal](../screenshots/MultimodalSearch.jpg)

**Combine text and image for best results:**
- Text query: "black shoes"
- Reference image: Upload shoe style
- Combined embeddings
- More precise matching
- Higher accuracy

**Use cases:**
- "Find this dress in blue"
- "Similar style but formal"
- "Same pattern different color"

---

### 💬 AI Chat Interface

<table>
<tr>
<td width="50%">

**Turkish Chat**
![Chat TR](../screenshots/ChatbotTC.jpg)

Natural conversation in Turkish with product recommendations

</td>
<td width="50%">

**English Chat**
![Chat EN](../screenshots/Ekran_AlıntısıChatbot.PNG)

Llama-3.3-70B powered multilingual support

</td>
</tr>
</table>

**Chat Features:**
- Natural language understanding
- Product recommendations with images
- Similarity scoring
- Personalization toggle
- Context-aware responses
- Conversation history
- Multi-turn dialogue
- Favorite products directly from chat

**Example conversations:**
- "I need a black evening dress"
- "Show me casual summer outfits"
- "What goes well with blue jeans?"
- "I want 1950s style red wedding dress"

---

### ❤️ Favorites Management
![Favorites](../screenshots/Favorites.jpg)

**Features:**
- Save unlimited favorites
- Grid view of saved items
- Product details on each card
- Remove from favorites
- Quick search from favorites
- Organized by date added

**Product Card Details:**
- Product image
- Product name
- Category (Apparel, Accessories, etc.)
- Color information
- Date added
- One-click remove button

---

### 👤 User Profile & Preferences
![Profile](../screenshots/Profile.jpg)

**Profile Sections:**

1. **Account Information**
   - Email display
   - Account type

2. **Style Preferences** (Select multiple)
   - Casual
   - Formal
   - Sportswear
   - Streetwear
   - Elegant
   - Bohemian

3. **Size Preferences**
   - XS, S, M, L, XL, XXL
   - Single or multiple selection

4. **Favorite Colors** (Boost search results)
   - Black, White, Blue, Red
   - Green, Yellow, Pink, Navy
   - Gray, Brown

**How Personalization Works:**
- Selected preferences boost matching products
- Favorite colors get priority in results
- Preferred styles ranked higher
- Size filtering for better matches
- Real-time preference updates

---

## 🚀 Quick Start

### Windows

```cmd
REM Setup (first time)
setup_frontend.bat

REM Run development server
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

---

## 📂 Project Structure

```
frontend/
├── src/
│   ├── components/              # Reusable components
│   │   └── ProtectedRoute.jsx  # Route protection
│   ├── contexts/               # React contexts
│   │   └── AuthContext.jsx     # Auth state management
│   ├── pages/                  # Page components
│   │   ├── HomePage.jsx        # Landing page
│   │   ├── LoginPage.jsx       # Login interface
│   │   ├── RegisterPage.jsx    # Registration
│   │   ├── SearchPage.jsx      # Search interface
│   │   ├── ChatPage.jsx        # AI chat
│   │   ├── FavoritesPage.jsx   # Saved products
│   │   └── ProfilePage.jsx     # User profile
│   ├── services/               # API services
│   │   └── api.js              # Backend communication
│   ├── App.jsx                 # Main app component
│   ├── main.jsx                # Entry point
│   └── index.css               # Global styles
├── public/                     # Static assets
├── index.html                  # HTML template
├── vite.config.js              # Vite configuration
├── package.json                # Dependencies
├── setup_frontend.bat          # Windows setup script
└── run_frontend.bat            # Windows run script
```

---

## 🔧 Configuration

Create `.env` file in frontend directory:

```env
VITE_API_URL=http://localhost:8000/api
```

For production:
```env
VITE_API_URL=https://your-api-domain.com/api
```

---

## 📦 Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }
}
```

---

## 🎯 Available Routes

| Route | Page | Description | Auth Required |
|-------|------|-------------|---------------|
| `/` | Home | Landing page | ❌ |
| `/login` | Login | User authentication | ❌ |
| `/register` | Register | New user registration | ❌ |
| `/search` | Search | Product search (text/image/multimodal) | ✅ |
| `/chat` | Chat | AI chat assistant | ✅ |
| `/favorites` | Favorites | Saved products | ✅ |
| `/profile` | Profile | User settings & preferences | ✅ |

---

## 🔐 Authentication Flow

```
1. User Registration
   └─> POST /api/auth/register
       └─> Validation
           └─> User created in MongoDB
               └─> Auto-login with JWT tokens

2. User Login
   └─> POST /api/auth/login
       └─> Credentials check
           └─> JWT tokens generated
               ├─> access_token (30min)
               └─> refresh_token (7 days)
                   └─> Stored in localStorage
                       └─> Redirect to home

3. Protected Route Access
   └─> Check localStorage for tokens
       ├─> Valid? → Allow access
       └─> Expired? → Refresh token
           ├─> Success → New access_token
           └─> Fail → Redirect to login

4. Logout
   └─> Clear localStorage
       └─> Redirect to home
```

---

## 🎨 Styling

**Approach:** Modern CSS with custom properties

**Color Scheme:**
```css
:root {
  --primary: #6366f1;          /* Indigo */
  --primary-dark: #4f46e5;
  --secondary: #8b5cf6;         /* Purple */
  --accent: #ec4899;            /* Pink */
  --background: #f8fafc;
  --surface: #ffffff;
  --text: #1e293b;
  --text-light: #64748b;
  --border: #e2e8f0;
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
}
```

**Typography:**
- Font: System fonts (San Francisco, Segoe UI, Roboto)
- Base size: 16px
- Line height: 1.5
- Heading scale: 1.25 ratio

**Layout:**
- Max width: 1400px
- Grid: CSS Grid for product layouts
- Flexbox: Component layouts
- Responsive: Mobile-first approach

---

## 🎬 User Journey Examples

### First-Time User
1. **Land on homepage** (Anasayfa.jpg)
   - See feature overview
   - Click "Get Started" or "Register"

2. **Create account** (CreateAccount.jpg)
   - Fill registration form
   - Auto-login after registration

3. **Welcome back** (Anasayfa2.jpg)
   - Personalized greeting
   - Feature cards now active

4. **Set preferences** (Profile.jpg)
   - Choose styles (Casual, Formal, etc.)
   - Select sizes
   - Pick favorite colors

5. **First search** (TextSearchWithResults.jpg)
   - Try text search: "red cap"
   - See personalized results
   - Add to favorites

6. **Try chat** (ChatbotTC.jpg)
   - Ask: "Show me black dresses"
   - Get recommendations
   - Click products to favorite

### Returning User
1. **Login** (LoginPage.jpg)
   - Email + Password
   - Auto-redirect to home

2. **Check favorites** (Favorites.jpg)
   - View saved products
   - Remove unwanted items

3. **Image search** (İmageSearch.jpg + İmageSearchResults.jpg)
   - Upload reference image
   - Find similar products
   - Personalization active

4. **Multimodal search** (MultimodalSearch.jpg)
   - Combine text + image
   - Get precise matches

---

## 🚀 Build for Production

### Build command:
```bash
npm run build
```

Output structure:
```
dist/
├── index.html
├── assets/
│   ├── index-[hash].js
│   ├── index-[hash].css
│   └── [other assets]
└── [static files]
```

### Deploy to Vercel:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Deploy to Netlify:
```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod --dir=dist
```

---

## 🆘 Troubleshooting

### Port already in use
```bash
# Kill process on port 5173
netstat -ano | findstr :5173
taskkill /PID [PID] /F

# Or change port in vite.config.js
export default {
  server: { port: 3000 }
}
```

### API connection error
1. Check `VITE_API_URL` in `.env`
2. Ensure backend is running: http://localhost:8000/docs
3. Check browser console for CORS errors
4. Verify network requests in DevTools

### Dependencies error
```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Authentication issues
1. Check JWT tokens in localStorage
2. Verify token expiration
3. Test login endpoint in backend docs
4. Clear localStorage and re-login

### Search not working
1. Backend ML models loaded?
2. Check API endpoint responses
3. Verify GROQ API key (for chat)
4. Test search in backend docs first

---

## 🎯 Performance Tips

### Optimization:
- Lazy load routes: `React.lazy()`
- Image optimization: Use WebP format
- Code splitting: Automatic with Vite
- Memoization: Use `React.memo()` for heavy components
- Debounce: Search input (300ms delay)

### Bundle Size:
- Initial: ~150 KB (gzipped)
- Vendor: ~130 KB (React, Router, Axios)
- Total: ~280 KB

---

## 📊 Component Overview

### Key Components

**ProductCard:**
- Reusable product display
- Image with lazy loading
- Name, category, color
- Favorite button
- Hover effects

**SearchBar:**
- Text input with debounce
- Clear button
- Search suggestions (future)
- Loading state

**ImageUpload:**
- Drag & drop zone
- File input fallback
- Preview with remove
- Size validation

**ChatMessage:**
- User vs AI styling
- Product recommendations
- Timestamps
- Copy/share options

---

## 📞 Support

### Debug Tools:
- **Browser Console:** F12 → Console
- **Network Tab:** F12 → Network
- **React DevTools:** Chrome extension
- **Redux DevTools:** For state debugging

### Common Issues:
| Issue | Solution |
|-------|----------|
| White screen | Check console for errors |
| Login fails | Verify backend is running |
| Search empty | Check ML models loaded |
| Chat not working | Verify GROQ API key |
| Favorites not saving | Check authentication |

---

## 🧪 Testing

### Manual Testing Checklist:
- [ ] Register new user
- [ ] Login existing user
- [ ] Text search works
- [ ] Image search works
- [ ] Multimodal search works
- [ ] Chat responds
- [ ] Favorites add/remove
- [ ] Profile saves preferences
- [ ] Logout works
- [ ] Protected routes redirect
- [ ] Personalization toggle works
- [ ] Responsive on mobile

---

## 📸 Screenshots Index

All frontend screenshots:

1. **Anasayfa.jpg** - Landing page (logged out)
2. **Anasayfa2.jpg** - Home page (logged in)
3. **LoginPage.jpg** - Login interface
4. **CreateAccount.jpg** - Registration form
5. **SearchPage.jpg** - Empty search page
6. **TextSearchWithResults.jpg** - Text search with results
7. **İmageSearch.jpg** - Image upload interface
8. **İmageSearchResults.jpg** - Image search results
9. **MultimodalSearch.jpg** - Combined search
10. **ChatbotTC.jpg** - Chat (Turkish)
11. **Ekran_AlıntısıChatbot.PNG** - Chat (English)
12. **Favorites.jpg** - Favorites page
13. **Profile.jpg** - Profile & preferences

---

## 🎓 Learning Resources

**React:**
- https://react.dev/
- https://react.dev/learn

**Vite:**
- https://vitejs.dev/
- https://vitejs.dev/guide/

**React Router:**
- https://reactrouter.com/
- https://reactrouter.com/en/main/start/tutorial

**Axios:**
- https://axios-http.com/
- https://axios-http.com/docs/intro

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share feedback

---

**Made with ❤️ for AI Fashion Assistant v3.0**  
**Status:** Production Ready ✅  
**Last Updated:** January 2026  
**Framework:** React 18 + Vite 5
