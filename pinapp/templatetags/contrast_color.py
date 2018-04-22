# coding: utf-8
import matplotlib.colors as colors
import wcag_contrast_ratio as contrast
from django.template import Library

register = Library()


@register.filter(name='contrast_color')
def contrast_color(hex_color):
    rgb_color = colors.hex2color(hex_color)

    black = (0.0, 0.0, 0.0)
    black_contrast = contrast.rgb(rgb_color, black)

    white = (1.0, 1.0, 1.0)
    white_contrast = contrast.rgb(rgb_color, white)

    if white_contrast > black_contrast:
        return "#ffffff"
    else:
        return "#000000"
