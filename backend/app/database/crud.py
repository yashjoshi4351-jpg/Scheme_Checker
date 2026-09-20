import json
from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.scheme import Scheme
from app.models.rule import Rule
from app.models.eligibility_result import EligibilityResult


# ==================================================
# USER CRUD
# ==================================================

def create_user(
    db: Session,
    user_data: dict
) -> User:
    extra_data = user_data.get("extra_data")
    if isinstance(extra_data, dict):
        extra_data = json.dumps(extra_data)

    user = User(
        name=user_data.get("name") or "Citizen",
        age=user_data.get("age"),
        gender=user_data.get("gender"),
        state=user_data.get("state"),
        district=user_data.get("district"),
        rural_urban=user_data.get("rural_urban"),
        category=user_data.get("category"),
        annual_income=user_data.get("annual_income"),
        family_size=user_data.get("family_size"),
        employment_status=user_data.get("employment_status"),
        education_level=user_data.get("education_level") or user_data.get("education"),
        occupation=user_data.get("occupation"),
        marital_status=user_data.get("marital_status"),
        farmer=bool(user_data.get("farmer") or user_data.get("is_farmer")),
        land_ownership=bool(user_data.get("land_ownership")),
        disability=bool(user_data.get("disability") or user_data.get("has_disability")),
        house_ownership=bool(user_data.get("house_ownership") or user_data.get("owns_house")),
        bpl_status=bool(user_data.get("bpl_status") or user_data.get("is_bpl")),
        student_status=bool(user_data.get("student_status")),
        street_vendor=bool(user_data.get("street_vendor")),
        minority=bool(user_data.get("minority")),
        extra_data=extra_data,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user(
    db: Session,
    user_id: int
) -> Optional[User]:
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


# Alias for dependency compatibility
get_user_by_id = get_user


def update_user(
    db: Session,
    user_id: int,
    user_data: dict
) -> Optional[User]:
    user = get_user(db, user_id)
    if not user:
        return None

    for key, value in user_data.items():
        if hasattr(user, key) and key != "id":
            if key == "extra_data" and isinstance(value, dict):
                value = json.dumps(value)
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(
    db: Session,
    user_id: int
) -> bool:
    user = get_user(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True


# ==================================================
# SCHEME CRUD
# ==================================================

def create_scheme(
    db: Session,
    scheme_data: dict
) -> Scheme:
    benefits_val = scheme_data.get("benefits")
    if isinstance(benefits_val, dict):
        benefits_val = benefits_val.get("description") or json.dumps(benefits_val)
    elif isinstance(benefits_val, list):
        benefits_val = json.dumps(benefits_val)

    app_url = scheme_data.get("application_url")
    if not app_url and isinstance(scheme_data.get("application"), dict):
        app_url = scheme_data.get("application", {}).get("official_url")

    scheme = Scheme(
        scheme_id=scheme_data.get("scheme_id"),
        name=scheme_data.get("name"),
        ministry=scheme_data.get("ministry"),
        level=scheme_data.get("level"),
        description=scheme_data.get("description"),
        benefits=benefits_val,
        application_url=app_url,
        is_active=scheme_data.get("is_active", True)
    )

    db.add(scheme)
    db.commit()
    db.refresh(scheme)

    return scheme


def get_scheme(
    db: Session,
    scheme_identifier: Union[str, int]
) -> Optional[Scheme]:
    if isinstance(scheme_identifier, int) or (isinstance(scheme_identifier, str) and scheme_identifier.isdigit()):
        scheme = db.query(Scheme).filter(Scheme.id == int(scheme_identifier)).first()
        if scheme:
            return scheme

    return (
        db.query(Scheme)
        .filter(Scheme.scheme_id == str(scheme_identifier))
        .first()
    )


# Alias for dependency compatibility
get_scheme_by_id = get_scheme


def get_all_schemes(
    db: Session,
    active_only: bool = True
) -> List[Scheme]:
    query = db.query(Scheme)
    if active_only:
        query = query.filter(Scheme.is_active.is_(True))
    return query.all()


# ==================================================
# RULE CRUD
# ==================================================

def create_rule(
    db: Session,
    scheme: Scheme,
    rule_data: dict
) -> Rule:
    val = rule_data.get("value")
    if isinstance(val, (list, dict)):
        val_str = json.dumps(val)
    elif val is not None:
        val_str = str(val)
    else:
        val_str = None

    rule_id = rule_data.get("rule_id") or f"{scheme.scheme_id}_{rule_data.get('field')}"

    rule = Rule(
        scheme_id=scheme.id,
        rule_id=rule_id,
        field=rule_data.get("field"),
        operator=rule_data.get("operator"),
        value=val_str,
        description=rule_data.get("description"),
        is_required=rule_data.get("is_required", True)
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule


def get_rules_for_scheme(
    db: Session,
    scheme_identifier: Union[int, str]
) -> List[Rule]:
    scheme = get_scheme(db, scheme_identifier)
    if not scheme:
        return []

    return (
        db.query(Rule)
        .filter(Rule.scheme_id == scheme.id)
        .all()
    )


# ==================================================
# ELIGIBILITY RESULT CRUD
# ==================================================

def create_eligibility_result(
    db: Session,
    scheme_id: int,
    status: str,
    user_id: Optional[int] = None,
    reason: Optional[str] = None,
    matched_rules: Optional[Any] = None,
    failed_rules: Optional[Any] = None,
    profile_snapshot: Optional[Dict[str, Any]] = None
) -> EligibilityResult:
    result = EligibilityResult(
        user_id=user_id,
        scheme_id=scheme_id,
        status=status,
        reason=reason,
        matched_rules=json.dumps(matched_rules)
        if matched_rules is not None
        else None,
        failed_rules=json.dumps(failed_rules)
        if failed_rules is not None
        else None,
        profile_snapshot=json.dumps(profile_snapshot)
        if profile_snapshot is not None
        else None
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result


def get_user_results(
    db: Session,
    user_id: int
) -> List[EligibilityResult]:
    return (
        db.query(EligibilityResult)
        .filter(EligibilityResult.user_id == user_id)
        .order_by(EligibilityResult.checked_at.desc())
        .all()
    )


def get_all_eligibility_results(
    db: Session,
    limit: int = 100
) -> List[EligibilityResult]:
    return (
        db.query(EligibilityResult)
        .order_by(EligibilityResult.checked_at.desc())
        .limit(limit)
        .all()
    )


def delete_eligibility_result(
    db: Session,
    result_id: int
) -> bool:
    res = (
        db.query(EligibilityResult)
        .filter(EligibilityResult.id == result_id)
        .first()
    )
    if not res:
        return False

    db.delete(res)
    db.commit()
    return True