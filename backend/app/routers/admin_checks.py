# -*- coding: utf-8 -*-
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.db_checkers import (
    CheckResult,
    FixResult,
    Severity,
    list_checkers,
    get_checker,
)

router = APIRouter(tags=["admin"])


class CheckerMeta(BaseModel):
    check_id: str
    name: str
    description: str
    severity: Severity
    fixable: bool


class RunCheckRequest(BaseModel):
    issue_ids: Optional[List[str]] = None


class FixCheckRequest(BaseModel):
    issue_ids: Optional[List[str]] = None


@router.get("", response_model=List[CheckerMeta])
async def list_available_checks():
    """列出所有已注册的数据库检查器。"""
    return [
        CheckerMeta(
            check_id=c.check_id,
            name=c.name,
            description=c.description,
            severity=c.severity,
            fixable=c.fixable,
        )
        for c in list_checkers()
    ]


@router.post("/run-all", response_model=List[CheckResult])
async def run_all_checks():
    """运行所有检查器。"""
    results: List[CheckResult] = []
    for checker in list_checkers():
        issues = await checker.run()
        results.append(
            CheckResult(
                check_id=checker.check_id,
                name=checker.name,
                description=checker.description,
                severity=checker.severity,
                fixable=checker.fixable,
                issues=issues,
                issue_count=len(issues),
            )
        )
    return results


@router.post("/{check_id}/run", response_model=CheckResult)
async def run_single_check(check_id: str):
    """运行指定检查器。"""
    checker = get_checker(check_id)
    if checker is None:
        raise HTTPException(status_code=404, detail=f"Unknown check: {check_id}")
    issues = await checker.run()
    return CheckResult(
        check_id=checker.check_id,
        name=checker.name,
        description=checker.description,
        severity=checker.severity,
        fixable=checker.fixable,
        issues=issues,
        issue_count=len(issues),
    )


@router.post("/{check_id}/fix", response_model=FixResult)
async def fix_single_check(check_id: str, req: FixCheckRequest):
    """修复指定检查器发现的问题。若未提供 issue_ids，则修复所有可修复问题。"""
    checker = get_checker(check_id)
    if checker is None:
        raise HTTPException(status_code=404, detail=f"Unknown check: {check_id}")
    if not checker.fixable:
        raise HTTPException(status_code=400, detail="该检查器不支持自动修复")

    all_issues = await checker.run()
    if req.issue_ids:
        issue_map = {i.issue_id: i for i in all_issues}
        issues = [issue_map[iid] for iid in req.issue_ids if iid in issue_map]
    else:
        issues = all_issues

    return await checker.fix(issues)
