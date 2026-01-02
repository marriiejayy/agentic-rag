# 🌍 Travel Planner & Activity Finder

A modern, full-featured travel planning application that helps users discover destinations, plan trips, and find activities based on weather, location, and preferences.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://your-deployment-url.vercel.app)
[![React](https://img.shields.io/badge/React-19.2.0-blue)](https://reactjs.org)
[![Vite](https://img.shields.io/badge/Vite-7.2.2-purple)](https://vitejs.dev)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.1.17-38B2AC)](https://tailwindcss.com)

## ✨ Features

### 🗺️ Destination Discovery
- **Global Search** - Find destinations worldwide
- **Seasonal Recommendations** - Best places to visit based on time of year
- **Visual Previews** - Beautiful destination photos from Unsplash
- **Budget Filtering** - Filter by cost range ($ - $$$$)

### ⛅ Smart Trip Planning
- **Weather-Aware Planning** - Forecast integration for selected dates
- **Activity Suggestions** - Local attractions, restaurants, and points of interest
- **Packing List Generator** - Custom lists based on weather and activities
- **Budget Calculator** - Real-time currency conversion

### 🗓️ Interactive Tools
- **Trip Builder** - Drag-and-drop itinerary planning
- **Interactive Map** - Visual exploration with weather overlays
- **Multi-Day Forecasts** - Weather timeline for entire trip duration
- **Cost Breakdown** - Automatic budget tracking with currency conversion

### 🌐 Multi-API Integration
- **WeatherAPI.com** - Accurate weather forecasts
- **OpenCage** - Geocoding and location services
- **Unsplash** - High-quality destination photos
- **Foursquare** - Local attractions and venues
- **ExchangeRate-API** - Real-time currency conversion

## 🚀 Tech Stack

- **Frontend:** React 19.2.0 with Hooks
- **Build Tool:** Vite 7.2.2
- **Styling:** Tailwind CSS v4.1.17 (CSS-first approach)
- **Maps:** Leaflet/OpenStreetMap
- **Icons:** React Icons
- **Deployment:** Vercel

## 📦 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner
```

2. **Install dependencies**
```bash
npm install
```

3. **Set up environment variables**
```bash
cp .env.example .env.local
```
Edit `.env.local` and add your API keys:
```env
VITE_APP_WEATHERAPI_KEY=your_weatherapi_key
VITE_APP_OPENCAGE_KEY=your_opencage_key
VITE_APP_UNSPLASH_KEY=your_unsplash_key
VITE_APP_FOURSQUARE_CLIENT_ID=your_foursquare_client_id
VITE_APP_FOURSQUARE_CLIENT_SECRET=your_foursquare_client_secret
VITE_APP_EXCHANGERATE_KEY=your_exchangerate_key
```

4. **Run development server**
```bash
npm run dev
```

5. **Build for production**
```bash
npm run build
npm run preview
```

## 🔑 API Keys Required

| Service | Free Tier | Purpose | Sign-up Link |
|---------|-----------|---------|--------------|
| WeatherAPI.com | 1M calls/month | Weather forecasts | [Sign up](https://www.weatherapi.com/) |
| OpenCage Geocoding | 2,500 calls/day | Location search | [Sign up](https://opencagedata.com/) |
| Unsplash API | 50 calls/hour | Destination photos | [Sign up](https://unsplash.com/developers) |
| Foursquare Places | 5,000 calls/day | Attractions & venues | [Sign up](https://developer.foursquare.com/) |
| ExchangeRate-API | 1,500 calls/month | Currency conversion | [Sign up](https://www.exchangerate-api.com/) |

## 📁 Project Structure

```
travel-planner/
├── src/
│   ├── components/
│   │   ├── DestinationCard.jsx      # Destination display card
│   │   ├── TripBuilder.jsx          # Interactive trip planner
│   │   ├── MapExplorer.jsx          # Interactive map component
│   │   ├── WeatherTimeline.jsx      # Multi-day weather forecast
│   │   └── PackingList.jsx          # Dynamic packing list generator
│   ├── hooks/
│   │   ├── useDestinations.js       # Destination data fetching
│   │   ├── useTripPlanner.js        # Trip state management
│   │   ├── useWeatherForecast.js    # Weather data handling
│   │   └── useCurrencyConverter.js  # Real-time currency conversion
│   ├── utils/
│   │   ├── api.js                   # API configuration
│   │   └── helpers.js               # Utility functions
│   ├── styles/
│   │   └── index.css                # Custom styles
│   ├── App.jsx                      # Main application component
│   └── main.jsx                     # Application entry point
├── public/                          # Static assets
├── .env.example                     # Environment variables template
├── vite.config.js                   # Vite configuration
└── package.json                     # Dependencies and scripts
```

## 🎯 Key Components

### DestinationCard
Displays destination information with photos, weather, and quick actions.

### TripBuilder
Interactive itinerary planner with drag-and-drop functionality and day-by-day planning.

### MapExplorer
Interactive map showing destinations, weather overlays, and points of interest.

### WeatherTimeline
Visual weather forecast display for selected travel dates with activity compatibility.

## 🛠️ Development Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## 🚢 Deployment

### Deploy to Vercel (Recommended)
```bash
npm run build
vercel --prod
```

Or connect your GitHub repository to Vercel for automatic deployments.

### Environment Variables in Production
Remember to set all environment variables in your deployment platform (Vercel, Netlify, etc.).

## 🧪 Testing

Manual testing areas:
1. **Destination Search** - Try various city names and countries
2. **Trip Planning** - Create multi-day itineraries
3. **Weather Integration** - Check forecast accuracy
4. **Currency Conversion** - Test different currency pairs
5. **Responsive Design** - Test on mobile, tablet, and desktop

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [WeatherAPI.com](https://www.weatherapi.com/) for weather data
- [Unsplash](https://unsplash.com) for beautiful destination photos
- [OpenCage](https://opencagedata.com) for geocoding services
- [Foursquare](https://foursquare.com) for places data
- [ExchangeRate-API](https://www.exchangerate-api.com) for currency conversion

