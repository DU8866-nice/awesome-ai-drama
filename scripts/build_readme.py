"""Generate README.md (Chinese) and README.en.md (English) from data/tools.yaml.

Usage: python scripts/build_readme.py
Star counts and update dates come from data/stats.json (refresh it with
scripts/update_stats.py). Entries in each section are sorted by stars.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = "DU8866-nice/awesome-ai-drama"
NEW_DAYS = 90
STALE_DAYS = 365


def load():
    data = yaml.safe_load((ROOT / "data" / "tools.yaml").read_text(encoding="utf-8"))
    stats_path = ROOT / "data" / "stats.json"
    raw = json.loads(stats_path.read_text(encoding="utf-8")) if stats_path.exists() else {}
    stats = {k.lower(): v for k, v in raw.items()}
    return data, stats


def stars_text(n: int | None) -> str:
    if n is None:
        return "-"
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def marks(stat: dict | None, today: dt.date, lang: str) -> str:
    if not stat:
        return ""
    out = []
    created = dt.date.fromisoformat(stat["created"])
    pushed = dt.date.fromisoformat(stat["pushed"])
    if (today - created).days <= NEW_DAYS:
        out.append(" 🆕")
    if (today - pushed).days > STALE_DAYS:
        out.append(" 💤")
    return "".join(out)


def table(items, stats, today, lang):
    head = {
        "zh": "| 项目 | 说明 | ⭐ | 最近更新 |\n|---|---|---:|---|",
        "en": "| Project | Description | ⭐ | Last update |\n|---|---|---:|---|",
    }[lang]
    rows = []
    names = [i["repo"].split("/", 1)[1].lower() for i in items]
    def key(item):
        s = stats.get(item["repo"].lower())
        return -(s["stars"] if s else 0)
    for item in sorted(items, key=key):
        s = stats.get(item["repo"].lower())
        name = item["repo"].split("/", 1)[1]
        if names.count(name.lower()) > 1:
            name = item["repo"]
        link = f"[{name}](https://github.com/{item['repo']})"
        desc = item[lang].replace("|", "\\|")
        rows.append(f"| {link}{marks(s, today, lang)} | {desc} | {stars_text(s and s['stars'])} | "
                    f"{s['pushed'][:7] if s else '-'} |")
    return head + "\n" + "\n".join(rows)


def anchor(title: str) -> str:
    keep = []
    for ch in title.strip().lower():
        if ch.isalnum() or ch in "-_":
            keep.append(ch)
        elif ch == " ":
            keep.append("-")
    return "".join(keep)


TEXT = {
    "zh": {
        "title": "# Awesome AI Drama · AI 短剧 / 漫剧开源工具大全",
        "switch": "**简体中文** | [English](README.en.md)",
        "tagline": "从剧本、分镜、角色一致性、视频生成、配音口型到剪辑和合规发布，AI 短剧与漫剧全流程的开源工具精选。"
                   "每个项目都标注了星标数和最近更新时间，数据每周自动刷新、按热度重新排序。",
        "why_title": "## 为什么做这份清单",
        "why": (
            "AI 漫剧已经是短剧的主力：[澎湃号的一篇文章](https://www.thepaper.cn/newsDetail_forward_33483129)援引中国网络视听协会的数据称，"
            "2026 年一季度全行业上线微短剧约 12.8 万部，其中 AI 微短剧约 12.2 万部。"
            "开源社区里相关项目也在爆发，但散落在各处、良莠不齐。这里把**真正能用、仍在维护**的项目按制作流程整理好，"
            "并附上国内发布前必须知道的合规规定。"
        ),
        "flow_title": "## 制作流程一览",
        "flow": "```mermaid\nflowchart LR\n  A[剧本 / 小说改编] --> B[分镜脚本]\n  B --> C[角色与场景资产]\n  C --> D[图生视频]\n  D --> E[配音与口型]\n  E --> F[配乐与音效]\n  F --> G[剪辑 · 字幕 · 超分]\n  G --> H[标识与备案后发布]\n```",
        "start_title": "## 快速上手：选一条路线",
        "start": (
            "| 路线 | 适合谁 | 推荐组合 |\n|---|---|---|\n"
            "| 零代码 | 想最快出片 | [即梦 AI](https://jimeng.jianying.com/) / [可灵 AI](https://kling.ai/) 出镜头 + "
            "[IndexTTS](https://github.com/index-tts/index-tts) 配音 + [VideoCaptioner](https://github.com/WEIFENG2333/VideoCaptioner) 字幕 |\n"
            "| 一站式开源平台 | 想要完整工作台、可自部署 | [Toonflow](https://github.com/HBAI-Ltd/Toonflow-app) 或 "
            "[LocalMiniDrama](https://github.com/xuanyustudio/LocalMiniDrama)，接入自己的模型 Key |\n"
            "| 全本地 | 有显卡、想控制每一步 | [ComfyUI](https://github.com/Comfy-Org/ComfyUI) + [Wan2.2](https://github.com/Wan-Video/Wan2.2) + "
            "[Qwen-Image](https://github.com/QwenLM/Qwen-Image) 做角色图 + [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) + "
            "[InfiniteTalk](https://github.com/MeiGen-AI/InfiniteTalk) 对口型 |\n"
            "| Agent 工作流 | 用 Claude Code / Codex 写剧本分镜 | [shuohao-skills](https://github.com/eternityspring/shuohao-skills) 或 "
            "[drama-skills](https://github.com/zenstory-ai/drama-skills) 出剧本和分镜，再交给任意视频模型 |"
        ),
        "toc": "## 目录",
        "legend": "图例：🆕 近 {new} 天内新建　💤 超过一年没有更新　⭐ 星标数（{date} 更新）",
        "related": "## 相关合集",
        "compliance": "## 合规与发布（中国大陆）",
        "compliance_note": "> 以下为公开规定的摘要，方便快速了解，不构成法律意见。具体要求以原文和平台规则为准。",
        "platform_head": "| 平台 | 说明 |\n|---|---|",
        "contrib_title": "## 参与贡献",
        "contrib": "欢迎推荐项目或纠错：[提交 Issue](https://github.com/{repo}/issues/new/choose)，或者修改 "
                   "[`data/tools.yaml`](data/tools.yaml) 后提 PR，详见 [贡献指南](CONTRIBUTING.md)。README 由脚本生成，请不要直接改它。",
        "star_title": "## Star 趋势",
        "license": "## 许可\n\n[CC0 1.0](LICENSE)：本清单内容放弃版权，可自由使用。各项目的许可证以其仓库为准。",
    },
    "en": {
        "title": "# Awesome AI Drama",
        "switch": "[简体中文](README.md) | **English**",
        "tagline": "A curated list of open-source tools for making AI short dramas and AI motion comics (manju), from script and storyboard "
                   "to consistent characters, video generation, voice, lip sync, editing and release. Every entry shows its stars and last "
                   "update, refreshed and re-ranked weekly.",
        "why_title": "## Why this list",
        "why": (
            "AI dramas now make up most of China's micro-drama output: an [article on The Paper's creator platform](https://www.thepaper.cn/newsDetail_forward_33483129), "
            "citing the China Netcasting Services Association, says that about 122,000 of the roughly 128,000 micro-dramas released in Q1 2026 were AI-made. "
            "Open-source projects in this space are multiplying but scattered. This list keeps the ones that work and are still maintained, "
            "ordered by production stage, plus the Chinese rules you need to know before publishing."
        ),
        "flow_title": "## Production pipeline",
        "flow": "```mermaid\nflowchart LR\n  A[Script / adaptation] --> B[Storyboard]\n  B --> C[Character & scene assets]\n  C --> D[Image-to-video]\n  D --> E[Voice & lip sync]\n  E --> F[Music & SFX]\n  F --> G[Edit · subtitles · upscale]\n  G --> H[Label, file, publish]\n```",
        "start_title": "## Quick start: pick a route",
        "start": (
            "| Route | For | Suggested stack |\n|---|---|---|\n"
            "| No code | Fastest results | [Jimeng](https://jimeng.jianying.com/) or [Kling](https://kling.ai/) for shots + "
            "[IndexTTS](https://github.com/index-tts/index-tts) for voice + [VideoCaptioner](https://github.com/WEIFENG2333/VideoCaptioner) for subtitles |\n"
            "| All-in-one open studio | A full workspace you can self-host | [Toonflow](https://github.com/HBAI-Ltd/Toonflow-app) or "
            "[LocalMiniDrama](https://github.com/xuanyustudio/LocalMiniDrama) with your own model keys |\n"
            "| Fully local | You have a GPU and want control | [ComfyUI](https://github.com/Comfy-Org/ComfyUI) + [Wan2.2](https://github.com/Wan-Video/Wan2.2) + "
            "[Qwen-Image](https://github.com/QwenLM/Qwen-Image) for character sheets + [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) + "
            "[InfiniteTalk](https://github.com/MeiGen-AI/InfiniteTalk) for lip sync |\n"
            "| Agent workflow | Claude Code or Codex writes scripts and shots | [shuohao-skills](https://github.com/eternityspring/shuohao-skills) or "
            "[drama-skills](https://github.com/zenstory-ai/drama-skills), then any video model |"
        ),
        "toc": "## Contents",
        "legend": "Legend: 🆕 created in the last {new} days　💤 no update for over a year　⭐ stars (as of {date})",
        "related": "## Related lists",
        "compliance": "## Rules for publishing in mainland China",
        "compliance_note": "> A plain summary of public rules for orientation only, not legal advice. Check the original text and platform rules.",
        "platform_head": "| Platform | Description |\n|---|---|",
        "contrib_title": "## Contributing",
        "contrib": "Suggestions and fixes are welcome: [open an issue](https://github.com/{repo}/issues/new/choose) or edit "
                   "[`data/tools.yaml`](data/tools.yaml) and send a PR. See [CONTRIBUTING.md](CONTRIBUTING.md). The README is generated, please do not edit it by hand.",
        "star_title": "## Star history",
        "license": "## License\n\n[CC0 1.0](LICENSE). Each listed project keeps its own license.",
    },
}


def build(lang: str, data: dict, stats: dict, today: dt.date) -> str:
    t = TEXT[lang]
    snapshot = max((v["fetched"] for v in stats.values() if v.get("fetched")), default=today.isoformat())
    badges = (
        f"[![Stars](https://img.shields.io/github/stars/{REPO}?style=flat-square)](https://github.com/{REPO}) "
        f"[![Last commit](https://img.shields.io/github/last-commit/{REPO}?style=flat-square)](https://github.com/{REPO}/commits) "
        f"[![License: CC0-1.0](https://img.shields.io/badge/license-CC0--1.0-lightgrey?style=flat-square)](LICENSE) "
        f"[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)"
    )
    cats = data["categories"]
    plat_title = "## " + data[f"platforms_{lang}"]
    toc_titles = [t["start_title"]] + ["## " + c[lang] for c in cats] + [plat_title, t["compliance"], t["related"], t["contrib_title"]]
    toc = "\n".join(f"- [{x[3:]}](#{anchor(x[3:])})" for x in toc_titles)

    parts = [t["title"], badges, t["switch"], t["tagline"], t["why_title"], t["why"], t["flow_title"], t["flow"],
             t["start_title"], t["start"], t["toc"], toc,
             t["legend"].format(new=NEW_DAYS, date=snapshot[:10])]
    for c in cats:
        parts += ["## " + c[lang], c[f"{lang}_intro"], table(c["items"], stats, today, lang)]

    parts += [plat_title, data[f"platforms_intro_{lang}"],
              t["platform_head"] + "\n" + "\n".join(
                  f"| [{p['name'] if lang == 'zh' else p['name_en']}]({p['url']}) | {p[lang]} |" for p in data["platforms"])]

    comp = [t["compliance"], t["compliance_note"]]
    for item in data["compliance"]:
        comp.append(f"- **[{item['title_' + lang]}]({item['url']})**：{item[lang]}" if lang == "zh"
                    else f"- **[{item['title_en']}]({item['url']})**: {item['en']}")
    parts.append("\n\n".join(comp[:2]) + "\n\n" + "\n".join(comp[2:]))

    parts += [t["related"], table(data["related"], stats, today, lang)]
    parts += [t["contrib_title"], t["contrib"].format(repo=REPO)]
    parts += [t["star_title"],
              f"[![Star History Chart](https://api.star-history.com/svg?repos={REPO}&type=Date)](https://star-history.com/#{REPO}&Date)"]
    parts.append(t["license"])
    return "\n\n".join(parts) + "\n"


def main():
    data, stats = load()
    today = dt.date.today()
    (ROOT / "README.md").write_text(build("zh", data, stats, today), encoding="utf-8")
    (ROOT / "README.en.md").write_text(build("en", data, stats, today), encoding="utf-8")
    missing = [i["repo"] for c in data["categories"] for i in c["items"] if i["repo"].lower() not in stats]
    print(f"README.md and README.en.md written; entries without stats: {missing or 'none'}")


if __name__ == "__main__":
    main()
