"""
uploadFile/matching.py

Core validation + matching logic for the Excel upload pipeline.
Takes one parsed row (already split into action_type / crop / quantity /
input fields by the file parser) and decides which "bucket" it lands in:

    - "inserted"        -> written to the DB
    - "duplicate"        -> already exists, skipped with a warning
    - "needs_suggestion" -> no exact match, but close candidates found -
                            user is asked "did you mean...?"
    - "error"            -> hard stop, no match and nothing close either -
                            user must fix Excel and re-upload
    - "not_supported"    -> no table for this action type yet (Planting)
    - "ignored"          -> known but intentionally unsupported (Pruning etc.)
    - "unknown"          -> action type not recognised at all
"""

import re
import unicodedata
import datetime
import difflib

from productionReport.models import Product, ProductionReport, ProductionReportDetails
from inputReport.models import Input, InputReport, InputReportDetails
from plantingReport.models import PlantingReport, PlantingReportDetails
from core.reportUtils import CultivationTypes


def _coerce_date(value):
    if value is None or value == "":
        return None
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError:
        return None


def _safe_str(value) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value != value:  # NaN != NaN
        return ""
    return str(value)


def split_crop_list(crop_raw) -> list:
    """'Cucumber/Green beans/Courgette' -> ['Cucumber', 'Green beans', 'Courgette']
    '70 ROCKET-70 CORIANDER' -> ['70 ROCKET', '70 CORIANDER']
    Returns a single-item list if there's nothing to split."""
    text = _safe_str(crop_raw)
    if "/" in text:
        parts = text.split("/")
    elif "-" in text:
        parts = text.split("-")
    else:
        parts = [text]
    return [p.strip() for p in parts if p.strip()]


# ---------------------------------------------------------------------------
# Action type classification
# ---------------------------------------------------------------------------

HARVEST_LABELS = {"harvest"}

# Spraying, Root Irrigation (fertigation despite the name), and Release of
# Beneficial Insects all collapse into a single "input" action - they were
# already treated identically downstream in validate_row, this just makes
# that explicit at classification time instead of splitting them into
# "input"/"insect_input" and merging them again one line later.
# "input" itself is included so the new Crop Log template's Task dropdown
# (Harvest/Input/Planting) classifies directly without needing to know
# which of the three legacy sub-labels it used to be.
INPUT_LABELS = {"input", "spraying", "root irrigation", "release of beneficial insects"}

PLANTING_LABELS = {"planting"}

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
    value = _safe_str(value).strip()
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
#
# DB names are *usually* stored as "<name> - <place>" but not always - some
# entries use "<name> (<place>)", some have no space around the dash, some
# have no separator at all ("<name> <place>"), and some have no place
# suffix whatsoever. So every candidate is compared under several
# normalized representations: the full raw name, the name with a trailing
# "- place"/"(place)" suffix stripped, and a "flattened" form where any
# separator character is collapsed to a space (so dash/paren/comma variants
# and the no-separator case all converge on the same comparable string).
# If none of these produce an exact match, fall back to fuzzy matching and
# surface close candidates as "did you mean...?" suggestions instead of
# silently guessing.
# ---------------------------------------------------------------------------

FUZZY_CUTOFF = 0.72
MAX_SUGGESTIONS = 3

_SEPARATOR_RE = re.compile(r"[-–—(),]")


def _name_variants(db_name: str) -> list:
    """Every normalized form of a DB name worth comparing against."""
    variants = {_normalize_text(db_name)}

    # Strip a trailing "- place" / "– place" style suffix (any dash
    # variant, any spacing, including no space at all).
    m = re.match(r"^(.*?)\s*[-–—]\s*.+$", db_name)
    if m and m.group(1).strip():
        variants.add(_normalize_text(m.group(1)))

    # Strip a trailing "(place)" suffix (any spacing before the paren).
    m = re.match(r"^(.*?)\s*\(.+?\)\s*$", db_name)
    if m and m.group(1).strip():
        variants.add(_normalize_text(m.group(1)))

    # Flattened form: collapse dashes/parens/commas to a single space, so
    # "Tomato-Ioannis", "Tomato - Ioannis", "Tomato(Ioannis)" and
    # "Tomato Ioannis" (no separator at all) all normalize to the same
    # comparable string. This turns the "<product> <place>" case into an
    # exact match instead of relying on fuzzy matching.
    flattened = _SEPARATOR_RE.sub(" ", db_name)
    flattened = re.sub(r"\s+", " ", flattened).strip()
    variants.add(_normalize_text(flattened))

    return variants


def _find_match(raw_name, candidates, name_attr="name"):
    """
    candidates: queryset/list of Product or Input objects
    Returns (exact_match_or_None, [suggestion_objects]) - suggestions are
    only populated when there's no exact match.
    """
    target = _singularize(_normalize_text(raw_name))
    if not target:
        return None, []

    # Pass 1: exact match (after normalization + singularizing) against
    # any variant of the DB name.
    for obj in candidates:
        db_name = getattr(obj, name_attr)
        for variant in _name_variants(db_name):
            if _singularize(variant) == target:
                return obj, []

    # Pass 2: fuzzy match - only offered as suggestions, never auto-applied.
    lookup = {}  # normalized variant -> object
    for obj in candidates:
        db_name = getattr(obj, name_attr)
        for variant in _name_variants(db_name):
            lookup[variant] = obj

    close = difflib.get_close_matches(target, lookup.keys(), n=MAX_SUGGESTIONS, cutoff=FUZZY_CUTOFF)
    suggestions = []
    seen_pks = set()
    for variant in close:
        obj = lookup[variant]
        if obj.pk not in seen_pks:
            suggestions.append(obj)
            seen_pks.add(obj.pk)

    return None, suggestions


def match_product(raw_crop_name: str, living_lab: str):
    candidates = Product.objects.filter(living_lab=living_lab)
    return _find_match(raw_crop_name, candidates, name_attr="name")


def match_input(raw_input_name: str, living_lab: str):
    candidates = Input.objects.filter(living_lab=living_lab)
    return _find_match(raw_input_name, candidates, name_attr="name")


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


def extract_quantity_and_unit(row: dict):
    """
    Returns (number, unit) for a Harvest/Input row, tolerating either
    source format:
      - legacy 'cultivation_tasks_v1' template: quantity and unit combined
        in one cell (quantity_raw='100ml') -> delegates to parse_quantity.
      - new 'crop_log_v1' template: quantity and unit already split into
        separate columns (quantity_raw='100', unit_raw='ml') -> parsed
        directly, no regex splitting needed since there's nothing to split.
    This is the one place that needs to know about the two template
    shapes - everything downstream (resolve_quantity_for_product, duplicate
    checks, etc.) just sees a plain (number, unit) pair either way.
    """
    unit_raw = row.get("unit_raw")
    if unit_raw:
        try:
            number = float(_safe_str(row.get("quantity_raw", "")).strip().replace(",", "."))
        except ValueError:
            return None, None
        return number, _singularize(_safe_str(unit_raw).strip().lower())
    return parse_quantity(row.get("quantity_raw", ""))


def resolve_quantity_for_product(number: float, unit: str, product: Product):
    """
    Convert a parsed (number, unit) into the quantity expected by the
    product's own unit. Returns the converted number, or None if the
    units are incompatible and can't be auto-converted.
    """
    product_unit = _singularize(product.unit.lower())

    if unit == product_unit:
        return number

    if unit in WEIGHT_UNITS_TO_KG and product_unit in WEIGHT_UNITS_TO_KG:
        value_in_kg = number * WEIGHT_UNITS_TO_KG[unit]
        return value_in_kg / WEIGHT_UNITS_TO_KG[product_unit]

    if unit in WEIGHT_UNITS_TO_KG and product_unit not in WEIGHT_UNITS_TO_KG:
        value_in_kg = number * WEIGHT_UNITS_TO_KG[unit]
        return value_in_kg / product.kg_conversion_factor

    return None


# ---------------------------------------------------------------------------
# Planting item parsing
#
# Unlike Harvest (crop name and quantity live in separate columns), Planting
# rows pack quantity + crop name together in one cell, e.g. "70 ROCKET" or
# "53 BLACK CHERRY TOMATO PLANTS". Multi-crop rows chain several of these
# with "-" (already handled generically by split_crop_list before this ever
# runs) - by the time a string reaches parse_planting_item it should be a
# single "<number> <crop name>[ <unit hint>]" item.
#
# ASSUMPTION: when no unit hint word is present at all (no "plants"/"m2"),
# this defaults to CultivationTypes.NbPlants rather than forcing a review -
# every sample row with no explicit unit word was unambiguously a plant
# count. If that's not a safe assumption for other templates/sites, this
# default should instead return unit=None and let validate_row force
# needs_review, same as InputReportDetails.area currently does.
# ---------------------------------------------------------------------------

_PLANTING_UNIT_HINT_RE = re.compile(r"\b(m²|m2|sqm|plants?)\s*$", re.IGNORECASE)


def parse_planting_item(raw_token):
    """'70 ROCKET' -> (70.0, CultivationTypes.NbPlants, 'ROCKET')
    '53 BLACK CHERRY TOMATO PLANTS' -> (53.0, CultivationTypes.NbPlants, 'BLACK CHERRY TOMATO')
    '12 m2 SPINACH' or '12 SPINACH m2' -> (12.0, CultivationTypes.Surface, 'SPINACH')
    Returns (None, None, None) if unparseable."""
    text = _safe_str(raw_token).strip()
    if not text:
        return None, None, None

    match = re.match(r"^(\d+(?:[.,]\d+)?)\s*(.+)$", text)
    if not match:
        return None, None, None

    number = float(match.group(1).replace(",", "."))
    remainder = match.group(2).strip()

    unit = None
    hint = _PLANTING_UNIT_HINT_RE.search(remainder)
    crop_name = remainder
    if hint:
        token = hint.group(1).lower()
        crop_name = remainder[: hint.start()].strip()
        unit = CultivationTypes.Surface if token in ("m²", "m2", "sqm") else CultivationTypes.NbPlants

    if unit is None:
        unit = CultivationTypes.NbPlants  # see ASSUMPTION note above

    if not crop_name:
        return None, None, None

    return number, unit, crop_name


def extract_planting_fields(row: dict):
    """
    Returns (number, unit, crop_name, split_error) for a Planting row,
    tolerating either source format:
      - legacy 'cultivation_tasks_v1' template: quantity and crop name
        packed together in one cell (crop_raw='70 ROCKET'), possibly
        several chained with '-' or '/' (crop_raw='70 ROCKET-70 CORIANDER')
        -> the multi-item guard applies here, routing to the existing
        "Split into Multiple Rows" flow, then parse_planting_item extracts
        the embedded number once split down to one item per row.
      - new 'crop_log_v1' template: quantity, unit, and crop name already
        live in separate columns (crop_raw='Rocket', quantity_raw='70',
        unit_raw='plants') -> nothing to split, crop_raw is only ever a
        single crop name for this template, so the multi-item guard is
        skipped entirely (a literal '-' in a crop name from this template
        would be a real product name, not a delimiter).
    split_error is non-None only for the legacy multi-item case, signalling
    the caller should hard-error rather than treat a parse failure as
    "unreadable quantity".
    """
    unit_raw = row.get("unit_raw")

    if unit_raw:
        crop_name = _safe_str(row.get("crop_raw", "")).strip()
        try:
            number = float(_safe_str(row.get("quantity_raw", "")).strip().replace(",", "."))
        except ValueError:
            return None, None, None, None
        unit_text = _safe_str(unit_raw).strip().lower()
        unit = CultivationTypes.Surface if unit_text in ("m2", "m²", "sqm") else CultivationTypes.NbPlants
        if not crop_name:
            return None, None, None, None
        return number, unit, crop_name, None

    crop_raw = _safe_str(row.get("crop_raw", ""))
    if "/" in crop_raw or "-" in crop_raw:
        return None, None, None, (
            f"Multiple plantings found in one row ('{crop_raw}'). Fix in Excel and re-upload."
        )

    number, unit, crop_name = parse_planting_item(crop_raw)
    return number, unit, crop_name, None


# ---------------------------------------------------------------------------
# Duplicate checks - Harvest AND Input both need this. Neither table has a
# unique constraint in the DB, so this is app-level, keyed on living_lab
# (city) rather than garden, since garden is no longer collected at upload.
# ---------------------------------------------------------------------------

def is_duplicate_harvest(production_date, living_lab: str, product: Product, quantity: float) -> bool:
    return ProductionReportDetails.objects.filter(
        name=product,
        quantity=quantity,
        report_id__production_date=production_date,
        report_id__city=living_lab,
    ).exists()


def is_duplicate_input(application_date, living_lab: str, input_obj: Input, product: Product, quantity: float) -> bool:
    return InputReportDetails.objects.filter(
        name_input=input_obj,
        name_product=product,
        quantity=quantity,
        report_id__application_date=application_date,
        report_id__city=living_lab,
    ).exists()


def is_duplicate_planting(planting_date, living_lab: str, product: Product, quantity: float) -> bool:
    return PlantingReportDetails.objects.filter(
        name=product,
        area_quantity_planted=quantity,
        report_id__planting_date=planting_date,
        report_id__city=living_lab,
    ).exists()


# ---------------------------------------------------------------------------
# Main entry point - validate one parsed row
# ---------------------------------------------------------------------------

def _suggestion_result(field_label: str, field_key: str, raw_value: str, suggestions: list) -> dict:
    names = [s.name for s in suggestions]
    return {
        "bucket": "needs_suggestion",
        "message": f"Couldn't find an exact match for {field_label} '{raw_value}'. Did you mean: {', '.join(names)}?",
        "suggestions": names,
        "suggestion_field": field_key,
    }


def validate_row(row: dict, living_lab: str) -> dict:
    """
    row expected keys: action_type_raw, crop_raw, quantity_raw,
                        (for input rows) input_name_raw
    Returns: {"bucket": ..., "message": ..., "product": ..., "quantity": ...}
    """
    action = classify_action_type(row.get("action_type_raw", ""))
    row = {**row, "production_date": _coerce_date(row.get("production_date"))}

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
        crop_raw = row.get("crop_raw", "")
        product, suggestions = match_product(crop_raw, living_lab)
        if product is None:
            if suggestions:
                return _suggestion_result("crop", "crop_raw", crop_raw, suggestions)
            return {
                "bucket": "error",
                "message": f"'{crop_raw}' does not match any known product. Fix in Excel and re-upload.",
            }

        number, unit = extract_quantity_and_unit(row)
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

        if is_duplicate_harvest(row.get("production_date"), living_lab, product, quantity):
            return {"bucket": "duplicate", "message": f"'{product.name}' entry already exists - skipped."}

        return {
            "bucket": "inserted",
            "report_type": "harvest",
            "product": product,
            "quantity": quantity,
            "message": f"Matched to '{product.name}'. {quantity} {product.unit} will be recorded as harvested.",
        }

    if action == "input":
        crop_raw = _safe_str(row.get("crop_raw", ""))
        if "/" in crop_raw or "-" in crop_raw:
            return {
                "bucket": "error",
                "message": f"Multiple products found in one row ('{crop_raw}'). Fix in Excel and re-upload.",
            }

        input_name_raw = row.get("input_name_raw", "")
        input_obj, input_suggestions = match_input(input_name_raw, living_lab)
        if input_obj is None:
            if input_suggestions:
                return _suggestion_result("input/fertilizer", "input_name_raw", input_name_raw, input_suggestions)
            return {
                "bucket": "error",
                "message": f"'{input_name_raw}' does not match any known input. Fix in Excel and re-upload.",
            }

        product, product_suggestions = match_product(crop_raw, living_lab)
        if product is None:
            if product_suggestions:
                return _suggestion_result("crop", "crop_raw", crop_raw, product_suggestions)
            return {
                "bucket": "error",
                "message": f"'{crop_raw}' does not match any known product. Fix in Excel and re-upload.",
            }

        number, unit = extract_quantity_and_unit(row)
        if number is None:
            return {
                "bucket": "error",
                "message": f"Missing or unreadable quantity '{row.get('quantity_raw')}'. Fix in Excel and re-upload.",
            }

        if is_duplicate_input(row.get("production_date"), living_lab, input_obj, product, number):
            return {"bucket": "duplicate", "message": f"'{input_obj.name}' on '{product.name}' already exists - skipped."}

        return {
            "bucket": "inserted",
            "report_type": "input",
            "input": input_obj,
            "product": product,
            "quantity": number,
            "message": f"Matched '{input_obj.name}' applied to '{product.name}'. Quantity: {number}.",
        }

    if action == "planting":
        number, unit, crop_name, split_error = extract_planting_fields(row)
        if split_error:
            return {
                "bucket": "error",
                "message": split_error,
            }
        if number is None:
            return {
                "bucket": "error",
                "message": f"Could not read planting quantity from '{row.get('crop_raw')}'. Fix in Excel and re-upload.",
            }

        product, suggestions = match_product(crop_name, living_lab)
        if product is None:
            if suggestions:
                return _suggestion_result("crop", "crop_raw", crop_name, suggestions)
            return {
                "bucket": "error",
                "message": f"'{crop_name}' does not match any known product. Fix in Excel and re-upload.",
            }

        if is_duplicate_planting(row.get("production_date"), living_lab, product, number):
            return {"bucket": "duplicate", "message": f"'{product.name}' planting entry already exists - skipped."}

        return {
            "bucket": "inserted",
            "report_type": "planting",
            "product": product,
            "quantity": number,
            "planting_unit": unit,
            "message": f"Matched to '{product.name}'. {number} {unit} will be recorded as planted.",
        }

    return {"bucket": "unknown", "message": f"Unhandled action type '{action}'."}