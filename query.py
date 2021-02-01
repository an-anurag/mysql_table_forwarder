"""
This is the sql query for mysql table from which we are fetching records
This can be any sql 'SELECT' query
"""

query = '''
SELECT ilv.TIMESTAMP, ilv.backlog_id, ilv.event_id, ilv.corr_engine_ctx, ilv.STATUS, ilv.plugin_id, ilv.plugin_sid,
ilv.protocol, ilv.src_ip, ilv.dst_ip, ilv.src_port, ilv.dst_port, ilv.risk, ilv.efr, ilv.username,
ilv.source, ilv.similar, ilv.removable, ilv.in_file, ilv.csimilar, ilv.kid, ilv.kingdom, ilv.category,
ilv.subcategory, ilv.label, ilv.plugin1, ilv.plugin_sid1, ilv.asset_risk_score, ilv.asset_os, ilv.tenant_id,
ilv.asset_cpu, ilv.asset_workgroup, ilv.asset_memory, ilv.asset_department, ilv.asset_state, ilv.asset_username,
ilv.asset_acl, ilv.asset_route, ilv.asset_storage, ilv.asset_role, ilv.asset_video, ilv.asset_model,

(SELECT ( SELECT inet6_ntoa(ip) FROM sensor WHERE hex(id) =  hex(e1.sensor_id)) 
FROM  backlog b  LEFT OUTER JOIN backlog_event be ON be.backlog_id = b.id   
LEFT OUTER JOIN event e1 ON be.event_id = e1.id LEFT OUTER JOIN sensor ON sensor.id = e1.sensor_id 
WHERE  hex(b.id) = ilv.backlog_id AND e1.sensor_id IS NOT NULL  limit 1) AS sensor_ip


FROM (SELECT DISTINCT HEX (a.backlog_id) AS backlog_id, HEX(a.event_id) AS event_id,
HEX(a.corr_engine_ctx) AS corr_engine_ctx, a.timestamp AS TIMESTAMP,
a.status AS STATUS, a.plugin_id AS plugin_id, a.plugin_sid AS plugin_sid, a.protocol AS protocol,
INET6_NTOA(a.src_ip) AS src_ip, INET6_NTOA(a.dst_ip) AS dst_ip, a.src_port AS src_port,
a.dst_port AS dst_port, a.risk AS risk, a.efr AS efr,e.username AS username,
(CASE WHEN hi.host_id IS NOT NULL THEN 'Internal' ELSE 'External' END) AS source,
a.similar AS similar, a.removable AS removable, a.in_file AS in_file, COUNT(DISTINCT a.similar) AS csimilar,
ki.id AS kid,ki.name AS kingdom, ca.name AS category, ta.subcategory AS subcategory, t.name AS label,
p.name AS plugin1, ps.name AS plugin_sid1, h.asset AS asset_risk_score, hp.value AS asset_os,
HEX(id_ctx) AS tenant_id, hp1.value AS asset_cpu, hp2.value AS asset_workgroup, hp3.value AS asset_memory,
hp4.value AS asset_department, hp5.value AS asset_state,hp6.value AS asset_username, hp7.value AS asset_acl,
hp8.value AS asset_route, hp9.value AS asset_storage, hp10.value AS asset_role, hp11.value AS asset_video,
hp12.value AS asset_model 

 
FROM alarm a INNER JOIN alarm_events ae ON a.backlog_id = ae.alarm_id AND ae.log_pushed_flag = 0
INNER JOIN alarm_ctxs ac ON ac.id_alarm = a.backlog_id 
LEFT OUTER JOIN event e ON a.event_id = e.id
-- LEFT OUTER JOIN sensor on sensor.id = e.sensor_id
LEFT OUTER JOIN alarm_taxonomy ta ON a.plugin_sid=ta.sid AND a.corr_engine_ctx=ta.engine_id
LEFT OUTER JOIN alarm_kingdoms ki ON ta.kingdom=ki.id LEFT OUTER JOIN alarm_categories ca ON ta.category=ca.id
LEFT OUTER JOIN plugin p ON p.id = a.plugin_id
LEFT OUTER JOIN plugin_sid ps ON -- p.ctx = ps.plugin_ctx
p.id = ps.plugin_id AND ps.sid = a.plugin_sid
LEFT OUTER JOIN host_ip hi ON hi.ip = a.dst_ip
LEFT OUTER JOIN host h ON h.id = hi.host_id
LEFT OUTER JOIN host_properties hp ON h.id = hp.host_id AND hp.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'operating-system')
LEFT OUTER JOIN host_properties hp1 ON h.id = hp1.host_id AND hp1.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'cpu')
LEFT OUTER JOIN host_properties hp2 ON h.id = hp2.host_id AND hp2.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'workgroup')
LEFT OUTER JOIN host_properties hp3 ON h.id = hp3.host_id AND hp3.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'memory')
LEFT OUTER JOIN host_properties hp4 ON h.id = hp4.host_id AND hp4.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'department')
LEFT OUTER JOIN host_properties hp5 ON h.id = hp5.host_id AND hp5.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'state')
LEFT OUTER JOIN host_properties hp6 ON h.id = hp6.host_id AND hp6.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'username')
LEFT OUTER JOIN host_properties hp7 ON h.id = hp7.host_id AND hp7.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'acl')
LEFT OUTER JOIN host_properties hp8 ON h.id = hp8.host_id AND hp8.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'route')
LEFT OUTER JOIN host_properties hp9 ON h.id = hp9.host_id AND hp9.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'storage')
LEFT OUTER JOIN host_properties hp10 ON h.id = hp10.host_id AND hp10.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'role')
LEFT OUTER JOIN host_properties hp11 ON h.id = hp11.host_id AND hp11.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'video')
LEFT OUTER JOIN host_properties hp12 ON h.id = hp12.host_id AND hp12.property_ref =
(SELECT id FROM host_property_reference WHERE NAME = 'model')
LEFT OUTER JOIN component_tags ct ON ct.id_component = a.backlog_id
LEFT OUTER JOIN tag t ON ct.id_tag = t.id,backlog b
WHERE a.status = 'open'
AND a.backlog_id=b.id
AND b.timestamp <> '1970-01-01 00:00:00' AND a.timestamp > '{}'
GROUP BY a.similar
ORDER BY a.timestamp) ilv;
'''