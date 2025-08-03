import { useEffect, useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import ClubContext from '../ClubContext'

function Clubs() {
  const [clubs, setClubs] = useState([])
  const { setClubId } = useContext(ClubContext)
  const navigate = useNavigate()

  useEffect(() => {
    fetch('/api/clubs')
      .then(res => res.json())
      .then(data => setClubs(data.clubs || []))
  }, [])

  const chooseClub = (id) => {
    setClubId(id)
    navigate('/')
  }

  return (
    <div>
      <h2>Select Club</h2>
      <ul>
        {clubs.map(c => (
          <li key={c.id}>
            <button onClick={() => chooseClub(c.id)}>{c.name}</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Clubs
