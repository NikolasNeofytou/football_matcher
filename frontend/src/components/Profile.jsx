import { useEffect, useState } from 'react'

function Profile() {
  const [profile, setProfile] = useState(null)

  useEffect(() => {
    fetch('/api/profile')
      .then(res => res.json())
      .then(setProfile)
  }, [])

  if (!profile) return <div>Loading...</div>

  return (
    <div>
      <h2>{profile.username}</h2>
      <p>Email: {profile.email}</p>
      {profile.team && <p>Team: {profile.team.name}</p>}
    </div>
  )
}

export default Profile
