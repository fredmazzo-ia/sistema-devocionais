import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import NewsList from './components/NewsList'
import Notifications from './components/Notifications'
import MonitoringStatus from './components/MonitoringStatus'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-title">📰 Monitoramento de Notícias</h1>
            <div className="nav-links">
              <Link to="/">Dashboard</Link>
              <Link to="/news">Notícias</Link>
              <Link to="/notifications">Notificações</Link>
              <Link to="/monitoring">Monitoramento</Link>
            </div>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/news" element={<NewsList />} />
            <Route path="/notifications" element={<Notifications />} />
            <Route path="/monitoring" element={<MonitoringStatus />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App

