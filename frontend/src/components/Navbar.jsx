import { Link, NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Home' },
  { to: '/add-vehicle', label: 'Add Vehicle' },
  { to: '/remove-vehicle', label: 'Remove Vehicle' },
  { to: '/book-parking', label: 'Book Parking' },
  { to: '/view-bookings', label: 'My Booking' },
  { to: '/view-tickets', label: 'My Tickets' },
]

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        Smart<span>Park</span>
      </Link>
      <ul className="navbar-links">
        {links.map(({ to, label }) => (
          <li key={to}>
            <NavLink
              to={to}
              end={to === '/'}
              className={({ isActive }) => (isActive ? 'active' : '')}
            >
              {label}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}
