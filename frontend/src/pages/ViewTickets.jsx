import { useState } from 'react'
import { getTickets } from '../api/client'

function TypeBadge({ type }) {
  const cls = {
    PARKING: 'status-badge badge-parking',
    VIOLATION: 'status-badge badge-violation',
    OVERCHARGE: 'status-badge badge-overcharge',
  }[type] || 'status-badge'
  return <span className={cls}>{type}</span>
}

function StatusBadge({ status }) {
  const cls = {
    UNPAID: 'status-badge badge-unpaid',
    PAID: 'status-badge badge-paid',
    CANCELLED: 'status-badge badge-cancelled',
  }[status] || 'status-badge'
  return <span className={cls}>{status}</span>
}

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleString()
}

export default function ViewTickets() {
  const [licensePlate, setLicensePlate] = useState('')
  const [accessKey, setAccessKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null) // { driver_id, tickets: [] }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setResult(null)

    const plate = licensePlate.trim().toUpperCase()
    if (!plate) return setError('Please enter your license plate.')
    if (!accessKey.trim()) return setError('Please enter your password.')

    setLoading(true)
    try {
      const data = await getTickets(plate, accessKey.trim())
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const tickets = result?.tickets ?? []

  return (
    <div>
      <div className="page-header">
        <h1>My Tickets</h1>
        <p>View your full parking and violation ticket history.</p>
      </div>

      <div className="card" style={{ maxWidth: 480, marginBottom: 24 }}>
        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit}>
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
            {loading ? <><span className="spinner" /> Loading…</> : 'View Tickets'}
          </button>
        </form>
      </div>

      {result && (
        <div className="card">
          <div className="section-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Ticket History — Driver #{result.driver_id}</span>
            <span className="text-muted" style={{ fontSize: '0.82rem', fontWeight: 400 }}>
              {tickets.length} ticket{tickets.length !== 1 ? 's' : ''}
            </span>
          </div>

          {tickets.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🎟️</div>
              <p>No tickets found for this account.</p>
            </div>
          ) : (
            <div className="tickets-table-wrapper">
              <table className="tickets-table">
                <thead>
                  <tr>
                    <th>Ticket #</th>
                    <th>Type</th>
                    <th>Lot</th>
                    <th>Spot</th>
                    <th>Duration</th>
                    <th>Amount</th>
                    <th>Issued</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {tickets.map((t) => (
                    <tr key={t.ticket_id}>
                      <td>#{t.ticket_id}</td>
                      <td><TypeBadge type={t.type} /></td>
                      <td>{t.lot_name ?? '—'}</td>
                      <td>{t.spot_number != null ? `#${t.spot_number}` : '—'}</td>
                      <td>{t.duration != null ? `${t.duration}h` : '—'}</td>
                      <td>${parseFloat(t.amount).toFixed(2)}</td>
                      <td style={{ whiteSpace: 'nowrap' }}>{formatDate(t.issued_at)}</td>
                      <td><StatusBadge status={t.status} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
