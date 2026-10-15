"""Validate matching T1000-E Nordic DFU and UF2 files before publishing."""

import argparse
import binascii
import hashlib
import json
from pathlib import Path
import struct
import zipfile


def verify(stem: Path, version: str):
    zip_path = stem.with_suffix(".zip")
    uf2_path = stem.with_suffix(".uf2")
    with zipfile.ZipFile(zip_path) as package:
        if package.testzip():
            raise ValueError("ZIP checksum failed")
        manifest = json.loads(package.read("manifest.json"))["manifest"]
        app = manifest["application"]
        binary = package.read(app["bin_file"])
        init = package.read(app["dat_file"])
        info = app["init_packet_data"]

    crc = binascii.crc_hqx(binary, 0xFFFF)
    if crc != info["firmware_crc16"]:
        raise ValueError("Firmware CRC16 does not match the DFU manifest")
    if struct.unpack("<HHIHHH", init) != (
        82, 65535, info["application_version"], 1, 0x123, crc
    ):
        raise ValueError("Unexpected Nordic DFU init packet")
    if info["softdevice_req"] != [0x123]:
        raise ValueError("Unexpected SoftDevice requirement")

    uf2 = uf2_path.read_bytes()
    if not uf2 or len(uf2) % 512:
        raise ValueError("UF2 length is not a multiple of 512")
    count = len(uf2) // 512
    payload = bytearray()
    for i in range(count):
        block = uf2[i * 512 : (i + 1) * 512]
        magic0, magic1, flags, addr, size, number, total, family = struct.unpack_from("<8I", block)
        end_magic = struct.unpack_from("<I", block, 508)[0]
        if (magic0, magic1, end_magic) != (0x0A324655, 0x9E5D5157, 0x0AB16F30):
            raise ValueError(f"UF2 block {i}: invalid magic")
        if (number, total, size, addr) != (i, count, 256, 0x27000 + i * 256):
            raise ValueError(f"UF2 block {i}: invalid sequence or address")
        if not flags & 0x2000 or family != 0xADA52840:
            raise ValueError(f"UF2 block {i}: incorrect board family")
        payload.extend(block[32 : 32 + size])
    if len(binary) > 708608 or len(payload) - len(binary) not in range(256):
        raise ValueError("Application is outside the expected T1000-E flash layout")
    if payload[: len(binary)] != binary:
        raise ValueError("ZIP and UF2 contain different firmware")
    stack, reset = struct.unpack_from("<II", binary)
    if not (0x20000000 < stack <= 0x20040000 and reset & 1 and 0x27000 <= reset < 0xD4000):
        raise ValueError("Application vector table is invalid")
    if version.encode("ascii") not in binary:
        raise ValueError("Expected firmware version marker is missing")

    print(f"OK: DFU manifest, CRC16, UF2 blocks, vectors and version {version}")
    print(f"ZIP/UF2 contain the same {len(binary)} application bytes")
    return zip_path, uf2_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stem", type=Path, help="Firmware filename without .zip/.uf2")
    parser.add_argument("--version", default="v1.18.0-telem-v9")
    parser.add_argument("--write-checksums", action="store_true")
    args = parser.parse_args()
    paths = verify(args.stem, args.version)
    checksums = "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n" for p in paths)
    print(checksums, end="")
    if args.write_checksums:
        args.stem.with_suffix(".sha256").write_text(checksums, encoding="ascii")
