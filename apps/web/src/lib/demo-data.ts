export const benefits = [
  { id: "benefit-lounge", name: "机场贵宾室", source: "臻享计划", balance: "3次", expiry: "2026-12-31", status: "可直接使用", tone: "success", scope: "中国大陆20个机场", companion: "可携1人，同行人虚拟费用¥80", children: "2岁以下免费，2—12岁¥50", booking: "建议提前2小时预约", cancel: "使用前2小时取消可退回次数" },
  { id: "benefit-dining", name: "机场餐饮抵扣", source: "商务信用卡", balance: "¥320", expiry: "2026-10-31", status: "需要预约", tone: "warning", scope: "指定机场餐厅", companion: "可共享抵扣额度", children: "按餐厅规则", booking: "使用前30分钟领取", cancel: "未核销自动退回" },
  { id: "benefit-fast", name: "快速安检", source: "臻享计划", balance: "5次", expiry: "2026-12-31", status: "可直接使用", tone: "success", scope: "SHA、PEK、CAN、SZX", companion: "不可携伴", children: "随主用户通行", booking: "无需预约", cancel: "生成后30分钟失效" },
  { id: "benefit-transfer", name: "接送机礼宾", source: "企业福利", balance: "1次", expiry: "2026-09-30", status: "需补充信息", tone: "warning", scope: "上海、北京城区", companion: "最多3名同行人", children: "儿童座椅需预约", booking: "至少提前24小时", cancel: "12小时前可取消" },
];

export const recommendations = [
  { id: "service-lounge-001", type: "贵宾室", name: "云际贵宾休息室（虚拟）", reason: "位于T2安检后，与登机口同方向，可预留50分钟休息。", location: "上海虹桥 T2 · 安检后", time: "13:00—13:50", distance: "步行8分钟", inventory: "余量8", cost: "扣1次 · ¥0", score: 96, rule: "demo-lounge-017@3" },
  { id: "service-fast-001", type: "快速安检", name: "T2快速安检通道（虚拟）", reason: "预计节省15分钟，可为贵宾室安排留出更多缓冲。", location: "上海虹桥 T2 · 出发层", time: "12:35—12:45", distance: "值机区旁", inventory: "可用", cost: "扣1次 · ¥0", score: 91, rule: "demo-fast-004@2" },
  { id: "service-dining-001", type: "餐饮", name: "航味餐厅80元权益（虚拟）", reason: "在前往贵宾室的路径上，可与休息室组合使用。", location: "上海虹桥 T2 · 安检后", time: "12:45—13:10", distance: "步行5分钟", inventory: "余量充足", cost: "抵扣¥80", score: 84, rule: "demo-dining-009@1" },
];

export const timeline = [
  { time: "11:40", title: "从公司出发", detail: "预计车程30分钟，已加入10分钟拥堵缓冲", type: "travel" },
  { time: "12:20", title: "到达上海虹桥T2", detail: "无需托运行李", type: "airport" },
  { time: "12:35", title: "使用快速安检", detail: "预计10分钟，扣除虚拟权益1次", type: "service" },
  { time: "13:00", title: "进入云际贵宾休息室", detail: "建议停留50分钟", type: "service" },
  { time: "13:50", title: "前往登机口", detail: "步行8分钟，预留32分钟登机缓冲", type: "walk" },
  { time: "14:30", title: "MU5105起飞", detail: "上海虹桥T2 → 北京首都T2", type: "flight" },
];

export const order = {
  id: "VC-DEMO-260810-008", status: "已确认", service: "云际贵宾休息室（虚拟）", location: "上海虹桥T2 · 安检后", useAt: "2026-08-10 13:00", traveler: "林晨", party: "1名成人", points: "贵宾室权益1次", fee: "¥0", cancel: "使用前2小时取消可退回虚拟次数", voucher: "DEMO-QR-008", rule: "demo-lounge-017@3",
};

export const conversations = [
  { id: "demo-conversation-001", user: "林晨", intent: "航站楼变化后的贵宾室改订", level: "重要", wait: "38分钟", sla: "22分钟后", status: "待接管" },
  { id: "demo-conversation-002", user: "陈女士", intent: "儿童同行费用咨询", level: "普通", wait: "1小时", sla: "3小时后", status: "AI处理中" },
  { id: "demo-conversation-003", user: "赵先生", intent: "取消模拟订单", level: "普通", wait: "2小时", sla: "2小时后", status: "待接管" },
];

export const knowledge = [
  { title: "臻享计划贵宾室使用说明", type: "权益说明", scope: "臻享计划", version: "v3", status: "已发布", updated: "2026-07-18", citations: 186 },
  { title: "上海虹桥T2服务点指南", type: "机场服务", scope: "SHA/T2", version: "v5", status: "已发布", updated: "2026-07-16", citations: 94 },
  { title: "航变后的服务处理SOP", type: "客服流程", scope: "全部租户", version: "v2", status: "待审核", updated: "2026-07-19", citations: 0 },
  { title: "儿童及同行人费用说明", type: "权益说明", scope: "臻享计划", version: "v1", status: "即将失效", updated: "2026-06-02", citations: 47 },
];

export const rules = [
  { id: "demo-lounge-017", name: "贵宾室本人资格", version: "3", scope: "臻享计划", tests: "24/24", status: "已发布", effective: "2026-07-01" },
  { id: "demo-change-011", name: "临近起飞改订限制", version: "3", scope: "全部计划", tests: "21/22", status: "草稿", effective: "未安排" },
  { id: "demo-child-006", name: "儿童额外费用", version: "2", scope: "臻享计划", tests: "18/18", status: "待审核", effective: "2026-08-01" },
  { id: "demo-fast-004", name: "快速安检资格", version: "2", scope: "臻享计划", tests: "16/16", status: "已发布", effective: "2026-06-01" },
];

export const managedServices = [
  { name: "云际贵宾休息室（虚拟）", type: "贵宾室", location: "SHA T2", hours: "12:00—21:00", inventory: 8, status: "营业中", quality: "98.1%" },
  { name: "航味餐厅（虚拟）", type: "餐饮", location: "SHA T2", hours: "06:00—22:00", inventory: 32, status: "营业中", quality: "96.4%" },
  { name: "T2快速安检（虚拟）", type: "快速安检", location: "SHA T2", hours: "05:30—21:30", inventory: 99, status: "营业中", quality: "99.2%" },
  { name: "云廊T1休息室（虚拟）", type: "贵宾室", location: "SHA T1", hours: "08:00—20:00", inventory: 0, status: "临时关闭", quality: "91.8%" },
];

export const qualityIssues = [
  { id: "Q-1042", type: "规则冲突", example: "航站楼变化后的临近起飞改订", count: 18, severity: "高", owner: "规则运营", status: "处理中" },
  { id: "Q-1039", type: "无答案", example: "境外机场儿童年龄边界", count: 12, severity: "中", owner: "知识运营", status: "待分配" },
  { id: "Q-1036", type: "错误引用", example: "引用了已失效的取消条款", count: 3, severity: "高", owner: "AI质量", status: "已修复" },
  { id: "Q-1028", type: "工具失败", example: "模拟库存查询超时", count: 7, severity: "中", owner: "平台研发", status: "监控中" },
];

