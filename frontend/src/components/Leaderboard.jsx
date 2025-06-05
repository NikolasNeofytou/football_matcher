import { useEffect, useState } from 'react'

function Leaderboard() {
  const [teams, setTeams] = useState(null)

  useEffect(() => {
    fetch('/api/leaderboard')
      .then(res => res.json())
      .then(data => setTeams(data.teams))
  }, [])

  if (!teams) return <div>Loading...</div>

  return (
    <div>
      <h2>Leaderboard</h2>
      <ol>
        {teams.map(t => (
          <li key={t.id}>{t.name} - {t.wins}W/{t.losses}L</li>
        ))}
      </ol>
    </div>
  )
}

export default Leaderboard
