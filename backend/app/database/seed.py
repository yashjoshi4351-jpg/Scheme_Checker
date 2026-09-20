import json
from pathlib import Path

from app.database.database import SessionLocal, create_tables
from app.database.crud import (
    create_scheme,
    create_rule,
    get_scheme
)


# ==================================================
# File Paths
# ==================================================

BASE_DIR = Path(__file__).resolve().parents[1]

SCHEMES_FILE = BASE_DIR / "data" / "schemes.json"
RULES_FILE = BASE_DIR / "data" / "rules.json"


# ==================================================
# Load JSON
# ==================================================

def load_json(file_path: Path):

    if not file_path.exists():
        raise FileNotFoundError(
            f"JSON file not found: {file_path}"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


# ==================================================
# Seed Database
# ==================================================

def seed_database():

    # Create tables first
    create_tables()

    raw_schemes = load_json(SCHEMES_FILE)
    schemes_data = raw_schemes.get("schemes", raw_schemes) if isinstance(raw_schemes, dict) else raw_schemes

    raw_rules = load_json(RULES_FILE)
    rules_data = raw_rules.get("rules", raw_rules) if isinstance(raw_rules, dict) else raw_rules

    db = SessionLocal()

    try:

        # ------------------------------------------
        # Insert Schemes
        # ------------------------------------------

        for scheme_data in schemes_data:

            scheme_id_code = scheme_data.get("scheme_id")
            existing_scheme = get_scheme(
                db,
                scheme_id_code
            )

            if existing_scheme:
                print(
                    f"Scheme already exists: "
                    f"{scheme_data.get('name')}"
                )
                continue

            scheme = create_scheme(
                db,
                scheme_data
            )

            print(
                f"Added scheme: {scheme.name} ({scheme.scheme_id})"
            )

        # ------------------------------------------
        # Insert Rules
        # ------------------------------------------

        for rule_group in rules_data:

            scheme_identifier = rule_group.get("scheme_id")

            scheme = get_scheme(
                db,
                scheme_identifier
            )

            if not scheme:
                print(
                    f"Warning: Scheme not found "
                    f"for rules of {scheme_identifier}"
                )
                continue

            sub_rules = rule_group.get("rules", [])
            # If the entry itself is a single rule
            if not sub_rules and "field" in rule_group:
                sub_rules = [rule_group]

            for r_idx, rule_item in enumerate(sub_rules):
                field_name = rule_item.get("field", f"rule_{r_idx}")
                rule_item_dict = dict(rule_item)
                if not rule_item_dict.get("rule_id"):
                    rule_item_dict["rule_id"] = f"{scheme.scheme_id}_{field_name}"

                create_rule(
                    db,
                    scheme,
                    rule_item_dict
                )

                print(
                    f"  Added rule: {rule_item_dict['rule_id']}"
                )

        print("\nDatabase seeding completed successfully.")

    finally:
        db.close()


# ==================================================
# Run Seeder
# ==================================================

if __name__ == "__main__":
    seed_database()