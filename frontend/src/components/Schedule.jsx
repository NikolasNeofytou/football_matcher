import { useEffect, useState, useContext } from 'react'
import ClubContext from '../ClubContext'

function Schedule() {
  const [data, setData] = useState(null)
  const [message, setMessage] = useState('')
  const { clubId } = useContext(ClubContext)

  useEffect(() => {
    if (!clubId) return
    fetch(`/api/clubs/${clubId}/schedule`)
      .then(res => res.json())
      .then(setData)
  }, [clubId])

  const reserve = (slot) => {
    fetch('/api/reservation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start: slot.start, end: slot.end, club_id: clubId })
    })
      .then(res => res.json())
      .then(res => {
        if (res.message) {
          setMessage(res.message)
        } else if (res.error) {
          setMessage(res.error)
        }
        return fetch(`/api/clubs/${clubId}/schedule`)
          .then(r => r.json())
          .then(setData)
      })
  }
  if (!clubId) return <div>Please select a club to view the schedule.</div>
  if (!data) return <div>Loading...</div>

  return (
    <div>
      <h2>Schedule for Club {clubId}</h2>
      {message && <p>{message}</p>}
      <table className="schedule-grid">
        <thead>
          <tr>
            <th></th>
            {data.schedule.map(day => (
              <th key={day.date}>{new Date(day.date).toLocaleDateString()}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.hours.map((hr, i) => (
            <tr key={hr}>
              <td>{hr}:00</td>
              {data.schedule.map(day => {
                const slot = day.slots[i]
                return (
                  <td
                    key={day.date}
                    className={slot.reserved ? 'reserved' : 'free'}
                    onClick={() => !slot.reserved && reserve(slot)}
                  ></td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Schedule
