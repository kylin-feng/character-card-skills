# 麟鸣 · AI 漫剧角色卡

> 用于 AI 短剧 / 漫剧 / 视频生成的**形象锚定卡**
> 含：核心 Prompt、多角度分镜、表情包、镜头脚本、负面词
> 版本 v1.0 ｜ 全年龄向

---

## 一、角色一句话简介（片头字幕用）

> **麟鸣**
> 一位神明留下的最后一名侍者。
> 神走了，但灯还亮着——因为一直是她在点。

---

## 二、核心形象锚定（每一镜必带，保证一致性）

> 📌 **形象依据**：`assets/refs/ref-01-rooftop-sunset.jpg`（黄昏天台圆头像）、
> `ref-02-classroom.jpg`（教室）、`ref-03-snowy-street.jpg`（雪夜街道）——已实读三图核对。
>
> ⚠️ **先分清用哪个模型**：豆包 Seedream 用「自然语言版」；
> Stable Diffusion / ComfyUI 才用「英文标签版 / 权重版」。**两者不要混用。**

### A. 豆包 Seedream 用 · 自然语言版（推荐，用户指定豆包）

**参考图路线（最稳，一致性最好）**

> 以我上传的图为参考，这是同一个角色。请严格保持她的银灰白色长直发、齐刘海、
> 银灰色猫耳（边缘白色绒毛）、头顶金色光环、白色荷叶边女仆头饰与金色发箍、
> 双侧宝蓝色蝴蝶结、金黄色瞳孔、白色露肩女仆围裙裙装、蓝灰色肩带、
> 以及上深下浅的蓝色渐变领带——全部完全一致。
>
> 生成：<镜头与场景>。<画风>，柔和光影，高质量。

**纯文生图版（无参考图时）**

> 一个动漫少女，银灰白色长直发及膝，齐刘海，发丝冷调；头顶一对猫耳，
> 耳背银灰、边缘白色绒毛、内耳浅粉；头顶悬浮一枚金色发光细圆环；
> 戴白色荷叶边女仆头饰，额前有一条金色细发箍；猫耳外侧下方各系一只宝蓝色蝴蝶结，
> 缎带垂下；金黄琥珀色大眼睛，圆眼型，高光明亮；穿白色女仆围裙式连衣裙，
> 露肩，白色荷叶边泡泡短袖，裙身有金色细描边，配蓝灰色肩带；
> 白色立领衬衫领，系一条中蓝色渐变领带（上深下浅）；脸颊淡红晕，柔和微笑。
> 日系动画风格，清透柔光，高质量。

> ⚠️ 豆包**不支持** `(关键词:1.3)` 权重语法，也不吃独立的负面提示词框。
> 要排除什么，直接在正向描述里说清楚（例如「银灰白色头发，不是金色」）。

### B. Stable Diffusion / ComfyUI 用 · 英文标签版

```
1girl, solo, long straight silver-white hair, knee length, blunt bangs,
grey cat ears with white fluffy inner edge, pink inner ear,
glowing golden halo above head,
white frilled maid headdress, thin gold headband,
blue ribbon bows on both sides of hair, ribbon streamers,
golden amber eyes, round eyes, bright detailed highlights,
white maid apron dress, bare shoulders, frilled puff short sleeves,
gold trim on dress, blue-grey apron straps,
white collared shirt collar, blue gradient necktie,
blush, soft smile,
anime style, soft lighting, clean lineart, masterpiece, best quality
```

**权重强化版（仅 SD 系，特征易丢时用）**
```
1girl, solo,
(long straight silver-white hair:1.3), blunt bangs,
(grey cat ears:1.3), (glowing golden halo:1.3),
(white frilled maid headdress:1.2), gold headband,
(blue hair ribbons:1.2),
(golden amber eyes:1.3),
(white maid apron dress:1.2), bare shoulders,
(blue-grey apron straps:1.2),
(blue gradient necktie:1.3),
blush, soft smile,
anime style, soft lighting, masterpiece, best quality
```

**负面 Prompt（仅 SD 系）**
```
(worst quality, low quality:1.4), bad anatomy, bad hands, extra fingers,
missing fingers, extra limbs, deformed, mutated,
(multiple girls:1.3), (blonde hair:1.3), (black hair:1.3), (twintails:1.2),
short hair, red eyes, blue eyes, green eyes,
(missing halo:1.2), (missing cat ears:1.2), (red necktie:1.3), missing necktie,
missing apron straps,
watermark, signature, text, logo, jpeg artifacts, blurry
```

---

## 三、五视图 / 三视图生成指令（建角色库先跑这一套）

| 视图 | 追加 Prompt |
|---|---|
| 正面全身 | `full body, front view, standing, simple white background, character sheet` |
| 侧面全身 | `full body, from side, standing, simple white background` |
| 背面全身 | `full body, from behind, standing, simple white background`（注意：背面要能看见光环与蝴蝶结结尾） |
| 半身正面 | `upper body, front view, looking at viewer, simple background` |
| 面部特写 | `close-up, face focus, looking at viewer, detailed eyes, simple background` |

> **建议流程**：先跑「半身正面」定基准图 → 满意后用它做参考图（i2i / reference / LoRA），再跑其余视图与全部分镜。这是保持一致性最省事的做法。

---

## 四、表情包 / 情绪素材（漫剧必备）

漫剧里 90% 的表现力靠表情切换。以下每条都自带**光环状态**——这是麟鸣独有的情绪语言，务必带上。

| 情绪 | 追加 Prompt | 光环表现 | 猫耳 |
|---|---|---|---|
| 温柔微笑（默认） | `gentle smile, half-closed eyes, soft expression` | 稳定暖金细环 | 自然竖立 |
| 惊喜 | `surprised, wide eyes, open mouth, :o` | 变亮、光屑飞散 | 猛地前竖 |
| 害羞 | `embarrassed, heavy blush, looking away, covering face` | **泛淡粉**、环身收窄 | 微微后倒 |
| 委屈 | `sad, teary eyes, wobbly mouth, downcast` | 暗淡、闪烁 | 完全耷拉 |
| 认真 / 守护 | `serious expression, determined eyes, wind blowing hair` | **拉大、边缘十字光芒** | 贴头警戒 |
| 得意 | `smug smile, closed eyes, hands on hips` | 亮度上跳 | 高高竖起 |
| 困倦 | `sleepy, half-lidded eyes, yawning` | 极暗、缓慢明灭 | 松软下垂 |
| 吃到辣 | `crying, teary eyes, tongue out, panicking` | **疯狂闪烁** | 乱抖 |
| 被摸耳朵 | `flustered, hands covering cat ears, intense blush, wide eyes` | 淡粉、急速收缩 | 僵直不动 |
| 落寞 | `melancholic, looking down, distant eyes, faint smile` | 几乎熄灭的细线 | 平放 |

---

## 五、场景库（对应你给的三张图，可直接扩展成剧集）

### 场景 A · 黄昏天台 / 城市屋顶（首图）
```
rooftop, sunset sky, golden hour, dramatic clouds, city buildings background,
warm backlight, halo with cross-shaped light rays, cinematic
```
**情绪定位**：神性、庄严、故事的「起源感」。适合片头、回忆杀、揭示身世。

### 场景 B · 教室日常（二图）
```
classroom, sitting at desk, afternoon sunlight through window,
blackboard background, writing in notebook, warm indoor light, slice of life
```
**情绪定位**：日常、轻松、可爱。适合日常单元剧、搞笑桥段、学园线。

### 场景 C · 雪夜街道（三图）
```
snowy night street, falling snow, warm street lamps, european town buildings,
bokeh lights, cold blue and warm orange contrast, cinematic
```
**情绪定位**：孤独中的温暖、重逢、告白级情绪。适合高光集、片尾、感情线爆发点。

### 扩展场景（建议补齐，够撑一季）
| 场景 | Prompt 关键词 | 用途 |
|---|---|---|
| 深夜厨房 | `kitchen at night, dim warm light, cooking, steam, apron` | 温情、心事 |
| 废墟神殿 | `ruined ancient temple, broken pillars, overgrown grass, dust in light beams` | 回忆、身世 |
| 便利店门口 | `convenience store entrance at night, neon sign, holding hot drink` | 日常邂逅 |
| 雨天公交站 | `bus stop, heavy rain, umbrella, wet ground reflection, thunderstorm` | 脆弱、靠近 |
| 樱花街道 | `cherry blossom street, petals falling, spring, soft pink light` | 新篇章、开学 |

---

## 六、镜头语言（分镜通用规格）

| 镜别 | Prompt | 用在哪 |
|---|---|---|
| 大远景 | `wide shot, full body, environment focus` | 建立场景、开场 |
| 中景 | `medium shot, upper body` | 日常对话主力（占比最高） |
| 特写 | `close-up, face focus, detailed eyes` | 情绪爆点 |
| 仰角 | `from below, low angle, dramatic` | 神性、守护、气势 |
| 俯角 | `from above, high angle` | 脆弱、孤独 |
| 过肩 | `over the shoulder shot, from behind` | 双人对话 |
| 眼睛特写 | `extreme close-up on eyes, amber eyes, reflection in eyes` | 高潮、泪点 |
| 光环特写 | `close-up on glowing halo, golden light particles, bokeh` | 转场、情绪符号 |

---

## 七、示例分镜脚本（第 1 集 · 试片段）

> **标题：《点灯的人》**
> 时长约 60 秒 ｜ 8 镜

| # | 镜别 | 画面 Prompt（在核心锚定 Prompt 后追加） | 台词 / 旁白 |
|---|---|---|---|
| 1 | 大远景·仰角 | `ruined ancient temple at dusk, broken pillars, wide shot, from below, lonely atmosphere` | （旁白）很久以前，有一位掌管归途的神。 |
| 2 | 中景·背影 | `standing alone in ruined temple, from behind, full body, dust in light beams` | （旁白）后来，信仰散了，神也睡了。 |
| 3 | 特写·光环 | `close-up on glowing halo, dim golden light, dark background, floating dust` | （旁白）侍者一个一个离开。只剩最后一个。 |
| 4 | 面部特写·落寞 | `close-up, melancholic expression, looking down, faint smile, dim lighting` | 麟鸣：「……今天，也没有人来呢。」 |
| 5 | 中景·惊觉 | `surprised expression, wide eyes, looking at a lit lantern, warm light on face` | （旁白）直到那天她发现，灯还是每晚都亮。 |
| 6 | 特写·顿悟 | `extreme close-up on amber eyes, reflection of lantern flame in eyes, tears welling` | 麟鸣：「……啊。」「原来，一直是我自己点的。」 |
| 7 | 全身·转身 | `full body, turning around, wind blowing silver hair and skirt, halo brightening, determined expression, from below` | （无台词，光环由暗转亮） |
| 8 | 雪夜街道·中景 | `snowy night street, warm street lamps, soft smile, holding hot drink, looking at viewer, cinematic` | 麟鸣：「我不等了。」「我现在有想见的人——我就直接去见了。」 |

---

## 八、配音 / TTS 参数建议

| 项目 | 设定 |
|---|---|
| 音色 | 少女音，偏软中音，不要过度甜腻 |
| 语速 | 中偏慢（0.9x），日常段可回到 1.0x |
| 情绪基调 | 温柔、含笑 |
| 句尾处理 | 轻轻上扬，带一点气声 |
| 紧张时 | 语速加快 + 音量降低 + 结巴「那个、那个……」 |
| 认真时 | 语速放慢、音调压低、停顿加长 |
| 口癖 | 「……嗯！」「我在的哦。」「那个、那个……」 |

---

## 九、一致性避坑清单（漫剧最容易翻车的地方）

按**实际观察三张原图**总结的易丢特征，从最容易丢的排起：

1. **蓝灰色肩带最容易被漏** —— 三张图里都有（教室图、雪夜图最明显），
   但描述时最容易忘。丢了整套裙装的结构就不对了
2. **光环** —— 每镜必提。注意两种形态：常态是**细圆环**，
   情绪激动时是**大光环＋垂直十字光柱**（角色卡1 就是后者），别混用
3. **领带是渐变不是纯色** —— 上深下浅的蓝。写「纯蓝」会丢掉层次
4. **头发容易被"主流化"成金色** —— 必须强调银灰白
5. **猫耳不是纯白** —— 耳背是银灰（同发色），只有边缘绒毛是白的，内耳浅粉。
   写「白猫耳」会得到错的耳朵
6. **发箍与头饰是两件东西** —— 白色荷叶边头饰在头顶，金色细发箍在额前，别合并
7. **眼睛容易变蓝** —— 必须强调金黄／琥珀色
8. **裙身金色细描边** —— 细节，但有了质感明显不同
9. **背面镜头** —— 光环从背后仍可见，蝴蝶结缎带要露出
10. **强烈建议**：先定一张基准图，之后全部走参考图 / i2i / LoRA。
    纯文生图跨镜必然漂移，这不是提示词能解决的问题

---

## 十、剧集方向建议（可拓展成一季）

| 集数 | 主题 | 情绪 |
|---|---|---|
| 01 | 点灯的人（起源） | 孤独 → 决意 |
| 02 | 转学第一天（数学考砸） | 搞笑日常 |
| 03 | 关于辣这件事 | 纯搞笑 |
| 04 | 「你不用管我」 | 第一次情绪冲突 |
| 05 | 雷雨天的半步 | 脆弱、靠近 |
| 06 | 她昏睡了三天 | 揭示神格残响，泪点 |
| 07 | 神殿的旧灯 | 身世揭晓 |
| 08 | 平安到家（终章） | 主题回收，圆满 |
