// import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
// import Login from './Login.jsx';
import Logout from './Logout.jsx';
import HomePage from './pages/HomePage.jsx';
import Register from './pages/Register.jsx';
import LoginPage from './pages/LoginPage.jsx';
import MonitoringPage from './pages/MonitoringPage.jsx';
import LightPage from './pages/LightPage.jsx';
import MotionPage from './pages/MotionPage.jsx';
import MyFunctionsPage from './pages/MyFunctionsPage.jsx';
import HelpPage from './pages/HelpPage.jsx';
import TelegramPage from './pages/TelegramPage.jsx';
import CalendarPlanPage from './pages/CalendarPlanPage.jsx';
import SettingsPage from './pages/SettingsPage.jsx';
import BudgetPage from './pages/BudgetPage.jsx';

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<LoginPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/logout" element={<Logout />} />
      <Route path="/home" element={<HomePage />} />
      <Route path="/register" element={<Register />} />
      <Route path="/motion" element={<MotionPage />} />
      <Route path="/monitoring" element={<MonitoringPage />} />
      <Route path="/light" element={<LightPage />} />
      <Route path="/functions" element={<MyFunctionsPage />} />
      <Route path='/help' element={<HelpPage />} />
      <Route path='/telegram' element={<TelegramPage />} />
      <Route path="/calendarplan" element={<CalendarPlanPage />} />
      <Route path='/settings' element={<SettingsPage />} />
      <Route path='/budget' element={<BudgetPage />} />
      </Routes>
    </Router>
  );
}

export default App;