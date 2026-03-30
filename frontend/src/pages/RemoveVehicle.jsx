import { useState } from 'react'
import { suspendVehicle } from '../api/client'

export default function RemoveVehicle() {
  const [licensePlate, setLicensePlate] = useState('')
  const [accessKey, setAccessKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSuccess(false)

    const plate = licensePlate.trim().toUpperCase()
    if (!plate) return setError('Please enter your license plate.')
    if (!accessKey.trim()) return setError('Please enter your password.')

    const confirmed = window.confirm(
      `Are you sure you want to deregister vehicle "${plate}"? This will suspend the vehicle from the system.`
    )
    if (!confirmed) return

    setLoading(true)
    try {
      await suspendVehicle(plate, accessKey.trim())
      setSuccess(true)
      setLicensePlate('')
      setAccessKey('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1>Remove Vehicle</h1>
        <p>Deregister a vehicle. Its record will be suspended but billing history is preserved.</p>
      </div>

      <div className="card" style={{ maxWidth: 480 }}>
        {error && <div className="alert alert-error">{error}</div>}

        {success && (
          <div className="alert alert-success">
            Vehicle successfully deregistered. If the same license plate is registered again in the future, it will be treated as a new account.
          </div>
        )}

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
          </div>

          <div className="form-group">
            <label htmlFor="access-key">Password *</label>
            <input
              id="access-key"
              type="password"
              placeholder="Your parking password"
              value={accessKey}
              onChange={(e) => setAccessKey(e.target.value)}
              required
            />
          </div>

          <div className="alert alert-info" style={{ marginBottom: 16 }}>
            <strong>Note:</strong> If this license plate is registered again in the future, it will receive a new Driver ID and a fresh billing history.
          </div>

          <button
            className="btn btn-danger btn-full"
            type="submit"
            disabled={loading}
          >
            {loading ? <><span className="spinner" /> Removing…</> : 'Remove Vehicle'}
          </button>
        </form>
      </div>
    </div>
  )
}
