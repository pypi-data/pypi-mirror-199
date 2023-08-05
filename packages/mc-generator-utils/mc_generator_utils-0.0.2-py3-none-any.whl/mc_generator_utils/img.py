from cv2 import imread, IMREAD_UNCHANGED
from numpy import zeros

def stackImages(base, mask, x, y):
  if (base.shape[2] == 3):
    base = addAlpha(base, 255)

  if (mask.shape[2] == 3):
    mask = addAlpha(mask, 255)

  subBase = base[x: x + mask.shape[0], y: y + mask.shape[1]]

  shape = (mask.shape[0], mask.shape[1], 1)
  alpha_base = subBase[:, :, 3].reshape(shape) / 255
  alpha_mask = mask[:, :, 3].reshape(shape) / 255

  subBase = mask * alpha_mask + subBase * alpha_base * (1 - alpha_mask)
  subBase[:,:,3] = ((1 - (1 - alpha_mask) * (1 - alpha_base)) * 255).reshape(shape[:-1])

  base[x: x + mask.shape[0], y: y + mask.shape[1]] = subBase
  return base

def load(file):
  return imread(file, IMREAD_UNCHANGED)

def addAlpha(img, val):
  out = zeros((img.shape[0], img.shape[1], 4), dtype=img.dtype) + val
  out[:, :, :3] = img
  return out