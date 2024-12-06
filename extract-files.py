#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools
from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_17_2'

namespace_imports = [
	'device/xiaomi/fleur',
	'hardware/mediatek',
	'hardware/mediatek/libmtkperf_client',
	'hardware/xiaomi',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.mediatek.hardware.videotelephony@1.0',
    ): lib_fixup_vendor_suffix,
}

blob_fixups: blob_fixups_user_type = {
    'system_ext/priv-app/ImsService/ImsService.apk': blob_fixup()
        .apktool_patch('blob-patches/ImsService.patch', '-r'),
    'system_ext/lib64/libsink.so': blob_fixup()
        .add_needed('libshim_sink.so'),
    'system_ext/lib64/libsource.so': blob_fixup()
        .add_needed('libui_shim.so'),
    'vendor/etc/init/android.hardware.neuralnetworks@1.3-service-mtk-neuron.rc': blob_fixup()
        .regex_replace('start', 'enable'),
    'vendor/etc/init/android.hardware.secure_element@1.2-service-mediatek.rc': blob_fixup()
        .regex_replace('sea', 'fleur'),
    (
        'vendor/etc/init/init.batterysecret.rc',
        'vendor/etc/init/init.mi_thermald.rc',
    ): blob_fixup()
        .regex_replace('seclabel.*\n?', ''),
    'vendor/etc/camera/camerabooster.json': blob_fixup()
        .regex_replace('"sea"', '"fleur"'),
    (
        'vendor/bin/mnld',
        'vendor/lib64/libcam.utils.sensorprovider.so',
        'vendor/lib64/librgbwlightsensor.so',
        'vendor/lib64/libaalservice.so',
    ): blob_fixup()
        .add_needed('libshim_sensors.so'),
    (
        'vendor/lib64/libmtkcam_stdutils.so',
        'vendor/lib64/hw/android.hardware.camera.provider@2.6-impl-mediatek.so',
        'vendor/lib64/hw/vendor.mediatek.hardware.pq@2.15-impl.so',
    ): blob_fixup()
        .replace_needed('libutils.so', 'libutils-v32.so'),
    'vendor/lib64/libmtkcam_featurepolicy.so': blob_fixup()
        .binary_regex_replace(b'\x34\xE8\x87\x40\xB9', b'\x34\x28\x02\x80\x52'),
    (
        'vendor/bin/hw/android.hardware.gnss-service.mediatek',
        'vendor/lib64/hw/android.hardware.gnss-impl-mediatek.so',
    ): blob_fixup()
        .replace_needed('android.hardware.gnss-V1-ndk_platform.so', 'android.hardware.gnss-V1-ndk.so'),
    'vendor/bin/hw/android.hardware.media.c2@1.2-mediatek': blob_fixup()
        .add_needed('libstagefright_foundation-v33.so')
        .replace_needed('libavservices_minijail_vendor.so', 'libavservices_minijail.so'),
    (
        'vendor/lib64/vendor.mediatek.hardware.power@1.1.so',
        'vendor/lib64/vendor.mediatek.hardware.power@2.0.so',
    ): blob_fixup()
        .add_needed('libshim_power.so'),
    (
        'vendor/lib64/libwvhidl.so',
        'vendor/lib64/mediadrm/libwvdrmengine.so',
    ): blob_fixup()
        .replace_needed('libprotobuf-cpp-lite-3.9.1.so', 'libprotobuf-cpp-full-3.9.1.so'),
    'vendor/lib64/libvendor.goodix.hardware.biometrics.fingerprint@2.1.so': blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so'),
    'vendor/lib64/libmnl.so': blob_fixup()
        .add_needed('libcutils.so'),
    (
        'vendor/lib/libteei_daemon_vfs.so',
        'vendor/lib64/libteei_daemon_vfs.so',
        'vendor/lib64/libSQLiteModule_VER_ALL.so',
        'vendor/lib64/lib3a.flash.so',
        'vendor/lib64/lib3a.ae.stat.so',
        'vendor/lib64/lib3a.sensors.color.so',
        'vendor/lib64/lib3a.sensors.flicker.so',
        'vendor/lib64/libaaa_ltm.so',
    ): blob_fixup()
        .add_needed('liblog.so'),
    'vendor/lib64/hw/fingerprint.fpc.default.so': blob_fixup()
        .binary_regex_replace(b'1f2afd7bc2a8c0035fd600000000ff8301d1fd7b02a9fd830091f85f03a9', b'1f2afd7bc2a8c0035fd600000000c0035fd6fd7b02a9fd830091f85f03a9'),
}

module = ExtractUtilsModule(
    'fleur',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
    check_elf=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
