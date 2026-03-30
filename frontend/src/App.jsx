import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import AddVehicle from './pages/AddVehicle'
import RemoveVehicle from './pages/RemoveVehicle'
import BookParking from './pages/BookParking'
import ViewBookings from './pages/ViewBookings'
import ViewTickets from './pages/ViewTickets'

function App() {
  return (
    <BrowserRouter>
      <div className="app-wrapper">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/add-vehicle" element={<AddVehicle />} />
            <Route path="/remove-vehicle" element={<RemoveVehicle />} />
            <Route path="/book-parking" element={<BookParking />} />
            <Route path="/view-bookings" element={<ViewBookings />} />
            <Route path="/view-tickets" element={<ViewTickets />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
