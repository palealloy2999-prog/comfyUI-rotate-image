import math
from typing import Tuple

import numpy as np
import torch
from PIL import Image


class RotateImageNode:
    """Rotate an image and fill the surrounding area with a chosen background."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "angle": ("FLOAT", {"default": 0.0, "min": -360.0, "max": 360.0, "step": 1.0}),
                "background_mode": (["fit", "white", "black", "custom"], {"default": "fit"}),
                "custom_color": ("STRING", {"default": "#FFFFFF"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "rotate"
    CATEGORY = "image/transform"

    def rotate(self, image, angle, background_mode, custom_color):
        if isinstance(image, torch.Tensor):
            image_array = image.detach().cpu().numpy()
        else:
            image_array = np.array(image)

        if image_array.ndim != 4:
            raise ValueError("Expected image tensor with shape [batch, height, width, channels]")

        batch, height, width, channels = image_array.shape
        if channels != 3:
            raise ValueError("Expected RGB images with 3 channels")

        if angle is None:
            angle = 0.0

        fill_color = self._resolve_background_color(background_mode, custom_color)
        output_images = []

        scale_for_fit = 1.0
        if background_mode == "fit":
            radians = math.radians(float(angle))
            abs_cos = abs(math.cos(radians))
            abs_sin = abs(math.sin(radians))
            if abs_cos < 1e-12:
                abs_cos = 0.0
            if abs_sin < 1e-12:
                abs_sin = 0.0
            required_width = width * abs_cos + height * abs_sin
            required_height = width * abs_sin + height * abs_cos
            scale_for_fit = max(required_width / width, required_height / height)

        for index in range(batch):
            frame = image_array[index]
            rgb = np.clip(np.round(frame * 255.0), 0, 255).astype(np.uint8)
            pil_image = Image.fromarray(rgb, mode="RGB")

            if background_mode == "fit":
                # Scale the image first using the calculated scale
                scaled_width = max(1, math.ceil(width * scale_for_fit))
                scaled_height = max(1, math.ceil(height * scale_for_fit))
                pil_image = pil_image.resize((scaled_width, scaled_height), resample=Image.Resampling.BICUBIC)
                # Rotate with expand=True to get full rotated image
                rotated = pil_image.rotate(float(angle), expand=True, resample=Image.Resampling.BICUBIC, fillcolor=fill_color)
                # Crop to output canvas size from center
                left = (rotated.width - width) // 2
                top = (rotated.height - height) // 2
                right = left + width
                bottom = top + height
                result = rotated.crop((left, top, right, bottom))
            else:
                # For white/black/custom, rotate without expand and center on canvas
                rotated = pil_image.rotate(float(angle), expand=False, resample=Image.Resampling.BICUBIC, fillcolor=fill_color)
                result = rotated

            result_array = np.asarray(result, dtype=np.float32) / 255.0
            output_images.append(result_array)

        output = np.stack(output_images, axis=0)
        if isinstance(image, torch.Tensor):
            return (torch.from_numpy(output).to(device=image.device, dtype=image.dtype),)
        return (output,)

    def _resolve_background_color(self, background_mode: str, custom_color: str) -> Tuple[int, int, int]:
        if background_mode == "white":
            return (255, 255, 255)
        if background_mode == "black":
            return (0, 0, 0)
        if background_mode == "custom":
            return self._parse_hex_color(custom_color)
        return (255, 255, 255)

    def _parse_hex_color(self, value: str) -> Tuple[int, int, int]:
        if value is None:
            value = "#FFFFFF"
        value = str(value).strip()
        if not value.startswith("#"):
            value = f"#{value}"
        if len(value) == 4:
            value = "#" + "".join(ch * 2 for ch in value[1:])
        if len(value) != 7:
            raise ValueError("custom_color must be a 3-digit or 6-digit hexadecimal color")
        try:
            return tuple(int(value[idx:idx + 2], 16) for idx in (1, 3, 5))
        except ValueError as exc:
            raise ValueError("custom_color must be a valid hexadecimal color") from exc


NODE_CLASS_MAPPINGS = {"RotateImageNode": RotateImageNode}
NODE_DISPLAY_NAME_MAPPINGS = {"RotateImageNode": "Rotate Image"}
