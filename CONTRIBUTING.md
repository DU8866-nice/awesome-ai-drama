# 贡献指南 · Contributing

感谢帮忙完善这份清单！ / Thanks for helping improve the list! (English below.)

## 收录标准

- 和 AI 短剧 / 漫剧制作直接相关：剧本、分镜、角色一致性、视频生成、配音、口型、配乐音效、剪辑字幕、发布合规等环节之一。
- GitHub 上的开源项目，近 12 个月内有更新，且不是已归档仓库。
- 能实际使用：有可运行的代码、模型权重或安装说明，不收只有宣传页的项目。
- 不收：去水印 / 去除 AI 标识、换脸冒充真人、盗版资源等违法或侵权用途的工具。

## 怎么提交

1. 只改 [`data/tools.yaml`](data/tools.yaml)，在合适的分类下加一条：

   ```yaml
   - repo: owner/name
     zh: "一句话中文说明，讲清它做什么。"
     en: "One-sentence English description."
   ```

2. 运行脚本更新数据并生成 README（需要 Python 3.10+ 和 PyYAML）：

   ```bash
   pip install pyyaml
   GITHUB_TOKEN=你的token python scripts/update_stats.py   # 可选，刷新星标
   python scripts/build_readme.py
   ```

3. 提 PR，说明为什么推荐它。不方便改文件的话，直接[提 Issue 推荐](../../issues/new/choose)也可以。

说明请用自己的话写，客观描述功能，不要照搬宣传语或写"最强""第一"之类的词。

---

## Criteria

- Directly useful for making AI short dramas or motion comics (script, storyboard, character consistency, video, voice, lip sync, music, editing, release).
- Open source on GitHub, updated within the last 12 months, not archived.
- Actually usable: runnable code, weights or install instructions.
- Not accepted: tools for removing watermarks or AI labels, impersonating real people, or piracy.

## How to submit

1. Edit only [`data/tools.yaml`](data/tools.yaml) and add an entry under the right category (`repo`, `zh`, `en`).
2. Run `python scripts/build_readme.py` (optionally `scripts/update_stats.py` with a `GITHUB_TOKEN` first).
3. Open a PR explaining why the project belongs here, or [open an issue](../../issues/new/choose) instead.

Describe what the project does in plain words; skip marketing superlatives.
