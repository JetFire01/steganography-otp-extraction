# steganography-extraction-otp

Extraction of messages hidden in images with LSB steganography, followed by the decryption of an image encrypted with a one-time pad.

## How it works

The program follows a chain of clues hidden in several images:

1. **First message**: read from the least significant bit of the green channel of `kirby.png`. The result is a poem.
2. **Clue**: the uppercase letters of the poem tell where the second message is.
3. **Second message**: read from the two least significant bits of the red channel of `ghsc.png`. It explains how the key is hidden.
4. **Key**: a 225x225 image hidden in `gtaVI.png`, each key pixel being spread over a 2x2 square of pixels.
5. **Decryption**: `cipherimage.png` XOR key gives the original image.

## Requirements

- Python 3
- NumPy
- Pillow

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install numpy pillow
```

## Usage

The images of the assignment are in the `images/` folder. Run the program from the root of the project:

```bash
python3 src/steganography_extraction_otp/main.py
```

The hidden messages are printed in the terminal. The key and the decrypted image are saved in `images/` as `key.png` and `decrypted.png`.

## Project structure

```
├── images/                              # input images, key and decrypted image
├── src/steganography_extraction_otp/
│   └── main.py                          # the program
└── README.md
```