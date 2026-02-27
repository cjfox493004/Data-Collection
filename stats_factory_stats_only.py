from typing import List
import csv

from models import Stats


def _to_int(val: str) -> int | None:
    if val is None:
        return None
    v = str(val).strip()
    if v == "":
        return None
    try:
        return int(v)
    except ValueError:
        digits = "".join(ch for ch in v if ch.isdigit() or ch == '-')
        try:
            return int(digits) if digits != "" else None
        except Exception:
            return None


def _to_float(val: str) -> float | None:
    if val is None:
        return None
    v = str(val).strip()
    if v == "":
        return None
    try:
        return float(v)
    except ValueError:
        if v.startswith('.'):
            try:
                return float('0' + v)
            except ValueError:
                return None
        return None


def generate_stats_from_stats_new(csv_path: str = "stats_new.csv") -> List[Stats]:
    """Parse `stats_new.csv` and return a list of `Stats` instances.

    Skips rows missing `First_Name` or `Last_Name`.
    """
    stats_list: List[Stats] = []

    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            first = (row.get("First_Name") or "").strip()
            last = (row.get("Last_Name") or "").strip()
            if not first or not last:
                continue

            number = _to_int(row.get("Number"))

            stat = Stats(
                first_name=first,
                last_name=last,
                number=number,
                gp=_to_int(row.get("GP")),
                blk=_to_int(row.get("BLK")),
                g=_to_int(row.get("G")),
                a=_to_int(row.get("A")),
                pts=_to_int(row.get("PTS")),
                sh=_to_int(row.get("SH")),
                sh_pct=_to_float(row.get("SH_PCT")),
                plus_minus=_to_int(row.get("Plus_Minus")),
                ppg=_to_int(row.get("PPG")),
                shg=_to_int(row.get("SHG")),
                fg=_to_int(row.get("FG")),
                gwg=_to_int(row.get("GWG")),
                gtg=_to_int(row.get("GTG")),
                otg=_to_int(row.get("OTG")),
                htg=_to_int(row.get("HTG")),
                uag=_to_int(row.get("UAG")),
                pn_pim=(row.get("PN-PIM") or "").strip() or None,
                minutes=_to_int(row.get("MIN")),
                maj=_to_int(row.get("MAJ")),
                oth=_to_int(row.get("OTH")),
            )

            stats_list.append(stat)

    return stats_list


__all__ = ["generate_stats_from_stats_new"]
