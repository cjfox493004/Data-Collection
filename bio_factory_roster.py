from typing import List
import csv
import re

from models import Bio


def _to_int(val: str) -> int | None:
    v = (val or "").strip()
    if v == "":
        return None
    try:
        return int(v)
    except ValueError:
        digits = re.sub(r"\D", "", v)
        return int(digits) if digits else None


def generate_bios_from_roster(csv_path: str = "roster.csv") -> List[Bio]:
    """Parse `csv_path` (roster format) and return a list of `Bio` instances.

    Expected headers: `Number,First Name,Last Name,Position,Weight,Height,Hometown,Class,High School`.
    """
    bios: List[Bio] = []

    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            first = (row.get("First Name") or "").strip()
            last = (row.get("Last Name") or "").strip()
            if not first or not last:
                continue

            number = _to_int(row.get("Number"))
            position = (row.get("Position") or "").strip() or None
            height = (row.get("Height") or "").strip() or None
            weight = _to_int(row.get("Weight"))
            academic_class = (row.get("Class") or "").strip() or None
            hometown = (row.get("Hometown") or "").strip() or None
            high_school = (row.get("High School") or "").strip() or None

            bio = Bio(
                first_name=first,
                last_name=last,
                number=number,
                position=position,
                height=height,
                weight=weight,
                academic_class=academic_class,
                hometown=hometown,
                high_school=high_school,
            )
            bios.append(bio)

    return bios


__all__ = ["generate_bios_from_roster"]
