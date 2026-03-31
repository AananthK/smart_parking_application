import { mockGetLots, mockGetLotSpots } from './mock'

// API base URL — set VITE_API_URL in .env to point at your backend
// Vite proxy rewrites /api → http://localhost:8000 (see vite.config.js)
const API_BASE = '/api'
const USE_MOCK = import.meta.env.VITE_USE_MOCK === 'true'

async function request(method, path, body = null, params = null) {
  let url = `${API_BASE}${path}`
  if (params) {
    const qs = new URLSearchParams(params).toString()
    url += `?${qs}`
  }

  const options = {
    method,
    headers: { 'Content-Type': 'application/json' },
  }
  if (body) options.body = JSON.stringify(body)

  const res = await fetch(url, options)

  // 204 No Content
  if (res.status === 204) return null

  const data = await res.json().catch(() => ({ detail: 'Invalid response from server' }))

  if (!res.ok) {
    throw new Error(data.detail || data.message || `Request failed (${res.status})`)
  }

  return data
}

// ── Vehicles ──────────────────────────────────────────────────────
// POST /vehicles/register  { license_plate, owner_name }
//   → { driver_id, license_plate, owner_name, access_key }
export function registerVehicle(license_plate, owner_name) {
  return request('POST', '/vehicles/register', { license_plate, owner_name })
}

// POST /vehicles/suspend  { license_plate, access_key }
//   → { message }
export function suspendVehicle(license_plate, access_key) {
  return request('POST', '/vehicles/suspend', { license_plate, access_key })
}

// ── Lots ─────────────────────────────────────────────────────────
// GET /lots
//   → [{ lot_id, lot_name, lot_location, capacity, base_price, lot_status, available_count }]
export function getLots() {
  if (USE_MOCK) return mockGetLots()
  return request('GET', '/lots')
}

// GET /lots/:lot_id/spots
//   → [{ spot_id, spot_number, spot_type, status, current_vehicle }]
export function getLotSpots(lot_id) {
  if (USE_MOCK) return mockGetLotSpots(lot_id)
  return request('GET', `/lots/${lot_id}/spots`)
}

// ── Bookings ─────────────────────────────────────────────────────
// POST /bookings  { license_plate, access_key, spot_id, start_time, duration }
//   → { ticket_id, driver_id, spot_id, spot_number, lot_id, lot_name, amount, start_time, duration }
export function createBooking(license_plate, access_key, spot_id, start_time, duration) {
  return request('POST', '/bookings', { license_plate, access_key, spot_id, start_time, duration })
}

// GET /bookings/current  ?license_plate=&access_key=
//   → { ticket_id, driver_id, spot_id, spot_number, lot_id, lot_name, amount, start_time, duration, status }
//   or null / 404 when no active booking
export function getCurrentBooking(license_plate, access_key) {
  return request('GET', '/bookings/current', null, { license_plate, access_key })
}

// DELETE /bookings/:ticket_id  { license_plate, access_key }
//   → { message }
export function cancelBooking(ticket_id, license_plate, access_key) {
  return request('DELETE', `/bookings/${ticket_id}`, { license_plate, access_key })
}

// ── Tickets ───────────────────────────────────────────────────────
// GET /tickets  ?license_plate=&access_key=
//   → { driver_id, tickets: [{ ticket_id, spot_id, lot_name, amount, issued_at, duration, type, status }] }
export function getTickets(license_plate, access_key) {
  return request('GET', '/tickets', null, { license_plate, access_key })
}
