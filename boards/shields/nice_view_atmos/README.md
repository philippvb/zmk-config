# nice!view atmOS

The nice!view is a low-power, high refresh rate display meant to replace I2C OLEDs traditionally used.

This shield requires that an `&nice_view_spi` labeled SPI bus is provided with _at least_ MOSI, SCK, and CS pins defined.

## Regenerate slideshow art

The right-half slideshow art is generated from source images with Pillow via `uv`:

```sh
ATMOS="/Users/philippvonbachmann/Documents/atmos/atmOS/apps/web/public/images/mascot/alpha"
uv run --with pillow tools/convert_nice_view_art.py \
  --output-c boards/shields/nice_view_atmos/widgets/art.c \
  --output-h boards/shields/nice_view_atmos/widgets/art.h \
  --preview-dir /Users/philippvonbachmann/Documents/Codex/2026-06-05/i-have-a-new-corne-keyboard/outputs/atmos-nice-view-preview \
  --preview-inverted \
  "$ATMOS/atmos-mark-head-generated-v1.png" \
  "$ATMOS/avatar-wave-v1.png" \
  "$ATMOS/avatar-explorer-v1.png" \
  "$ATMOS/avatar-observer-v1.png" \
  "$ATMOS/avatar-leader-v1.png"
```

## Disable custom widget

The nice!view shield includes a custom vertical widget. To use the built-in ZMK one, add the following item to your `.conf` file:

```
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_BUILT_IN=y
CONFIG_ZMK_LV_FONT_DEFAULT_SMALL_MONTSERRAT_26=y
CONFIG_LV_FONT_DEFAULT_MONTSERRAT_26=y
```
