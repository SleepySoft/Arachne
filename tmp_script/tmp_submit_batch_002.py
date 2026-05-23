"""
Batch 002 完整提交脚本
整合节点、边、公司和暴露关系，通过API提交到系统。
"""

import os
import sys
sys.path.insert(0, 'backend')

import json
import asyncio
import httpx
from datetime import datetime, date

API_BASE = "http://localhost:8000/api/v1"

# [前面的数据定义省略，与之前相同]
# 由于文件太长，这里只保留提交逻辑，实际数据从 tmp_build_batch_002.py 导入

# 使用exec加载数据定义
with open('tmp_build_batch_002.py', 'r', encoding='utf-8') as f:
    code = f.read()
    # 只执行到 print 语句之前的数据定义部分
    # 找到最后一个 print 之前的内容
    idx = code.find('print("Data prepared:') 
    if idx > 0:
        code = code[:idx]
    exec(code)

async def submit_graph_batch():
    """提交产业图批次（节点+边）"""
    batch = {
        "batch_id": "batch_002_industrial_graph",
        "task_description": "Batch 002: 为10家深圳上市公司构建产业实体图，涵盖房地产、家电、珠宝、粮油、电子、半导体、港口、汽车服务、钟表、能源等产业链。",
        "nodes_to_upsert": NEW_NODES,
        "edges_to_upsert": EDGES,
        "rejected_or_pending": []
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/batches", json=batch, timeout=60.0)
        print(f"Graph batch status: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

async def submit_business_batch():
    """提交商业批次（公司+暴露关系）"""
    batch = {
        "batch_id": "batch_002_company_views",
        "task_description": "Batch 002: 为10家深圳上市公司构建公司视图，包括公司信息和产业节点暴露关系。",
        "industries_to_upsert": [],
        "industry_node_mappings_to_upsert": [],
        "companies_to_upsert": COMPANIES,
        "company_node_exposures_to_upsert": EXPOSURES
    }
    
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/business-batches", json=batch, timeout=60.0)
        print(f"Business batch status: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return result

async def main():
    print("=" * 60)
    print("Step 1: Submitting GraphRegistrationBatch (nodes + edges)")
    print("=" * 60)
    graph_result = await submit_graph_batch()
    
    print("\n" + "=" * 60)
    print("Step 2: Submitting BusinessRegistrationBatch (companies + exposures)")
    print("=" * 60)
    biz_result = await submit_business_batch()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Graph batch: nodes_created={graph_result.get('nodes_created')}, nodes_updated={graph_result.get('nodes_updated')}, edges_created={graph_result.get('edges_created')}, edges_updated={graph_result.get('edges_updated')}, errors={len(graph_result.get('errors', []))}")
    if graph_result.get('errors'):
        for e in graph_result['errors']:
            print(f"  ERROR: {e}")
    print(f"Business batch: companies_created={biz_result.get('companies_created')}, companies_updated={biz_result.get('companies_updated')}, exposures_created={biz_result.get('exposures_created')}, exposures_updated={biz_result.get('exposures_updated')}, errors={len(biz_result.get('errors', []))}")
    if biz_result.get('errors'):
        for e in biz_result['errors']:
            print(f"  ERROR: {e}")

asyncio.run(main())
