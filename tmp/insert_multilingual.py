#!/usr/bin/env python3
"""Insert 8 new case body blocks into each multilingual README.

For zh-CN/zh-TW: use translated titles.
For other languages: keep English titles (matching the existing repo pattern, e.g. Case 101).

Important: localized News/Menu sections are protected human-maintained assets.
This helper only inserts case bodies and must not be extended into a generic
README sync that rewrites localized News/Menu blocks.
"""
import json
import re
from pathlib import Path

REPO = Path('/Users/evolink/Desktop/github-repo/awesome-gpt-image-2-prompts')
MAPPING = REPO / 'tmp' / 'valid_mapping.json'

# Translated titles per case_number
TITLES_ZH_CN = {
    102: '收藏手办工作台摄影',
    103: '雨夜巴士站人像',
    168: '户外运动服网格广告',
    169: '地形字母卫星拼图',
    170: '冰咖啡产品信息图',
    171: '时尚连衣裙系列信息图',
    172: '黑白时尚封面',
    173: '快餐角色海报',
}
TITLES_ZH_TW = {
    102: '收藏手辦工作台攝影',
    103: '雨夜巴士站人像',
    168: '戶外運動服網格廣告',
    169: '地形字母衛星拼圖',
    170: '冰咖啡產品資訊圖',
    171: '時尚連衣裙系列資訊圖',
    172: '黑白時尚封面',
    173: '快餐角色海報',
}

# Section header anchors (where to insert before, per language)
# For portrait inserts, anchor = the Poster section header in that language.
# For poster inserts, anchor = the Character section header in that language.
SECTION_ANCHORS = {
    'README.md': ('## Poster & Illustration Cases', '## Character Design Cases'),
    'README_de.md': ('## Poster- und Illustrations-Faelle', '## Faelle zum Charakterdesign'),
    'README_es.md': ('## Casos de Posters e Ilustracion', '## Casos de Diseno de Personajes'),
    'README_fr.md': ('## Cas d Affiches et d Illustration', '## Cas de Design de Personnage'),
    'README_ja.md': ('## ポスターとイラストの事例', '## キャラクターデザイン事例'),
    'README_ko.md': ('## 포스터 및 일러스트 사례', '## 캐릭터 디자인 사례'),
    'README_pt.md': ('## Casos de Poster e Ilustracao', '## Casos de Design de Personagem'),
    'README_ru.md': ('## Кейсы постеров и иллюстраций', '## Кейсы дизайна персонажей'),
    'README_tr.md': ('## Poster ve Illustrasyon Vakalari', '## Karakter Tasarimi Vakalari'),
    'README_zh-CN.md': ('## 海报与插画案例', '## 角色设计案例'),
    'README_zh-TW.md': ('## 海報與插畫案例', '## 角色設計案例'),
}


def render_block(case_num, title_for_link, raw_title, handle, url, folder, prompt):
    return (
        f"<!-- Case {case_num}: {raw_title} (by @{handle}) -->\n"
        f"### Case {case_num}: [{title_for_link}]({url}) (by [@{handle}](https://x.com/{handle}))\n"
        "\n"
        "| Output |\n"
        "| :----: |\n"
        f"| <img src=\"./images/{folder}/output.jpg\" width=\"300\" alt=\"Output image\"> |\n"
        "\n"
        "**Prompt:**\n"
        "\n"
        "```\n"
        f"{prompt}\n"
        "```\n"
    )


def main():
    cases = json.loads(MAPPING.read_text())
    portrait_cases = sorted([c for c in cases if c['category_slug'] == 'portrait'], key=lambda c: c['case_number'])
    poster_cases = sorted([c for c in cases if c['category_slug'] == 'poster'], key=lambda c: c['case_number'])

    for fname, (poster_anchor, char_anchor) in SECTION_ANCHORS.items():
        if fname == 'README.md':
            continue  # already done
        path = REPO / fname
        text = path.read_text()

        if fname == 'README_zh-CN.md':
            title_map = TITLES_ZH_CN
        elif fname == 'README_zh-TW.md':
            title_map = TITLES_ZH_TW
        else:
            title_map = None

        # Build portrait insertion block
        portrait_blocks = []
        for c in portrait_cases:
            n = c['case_number']
            link_title = title_map[n] if title_map else c['title']
            raw_comment_title = title_map[n] if title_map else c['title']
            portrait_blocks.append(render_block(
                n, link_title, raw_comment_title, c['author_handle'],
                c['tweet_url'], c['folder_name'], c['prompt_text']))
        portrait_block = '\n'.join(portrait_blocks)

        poster_blocks = []
        for c in poster_cases:
            n = c['case_number']
            link_title = title_map[n] if title_map else c['title']
            raw_comment_title = title_map[n] if title_map else c['title']
            poster_blocks.append(render_block(
                n, link_title, raw_comment_title, c['author_handle'],
                c['tweet_url'], c['folder_name'], c['prompt_text']))
        poster_block = '\n'.join(poster_blocks)

        # Verify anchors are unique
        if text.count(poster_anchor) != 1:
            print(f"WARN {fname}: poster anchor '{poster_anchor}' appears {text.count(poster_anchor)} times")
            continue
        if text.count(char_anchor) != 1:
            print(f"WARN {fname}: char anchor '{char_anchor}' appears {text.count(char_anchor)} times")
            continue

        text = text.replace(poster_anchor, f"{portrait_block}\n{poster_anchor}", 1)
        text = text.replace(char_anchor, f"{poster_block}\n{char_anchor}", 1)

        path.write_text(text)
        print(f"OK {fname}: inserted 2 portrait + 6 poster cases")


if __name__ == '__main__':
    main()
