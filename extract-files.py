#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom/display',
    'hardware/qcom/display/gralloc',
    'vendor/qcom/common/vendor/adreno-r',
    'vendor/qcom/common/vendor/display/5.4',
    'vendor/qcom/common/vendor/gps-legacy',
    'vendor/qcom/common/vendor/media-5.4',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api*',
        'com.qualcomm.qti.imscmservice*',
        'com.qualcomm.qti.uceservice*',
        'libmmosal',
        'vendor.qti.data.*',
        'vendor.qti.diaghal*',
        'vendor.qti.hardware.data.*',
        'vendor.qti.hardware.embmssl*',
        'vendor.qti.hardware.limits*',
        'vendor.qti.hardware.mwqemadapter*',
        'vendor.qti.hardware.radio.*',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.ims.*',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.latency*',
    ): lib_fixup_vendor_suffix,
    (
        'libOmxCore',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('vendor/bin/hw/vendor.qti.hardware.vibrator.service', 'vendor/lib64/vendor.qti.hardware.vibrator.impl.so'): blob_fixup()
        .replace_needed('android.hardware.vibrator-V1-ndk_platform.so', 'android.hardware.vibrator-V2-ndk.so'),
    ('vendor/etc/media_codecs.xml', 'vendor/etc/media_codecs_yupik_v0.xml', 'vendor/etc/media_codecs_yupik_v1.xml'): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|vendor_audio).*\n', ''),
    'vendor/etc/seccomp_policy/atfwd@2.0.policy': blob_fixup()
        .add_line_if_missing('gettid: 1'),
    ('vendor/lib64/libgf_hal.so'): blob_fixup()
        .sig_replace('72 6F 2E 62 6F 6F 74 2E 66 6C 61 73 68 2E 6C 6F 63 6B 65 64', '72 6F 2E 62 6F 6F 74 6C 6F 61 64 65 72 2E 6C 6F 63 6B 65 64'),
    ('vendor/lib64/libwvhidl.so', 'vendor/lib64/mediadrm/libwvdrmengine.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    'vendor/bin/hw/android.hardware.biometrics.face-service.noth': blob_fixup()
        .replace_needed('android.hardware.biometrics.common-V1-ndk_platform.so', 'android.hardware.biometrics.common-V1-ndk.so')
        .replace_needed('android.hardware.biometrics.face-V1-ndk_platform.so', 'android.hardware.biometrics.face-V1-ndk.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'phone1',
    'nothing',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
