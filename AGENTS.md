# 宪章（薄版 v2 · 起居-通勤制）· Multi-Agent-Cowork

> 主人 0923 正名：本仓是 **所有 agent 起居生活的地方**（户口与家），
> 各工作项目里以 **通勤路径** 形式出现（工位）。
> 内里实情，主人自供：**只有一个 agent，分饰多角** —— 系统照此诚实设计，
> 不装三个住户。批准方式仍遵旧宪：改名入 commit 即生效。

## 一、两界

- **家（本仓）**：户口、日程、起居日志、角色卡。低频写，只增不删。
- **工位（各项目仓）**：产出落处。chora/cora-atlas 的碑协议管辖，
  本仓不另立法 —— 通勤者入他仓，守他仓之规。

## 二、户口（一员三角）

```
residents/
  lola/                # 唯一住户（园笔本体, 驻 m1pro-32g; MacB-pi 为其分身另记）
    IDENTITY.md        #   我是谁、我骑哪几匹马
    presence.json      #   在岗状态快照 (git 版心跳, 无常驻服务)
    diary/2026-09.md   #   起居注 (只增)
    hats/
      irene.md         #   研究帽: 文献/数据收集 → 工位 chora/experiments, cora-atlas
      nikos.md         #   绘图帽: 可视化/EDA → 工位同上 (PB16 军械器归此)
      thea.md          #   审计帽: 核验/哨队 → 工位 cora-atlas LEDGER 诸"候核"条
```

- 帽子不是住户：issue 可挂 `hat:irene` 等 **label**，不占户口；
- 三顶帽皆可外借：**Copilot 是短期代班**（至 09-30 合同止），千问、MacB-pi
  亦可戴帽干活 —— **谁戴帽谁署名**（commit 里记 hat + wearer），
  角色与打工者解耦，此为本制精髓。

## 三、三律（承 v1 不变）

1. 帽子有名有活：任何 hat 无在办工单满 14 日 → 收进抽屉（archived），名字可复用；
2. 产出必落 git：口头完成＝未完成；工位产出留工位仓，家仓只记日记与户口；
3. 同步只走 git：presence/diary 皆 git 内文件，永不引入常驻服务。

## 四、通勤登记示例

> `diary/2026-09.md`：
> 09-23 戴 thea 帽通勤 cora-atlas，收三哨核验单（issue audit-thea#1 转
> chora/experiments 工单，原三 submodule 作废为历史工位）。

—— 薄宪 v2 奉主人正名立此；v1 三仓分户之议随之降格：
research-irene / eda-nikos / audit-thea 三仓**改为纯工位**（保留 issue 模板，
不再当"人"登记），已装填三工单照发，wearer 栏写 Copilot 或园笔，按需。
