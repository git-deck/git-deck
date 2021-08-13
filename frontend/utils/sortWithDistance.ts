// NOTE: https://www.bugbugnow.net/2020/02/levenshtein-distance.html
const _calcDistance = (str1: string, str2: string) => {
  const len1 = str1.length
  const len2 = str2.length
  const max = len1 + len2
  const offset = max + 1
  let x
  let y
  let D
  let k
  let kk
  const V = new Array(offset * 2 + 1)

  V[1 + offset] = 0
  for (D = 0; D <= max; D++) {
    for (k = -D; k <= D; k += 2) {
      kk = k + offset
      x =
        k == -D || (k != D && V[kk - 1] < V[kk + 1]) ? V[kk + 1] : V[kk - 1] + 1
      y = x - k
      // while (x < len1 && y < len2 && str1[x] == str2[y]) {
      while (x < len1 && y < len2 && str1.charCodeAt(x) == str2.charCodeAt(y)) {
        x++
        y++
      }
      V[kk] = x
      if (x >= len1 && y >= len2) {
        return D
      }
    }
  }
  return -1
}

const calcDistance = (str1: string, str2: string) => {
  const m = Math.max(str1.length, str2.length)
  const d = _calcDistance(str1, str2)
  return 1 - d / m
}

const compareWithDistance = (query: string) => (a: string, b: string) => {
  // クエリの最初の2文字が一致、1文字が一致したものを優先して表示する
  const twoMatchA = query.slice(0, 2) === a.slice(0, 2)
  const twoMatchB = query.slice(0, 2) === b.slice(0, 2)
  if (twoMatchA && twoMatchB) {
    return 0
  } else if (twoMatchA) {
    return -1
  } else if (twoMatchB) {
    return 1
  }
  const oneMathcA = query[0] === a[0]
  const oneMathcB = query[0] === b[0]
  if (oneMathcA && oneMathcB) {
    return 0
  } else if (oneMathcA) {
    return -1
  } else if (oneMathcB) {
    return 1
  }

  // そのほかはレーベンシュタイン距離でソート
  const matchA = calcDistance(query, a)
  const matchB = calcDistance(query, b)
  return matchB > matchA ? 1 : matchA === matchB ? 0 : -1
}

export default compareWithDistance
