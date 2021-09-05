export const howLongAgo = (time) => {
  const now = new Date()

  if (now.getFullYear() !== time.getFullYear()) {
    return (
      time.getDate() +
      ' ' +
      time.toLocaleString('en', { month: 'short' }) +
      ' ' +
      time.getFullYear()
    )
  }

  let sec = Math.floor((now - time) / 1000)
  const days = Math.floor(sec / (24 * 3600))
  sec -= days * 24 * 3600
  const hours = Math.floor(sec / 3600)
  sec -= hours * 3600
  const minutes = Math.floor(sec / 60)
  sec -= minutes * 60

  if (days >= 7) {
    return time.getDate() + ' ' + time.toLocaleString('en', { month: 'short' })
  }
  if (days > 0) {
    return days + 'd'
  }
  if (hours > 0) {
    return hours + 'h'
  }
  if (minutes > 0) {
    return minutes + 'm'
  }
  return sec + 's'
}
