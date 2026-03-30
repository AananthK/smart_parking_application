import { useState, useEffect } from 'react'
import { getLots, getLotSpots, createBooking } from '../api/client'
import ParkingGrid from '../components/ParkingGrid'

function LotStatusBadge({ status }) {
  const cls = { OPEN: 'badge-open', FULL: 'badge-full', CLOSED: 'badge-closed' }[status] || 'badge-closed'
  return <span className={`lot-status-badge ${cls}`}>{status}</span>
}

export default function BookParking() {
  // Step 1 — lot selection
  const [lots, setLots] = useState([])
  const [lotsLoading, setLotsLoading] = useState(true)
  const [lotsError, setLotsError] = useState('')
  const [selectedLot, setSelectedLot] = useState(null)

  // Step 2 — spot selection
  const [spots, setSpots] = useState([])
  const [spotsLoading, setSpotsLoading] = useState(false)
  const [spotsError, setSpotsError] = useState('')
  const [selectedSpot, setSelectedSpot] = useState(null)

  // Step 3 — booking form
  const [licensePlate, setLicensePlate] = useState('')
  const [accessKey, setAccessKey] = useState('')
  const [startTime, setStartTime] = useState(defaultDateTime())
  const [duration, setDuration] = useState(1)
  const [bookingLoading, setBookingLoading] = useState(false)
  const [bookingError, setBookingError] = useState('')
  const [bookingResult, setBookingResult] = useState(null)

  function defaultDateTime() {
    const now = new Date()
    now.setSeconds(0, 0)
    return now.toISOString().slice(0, 16)
  }

  useEffect(() => {
    setLotsLoading(true)
    getLots()
      .then(setLots)
      .catch((err) => setLotsError(err.message))
      .finally(() => setLotsLoading(false))
  }, [])

  function handleLotSelect(lot) {
    if (lot.lot_status !== 'OPEN') return
    setSelectedLot(lot)
    setSelectedSpot(null)
    setBookingError('')
    setBookingResult(null)
    setSpotsError('')
    setSpotsLoading(true)
    getLotSpots(lot.lot_id)
      .then(setSpots)
      .catch((err) => setSpotsError(err.message))
      .finally(() => setSpotsLoading(false))
  }

  function refreshSpots() {
    if (!selectedLot) return
    setSpotsLoading(true)
    getLotSpots(selectedLot.lot_id)
      .then(setSpots)
      .catch((err) => setSpotsError(err.message))
      .finally(() => setSpotsLoading(false))
  }

  async function handleBook(e) {
    e.preventDefault()
    setBookingError('')

    if (!selectedSpot) return setBookingError('Please select a parking spot first.')
    const plate = licensePlate.trim().toUpperCase()
    if (!plate) return setBookingError('Please enter your license plate.')
    if (!accessKey.trim()) return setBookingError('Please enter your password.')
    if (!startTime) return setBookingError('Please choose a start time.')
    if (duration < 1 || duration > 24) return setBookingError('Duration must be between 1 and 24 hours.')

    setBookingLoading(true)
    try {
      const data = await createBooking(plate, accessKey.trim(), selectedSpot.spot_id, startTime, Number(duration))
      setBookingResult(data)
      setSelectedSpot(null)
      refreshSpots()
    } catch (err) {
      setBookingError(err.message)
    } finally {
      setBookingLoading(false)
    }
  }

  const estimatedCost = selectedLot
    ? (parseFloat(selectedLot.base_price) * duration).toFixed(2)
    : '0.00'

  if (bookingResult) {
    return (
      <div>
        <div className="page-header">
          <h1>Book Parking</h1>
        </div>
        <div className="card" style={{ maxWidth: 520 }}>
          <div className="alert alert-success">Booking confirmed!</div>
          <div style={{ marginBottom: 16 }}>
            <div className="info-row"><span className="key">Lot</span><span className="val">{bookingResult.lot_name}</span></div>
            <div className="info-row"><span className="key">Spot</span><span className="val">#{bookingResult.spot_number}</span></div>
            <div className="info-row"><span className="key">Start Time</span><span className="val">{new Date(bookingResult.start_time).toLocaleString()}</span></div>
            <div className="info-row"><span className="key">Duration</span><span className="val">{bookingResult.duration}h</span></div>
            <div className="info-row"><span className="key">Amount</span><span className="val">${parseFloat(bookingResult.amount).toFixed(2)}</span></div>
            <div className="info-row"><span className="key">Ticket ID</span><span className="val">#{bookingResult.ticket_id}</span></div>
          </div>
          <button className="btn btn-primary btn-full" onClick={() => setBookingResult(null)}>
            Book Another Spot
          </button>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="page-header">
        <h1>Book Parking</h1>
        <p>Choose a lot, select your spot, then confirm your booking.</p>
      </div>

      {/* Step 1 — Lot Selection */}
      <div className="card" style={{ marginBottom: 24 }}>
        <div className="step-header">
          <span className="step-badge">1</span>
          Select a Lot
        </div>

        {lotsError && <div className="alert alert-error">{lotsError}</div>}

        {lotsLoading ? (
          <div className="text-muted">Loading lots…</div>
        ) : (
          <div className="lot-grid">
            {lots.map((lot) => (
              <div
                key={lot.lot_id}
                className={`lot-card${selectedLot?.lot_id === lot.lot_id ? ' selected' : ''}${lot.lot_status !== 'OPEN' ? ' full' : ''}`}
                onClick={() => handleLotSelect(lot)}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 4 }}>
                  <h3>{lot.lot_name}</h3>
                  <LotStatusBadge status={lot.lot_status} />
                </div>
                <div className="lot-location">{lot.lot_location}</div>
                <div className="lot-meta">
                  <span>Base: <strong>${parseFloat(lot.base_price).toFixed(2)}/hr</strong></span>
                  <span>
                    {lot.available_count != null
                      ? `${lot.available_count} / ${lot.capacity} free`
                      : `${lot.capacity} spots`}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Step 2 — Spot Selection */}
      {selectedLot && (
        <div className="card" style={{ marginBottom: 24 }}>
          <div className="step-header">
            <span className="step-badge">2</span>
            Select a Spot — {selectedLot.lot_name}
            <button
              className="btn btn-outline btn-sm"
              onClick={refreshSpots}
              style={{ marginLeft: 'auto' }}
              type="button"
            >
              Refresh
            </button>
          </div>

          {spotsError && <div className="alert alert-error">{spotsError}</div>}

          {spotsLoading ? (
            <div className="text-muted">Loading spots…</div>
          ) : (
            <>
              <ParkingGrid
                spots={spots}
                selectedSpotId={selectedSpot?.spot_id}
                onSpotClick={setSelectedSpot}
              />
              {selectedSpot && (
                <div className="alert alert-info mt-4">
                  Selected: <strong>Spot #{selectedSpot.spot_number}</strong>
                  {selectedSpot.spot_type === 'RESERVED' && ' (Reserved)'}
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* Step 3 — Booking Form */}
      {selectedLot && (
        <div className="card" style={{ maxWidth: 520 }}>
          <div className="step-header">
            <span className="step-badge">3</span>
            Confirm Booking
          </div>

          {bookingError && <div className="alert alert-error">{bookingError}</div>}

          <form onSubmit={handleBook}>
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

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="start">Start Time *</label>
                <input
                  id="start"
                  type="datetime-local"
                  value={startTime}
                  onChange={(e) => setStartTime(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="dur">Duration (hours) *</label>
                <input
                  id="dur"
                  type="number"
                  min={1}
                  max={24}
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  required
                />
                <div className="form-hint">1 – 24 hours</div>
              </div>
            </div>

            <div
              style={{
                background: '#f0fdf4',
                border: '1px solid #bbf7d0',
                borderRadius: 7,
                padding: '12px 16px',
                marginBottom: 16,
                display: 'flex',
                justifyContent: 'space-between',
                fontSize: '0.9rem',
              }}
            >
              <span style={{ color: '#166534' }}>
                Estimated cost ({duration}h × ${parseFloat(selectedLot.base_price).toFixed(2)})
              </span>
              <strong style={{ color: '#166534' }}>${estimatedCost}</strong>
            </div>

            <button
              className="btn btn-success btn-full"
              type="submit"
              disabled={bookingLoading || !selectedSpot}
            >
              {bookingLoading ? <><span className="spinner" /> Processing…</> : 'Pay & Book'}
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
