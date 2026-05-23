import sys, os
os.chdir('C:/D/code/Arachne')
sys.path.insert(0, 'backend')
import asyncio
from app.database import get_async_driver

async def main():
    driver = get_async_driver()
    async with driver.session() as session:
        # 检查 container_handling_service 节点是否存在
        result = await session.run("MATCH (n:IndustrialNode {node_id: 'container_handling_service'}) RETURN n.node_id AS id, n.canonical_name_zh AS name")
        records = await result.data()
        print('container_handling_service nodes:', records)
        
        # 检查 bulk_cargo_to_handling 边
        result2 = await session.run("MATCH (a:IndustrialNode)-[r]->(b:IndustrialNode) WHERE r.edge_id = 'bulk_cargo_to_handling' RETURN a.node_id AS from_id, type(r) AS rel_type, b.node_id AS to_id")
        records2 = await result2.data()
        print('bulk_cargo_to_handling edges:', records2)
        
        # 搜索 bulk_cargo 相关的边
        result3 = await session.run("MATCH (a:IndustrialNode {node_id: 'bulk_cargo'})-[r]->(b) RETURN r.edge_id AS edge_id, type(r) AS rel_type, b.node_id AS to_id")
        records3 = await result3.data()
        print('bulk_cargo outgoing edges:', records3)
        
        # 查看所有包含 handling 的边
        result4 = await session.run("MATCH ()-[r]->() WHERE r.edge_id STARTS WITH 'bulk' OR r.edge_id CONTAINS 'handling' RETURN r.edge_id AS edge_id")
        records4 = await result4.data()
        print('bulk/handling related edges:', records4)
        
        # 检查所有 container 相关节点
        result5 = await session.run("MATCH (n:IndustrialNode) WHERE n.node_id CONTAINS 'container' RETURN n.node_id AS id, n.canonical_name_zh AS name")
        records5 = await result5.data()
        print('container related nodes:', records5)
        
    await driver.close()

asyncio.run(main())
