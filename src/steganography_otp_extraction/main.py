from PIL import Image
import numpy as np


FRENCH_ACCENTS = "àâçéèêëîïôùûü"


def bits_to_text(bits):
    """Group bits by 8 (most significant bit first) and convert each byte to an ASCII character."""
    text = ""
    for i in range(0, len(bits) - 7, 8): # -7 is required to avoid ending up with a fragment shorter than 8 bits
        byte = 0
        for bit in bits[i:i + 8]:
            byte = byte * 2 + int(bit)   # place a 0 on the right
        text += chr(byte)
    return text


def cut_at_garbage(text):
    """Keep the text only up to the first character that cannot belong to a French message."""
    for i, char in enumerate(text):
        if char != "\n" and not (32 <= ord(char) <= 126) and char not in FRENCH_ACCENTS:
            return text[:i]
    return text


def uppercase_letters(text):
    """Return only the uppercase letters of a text (the message hidden in the poem)."""
    result = ""
    for char in text:
        if char.isupper():
            result += char
    return result


# Step 1: first hidden message
kirby = np.asarray(Image.open("images/kirby.png"))

bits = []
for row in range(42, 47):
    for col in range(kirby.shape[1]):
        bits.append(kirby[row][col][1] & 1)   # channel 1 = green, "& 1" keeps the last bit

poem = cut_at_garbage(bits_to_text(bits))
print("First hidden message (poem):\n")
print(poem)

# Step 2: uppercase letter filter
clue = uppercase_letters(poem)
print("\nClue hidden in the uppercase letters:")
print(clue)

# Step 3: second hidden message
ghsc = np.asarray(Image.open("images/ghsc.png"))

bits = []
for col in range(119, 129):              # the value is selected empirically
    for row in range(ghsc.shape[0]):     # every row, from top to bottom
        red = ghsc[row][col][0]          # channel 0 = red
        bits.append((red >> 1) & 1)      # second-to-last bit first
        bits.append(red & 1)             # then the last bit

second_message = cut_at_garbage(bits_to_text(bits))
print("\nSecond hidden message:\n")
print(second_message)

# Step 4: the key image
gta = np.asarray(Image.open("images/gtaVI.png"))

KEY_SIZE = 225
key = np.zeros((KEY_SIZE, KEY_SIZE, 3), dtype=np.uint8)   # empty 225x225 RGB image

# Offsets of the 4 pixels inside a 2x2 square, in reading order
SQUARE = [(0, 0), (0, 1), (1, 0), (1, 1)]

for row in range(KEY_SIZE):
    for col in range(KEY_SIZE):
        for color in range(3):                            # 0 = red, 1 = green, 2 = blue
            value = 0
            for d_row, d_col in SQUARE:
                two_bits = gta[2 * row + d_row][2 * col + d_col][color] & 3   # keep the last two bits
                value = (value << 2) | int(two_bits)      # shift by 2 and append them
            key[row][col][color] = value

Image.fromarray(key).save("images/key.png")
print("\nKey image saved as key.png")

# Step 5: decrypt the cipherimage with the key
cipher = np.asarray(Image.open("images/cipherimage.png"))
decrypted = cipher ^ key                                  # XOR pixel by pixel, color by color
Image.fromarray(decrypted).save("images/decrypted.png")
print("Decrypted image saved as decrypted.png")