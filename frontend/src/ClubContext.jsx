import { createContext } from 'react'

const ClubContext = createContext({ clubId: null, setClubId: () => {} })

export default ClubContext
