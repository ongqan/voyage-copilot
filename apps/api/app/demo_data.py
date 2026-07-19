"""Fictional MVP data used until external systems are connected."""

BENEFITS = [
    {"id": "benefit-lounge", "name": "机场贵宾室", "source": "臻享计划", "balance": 3, "unit": "次", "status": "available", "expires_at": "2026-12-31", "rule_version": "demo-lounge-017@3"},
    {"id": "benefit-dining", "name": "机场餐饮抵扣", "source": "商务信用卡", "balance": 320, "unit": "CNY", "status": "reservation_required", "expires_at": "2026-10-31", "rule_version": "demo-dining-009@1"},
    {"id": "benefit-fast", "name": "快速安检", "source": "臻享计划", "balance": 5, "unit": "次", "status": "available", "expires_at": "2026-12-31", "rule_version": "demo-fast-004@2"},
]

RECOMMENDATIONS = [
    {"id": "service-lounge-001", "type": "lounge", "name": "云际贵宾休息室（虚拟）", "location": "SHA T2 安检后", "use_window": "13:00-13:50", "points": 1, "amount_minor": 0, "currency": "CNY", "inventory": 8, "score": 96, "reason_codes": ["TERMINAL_MATCH", "TIME_FIT", "ENTITLEMENT_ACTIVE"], "rule_version": "demo-lounge-017@3"},
    {"id": "service-fast-001", "type": "fast_track", "name": "T2快速安检通道（虚拟）", "location": "SHA T2 出发层", "use_window": "12:35-12:45", "points": 1, "amount_minor": 0, "currency": "CNY", "inventory": 99, "score": 91, "reason_codes": ["TIME_SAVED", "ENTITLEMENT_ACTIVE"], "rule_version": "demo-fast-004@2"},
    {"id": "service-dining-001", "type": "dining", "name": "航味餐厅80元权益（虚拟）", "location": "SHA T2 安检后", "use_window": "12:45-13:10", "points": 0, "amount_minor": -8000, "currency": "CNY", "inventory": 32, "score": 84, "reason_codes": ["ON_ROUTE", "TIME_FIT"], "rule_version": "demo-dining-009@1"},
]

TIMELINE = [
    {"time": "12:20", "type": "arrival", "title": "到达上海虹桥T2"},
    {"time": "12:35", "type": "service", "title": "使用快速安检"},
    {"time": "13:00", "type": "service", "title": "进入云际贵宾休息室"},
    {"time": "13:50", "type": "walk", "title": "前往登机口"},
    {"time": "14:30", "type": "flight", "title": "MU5105起飞"},
]

CONVERSATIONS = [
    {"id": "demo-conversation-001", "user": "林晨", "intent": "航站楼变化后的贵宾室改订", "risk_level": "important", "status": "waiting_for_agent", "sla_due_at": "2026-07-19T13:21:00+08:00"},
    {"id": "demo-conversation-002", "user": "陈女士", "intent": "儿童同行费用咨询", "risk_level": "normal", "status": "ai_processing", "sla_due_at": "2026-07-19T16:00:00+08:00"},
]

ADMIN_SUMMARY = {
    "users": 1284,
    "trip_parse_success_rate": 0.962,
    "recommendation_click_rate": 0.348,
    "mock_booking_conversion_rate": 0.173,
    "ai_resolution_rate": 0.78,
    "unconfirmed_write_count": 0,
}

