import { useState } from 'react'
import { registerVehicle } from '../api/client'

export default function AddVehicle() {
  const [licensePlate, setLicensePlate] = useState('')
  const [ownerName, setOwnerName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)
  const [copied, setCopied] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setResult(null)

    const plate = licensePlate.trim().toUpperCase()
    if (!plate) return setError('Please enter a license plate.')

    setLoading(true)
    try {
      const data = await registerVehicle(plate, ownerName.trim())
      setResult(data)
      setLicensePlate('')
      setOwnerName('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  function copyPassword() {
    navigator.clipboard.writeText(result.access_key).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  return (
    <div>
      <div className="page-header">
        <h1>Add Vehicle</h1>
        <p>Register your vehicle to access parking reservations.</p>
      </div>

      <div className="card" style={{ maxWidth: 480 }}>
        {error && <div className="alert alert-error">{error}</div>}

        {result ? (
          <div>
            <div className="alert alert-success">
              Vehicle registered successfully!
            </div>

            <div className="password-reveal">
              <h3>Save Your Password</h3>
              <p>
                This is the only time your password will be shown. You will need it to book parking, view bookings, and manage your account.
              </p>
              <div className="password-display">
                <code>{result.access_key}</code>
                <button
                  className="btn btn-outline btn-sm"
                  onClick={copyPassword}
                  type="button"
                >
                  {copied ? 'Copied!' : 'Copy'}
                </button>
              </div>
              <div className="mt-4" style={{ fontSize: '0.82rem', color: '#78350f' }}>
                <strong>Driver ID:</strong> {result.driver_id} &nbsp;|&nbsp;
                <strong>License Plate:</strong> {result.license_plate}
              </div>
            </div>

            <button
              className="btn btn-outline btn-full mt-4"
              onClick={() => setResult(null)}
              type="button"
            >
              Register Another Vehicle
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="license-plate">License Plate *</label>
              <input
                id="license-plate"
                type="text"
                placeholder="e.g. ABC 1234"
                value={licensePlate}
                onChange={(e) => setLicensePlate(e.target.value)}
                maxLength={11}
                required
                autoFocus
              />
              <div className="form-hint">Up to 11 characters including spaces/hyphens.</div>
            </div>

            <div className="form-group">
              <label htmlFor="owner-name">Owner Name (optional)</label>
              <input
                id="owner-name"
                type="text"
                placeholder="e.g. Jane Smith"
                value={ownerName}
                onChange={(e) => setOwnerName(e.target.value)}
                maxLength={100}
              />
            </div>

            <button className="btn btn-primary btn-full" type="submit" disabled={loading}>
              {loading ? <><span className="spinner" /> Registering…</> : 'Register Vehicle'}
            </button>
          </form>
        )}
      </div>
    </div>
  )
}
