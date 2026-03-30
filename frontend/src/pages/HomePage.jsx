import { Link } from 'react-router-dom'

const cards = [
  {
    to: '/add-vehicle',
    icon: '🚗',
    title: 'Add Vehicle',
    desc: 'Register your vehicle with a license plate to get started.',
  },
  {
    to: '/remove-vehicle',
    icon: '🗑️',
    title: 'Remove Vehicle',
    desc: 'Deregister a vehicle. The record is suspended but billing history is preserved.',
  },
  {
    to: '/book-parking',
    icon: '🅿️',
    title: 'Book Parking',
    desc: 'Browse available lots, pick a spot, and confirm your reservation.',
  },
  {
    to: '/view-bookings',
    icon: '📋',
    title: 'My Booking',
    desc: 'View your active booking on the lot grid and cancel if needed.',
  },
  {
    to: '/view-tickets',
    icon: '🎟️',
    title: 'My Tickets',
    desc: 'Review your full parking and violation ticket history.',
  },
]

export default function HomePage() {
  return (
    <div>
      <div className="home-hero">
        <h1>
          Smart<span>Park</span>
        </h1>
        <p>Real-time parking availability, dynamic pricing, and easy reservations — all in one place.</p>
      </div>

      <div className="home-grid">
        {cards.map(({ to, icon, title, desc }) => (
          <Link key={to} to={to} className="home-card">
            <span className="home-card-icon">{icon}</span>
            <h2>{title}</h2>
            <p>{desc}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
