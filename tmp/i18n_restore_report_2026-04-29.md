# i18n restore report 2026-04-29

- Baseline commit used: `6ebc85d` (`feat: add new prompt cases and sync localized updates`)
- Files fixed:
  - `README_de.md`
  - `README_es.md`
  - `README_fr.md`
  - `README_ja.md`
  - `README_ko.md`
  - `README_pt.md`
  - `README_ru.md`
  - `README_tr.md`
  - `README_zh-CN.md`
  - `README_zh-TW.md`

## What was restored

- Restored each localized `News` section from the last known-good multilingual baseline style/content, while replacing the broken English-overwritten recent entries.
- Added the latest consolidated April 29 news line in each locale's language.
- Rebuilt each localized `Menu` section against the current file structure and current case inventory, preserving all current case bodies and keeping April 29 case additions intact.
- Verified localized files still contain the same total case count as English and that menu case counts match case heading/comment counts.

## April 29 localized news lines added

- `README_de.md`
  - `- **29. April 2026:** 22 neue GPT-Image-2-Prompt-Faelle ueber die Review-Batches hinweg hinzugefuegt (3 E-Commerce, 3 Werbekreativ, 4 Portraet, 2 Charakterdesign, 9 Poster, 1 Vergleich), die lokalisierten Prompt-Eintraege fuer Fall 102 und 103 synchronisiert und den erweiterten Valid-Keep-Set-Durchlauf uebernommen`
- `README_es.md`
  - `- **29 de abril de 2026:** Se agregaron 22 nuevos casos de prompts de GPT-Image-2 en los lotes de revision (3 e-commerce, 3 creatividad publicitaria, 4 retrato, 2 diseno de personajes, 9 poster, 1 comparativa), se sincronizaron los prompts localizados de los Casos 102 y 103 y se incorporo la revision ampliada del conjunto valido conservado`
- `README_fr.md`
  - `- **29 avril 2026 :** Ajout de 22 nouveaux cas de prompts GPT-Image-2 dans les lots de revue (3 e-commerce, 3 creation publicitaire, 4 portrait, 2 design de personnage, 9 affiche, 1 comparaison), synchronisation des prompts localises des Cas 102 et 103 et integration du passage elargi sur l ensemble valide a conserver`
- `README_ja.md`
  - `- **2026年4月29日:** レビューバッチ全体で22件の新しいGPT-Image-2プロンプト事例を追加（Eコマース3、広告クリエイティブ3、ポートレート4、キャラクターデザイン2、ポスター9、比較1）し、Case 102 と 103 のローカライズ済みプロンプトを同期、さらに有効 keep-set の拡張見直しを反映`
- `README_ko.md`
  - `- **2026년 4월 29일:** 리뷰 배치 전반에 걸쳐 GPT-Image-2 신규 프롬프트 사례 22개를 추가하고(이커머스 3, 광고 크리에이티브 3, 인물 4, 캐릭터 디자인 2, 포스터 9, 비교 1), Case 102와 103의 현지화 프롬프트를 동기화했으며, 더 넓은 valid keep-set 점검 내용을 반영했습니다`
- `README_pt.md`
  - `- **29 de abril de 2026:** Foram adicionados 22 novos casos de prompts GPT-Image-2 nos lotes de revisao (3 e-commerce, 3 criativo publicitario, 4 retrato, 2 design de personagem, 9 poster, 1 comparacao), os prompts localizados dos Casos 102 e 103 foram sincronizados e a revisao ampliada do conjunto valido a manter foi incorporada`
- `README_ru.md`
  - `- **29 апреля 2026:** Добавлено 22 новых кейса с prompt для GPT-Image-2 по итогам ревью-батчей (3 e-commerce, 3 рекламный креатив, 4 портрет, 2 дизайн персонажа, 9 постер, 1 сравнение), синхронизированы локализованные prompt для кейсов 102 и 103 и включен расширенный проход по valid keep-set`
- `README_tr.md`
  - `- **29 Nisan 2026:** Inceleme partileri genelinde 22 yeni GPT-Image-2 prompt vakasi eklendi (3 e-ticaret, 3 reklam kreatifi, 4 portre, 2 karakter tasarimi, 9 poster, 1 karsilastirma), Case 102 ve 103 icin yerellestirilmis prompt girisleri senkronize edildi ve daha genis valid keep-set taramasi dahil edildi`
- `README_zh-CN.md`
  - `- **2026 年 4 月 29 日：** 在本轮 review 批次中新增 22 个 GPT-Image-2 prompt 案例（电商 3、广告创意 3、人像 4、角色设计 2、海报 9、对比 1），同步修正 Case 102 与 103 的多语言 prompt，并纳入更大范围的有效 keep-set 校验`
- `README_zh-TW.md`
  - `- **2026 年 4 月 29 日：** 在本輪 review 批次中新增 22 個 GPT-Image-2 prompt 案例（電商 3、廣告創意 3、人像 4、角色設計 2、海報 9、對比 1），同步修正 Case 102 與 103 的多語言 prompt，並納入更大範圍的有效 keep-set 校驗`

## Verification

- English and every localized README currently contain `312` case comments and `312` case headings.
- Each localized menu also contains `312` case entries.
- No localized README still contains English `Added ...` news bullets.

## Commit / push status

- Commit hash: `81f83ad`
- Push status: pushed to `origin/main`
