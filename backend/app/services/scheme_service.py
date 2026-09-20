from typing import Any, Dict, List, Optional, Union

from app.database import crud


class SchemeService:
    """
    Handles government scheme retrieval and management.
    """

    def __init__(self, db):
        self.db = db

    def get_all_schemes(
        self,
        active_only: bool = True,
    ) -> List[Any]:
        return crud.get_all_schemes(
            self.db,
            active_only=active_only,
        )

    def get_scheme(
        self,
        scheme_id: Union[int, str],
    ) -> Optional[Any]:
        return crud.get_scheme(
            self.db,
            scheme_id,
        )

    def get_rules(
        self,
        scheme_id: Union[int, str],
    ) -> List[Any]:
        return crud.get_rules_for_scheme(
            self.db,
            scheme_id,
        )

    def search_schemes(
        self,
        query: Optional[str] = None,
        state: Optional[str] = None,
        category: Optional[str] = None,
        occupation: Optional[str] = None,
        keyword: Optional[str] = None,
    ) -> List[Any]:
        schemes = self.get_all_schemes()

        term = (query or keyword or "").lower().strip()
        state_filter = (state or "").lower().strip()
        cat_filter = (category or "").lower().strip()
        occ_filter = (occupation or "").lower().strip()

        filtered = []
        for scheme in schemes:
            name = str(getattr(scheme, "name", "")).lower()
            desc = str(getattr(scheme, "description", "")).lower()
            ministry = str(getattr(scheme, "ministry", "")).lower()
            scheme_cat = str(getattr(scheme, "category", "")).lower()
            scheme_state = str(getattr(scheme, "state", "") or "").lower()

            if term and not (term in name or term in desc or term in ministry or term in scheme_cat):
                continue

            if cat_filter and cat_filter not in scheme_cat:
                continue

            if state_filter and scheme_state and state_filter not in scheme_state:
                continue

            filtered.append(scheme)

        return filtered