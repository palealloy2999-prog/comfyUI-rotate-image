# Rotate Image Node

[日本語](README_JA.md) | English

A custom ComfyUI node that rotates an input image and fills the surrounding area with a chosen background.

## Installation

1. Place this folder under `ComfyUI/custom_nodes`.
2. Restart ComfyUI.
3. Search for `Rotate Image` in the node list.

## Inputs

- image: input image tensor
- angle: rotation angle in degrees
- background_mode:
  - fit: scale the image to cover the original canvas, then crop it to the original size
  - white: fill the background with white
  - black: fill the background with black
  - custom: use a custom hex color
- custom_color: custom background color in hex format (for example #FF00AA)

## Output

- image: rotated image tensor
