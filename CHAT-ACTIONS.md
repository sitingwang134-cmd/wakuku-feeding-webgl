# 聊天驱动动作

当前线上方案：ElevenLabs 现有中文聊天 Agent 的客户端工具 `wakuku_action` → `dist/game-actions.js` → 游戏寻路/日常活动。文字和语音共用同一个工具回调；不是关键词匹配。

支持 sleep、sit、watch_tv、water、wash_hands、bath、swing、push_swing、blocks、cat、dog、eat、stop 和五个房间。新活动自动结束旧活动并等待起身；一次用户回合最多执行一次，关闭聊天、新消息、后台切换会取消等待中的请求。工具返回 started 仅表示已启动；不能据此宣称已抵达或完成。拒绝未知动作，不执行模型生成代码。

现有 Agent ID：agent_7601m6dn5nbwfgws9x9zc0emxqm4
客户端工具 ID：tool_9701m6e3zpjbekgr7tb4x3zmkank

## 本机真实 Laya（2026-11-02）

已安装 Laya 0.4.21，并下载官方 convaiinnovations/laya 的 multilingual 权重。本机服务 http://127.0.0.1:8880/ 使用 Apple MPS 推理；这不代表公开 GitHub/Medeo 已切换。

该入口注入 `window.WakukuLaya={endpoint:"/intent",direct:true}`。每条文字或语音转写直接提交 Laya，模型选择白名单动作，ElevenLabs 负责对话与声音，并接收实际执行结果。客户端工具不能覆盖 Laya 决策。服务失败、未知动作或低置信度不执行，不退回其他模型做动作判断。

服务实现和启动说明在 laya-service/README.md。否定、假设、引用及部分不支持请求有明确拒绝策略；这些规则只阻止执行，不选动作。中文模型覆盖仍有限，见 evaluation-final.json，不能声称已经可靠理解任意聊天。当前 context 传给服务，但分类暂不使用游戏状态。

请求：`POST {text,context}`；响应包含 engine、status、action、candidate 和模型分数。分数不是校准后的准确率。

## 测试

- `node tests/chat-actions.cjs`：实际房间碰撞/寻路下的活动启动、持续睡眠/泡澡/秋千、起床、取消旧指令、忙碌拒绝、未知动作与前往房间。
- 浏览器文字聊天端到端：睡觉实际走到床上、陪小狗；否定句和普通聊天单独验证。
- 手机麦克风与语音识别尚待真机验收；与文字工具共用执行链路。
