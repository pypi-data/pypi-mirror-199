import * as ThumbHash from './thumbhash.mjs'

const hash = [213, 7, 18, 29, 132, 95, 116, 137, 120, 136, 135, 118, 136, 135, 120, 120, 8, 135, 149, 96, 87]

const rgba = ThumbHash.thumbHashToRGBA(hash)

// console.log(hash)
console.log(rgba)