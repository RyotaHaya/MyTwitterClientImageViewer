type Todo = {
  id: number
  title: string
  description: string
  done: boolean
}

type CookieParam = {
  key: string
  value: string
  // expires: Date
  // maxAge: number
  // domain: string
  // secure: boolean
  // httpOnly: boolean
  // sameSite: boolean
}

type Prediction = {
  result: Prediction
  isArtWork: boolean
  isNSFW: boolean
}

// type Prediction = {
//   className: string
//   probability: number
// }
