# nice!view atmOS

The nice!view is a low-power, high refresh rate display meant to replace I2C OLEDs traditionally used.

This shield requires that an `&nice_view_spi` labeled SPI bus is provided with _at least_ MOSI, SCK, and CS pins defined.

## Regenerate slideshow art

The right-half slideshow art is generated from source images with Pillow via `uv`:

```sh
AGENT="/Users/philippvonbachmann/Documents/atmos/atmOS/apps/web/public/images/mascot/agent-builder"
IMAGES=(
  "$AGENT/avatar-wizard-color-v1.png"
  "$AGENT/avatar-detective-v1.png"
  "$AGENT/avatar-chef-v1.png"
  "$AGENT/avatar-dj-v1.png"
  "$AGENT/avatar-pirate-v1.png"
  "$AGENT/avatar-gardener-v1.png"
  "$AGENT/avatar-designer-v1.png"
  "$AGENT/avatar-security-v1.png"
  "$AGENT/avatar-engineer-v1.png"
  "$AGENT/avatar-scientist-v1.png"
  "$AGENT/avatar-support-v1.png"
  "$AGENT/avatar-legal-v1.png"
  "$AGENT/avatar-finance-v1.png"
  "$AGENT/avatar-operations-v1.png"
  "$AGENT/avatar-data-analyst-v1.png"
  "$AGENT/avatar-product-manager-v1.png"
  "$AGENT/avatar-writer-v1.png"
  "$AGENT/avatar-scheduler-v1.png"
  "$AGENT/avatar-email-v1.png"
  "$AGENT/avatar-automation-v1.png"
)

uv run --with pillow tools/convert_nice_view_art.py \
  --output-c boards/shields/nice_view_atmos/widgets/art.c \
  --output-h boards/shields/nice_view_atmos/widgets/art.h \
  --preview-dir /Users/philippvonbachmann/Documents/Codex/2026-06-05/i-have-a-new-corne-keyboard/outputs/atmos-nice-view-preview \
  --preview-inverted \
  --rotate 90 \
  "${IMAGES[@]}"
```

The `--rotate 90` option compensates for the Corne right display mount. The
converter also accepts `--rotate 180` or `--rotate 270` for other mounts.

## Disable custom widget

The nice!view shield includes a custom vertical widget. To use the built-in ZMK one, add the following item to your `.conf` file:

```
CONFIG_ZMK_DISPLAY_STATUS_SCREEN_BUILT_IN=y
CONFIG_ZMK_LV_FONT_DEFAULT_SMALL_MONTSERRAT_26=y
CONFIG_LV_FONT_DEFAULT_MONTSERRAT_26=y
```
