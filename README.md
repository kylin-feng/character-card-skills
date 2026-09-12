# Character Card Skills · 角色卡技能包

两个 Agent Skill：一个**锻造任意角色卡**的通用方法论，一个**麟鸣**原创角色的完整 IP 资产包。
为 [WorkBuddy](https://www.workbuddy.cn) / Claude Skills 等支持 `SKILL.md` 规范的 Agent 运行时设计。

```
character-card-skills/
├── character-card-forge/          # 通用：从零锻造任意角色卡
│   ├── SKILL.md
│   └── references/
│       ├── chara-card-v2.json     # 酒馆卡骨架模板（逐字段带说明）
│       └── seedream-prompts.md    # 豆包生图指令模板 + 避坑清单
└── linming-character-card/        # 具体 IP：麟鸣
    ├── SKILL.md
    ├── references/
    │   ├── character-bible.md     # 完整人设设定集
    │   ├── comic-prompts.md       # 漫剧提示词 / 分镜 / 表情差分
    │   └── production-notes.md    # 制作笔记与踩坑清单
    └── assets/
        ├── linming-sillytavern.json   # 可直接导入酒馆的 chara_card_v2
        └── refs/                      # 三张参考图（形象唯一依据）
```

---

## 1 · character-card-forge（通用）

**从一段描述、几张参考图或一个名字，产出可直接使用的角色卡三件套：**
人设设定集 Markdown + SillyTavern/酒馆可导入的 `chara_card_v2` JSON（含世界书）
+ AI 漫剧形象卡（生图指令、分镜、表情差分）。

核心方法：

- **Phase 1 · 形象锚定** —— 有图必真读；看不见就说看不见，不编色值
- **Phase 1.3 · 情绪外显道具** —— 给角色一个随情绪变化的可视元素（光环/耳朵/尾巴），
  一石三鸟：性格约束 + 分镜素材 + 防 OOC 锚点
- **Phase 2 · 性格三层** —— 表层 / 中层 / 里层，避免扁平人设
- **Phase 3 · 出卡** —— 设定集、酒馆 JSON、漫剧卡的分工与硬性要求

**触发**：「做个角色卡」「人设卡」「酒馆卡」「帮我设计一个角色」「根据这张图做个人设」

## 2 · linming-character-card（麟鸣）

一个已经做好的完整范例，也是一个可反复调用的原创角色 IP。

> **麟鸣** —— 一位被遗忘的神明留下的最后一名侍者。
> 神走了，但灯还亮着——因为一直是她在点。

猫耳眷属 + 女仆围裙裙装 + 头顶金色光环。核心设计是**光环 = 情绪显示器**：
害羞泛粉、开心跳动、说谎闪烁、护人时张开十字光柱。这一条同时解决了三件事——
她说不了谎（性格约束）、每句台词都有可写的视觉细节（分镜素材）、
模型有稳定行为锚点（不易 OOC）。

**触发**：「用麟鸣写一段」「麟鸣的镜头提示词」「麟鸣世界书」「麟鸣分镜」

---

## 安装

### WorkBuddy（用户级，所有项目可用）

```bash
# macOS / Linux
cp -r character-card-forge linming-character-card ~/.workbuddy/skills/

# Windows (PowerShell)
Copy-Item -Recurse character-card-forge,linming-character-card "$env:USERPROFILE\.workbuddy\skills\"
```

装完**重启会话**，技能即生效。也可以只装其中一个。

### 项目级（随仓库共享给协作者）

```bash
mkdir -p .workbuddy/skills
cp -r character-card-forge linming-character-card .workbuddy/skills/
```

---

## 使用示例

| 你说 | 触发 |
|---|---|
| 「帮我做个角色卡，参考这张图」 | `character-card-forge` |
| 「我想要个 AI 男友设定，毒舌但心软」 | `character-card-forge` |
| 「这个角色的世界书怎么写」 | `character-card-forge` |
| 「用麟鸣写一段她第一次被夸的戏」 | `linming-character-card` |
| 「出麟鸣雪夜街道的镜头提示词」 | `linming-character-card` |
| 「给麟鸣的酒馆卡加一条世界书」 | `linming-character-card` |

---

## 设计原则

1. **先定形象，再定灵魂，最后才谈格式**
2. **没读图就不写视觉细节** —— 编造的十六进制色值看起来专业，实则是假的
3. **能力都写限制** —— 无限制的能力是废设定
4. **提示词方言别混用** —— 豆包吃自然语言长句，`(keyword:1.3)` 是 SD 方言
5. **一致性靠参考图，不靠提示词** —— 先定基准图，之后全部以它为准
6. **不假装** —— 工具不在就说不在，改走降级路线

---

## License

MIT
