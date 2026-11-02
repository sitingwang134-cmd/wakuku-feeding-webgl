# 聊天驱动动作

当前线上方案：ElevenLabs 现有中文聊天 Agent 的客户端工具 `wakuku_action` → `dist/game-actions.js` → 游戏寻路/日常活动。文字和语音共用同一个工具回调；不是关键词匹配。

支持 sleep、sit、watch_tv、water、wash_hands、bath、swing、push_swing、blocks、cat、dog、eat、stop 和五个房间。新活动自动结束旧活动并等待起身；一次用户回合最多执行一次，关闭聊天、新消息、后台切换会取消等待中的请求。工具返回 started 仅表示已启动；不能据此宣称已抵达或完成。拒绝未知动作，不执行模型生成代码。

现有 Agent ID：agent_7601m6dn5nbwfgws9x9zc0emxqm4
客户端工具 ID：tool_9701m6e3zpjbekgr7tb4x3zmkank

## Laya 边界与预留接口

Laya 权重和推理服务尚未部署，不宣称已使用 Laya。官方浏览器示例首次约 1.3 GB 模型下载，不适合当前手机 WebGL 页面。当前 GitHub Pages/Medeo 为静态托管，不运行 Python 模型服务。

若后续提供自有 HTTPS 模型服务，可在 game-chat.js 前设置 `window.WakukuLaya={endpoint:'https://你的服务/intent'}`。客户端工具被调用时，会把最新用户文本与简要游戏状态发送到此地址，由服务端 Laya 确认动作。端点需允许游戏来源的 CORS，不把私密 API 密钥放在前端。

请求：`POST {text,context:{ready,activity,stage,room,moving,feeding}}`
响应：`{engine:"laya",status:"accepted",action:"sleep"}`；不确定时返回其他 status。服务端必须用真实 Laya 推理、在中文指令样本上验证阈值，不能用关键词规则冒充。服务故障、超时、未知动作均不执行。现有聊天 AI 仍负责决定何时需要工具，因此该接口是额外决策校验，不是每句话独立运行的 Laya 聊天系统。

## 测试

- `node tests/chat-actions.cjs`：实际房间碰撞/寻路下的活动启动、持续睡眠/泡澡/秋千、起床、取消旧指令、忙碌拒绝、未知动作与前往房间。
- 浏览器文字聊天端到端：睡觉实际走到床上、陪小狗；否定句和普通聊天单独验证。
- 手机麦克风与语音识别尚待真机验收；与文字工具共用执行链路。
