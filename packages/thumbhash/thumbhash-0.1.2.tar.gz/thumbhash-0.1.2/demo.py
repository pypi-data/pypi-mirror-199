from thumbhash import thumb_hash_to_rgba, image_to_thumb_hash, rgba_to_thumb_hash

_hash = image_to_thumb_hash('sunset.jpg')

print(_hash)

# thumb_hash = [86, 8, 10, 13, 128, 22, 234, 86, 111, 117, 135, 122, 119, 104, 153, 135, 250, 120, 24, 79, 228]

w, h, rgba = thumb_hash_to_rgba(_hash)

print(w,h)