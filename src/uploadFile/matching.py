"""
uploadFile/matching.py

Core validation + matching logic for the Excel upload pipeline.
Takes one parsed row (already split into action_type / crop / quantity /
input fields by the file parser) and decides which "bucket" it lands in:

    - "inserted"       -> written to the DB
    - "duplicate"       -> already exists, skipped with a warning
    - "error"           -> hard stop, user must fix Excel and re-upload
    - "not_supported"   -> no table for this action type yet (Planting)
    - "ignored"         -> known but intentionally unsupported (Pruning etc.)
    - "unknown"         -> action type not recognised at all

"""

import re
import unicodedata

from productionReport.models import Product, ProductionReportDetails
from inputReport.models import Input


# ---------------------------------------------------------------------------
# Action type classification
# ---------------------------------------------------------------------------

HARVEST_LABELS = {"harvest"}

INPUT_LABELS = {"spraying", "root irrigation"}          # -> InputReport, normal product match
INSECT_LABELS = {"release of beneficial insects"}       # -> InputReport, input_category = "other"

PLANTING_LABELS = {"planting"}                           # no model yet

IGNORED_LABELS = {
    "pruning",
    "pruning-staking",
    "weeding",
    "tomatoes staking",
    "incorporation",
    "works",
    "compost",
    "cleaning all plants and solar sterilization",
}


def classify_action_type(raw_task: str) -> str:
    task = _normalize_text(raw_task)

    if task in HARVEST_LABELS:
        return "harvest"
    if task in INPUT_LABELS:
        return "input"
    if task in INSECT_LABELS:
        return "insect_input"
    if task in PLANTING_LABELS:
        return "planting"
    if task in IGNORED_LABELS:
        return "ignored"
    return "unknown"


# ---------------------------------------------------------------------------
# Text normalization (casing, whitespace, Greek/Latin homoglyphs)
# ---------------------------------------------------------------------------

GREEK_TO_LATIN = {
    "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I", "Κ": "K",
    "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T", "Υ": "Y", "Χ": "X",
    "α": "a", "τ": "t", "ο": "o", "ε": "e", "η": "h",
}


def _normalize_text(value: str) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    value = "".join(GREEK_TO_LATIN.get(ch, ch) for ch in value)
    value = unicodedata.normalize("NFKC", value)
    return value.lower()


def _singularize(word: str) -> str:
    if word.endswith("es"):
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


# ---------------------------------------------------------------------------
# Product / Input matching
# ---------------------------------------------------------------------------

def _strip_living_lab_suffix(db_name: str) -> str:
    """DB names are stored as '<name> - <place>'. Strip the place part."""
    return db_name.rsplit(" - ", 1)[0]


def match_product(raw_crop_name: str, living_lab: str) -> Product | None:
    target = _normalize_text(raw_crop_name)
    target = _singularize(target)

    candidates = Product.objects.filter(living_lab=living_lab)
    for product in candidates:
        db_name = _normalize_text(_strip_living_lab_suffix(product.name))
        if _singularize(db_name) == target:
            return product
    return None


def match_input(raw_input_name: str, living_lab: str) -> Input | None:
    target = _normalize_text(raw_input_name)

    candidates = Input.objects.filter(living_lab=living_lab)
    for input_obj in candidates:
        db_name = _normalize_text(_strip_living_lab_suffix(input_obj.name))
        if db_name == target:
            return input_obj
    return None


# ---------------------------------------------------------------------------
# Quantity + unit parsing / conversion
# ---------------------------------------------------------------------------

WEIGHT_UNITS_TO_KG = {
    "kg": 1.0,
    "g": 0.001,
    "gr": 0.001,
}


def parse_quantity(raw_value: str):
    """'0,5 kg' -> (0.5, 'kg'). Returns (None, None) if unparseable."""
    if raw_value is None:
        return None, None
    text = str(raw_value).strip().replace(",", ".")
    match = re.match(r"^(\d+(?:\.\d+)?)\s*([a-zA-Z]+)$", text)
    if not match:
        return None, None
    number = float(match.group(1))
    unit = match.group(2).lower()
    return number, _singularize(unit)


def resolve_quantity_for_product(number: float, unit: str, product: Product):
    """
    Convert a parsed (number, unit) into the quantity expected by the
    product's own unit. Returns the converted number, or None if the
    units are incompatible and can't be auto-converted.
    """
    product_unit = _singularize(product.unit.lower())

    # Same unit already - no conversion needed
    if unit == product_unit:
        return number

    # Both are weight units (kg/g/gr) - convert via kg_conversion_factor
    if unit in WEIGHT_UNITS_TO_KG and product_unit in WEIGHT_UNITS_TO_KG:
        value_in_kg = number * WEIGHT_UNITS_TO_KG[unit]
        return value_in_kg / WEIGHT_UNITS_TO_KG[product_unit]

    if unit in WEIGHT_UNITS_TO_KG and product_unit not in WEIGHT_UNITS_TO_KG:
        # e.g. excel gives "1.2 kg" but product's unit is "bunch" - can't convert
        value_in_kg = number * WEIGHT_UNITS_TO_KG[unit]
        return value_in_kg / product.kg_conversion_factor

    # Non-weight units that don't match (e.g. "bunch" vs "head") - can't auto-convert
    return None


# ---------------------------------------------------------------------------
# Duplicate check (Harvest only - no unique constraint in the DB)
# ---------------------------------------------------------------------------

def is_duplicate_harvest(production_date, garden, product: Product, quantity: float) -> bool:
    return ProductionReportDetails.objects.filter(
        name=product,
        quantity=quantity,
        report_id__production_date=production_date,
        report_id__garden=garden,
    ).exists()


# ---------------------------------------------------------------------------
# Main entry point - validate one parsed row
# ---------------------------------------------------------------------------

def validate_row(row: dict, living_lab: str, garden) -> dict:
    """
    row expected keys: action_type_raw, crop_raw, quantity_raw,
                        (for input rows) input_name_raw
    Returns: {"bucket": ..., "message": ..., "product": ..., "quantity": ...}
    """
    action = classify_action_type(row.get("action_type_raw", ""))

    if action == "planting":
        return {"bucket": "not_supported", "message": "Planting rows are not entered - no table for this yet."}

    if action == "ignored":
        return {"bucket": "ignored", "message": f"'{row.get('action_type_raw')}' rows are ignored - not supported yet."}

    if action == "unknown":
        return {
            "bucket": "unknown",
            "message": (
                f"Unrecognized crop management type '{row.get('action_type_raw')}'. "
                "If this looks wrong, contact the Feed4Food team."
            ),
        }

    if action == "harvest":
        product = match_product(row.get("crop_raw", ""), living_lab)
        if product is None:
            return {
                "bucket": "error",
                "message": f"'{row.get('crop_raw')}' does not match any known product. Fix in Excel and re-upload.",
            }

        number, unit = parse_quantity(row.get("quantity_raw", ""))
        if number is None:
            return {
                "bucket": "error",
                "message": f"Could not read quantity '{row.get('quantity_raw')}'. Fix in Excel and re-upload.",
            }

        quantity = resolve_quantity_for_product(number, unit, product)
        if quantity is None:
            return {
                "bucket": "error",
                "message": (
                    f"Unit '{unit}' does not match expected unit '{product.unit}' "
                    f"for '{product.name}'. Fix in Excel and re-upload."
                ),
            }

        if is_duplicate_harvest(row.get("production_date"), garden, product, quantity):
            return {"bucket": "duplicate", "message": f"'{product.name}' entry already exists - skipped."}

        return {"bucket": "inserted", "product": product, "quantity": quantity}

    if action in ("input", "insect_input"):
        # For now: multi-product cells and missing quantity are hard errors, no auto-split
        crop_raw = row.get("crop_raw", "")
        if "/" in crop_raw or "-" in crop_raw:
            return {
                "bucket": "error",
                "message": f"Multiple products found in one row ('{crop_raw}'). Fix in Excel and re-upload.",
            }

        input_obj = match_input(row.get("input_name_raw", ""), living_lab)
        if input_obj is None:
            return {
                "bucket": "error",
                "message": f"'{row.get('input_name_raw')}' does not match any known input. Fix in Excel and re-upload.",
            }

        product = match_product(crop_raw, living_lab)
        if product is None:
            return {
                "bucket": "error",
                "message": f"'{crop_raw}' does not match any known product. Fix in Excel and re-upload.",
            }

        number, unit = parse_quantity(row.get("quantity_raw", ""))
        if number is None:
            return {
                "bucket": "error",
                "message": f"Missing or unreadable quantity '{row.get('quantity_raw')}'. Fix in Excel and re-upload.",
            }

        return {"bucket": "inserted", "input": input_obj, "product": product, "quantity": number}

    return {"bucket": "unknown", "message": f"Unhandled action type '{action}'."}