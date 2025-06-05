import { useEffect, useState } from 'react'

function Schedule() {
  const [data, setData] = useState(null)
  const [message, setMessage] = useState('')

  useEffect(() => {
    fetch('/api/schedule')
      .then(res => res.json())
      .then(setData)
  }, [])

  const reserve = (slot) => {
    fetch('/api/reservation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start: slot.start, end: slot.end })
    })
      .then(res => res.json())
      .then(res => {
        if (res.message) {
          setMessage(res.message)
        } else if (res.error) {
          setMessage(res.error)
        }
        return fetch('/api/schedule')
          .then(r => r.json())
          .then(setData)
      })
  }

  if (!data) return <div>Loading...</div>

  return (
    <div>
      <h2>Schedule</h2>
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
