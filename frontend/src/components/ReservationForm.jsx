import { useState } from 'react'

function ReservationForm() {
  const [start, setStart] = useState('')
  const [end, setEnd] = useState('')
  const [message, setMessage] = useState('')

  const submit = (e) => {
    e.preventDefault()
    fetch('/api/reservation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ start, end })
    })
      .then(res => res.json())
      .then(data => setMessage(data.message))
  }

  return (
    <form onSubmit={submit}>
      <h2>Make Reservation</h2>
      <input type="datetime-local" value={start} onChange={e => setStart(e.target.value)} required />
      <input type="datetime-local" value={end} onChange={e => setEnd(e.target.value)} required />
      <button type="submit">Reserve</button>
      {message && <p>{message}</p>}
    </form>
  )
}

export default ReservationForm
