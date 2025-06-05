import { useEffect, useState } from 'react'

function Schedule() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/schedule')
      .then(res => res.json())
      .then(setData)
  }, [])

  if (!data) return <div>Loading...</div>

  return (
    <div>
      <h2>Schedule</h2>
      {data.schedule.map((day, idx) => (
        <div key={idx}>
          <h3>{new Date(day.date).toDateString()}</h3>
          <ul>
            {day.slots.map((slot, i) => (
              <li key={i}>
                {new Date(slot.start).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'})}
                {' - '}
                {slot.reserved ? 'Reserved' : 'Free'}
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}

export default Schedule
