#
# Copyright (C) 2024 The LineageOS Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit from device makefile.
$(call inherit-product, device/xiaomi/fleur/device.mk)

# Inherit some common PixelAge stuff.
$(call inherit-product, vendor/pixelage/config/common_full_phone.mk)

# Boot animation
TARGET_BOOT_ANIMATION_RES := 1080
TARGET_SCREEN_HEIGHT := 2400
TARGET_SCREEN_WIDTH := 1080

# Pixelage
TARGET_FACE_UNLOCK_SUPPORTED := true
PIXELAGE_BUILDTYPE := OFFICIAL

PRODUCT_NAME := pixelage_fleur
PRODUCT_DEVICE := fleur
PRODUCT_MANUFACTURER := Xiaomi
PRODUCT_BRAND := Redmi
PRODUCT_MODEL := 2201117SY

PRODUCT_GMS_CLIENTID_BASE := android-xiaomi

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="fleur_global-user 13 SP1A.210812.016 V816.0.4.0.TKEMIXM release-keys" \
    BuildFingerprint=Redmi/fleur_global/fleur:13/SP1A.210812.016/V816.0.4.0.TKEMIXM:user/release-keys
