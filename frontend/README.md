# Outbreak Prediction System - Frontend

Real-time outbreak prediction dashboard built with React, TypeScript, and TailwindCSS.

## Features

- 🌐 **WebSocket Connection**: Real-time updates from prediction backend
- 📊 **District Dashboard**: Visual cards for each district's outbreak status
- 🚨 **Outbreak Alerts**: Toast notifications for detected outbreaks
- 📋 **Live Logs**: Scrollable log viewer for debugging
- 📱 **Responsive Design**: Mobile-friendly layout

## Prerequisites

- Node.js 18+
- npm or yarn

## Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Configuration

Create a `.env` file (optional) to override defaults:

```env
VITE_WS_URL=ws://localhost:8000/ws
VITE_API_URL=http://localhost:8000
```

**Default Values:**
- WebSocket URL: `ws://localhost:8000/ws`
- API URL: `http://localhost:8000`

## Running the Application

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx        # Main dashboard with district grid
│   │   ├── DistrictCard.tsx     # Individual district card
│   │   ├── LiveLogViewer.tsx    # Prediction log viewer
│   │   ├── NotificationSystem.tsx # Toast alerts
│   │   └── index.ts
│   ├── hooks/
│   │   ├── useWebSocket.ts      # WebSocket connection hook
│   │   └── index.ts
│   ├── utils/
│   │   ├── types.ts             # TypeScript interfaces
│   │   ├── constants.ts         # App constants & utilities
│   │   └── index.ts
│   ├── App.tsx                  # Main application
│   ├── main.tsx                 # Entry point
│   └── index.css                # TailwindCSS styles
├── public/
├── index.html
├── package.json
├── vite.config.ts
└── README.md
```

## Usage

1. Start the backend server first
2. Run `npm run dev` to start the frontend
3. Open `http://localhost:5173` in your browser
4. The dashboard will automatically connect to the WebSocket server
5. Predictions will appear every 10 seconds

## Alert Thresholds

Outbreak alerts are triggered when:
- `outbreak_flag === true`
- `outbreak_prob > 0.6`

## Technologies

- React 18
- TypeScript
- Vite
- TailwindCSS
- WebSocket API

## License

MIT
