from __future__ import annotations

import json
import sqlite3
from datetime import datetime, UTC
from pathlib import Path
from uuid import uuid4

from app.models import AnalysisRequest, AnalysisResponse, StoredAnalysis


class AnalysisRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_path)

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS cases (
                    case_id TEXT PRIMARY KEY,
                    user_query TEXT NOT NULL,
                    case_type_hint TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS materials (
                    material_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    FOREIGN KEY(case_id) REFERENCES cases(case_id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS analyses (
                    analysis_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    request_json TEXT NOT NULL,
                    response_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(case_id) REFERENCES cases(case_id)
                )
                """
            )

    def save(self, request: AnalysisRequest, response: AnalysisResponse) -> None:
        created_at = response.created_at.isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO cases (case_id, user_query, case_type_hint, created_at) VALUES (?, ?, ?, ?)",
                (response.case_id, request.user_query, request.case_type_hint, created_at),
            )
            for material in request.materials:
                conn.execute(
                    "INSERT INTO materials (material_id, case_id, title, content) VALUES (?, ?, ?, ?)",
                    (str(uuid4()), response.case_id, material.title, material.content),
                )
            conn.execute(
                "INSERT INTO analyses (analysis_id, case_id, request_json, response_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (
                    response.analysis_id,
                    response.case_id,
                    request.model_dump_json(),
                    response.model_dump_json(),
                    created_at,
                ),
            )

    def get_analysis(self, analysis_id: str) -> StoredAnalysis | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT case_id, request_json, response_json, created_at FROM analyses WHERE analysis_id = ?",
                (analysis_id,),
            ).fetchone()
        if row is None:
            return None
        case_id, request_json, response_json, created_at = row
        return StoredAnalysis(
            analysis_id=analysis_id,
            case_id=case_id,
            request=AnalysisRequest.model_validate_json(request_json),
            response=AnalysisResponse.model_validate_json(response_json),
            created_at=datetime.fromisoformat(created_at),
        )

    def create_case_id(self) -> str:
        return str(uuid4())

    def create_analysis_id(self) -> str:
        return str(uuid4())

    def now(self) -> datetime:
        return datetime.now(UTC)
