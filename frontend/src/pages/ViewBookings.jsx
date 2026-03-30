import { useState } from 'react'
import { getCurrentBooking, cancelBooking, getLotSpots } from '../api/client'
import ParkingGrid from '../components/ParkingGrid'

export default function ViewBookings() {
  const [licensePlate, setLicensePlate] = useState('')
  const [accessKey, setAccessKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [booking, setBooking] = useState(null)       // current booking / ticket
  const [spots, setSpots] = useState([])             // spots for booking's lot
  const [yourSpotId, setYourSpotId] = useState(null) // the booked spot_id

  const [cancelLoading, setCancelLoading] = useState(false)
  const [cancelError, setCancelError] = useState('')
  const [cancelDone, setCancelDone] = useState(false)

  // Store creds for cancel
  const [savedCreds, setSavedCreds] = useState(null)

  async function handleSearch(e) {
    e.preventDefault()
    setError('')
    setBooking(null)
    setSpots([])
    setCancelDone(false)
    setCancelError('')

    const plate = licensePlate.trim().toUpperCase()
    if (!plate) return setError('Please enter your license plate.')
    if (!accessKey.trim()) return setError('Please enter your password.')

    setLoading(true)
    try {
      const data = await getCurrentBooking(plate, accessKey.trim())

      if (!data || !data.ticket_id) {
        setBooking(null)
      } else {
        setBooking(data)
        setSavedCreds({ plate, accessKey: accessKey.trim() })
        setYourSpotId(data.spot_id)

        // Load the lot grid
        const lotSpots = await getLotSpots(data.lot_id)
        setSpots(lotSpots)
      }
    } catch (err) {
      // 404 = no active booking
      if (err.message.includes('404') || err.message.toLowerCase().includes('no booking') || err.message.toLowerCase().includes('not found')) {
        setBooking(null)
        setError('No active booking found for this vehicle.')
      } else {
        setError(err.message)
      }
    } finally {
      setLoading(false)
    }
  }

  async function handleCancel() {
    const confirmed = window.confirm('Are you sure you want to cancel your booking?')
    if (!confirmed) return

    setCancelError('')
    setCancelLoading(true)
    try {
      await cancelBooking(booking.ticket_id, savedCreds.plate, savedCreds.accessKey)
      setCancelDone(true)
      setBooking(null)
      setSpots([])
    } catch (err) {
      setCancelError(err.message)
    } finally {
      setCancelLoading(false)
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1>My Booking</h1>
        <p>View your active booking and cancel if needed.</p>
      </div>

      {/* Login form */}
      <div className="card" style={{ maxWidth: 480, marginBottom: 24 }}>
        {error && <div className="alert alert-error">{error}</div>}
        {cancelDone && (
          <div className="alert alert-success">Booking cancelled successfully.</div>
        )}

        <form onSubmit={handleSearch}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="lp">License Plate *</label>
              <input
                id="lp"
                type="text"
                placeholder="ABC 1234"
                value={licensePlate}
                onChange={(e) => setLicensePlate(e.target.value)}
                maxLength={11}
                required
                autoFocus
              />
            </div>
            <div className="form-group">
              <label htmlFor="ak">Password *</label>
              <input
                id="ak"
                type="password"
                placeholder="Your password"
                value={accessKey}
                onChange={(e) => setAccessKey(e.target.value)}
                required
              />
            </div>
          </div>
          <button className="btn btn-primary btn-full" type="submit" disabled={loading}>
            {loading ? <><span className="spinner" /> Searching…</> : 'Find My Booking'}
          </button>
        </form>
      </div>

      {/* Active booking */}
      {booking && (
        <div className="card">
          <div className="section-title">Active Booking</div>

          <div className="booking-detail">
            <div className="booking-detail-item">
              <div className="label">Lot</div>
              <div className="value">{booking.lot_name}</div>
            </div>
            <div className="booking-detail-item">
              <div className="label">Spot</div>
              <div className="value">#{booking.spot_number}</div>
            </div>
            <div className="booking-detail-item">
              <div className="label">Start</div>
              <div className="value">{new Date(booking.start_time).toLocaleString()}</div>
            </div>
            <div className="booking-detail-item">
              <div className="label">Duration</div>
              <div className="value">{booking.duration}h</div>
            </div>
            <div className="booking-detail-item">
              <div className="label">Amount</div>
              <div className="value">${parseFloat(booking.amount).toFixed(2)}</div>
            </div>
            <div className="booking-detail-item">
              <div className="label">Ticket ID</div>
              <div className="value">#{booking.ticket_id}</div>
            </div>
          </div>

          {/* Lot grid */}
          {spots.length > 0 && (
            <div style={{ marginBottom: 20 }}>
              <div className="section-title">Lot Grid — {booking.lot_name}</div>
              <ParkingGrid spots={spots} yourSpotId={yourSpotId} />
            </div>
          )}

          {cancelError && <div className="alert alert-error">{cancelError}</div>}

          <button
            className="btn btn-danger"
            onClick={handleCancel}
            disabled={cancelLoading}
          >
            {cancelLoading ? <><span className="spinner" /> Cancelling…</> : 'Cancel Booking'}
          </button>
        </div>
      )}
    </div>
  )
}
