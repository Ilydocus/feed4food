"""
uploadFile/parser.py

Turns a raw uploaded file into a list of row dicts shaped for
`matching.validate_row()`.

Two templates are supported:
  - "cultivation_tasks_v1" - the original "Cultivation tasks and
    PPP-ferti" layout (f4f.xlsx). Fixed 14-column block, header/plot-detail
    rows 0-9, data starts row 10.
  - "crop_log_v1" - the newer, simplified "Crop Log" template. Real header
    row (row 0), one example row (row 1) to skip, plain columns with a
    Task dropdown (Harvest/Input/Planting) and separate Quantity/Unit
    columns instead of the legacy template's compound cells.
"""

import pandas as pd


# Column order for the "cultivation_tasks_v1" template.
# Data rows start at row 10 (0-indexed) - rows 0-9 are the plot header block
# (community/area/plan/block/plot no.) which is handled separately, not per-row.
CULTIVATION_TASKS_V1_COLUMNS = [
    "date",
    "task",
    "crop",
    "col3",
    "irrig_qty",
    "harvest_qty",
    "pest_disease",
    "pest_product",
    "license",
    "active_ing",
    "dosage",
    "total_pest_qty",
    "application_num",
    "pre_harvest_interval",
]

DATA_START_ROW = 10


def _load_dataframe(uploaded_file) -> pd.DataFrame:
    if uploaded_file.name.lower().endswith(".csv"):
        return pd.read_csv(uploaded_file, header=None)
    return pd.read_excel(uploaded_file, header=None)


def parse_cultivation_tasks_v1(uploaded_file) -> list[dict]:
    df = _load_dataframe(uploaded_file)
    df.columns = CULTIVATION_TASKS_V1_COLUMNS + list(df.columns[len(CULTIVATION_TASKS_V1_COLUMNS):])
    data = df.iloc[DATA_START_ROW:]

    rows = []
    for excel_row_number, record in data.iterrows():
        task_raw = record.get("task")
        if pd.isna(task_raw) or str(task_raw).strip() == "":
            continue  # skip blank rows

        production_date = _parse_date(record.get("date"))

        row = {
            "source_row_number": int(excel_row_number) + 1,  # 1-indexed, matches what user sees in Excel
            "action_type_raw": task_raw,
            "production_date": production_date,
            "crop_raw": record.get("crop"),
            "quantity_raw": _first_non_empty(record.get("harvest_qty"), record.get("total_pest_qty")),
            "input_name_raw": record.get("pest_product"),
        }
        rows.append(row)

    return rows


CROP_LOG_V1_SHEET_NAME = "Crop Log"


CROP_LOG_V1_COLUMN_MAP = {
    "Date": "date",
    "Task": "task",
    "Crop / Product": "crop",
    "Quantity": "quantity",
    "Unit": "unit",
    "Input / Fertilizer Name": "input_name",
    "Area (m2)": "area",
}

CROP_LOG_V1_DATA_START_ROW = 1


def _load_crop_log_dataframe(uploaded_file) -> pd.DataFrame:
    if uploaded_file.name.lower().endswith(".csv"):
        return pd.read_csv(uploaded_file, header=0)
    return pd.read_excel(uploaded_file, sheet_name=CROP_LOG_V1_SHEET_NAME, header=0)


def parse_crop_log_v1(uploaded_file) -> list[dict]:
    df = _load_crop_log_dataframe(uploaded_file)
    df = df.rename(columns=CROP_LOG_V1_COLUMN_MAP)
    data = df.iloc[CROP_LOG_V1_DATA_START_ROW:]

    rows = []
    for excel_row_number, record in data.iterrows():
        task_raw = record.get("task")
        if pd.isna(task_raw) or str(task_raw).strip() == "":
            continue 

        production_date = _parse_date(record.get("date"))

        row = {
            "source_row_number": int(excel_row_number) + 2,
            "action_type_raw": task_raw,
            "production_date": production_date,
            "crop_raw": record.get("crop"),
            "quantity_raw": record.get("quantity"),
            "unit_raw": record.get("unit"),
            "input_name_raw": record.get("input_name"),
            "area": record.get("area"),
        }
        rows.append(row)

    return rows


def _first_non_empty(*values):
    for v in values:
        if v is not None and not pd.isna(v) and str(v).strip() != "":
            return v
    return None


def _parse_date(raw_date):
    if raw_date is None or pd.isna(raw_date):
        return None
    try:
        return pd.to_datetime(raw_date).date()
    except (ValueError, TypeError):
        return None


TEMPLATE_PARSERS = {
    "cultivation_tasks_v1": parse_cultivation_tasks_v1,
    "crop_log_v1": parse_crop_log_v1,
}


def parse_file(uploaded_file, template_id: str) -> list[dict]:
    parser_fn = TEMPLATE_PARSERS.get(template_id)
    if parser_fn is None:
        raise ValueError(f"Unknown template '{template_id}'")
    return parser_fn(uploaded_file)