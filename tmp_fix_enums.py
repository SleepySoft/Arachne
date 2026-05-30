with open('tmp_script/tmp_submit_batch_021.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('"entity_type": "COMPONENT"', '"entity_type": "component"')
content = content.replace('"entity_type": "DEVICE"', '"entity_type": "device"')
content = content.replace('"entity_type": "SERVICE"', '"entity_type": "service"')
content = content.replace('"entity_type": "MATERIAL"', '"entity_type": "material"')
content = content.replace('"entity_type": "SUBSYSTEM"', '"entity_type": "subsystem"')
content = content.replace('"edge_type": "COMPOSITION"', '"edge_type": "composition"')
content = content.replace('"edge_type": "MATERIAL_FLOW"', '"edge_type": "material_flow"')
content = content.replace('"edge_type": "SERVICE_FLOW"', '"edge_type": "service_flow"')
content = content.replace('"company_type": "PUBLIC"', '"company_type": "public"')
content = content.replace('"activity_type": "MANUFACTURE"', '"activity_type": "manufacture"')
content = content.replace('"activity_type": "DESIGN"', '"activity_type": "design"')
content = content.replace('"activity_type": "PRODUCE"', '"activity_type": "produce"')
content = content.replace('"activity_type": "OPERATE"', '"activity_type": "operate"')
content = content.replace('"activity_type": "PROVIDE_SERVICE"', '"activity_type": "provide_service"')

with open('tmp_script/tmp_submit_batch_021.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed')
