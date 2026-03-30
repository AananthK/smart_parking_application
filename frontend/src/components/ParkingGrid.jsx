// ParkingGrid — renders a colour-coded grid of parking spots
//
// Props:
//   spots          – array of { spot_id, spot_number, spot_type, status }
//   selectedSpotId – spot_id the user has clicked (shown in amber)
//   yourSpotId     – spot_id belonging to the current user (shown in blue)
//   onSpotClick    – (spot) => void — called when an AVAILABLE spot is clicked
//                   omit to make the grid read-only

export default function ParkingGrid({ spots = [], selectedSpotId, yourSpotId, onSpotClick }) {
  function getClassName(spot) {
    if (spot.spot_id === yourSpotId) return 'spot spot-yours'
    if (spot.spot_id === selectedSpotId) return 'spot spot-selected'
    if (spot.status === 'AVAILABLE') return 'spot spot-available'
    if (spot.status === 'OCCUPIED') return 'spot spot-occupied'
    return 'spot spot-oos'
  }

  function handleClick(spot) {
    if (!onSpotClick) return
    if (spot.spot_id === yourSpotId) return
    if (spot.status !== 'AVAILABLE') return
    onSpotClick(spot)
  }

  // Sort spots by spot_number so the grid reads left-to-right
  const sorted = [...spots].sort((a, b) => a.spot_number - b.spot_number)

  return (
    <div>
      <div className="parking-grid-wrapper">
        <div className="parking-grid">
          {sorted.map((spot) => (
            <div
              key={spot.spot_id}
              className={getClassName(spot)}
              onClick={() => handleClick(spot)}
              title={`Spot #${spot.spot_number} (${spot.spot_type}) — ${spot.status}`}
            >
              {spot.spot_number}
            </div>
          ))}
        </div>
      </div>

      <div className="grid-legend">
        <span className="legend-item">
          <span className="legend-dot" style={{ background: 'var(--spot-available)' }} />
          Available
        </span>
        <span className="legend-item">
          <span className="legend-dot" style={{ background: 'var(--spot-occupied)' }} />
          Occupied
        </span>
        <span className="legend-item">
          <span className="legend-dot" style={{ background: 'var(--spot-oos)' }} />
          Out of Service
        </span>
        {(selectedSpotId || yourSpotId) && (
          <>
            {selectedSpotId && !yourSpotId && (
              <span className="legend-item">
                <span className="legend-dot" style={{ background: 'var(--spot-selected)' }} />
                Selected
              </span>
            )}
            {yourSpotId && (
              <span className="legend-item">
                <span className="legend-dot" style={{ background: 'var(--spot-yours)' }} />
                Your Spot
              </span>
            )}
          </>
        )}
      </div>
    </div>
  )
}
