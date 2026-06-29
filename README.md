# AI-week-exploration

## circle_crop.py

Crop any image into a circle with a transparent background (anti-aliased edges).
It center-crops to a square first, then applies a circular mask and saves a PNG.

### Setup

```bash
pip install -r requirements.txt
```

### Usage

```bash
# Writes input_circle.png next to the input
python circle_crop.py input.jpg

# Custom output path
python circle_crop.py input.jpg -o avatar.png

# Resize to a fixed diameter (square)
python circle_crop.py input.jpg --size 512
```
