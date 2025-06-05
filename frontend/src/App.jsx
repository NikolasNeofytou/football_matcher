import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Schedule from './components/Schedule'
import ReservationForm from './components/ReservationForm'
import Login from './components/Login'
import Register from './components/Register'
import Profile from './components/Profile'
import Leaderboard from './components/Leaderboard'

function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Schedule</Link> |{' '}
        <Link to="/leaderboard">Leaderboard</Link> |{' '}
        <Link to="/profile">Profile</Link> |{' '}
        <Link to="/login">Login</Link> |{' '}
        <Link to="/register">Register</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Schedule />} />
        <Route path="/reserve" element={<ReservationForm />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
