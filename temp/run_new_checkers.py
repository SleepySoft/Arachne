# -*- coding: utf-8 -*-
import asyncio
from app.services.db_checkers import get_checker


async def main():
    for cid in ["entity_domain_boundary", "device_to_product_direct_edge"]:
        checker = get_checker(cid)
        if not checker:
            print(f"checker {cid} not found")
            continue
        print(f"\n=== {checker.check_id}: {checker.name} ===")
        print(checker.description)
        issues = await checker.run()
        print(f"issues: {len(issues)}")
        for i in issues:
            print(f"  [{i.severity}] {i.title}: {i.summary}")
            print(f"       affected: {i.affected_ids}")
        if issues and checker.fixable:
            fix = await checker.fix(issues)
            print(f"  fixed: {fix.fixed_count}, skipped: {fix.skipped_count}, messages: {fix.messages}")


if __name__ == "__main__":
    asyncio.run(main())
