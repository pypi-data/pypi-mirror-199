"""
A parser for the output file from Crystal Disk Info
"""

from __future__ import annotations

import dataclasses
import enum
import functools
import pathlib
import platform
import shutil
import subprocess

CRYSTAL_DISK_INFO_X64_NAME = "DiskInfo64.exe"
CRYSTAL_DISK_INFO_X32_NAME = "DiskInfo32.exe"


def is_64bit_os() -> bool:
    """
    Returns True if the OS is 64-bit, False otherwise.
    """
    return platform.machine().endswith("64")


@dataclasses.dataclass(frozen=True, eq=True)
class DiskSMARTAttribute:
    """
    Holds data for a single SMART attribute.
    """

    id: int
    name: str
    raw: int
    current: int | None = None
    worst: int | None = None
    threshold: int | None = None


@dataclasses.dataclass(frozen=True, eq=True)
class DiskHealth:
    """
    Holds health data for a disk.
    """

    status: str
    smart: tuple[DiskSMARTAttribute]
    percent: int | None


@dataclasses.dataclass(frozen=True, eq=True)
class Disk:
    """
    Holds data for a single disk.
    """

    model: str | None = None
    firmware: str | None = None
    serial: str | None = None
    size: str | None = None
    health: DiskHealth | None = None
    raw: dict[str, str] | None = None

    @classmethod
    def from_info(
        cls, raw_disk_attrs: dict, disk_smart_attrs: list[DiskSMARTAttribute]
    ) -> Disk:
        """
        Creates a Disk object from the raw disk info and SMART attributes.
        """
        health_status = raw_disk_attrs.get("Health Status", "Unknown")
        health_percent = None
        health_str = health_status.split("(")[0].strip()
        try:
            health_percent = int(
                health_status.split(" ")[1].split("(")[1].split(" ")[0]
            )
        except IndexError:
            pass

        return cls(
            model=raw_disk_attrs.get("Model", None),
            firmware=raw_disk_attrs.get("Firmware", None),
            serial=raw_disk_attrs.get("Serial Number", None),
            size=raw_disk_attrs.get("Disk Size", None).split("(")[0].strip()
            if raw_disk_attrs.get("Disk Size", None)
            else None,
            health=DiskHealth(
                status=health_str, smart=tuple(disk_smart_attrs), percent=health_percent
            ),
            raw=raw_disk_attrs,
        )

    def __repr__(self):
        """
        Returns a string representation of the Disk object.
        """
        return f"<Disk - {self.model} - {self.serial} - {self.size}>"


class ParseState(enum.Enum):
    """
    Used for the parsing state machine
    """

    Header = enum.auto()
    Other = enum.auto()
    DiskList = enum.auto()
    DiskHeader = enum.auto()
    DiskInfo = enum.auto()
    DiskSmartHeader = enum.auto()
    DiskSmartAta = enum.auto()
    DiskSmartNvme = enum.auto()


@dataclasses.dataclass(unsafe_hash=True)
class CrystalDiskInfo:
    """
    A class for parsing the output file from Crystal Disk Info
    """

    exe: pathlib.Path | None = None

    @functools.cache
    def is_shim(self) -> False:
        """
        Returns True if the exe is a chocolatey shim, False otherwise.
        """
        try:
            return (
                "shim"
                in subprocess.check_output(
                    [
                        "powershell",
                        f'(Get-Item "{self.exe}").VersionInfo.FileDescription',
                    ]
                ).decode()
            )
        except subprocess.CalledProcessError:
            return False

    @property
    def dump_dir(self):
        """
        Returns the directory that the DiskInfo.txt file will be dumped to.
        """
        if self.is_shim():
            # chocolatey is weird.. it has a shim, but the actual exe is in a different place, so running /CopyExit leaves the output in real exe's place.
            dump_dir = self.exe.parent.parent / "lib/crystaldiskinfo.portable/tools"
        else:
            dump_dir = self.exe.parent

        if not dump_dir.is_dir():
            raise FileNotFoundError(f"Could not find dump dir for {self.exe}")

        return dump_dir

    @classmethod
    def get(cls) -> CrystalDiskInfo:
        """
        Returns a filled out instance of CrystalDiskInfo with references to the installed Crystal Disk Info executable
        """
        exe_name = (
            CRYSTAL_DISK_INFO_X64_NAME if is_64bit_os() else CRYSTAL_DISK_INFO_X32_NAME
        )
        exe_full_path = None
        if full_path := shutil.which(exe_name):
            exe_full_path = pathlib.Path(full_path)
        elif full_path := shutil.which(CRYSTAL_DISK_INFO_X32_NAME):
            # if the native version isn't found, see if we can find the 32 bit version.
            exe_full_path = pathlib.Path(full_path)

        for test_dir in (
            pathlib.Path(r"C:\Program Files\CrystalDiskInfo"),
            pathlib.Path(r"C:\Program Files (x86)\CrystalDiskInfo"),
        ):
            possible_exe = test_dir / exe_name
            if possible_exe.is_file():
                exe_full_path = possible_exe
                break

        if exe_full_path:
            return cls(exe_full_path)

        raise ValueError(
            "Unable to make a CrystalDiskInfo object... was crystal disk info installed?"
        )

    def get_raw_disk_info(self) -> str:
        """
        Returns the raw disk info string from Crystal Disk Info

        Note that if we are not running as admin, the user may be prompted by UAC.
        """
        args = [str(self.exe)]
        if self.is_shim():
            args.append("--shimgen-waitforexit")
        args.append("/CopyExit")
        subprocess.check_call(args)
        return (self.dump_dir / "DiskInfo.txt").read_text()

    def get_disks(self, disk_info_file: pathlib.Path | None = None) -> list[Disk]:
        """
        Returns a list of Disk objects from the raw disk info string.

        If disk_info_file is provided, it will be used instead of calling crystal disk info directly to get the raw disk info.
        """
        ret_disks = []
        if disk_info_file:
            raw_disk_info_lines = disk_info_file.read_text().splitlines()
        else:
            raw_disk_info_lines = self.get_raw_disk_info().splitlines()
        state = ParseState.Header
        raw_disk_attrs = {}
        disk_smart_attrs = []

        for line in raw_disk_info_lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("-- Disk List "):
                state = ParseState.DiskList
                continue

            if state in (ParseState.DiskList, ParseState.Other):
                if line.startswith("----"):
                    state = ParseState.DiskHeader
                    continue

            if state == ParseState.DiskHeader:
                if line.startswith("----"):
                    state = ParseState.DiskInfo

                    if raw_disk_attrs:
                        ret_disks.append(
                            Disk.from_info(raw_disk_attrs, disk_smart_attrs)
                        )

                    raw_disk_attrs = {}
                    disk_smart_attrs = []
                    continue

            if state == ParseState.DiskInfo:
                if line.startswith("-- S.M.A.R.T."):
                    state = ParseState.DiskSmartHeader
                    continue

                key, value = [a.strip() for a in line.split(":", 1)]
                raw_disk_attrs[key] = value

            if state == ParseState.DiskSmartHeader:
                if "Cur" in line:
                    state = ParseState.DiskSmartAta
                    continue
                else:
                    state = ParseState.DiskSmartNvme
                    continue

            if state in (ParseState.DiskSmartAta, ParseState.DiskSmartNvme):
                line = line.replace("_", "")
                if line.startswith("--"):
                    state = ParseState.Other
                    continue

            if state == ParseState.DiskSmartAta:
                if line[0].lower() in "0123456789abcdef":
                    attr_id, cur, wor, thr, attr_raw, attr_name = [
                        a.strip() for a in line.split(None, 5)
                    ]
                    disk_smart_attrs.append(
                        DiskSMARTAttribute(
                            int(attr_id, 16),
                            attr_name,
                            int(attr_raw, 16),
                            int(cur),
                            worst=int(wor),
                            threshold=int(thr),
                        )
                    )
            if state == ParseState.DiskSmartNvme:
                if line[0].lower() in "0123456789abcdef":
                    attr_id, attr_raw, attr_name = [
                        a.strip() for a in line.split(None, 2)
                    ]
                    disk_smart_attrs.append(
                        DiskSMARTAttribute(
                            int(attr_id, 16), attr_name, int(attr_raw, 16)
                        )
                    )

        if raw_disk_attrs:
            ret_disks.append(Disk.from_info(raw_disk_attrs, disk_smart_attrs))

        return ret_disks
