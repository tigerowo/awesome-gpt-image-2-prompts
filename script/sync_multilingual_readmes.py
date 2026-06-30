#!/usr/bin/env python3
"""Sync localized README files from README.md.

Important: localized News and Menu sections are human-maintained assets.
Generic sync runs must preserve those sections by default so repository-wide
content refreshes cannot silently overwrite curated localized updates.

Use --rewrite-protected-sections only for the rare maintenance task where a
human intentionally wants this script to regenerate localized News/Menu.
"""

import argparse
import re
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"


LOCALES = {
    "de": {
        "path": ROOT / "README_de.md",
        "logo_alt": "Projektlogo",
        "intro_heading": "Einfuehrung",
        "intro_title": "Willkommen im Repository awesome-gpt-image-2-prompts! 🤗",
        "intro_body": "**Wir sammeln hochwertige Prompts und Bildbeispiele fuer GPT-Image-2 aus den Bereichen Portraet, Poster, Charakterblaetter, UI-Mockups und Community-Experimente.**",
        "intro_source": "Die meisten Beispiele in diesem Repository wurden aus X/Twitter, Creator-Communities, oeffentlichen Demos und geteilten Experimenten kuratiert.",
        "intro_try": "Teste es auf Evolink: [GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "Wenn dir das nuetzt, gib dem Repository gern einen Star. ⭐",
        "note_1": "> Dieses Repository konzentriert sich auf wiederverwendbare Prompt-Muster, Referenzfaelle und aufgabenspezifische Beispiele fuer GPT-Image-2 auf Evolink.",
        "note_2": "> Aktuelle prompt-only Updates werden ausserdem in `gpt_image_2_prompt.json` dokumentiert.",
        "news_heading": "Neuigkeiten",
        "news": [
            "- **30. April 2026:** 9 neue GPT-Image-2-Prompt-Faelle aus dem Suchbatch der letzten 24 Stunden hinzugefuegt (3 Portraet, 1 Poster, 3 UI, 2 Vergleich) nach Freigabe und validierter Medienpruefung",
            "- **21. April 2026:** 48 neue Prompt-Faelle in die Galerieabschnitte einsortiert und verlinkte Ausgabebilder heruntergeladen",
            "- **21. April 2026:** 12 neue GPT-Image-2-Prompts fuer Portraet-, Poster-, UI- und Vergleichsfaelle hinzugefuegt",
            "- **20. April 2026:** 10 neu kuratierte GPT-Image-2-Prompts mit lokalen Bildassets und README-Updates hinzugefuegt.",
            "- **19. April 2026:** 10 neue GPT-Image-2-Prompts fuer Poster-, UI- und Vergleichsfaelle hinzugefuegt",
            "- **18. April 2026:** Erste Veroeffentlichung des Repositories mit einer kuratierten GPT-Image-2-Fallsammlung",
        ],
        "menu_heading": "Inhaltsverzeichnis",
        "section_intro": "Einfuehrung",
        "section_news": "Neuigkeiten",
        "section_menu": "Inhaltsverzeichnis",
        "section_portrait": "Portraet- und Fotografie-Faelle",
        "section_poster": "Poster- und Illustrations-Faelle",
        "section_character": "Faelle zum Charakterdesign",
        "section_ui": "UI- und Social-Media-Mockup-Faelle",
        "section_comparison": "Vergleiche und Community-Beispiele",
        "section_ack": "Danksagungen",
        "output": "Ergebnis",
        "output_alt": "Ergebnisbild",
        "prompt": "Prompt",
        "ack_intro": "Dieses Repository wurde von herausragenden offenen Prompt-Sammlungen und von der Community geteilten GPT-Image-2-Experimenten inspiriert.",
        "ack_thanks": "Dank an alle Creator und Mitwirkenden, die ihre Arbeiten oeffentlich geteilt und diese Fallstudien moeglich gemacht haben.",
        "ack_note": "*Wir koennen nicht garantieren, dass jeder Fall dem urspruenglichen Creator korrekt zugeordnet ist. Wenn etwas korrigiert werden muss, kontaktiere uns bitte, dann aktualisieren wir es.*",
        "ack_more": "Wenn du weitere interessante GPT-Image-2-Prompt-Faelle teilen moechtest, melde dich gern und hilf uns, die Evolink-Prompt-Bibliothek auszubauen.",
    },
    "es": {
        "path": ROOT / "README_es.md",
        "logo_alt": "Logotipo del proyecto",
        "intro_heading": "Introduccion",
        "intro_title": "Bienvenido al repositorio awesome-gpt-image-2-prompts! 🤗",
        "intro_body": "**Recopilamos prompts de alta calidad y ejemplos de imagen para GPT-Image-2 en retratos, posters, hojas de personajes, maquetas de UI y experimentos de la comunidad.**",
        "intro_source": "La mayoria de los casos de este repositorio estan recopilados de X/Twitter, comunidades de creadores, demos publicas y experimentos compartidos.",
        "intro_try": "Pruebalo en Evolink: [GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "Si esto te resulta util, considera darle una estrella. ⭐",
        "note_1": "> Este repositorio se centra en patrones de prompts reutilizables, casos de referencia y ejemplos especificos por tarea para GPT-Image-2 en Evolink.",
        "note_2": "> Las actualizaciones recientes solo de prompts tambien se registran en `gpt_image_2_prompt.json`.",
        "news_heading": "Novedades",
        "news": [
            "- **30 de abril de 2026:** Se agregaron 9 nuevos casos de prompts de GPT-Image-2 del lote de busqueda de las ultimas 24 horas (3 retrato, 1 poster, 3 UI, 2 comparativa) tras la aprobacion y la validacion de medios",
            "- **21 de abril de 2026:** Se categorizaron 48 nuevos casos de prompts en las secciones de la galeria y se descargaron las imagenes de salida enlazadas",
            "- **21 de abril de 2026:** Se agregaron 12 nuevos prompts de GPT-Image-2 en casos de retrato, poster, UI y comparativas",
            "- **20 de abril de 2026:** Se agregaron 10 nuevos prompts curados de GPT-Image-2 con recursos de imagen locales y actualizaciones del README.",
            "- **19 de abril de 2026:** Se agregaron 10 nuevos prompts de GPT-Image-2 en casos de poster, UI y comparativas",
            "- **18 de abril de 2026:** Primera publicacion del repositorio con una seleccion curada de casos de GPT-Image-2",
        ],
        "menu_heading": "Indice",
        "section_intro": "Introduccion",
        "section_news": "Novedades",
        "section_menu": "Indice",
        "section_portrait": "Casos de Retrato y Fotografia",
        "section_poster": "Casos de Posters e Ilustracion",
        "section_character": "Casos de Diseno de Personajes",
        "section_ui": "Casos de UI y Mockups de Redes Sociales",
        "section_comparison": "Comparativas y Ejemplos de la Comunidad",
        "section_ack": "Agradecimientos",
        "output": "Resultado",
        "output_alt": "Imagen de resultado",
        "prompt": "Prompt",
        "ack_intro": "Este repositorio se inspiro en destacadas colecciones abiertas de prompts y en experimentos de GPT-Image-2 compartidos por la comunidad.",
        "ack_thanks": "Gracias a los creadores y colaboradores que compartieron su trabajo publicamente e hicieron posibles estos casos de estudio.",
        "ack_note": "*No podemos garantizar que cada caso este atribuido correctamente al creador original. Si algo debe corregirse, contactanos y lo actualizaremos.*",
        "ack_more": "Si tienes mas casos interesantes de prompts de GPT-Image-2 para compartir, no dudes en escribirnos y ayudarnos a ampliar la biblioteca de prompts de Evolink.",
    },
    "fr": {
        "path": ROOT / "README_fr.md",
        "logo_alt": "Logo du projet",
        "intro_heading": "Introduction",
        "intro_title": "Bienvenue dans le depot awesome-gpt-image-2-prompts ! 🤗",
        "intro_body": "**Nous rassemblons des prompts de haute qualite et des exemples d images pour GPT-Image-2 sur les portraits, affiches, fiches de personnage, maquettes UI et experimentations de la communaute.**",
        "intro_source": "La plupart des cas de ce depot sont organises a partir de X/Twitter, de communautes de createurs, de demos publiques et d experimentations partagees.",
        "intro_try": "Essayez-le sur Evolink : [GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "Si cela vous est utile, pensez a mettre une etoile. ⭐",
        "note_1": "> Ce depot se concentre sur des modeles de prompts reutilisables, des cas de reference et des exemples par tache pour GPT-Image-2 sur Evolink.",
        "note_2": "> Les mises a jour recentes contenant uniquement des prompts sont egalement suivies dans `gpt_image_2_prompt.json`.",
        "news_heading": "Actualites",
        "news": [
            "- **30 avril 2026 :** Ajout de 9 nouveaux cas de prompts GPT-Image-2 issus du lot de recherche des dernieres 24 heures (3 portrait, 1 affiche, 3 UI, 2 comparaison) apres approbation et validation des medias",
            "- **21 avril 2026 :** 48 nouveaux cas de prompts ont ete classes dans les sections de la galerie et les images de sortie liees ont ete telechargees",
            "- **21 avril 2026 :** Ajout de 12 nouveaux prompts GPT-Image-2 dans les categories portrait, affiche, UI et comparaison",
            "- **20 avril 2026 :** Ajout de 10 nouveaux prompts GPT-Image-2 organises avec des ressources image locales et des mises a jour du README.",
            "- **19 avril 2026 :** Ajout de 10 nouveaux prompts GPT-Image-2 dans les categories affiche, UI et comparaison",
            "- **18 avril 2026 :** Premiere publication du depot avec une selection organisee de cas GPT-Image-2",
        ],
        "menu_heading": "Sommaire",
        "section_intro": "Introduction",
        "section_news": "Actualites",
        "section_menu": "Sommaire",
        "section_portrait": "Cas de Portrait et Photographie",
        "section_poster": "Cas d Affiches et d Illustration",
        "section_character": "Cas de Design de Personnage",
        "section_ui": "Cas de Maquettes UI et Reseaux Sociaux",
        "section_comparison": "Comparaisons et Exemples de la Communaute",
        "section_ack": "Remerciements",
        "output": "Resultat",
        "output_alt": "Image du resultat",
        "prompt": "Prompt",
        "ack_intro": "Ce depot s inspire de remarquables collections ouvertes de prompts et d experimentations GPT-Image-2 partagees par la communaute.",
        "ack_thanks": "Merci aux createurs et contributeurs qui ont partage publiquement leur travail et rendu ces etudes de cas possibles.",
        "ack_note": "*Nous ne pouvons pas garantir que chaque cas soit attribue au createur d origine. Si quelque chose doit etre corrige, contactez-nous et nous le mettrons a jour.*",
        "ack_more": "Si vous avez d autres cas de prompts GPT-Image-2 interessants a partager, n hesitez pas a nous contacter pour aider a enrichir la bibliotheque de prompts Evolink.",
    },
    "ja": {
        "path": ROOT / "README_ja.md",
        "logo_alt": "プロジェクトロゴ",
        "intro_heading": "紹介",
        "intro_title": "awesome-gpt-image-2-prompts リポジトリへようこそ！🤗",
        "intro_body": "**このリポジトリでは、GPT-Image-2 の人物写真、ポスター、キャラクターシート、UI モックアップ、コミュニティ実験に関する高品質なプロンプトと画像例を集めています。**",
        "intro_source": "このリポジトリの多くの事例は、X/Twitter、クリエイターコミュニティ、公開デモ、共有された実験からキュレーションしています。",
        "intro_try": "Evolink で試す: [GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "役に立ったら Star をお願いします。⭐",
        "note_1": "> このリポジトリは、Evolink 上の GPT-Image-2 向けに、再利用しやすいプロンプトパターン、参照事例、タスク別サンプルをまとめています。",
        "note_2": "> 最近のプロンプトのみの更新は `gpt_image_2_prompt.json` にも記録しています。",
        "news_heading": "最新情報",
        "news": [
            "- **2026年4月30日:** 直近24時間の検索バッチから承認済みかつメディア検証済みの GPT-Image-2 プロンプト事例を9件追加（ポートレート3、ポスター1、UI 3、比較2）",
            "- **2026年4月21日:** 48件の新しいプロンプト事例をギャラリーの各セクションに整理し、リンク先の出力画像をダウンロードしました",
            "- **2026年4月21日:** ポートレート、ポスター、UI、比較カテゴリに GPT-Image-2 の新規プロンプトを 12 件追加",
            "- **2026年4月20日:** ローカル画像アセットと README 更新を含む GPT-Image-2 の新規キュレーション済みプロンプトを 10 件追加。",
            "- **2026年4月19日:** ポスター、UI、比較カテゴリに GPT-Image-2 の新規プロンプトを 10 件追加",
            "- **2026年4月18日:** キュレーションした GPT-Image-2 事例集としてリポジトリを初回公開",
        ],
        "menu_heading": "目次",
        "section_intro": "紹介",
        "section_news": "最新情報",
        "section_menu": "目次",
        "section_portrait": "ポートレートと写真の事例",
        "section_poster": "ポスターとイラストの事例",
        "section_character": "キャラクターデザイン事例",
        "section_ui": "UI とソーシャルメディアモックアップ事例",
        "section_comparison": "比較とコミュニティ事例",
        "section_ack": "謝辞",
        "output": "出力",
        "output_alt": "出力画像",
        "prompt": "プロンプト",
        "ack_intro": "このリポジトリは、優れたオープンなプロンプト集と、コミュニティで共有された GPT-Image-2 実験に着想を得ています。",
        "ack_thanks": "作品を公開し、これらのケーススタディを可能にしてくれたクリエイターと貢献者の皆さんに感謝します。",
        "ack_note": "*すべての事例が元の作者に正確に帰属していることを保証するものではありません。修正が必要な点があればご連絡ください。更新します。*",
        "ack_more": "共有したい GPT-Image-2 の面白いプロンプト事例があれば、ぜひご連絡ください。Evolink のプロンプトライブラリ拡充にご協力ください。",
    },
    "ko": {
        "path": ROOT / "README_ko.md",
        "logo_alt": "프로젝트 로고",
        "intro_heading": "소개",
        "intro_title": "awesome-gpt-image-2-prompts 저장소에 오신 것을 환영합니다! 🤗",
        "intro_body": "**이 저장소는 GPT-Image-2의 인물 사진, 포스터, 캐릭터 시트, UI 목업, 커뮤니티 실험을 위한 고품질 프롬프트와 이미지 예시를 모읍니다.**",
        "intro_source": "이 저장소의 대부분 사례는 X/Twitter, 크리에이터 커뮤니티, 공개 데모, 공유된 실험에서 큐레이션했습니다.",
        "intro_try": "Evolink에서 사용해 보기: [GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "유용했다면 Star를 부탁드립니다. ⭐",
        "note_1": "> 이 저장소는 Evolink의 GPT-Image-2를 위한 재사용 가능한 프롬프트 패턴, 참고 사례, 작업별 예시에 초점을 맞춥니다.",
        "note_2": "> 최근 프롬프트 전용 업데이트도 `gpt_image_2_prompt.json`에 함께 기록됩니다.",
        "news_heading": "최신 소식",
        "news": [
            "- **2026년 4월 30일:** 최근 24시간 검색 배치에서 승인되고 미디어 검증을 통과한 GPT-Image-2 신규 프롬프트 사례 9개를 추가했습니다 (인물 3, 포스터 1, UI 3, 비교 2)",
            "- **2026년 4월 21일:** 새 프롬프트 사례 48개를 갤러리 섹션별로 정리하고 연결된 출력 이미지를 다운로드했습니다",
            "- **2026년 4월 21일:** 인물, 포스터, UI, 비교 카테고리에 GPT-Image-2 신규 프롬프트 12개 추가",
            "- **2026년 4월 20일:** 로컬 이미지 자산과 README 업데이트를 포함한 GPT-Image-2 신규 큐레이션 프롬프트 10개 추가.",
            "- **2026년 4월 19일:** 포스터, UI, 비교 카테고리에 GPT-Image-2 신규 프롬프트 10개 추가",
            "- **2026년 4월 18일:** 큐레이션된 GPT-Image-2 사례 모음으로 저장소 첫 공개",
        ],
        "menu_heading": "목차",
        "section_intro": "소개",
        "section_news": "최신 소식",
        "section_menu": "목차",
        "section_portrait": "인물 및 사진 사례",
        "section_poster": "포스터 및 일러스트 사례",
        "section_character": "캐릭터 디자인 사례",
        "section_ui": "UI 및 소셜 미디어 목업 사례",
        "section_comparison": "비교 및 커뮤니티 사례",
        "section_ack": "감사의 말",
        "output": "결과",
        "output_alt": "출력 이미지",
        "prompt": "프롬프트",
        "ack_intro": "이 저장소는 뛰어난 공개 프롬프트 컬렉션과 커뮤니티에서 공유된 GPT-Image-2 실험에서 영감을 받았습니다.",
        "ack_thanks": "작업을 공개적으로 공유해 이러한 사례 연구를 가능하게 해준 창작자와 기여자들에게 감사드립니다.",
        "ack_note": "*모든 사례가 원저작자에게 정확히 귀속되었다고 보장할 수는 없습니다. 수정이 필요하면 연락해 주세요. 업데이트하겠습니다.*",
        "ack_more": "더 흥미로운 GPT-Image-2 프롬프트 사례가 있다면 언제든 공유해 주세요. Evolink 프롬프트 라이브러리 확장에 도움을 부탁드립니다.",
    },
    "pt": {
        "path": ROOT / "README_pt.md",
        "logo_alt": "Logotipo do projeto",
        "intro_heading": "Introducao",
        "intro_title": "Bem-vindo ao repositorio awesome-gpt-image-2-prompts! 🤗",
        "intro_body": "**Reunimos prompts de alta qualidade e exemplos de imagem para GPT-Image-2 em retratos, posters, fichas de personagens, mockups de UI e experimentos da comunidade.**",
        "intro_source": "A maioria dos casos deste repositorio foi curada a partir de X/Twitter, comunidades de criadores, demos publicas e experimentos compartilhados.",
        "intro_try": "Experimente no Evolink: [GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "Se isso for util, considere dar uma estrela. ⭐",
        "note_1": "> Este repositorio se concentra em padroes de prompts reutilizaveis, casos de referencia e exemplos especificos por tarefa para GPT-Image-2 no Evolink.",
        "note_2": "> Atualizacoes recentes apenas de prompts tambem sao registradas em `gpt_image_2_prompt.json`.",
        "news_heading": "Novidades",
        "news": [
            "- **21 de abril de 2026:** Foram categorizados 48 novos casos de prompts nas secoes da galeria e baixadas as imagens de saida vinculadas",
            "- **21 de abril de 2026:** Adicionados 12 novos prompts de GPT-Image-2 em casos de retrato, poster, UI e comparacao",
            "- **20 de abril de 2026:** Adicionados 10 novos prompts curados de GPT-Image-2 com recursos de imagem locais e atualizacoes do README.",
            "- **19 de abril de 2026:** Adicionados 10 novos prompts de GPT-Image-2 em casos de poster, UI e comparacao",
            "- **18 de abril de 2026:** Primeira publicacao do repositorio com um conjunto curado de casos de GPT-Image-2",
        ],
        "menu_heading": "Indice",
        "section_intro": "Introducao",
        "section_news": "Novidades",
        "section_menu": "Indice",
        "section_portrait": "Casos de Retrato e Fotografia",
        "section_poster": "Casos de Poster e Ilustracao",
        "section_character": "Casos de Design de Personagem",
        "section_ui": "Casos de UI e Mockups de Redes Sociais",
        "section_comparison": "Comparacoes e Exemplos da Comunidade",
        "section_ack": "Agradecimentos",
        "output": "Resultado",
        "output_alt": "Imagem de resultado",
        "prompt": "Prompt",
        "ack_intro": "Este repositorio foi inspirado por excelentes colecoes abertas de prompts e por experimentos de GPT-Image-2 compartilhados pela comunidade.",
        "ack_thanks": "Obrigado aos criadores e contribuidores que compartilharam seu trabalho publicamente e tornaram estes estudos de caso possiveis.",
        "ack_note": "*Nao podemos garantir que cada caso esteja atribuido ao criador original. Se algo precisar ser corrigido, entre em contato e atualizaremos.*",
        "ack_more": "Se voce tiver mais casos interessantes de prompts de GPT-Image-2 para compartilhar, fique a vontade para falar conosco e ajudar a expandir a biblioteca de prompts da Evolink.",
    },
    "ru": {
        "path": ROOT / "README_ru.md",
        "logo_alt": "Логотип проекта",
        "intro_heading": "Введение",
        "intro_title": "Добро пожаловать в репозиторий awesome-gpt-image-2-prompts! 🤗",
        "intro_body": "**Мы собираем качественные промпты и примеры изображений для GPT-Image-2 по портретам, постерам, карточкам персонажей, UI-макетам и экспериментам сообщества.**",
        "intro_source": "Большинство кейсов в этом репозитории отобрано из X/Twitter, сообществ авторов, публичных демо и совместно опубликованных экспериментов.",
        "intro_try": "Попробовать в Evolink: [GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "Если это полезно, поставьте звезду. ⭐",
        "note_1": "> Этот репозиторий посвящен переиспользуемым шаблонам промптов, референсным кейсам и примерам задач для GPT-Image-2 в Evolink.",
        "note_2": "> Последние обновления только с промптами также отслеживаются в `gpt_image_2_prompt.json`.",
        "news_heading": "Новости",
        "news": [
            "- **21 апреля 2026:** 48 новых кейсов с промптами были распределены по разделам галереи, а связанные выходные изображения были загружены",
            "- **21 апреля 2026:** Добавлено 12 новых промптов GPT-Image-2 для портретов, постеров, UI и сравнительных кейсов",
            "- **20 апреля 2026:** Добавлено 10 новых отобранных промптов GPT-Image-2 с локальными изображениями и обновлениями README.",
            "- **19 апреля 2026:** Добавлено 10 новых промптов GPT-Image-2 для постеров, UI и сравнительных кейсов",
            "- **18 апреля 2026:** Первый релиз репозитория с отобранным набором кейсов GPT-Image-2",
        ],
        "menu_heading": "Оглавление",
        "section_intro": "Введение",
        "section_news": "Новости",
        "section_menu": "Оглавление",
        "section_portrait": "Кейсы портретов и фотографии",
        "section_poster": "Кейсы постеров и иллюстраций",
        "section_character": "Кейсы дизайна персонажей",
        "section_ui": "Кейсы UI и макетов соцсетей",
        "section_comparison": "Сравнения и примеры сообщества",
        "section_ack": "Благодарности",
        "output": "Результат",
        "output_alt": "Результирующее изображение",
        "prompt": "Промпт",
        "ack_intro": "Этот репозиторий вдохновлен выдающимися открытыми коллекциями промптов и экспериментами GPT-Image-2, которыми делилось сообщество.",
        "ack_thanks": "Спасибо авторам и участникам, которые публично делились своими работами и сделали эти кейсы возможными.",
        "ack_note": "*Мы не можем гарантировать, что каждый кейс атрибутирован исходному автору без ошибок. Если что-то нужно исправить, свяжитесь с нами, и мы обновим информацию.*",
        "ack_more": "Если у вас есть другие интересные кейсы с промптами GPT-Image-2, поделитесь ими с нами и помогите расширить библиотеку промптов Evolink.",
    },
    "tr": {
        "path": ROOT / "README_tr.md",
        "logo_alt": "Proje logosu",
        "intro_heading": "Giris",
        "intro_title": "awesome-gpt-image-2-prompts deposuna hos geldiniz! 🤗",
        "intro_body": "**Portreler, posterler, karakter sayfalari, UI mockuplari ve topluluk deneyleri icin GPT-Image-2 uzerine yuksek kaliteli promptlar ve gorsel ornekler derliyoruz.**",
        "intro_source": "Bu depodaki vakalarin cogu X/Twitter, uretici topluluklari, herkese acik demolar ve paylasilan deneylerden derlenmistir.",
        "intro_try": "Evolink uzerinde deneyin: [GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "Faydali bulduysaniz bir yildiz vermeyi dusunun. ⭐",
        "note_1": "> Bu depo, Evolink uzerindeki GPT-Image-2 icin yeniden kullanilabilir prompt kaliplari, referans vakalar ve goreve ozel orneklere odaklanir.",
        "note_2": "> Son yalnizca-prompt guncellemeleri `gpt_image_2_prompt.json` dosyasinda da takip edilir.",
        "news_heading": "Haberler",
        "news": [
            "- **21 Nisan 2026:** 48 yeni prompt vakasi galeri bolumlerine kategorilendi ve baglantili cikti gorselleri indirildi",
            "- **21 Nisan 2026:** Portre, poster, UI ve karsilastirma vakalarina 12 yeni GPT-Image-2 promptu eklendi",
            "- **20 Nisan 2026:** Yerel gorsel varliklari ve README guncellemeleriyle birlikte 10 yeni derlenmis GPT-Image-2 promptu eklendi.",
            "- **19 Nisan 2026:** Poster, UI ve karsilastirma vakalarina 10 yeni GPT-Image-2 promptu eklendi",
            "- **18 Nisan 2026:** Derlenmis GPT-Image-2 vaka setiyle deponun ilk yayini",
        ],
        "menu_heading": "Icindekiler",
        "section_intro": "Giris",
        "section_news": "Haberler",
        "section_menu": "Icindekiler",
        "section_portrait": "Portre ve Fotografcilik Vakalari",
        "section_poster": "Poster ve Illustrasyon Vakalari",
        "section_character": "Karakter Tasarimi Vakalari",
        "section_ui": "UI ve Sosyal Medya Mockup Vakalari",
        "section_comparison": "Karsilastirma ve Topluluk Ornekleri",
        "section_ack": "Tesekkurler",
        "output": "Sonuc",
        "output_alt": "Cikti gorseli",
        "prompt": "Prompt",
        "ack_intro": "Bu depo, etkileyici acik prompt koleksiyonlari ve toplulugun paylastigi GPT-Image-2 deneylerinden ilham almistir.",
        "ack_thanks": "Calismalarini herkese acik paylasan ve bu vaka calismalarini mumkun kilan ureticilere ve katkida bulunanlara tesekkurler.",
        "ack_note": "*Her vakanin orijinal ureticiye eksiksiz sekilde atfedildigini garanti edemeyiz. Duzeltilmesi gereken bir sey varsa lutfen bizimle iletisime gecin, guncelleriz.*",
        "ack_more": "Paylasmak istediginiz daha fazla ilginc GPT-Image-2 prompt vakasi varsa bize ulasin ve Evolink prompt kutuphanesini genisletmemize yardim edin.",
    },
    "zh-CN": {
        "path": ROOT / "README_zh-CN.md",
        "logo_alt": "项目 Logo",
        "intro_heading": "简介",
        "intro_title": "欢迎来到 awesome-gpt-image-2-prompts 仓库！🤗",
        "intro_body": "**我们收录了 GPT-Image-2 在人像、海报、角色设计、UI 原型及社区实验等场景下的高质量提示词与图像案例。**",
        "intro_source": "仓库中的大多数案例来源于 X/Twitter 上的创作者社区、公开演示及分享实验。",
        "intro_try": "在 Evolink 上体验：[GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "如果觉得有用，欢迎点个 Star。⭐",
        "note_1": "> 本仓库专注于 GPT-Image-2 在 Evolink 上的可复用提示词模板、参考案例与任务专项示例。",
        "note_2": "> 最近仅提示词的更新也会同步记录在 `gpt_image_2_prompt.json` 中。",
        "news_heading": "最新动态",
        "news": [
            "- **2026 年 4 月 21 日：** 已将 48 个新 prompt 案例整理归入图库分区，并下载对应链接输出图像",
            "- **2026 年 4 月 21 日：** 新增 12 个 GPT-Image-2 prompts，涵盖人像、海报、UI 与对比案例",
            "- **2026 年 4 月 20 日：** 新增 10 个精选 GPT-Image-2 prompts，并同步补充本地图片资源与 README 更新。",
            "- **2026 年 4 月 19 日：** 新增 10 个 GPT-Image-2 prompts，涵盖海报、UI 与对比案例",
            "- **2026 年 4 月 18 日：** 仓库首次发布，收录精选 GPT-Image-2 案例集",
        ],
        "menu_heading": "目录",
        "section_intro": "简介",
        "section_news": "最新动态",
        "section_menu": "目录",
        "section_portrait": "人像与摄影案例",
        "section_poster": "海报与插画案例",
        "section_character": "角色设计案例",
        "section_ui": "UI 与社交媒体截图案例",
        "section_comparison": "模型对比与社区案例",
        "section_ack": "致谢",
        "output": "输出效果",
        "output_alt": "输出图像",
        "prompt": "提示词",
        "ack_intro": "本仓库受到优秀的开源提示词集合以及社区分享的 GPT-Image-2 实验案例启发。",
        "ack_thanks": "感谢所有公开分享作品、让这些案例研究得以成立的创作者与贡献者。",
        "ack_note": "*我们无法保证每个案例都已准确归属于原始创作者。如需更正，请联系我们，我们会及时更新。*",
        "ack_more": "如果你还有更多有趣的 GPT-Image-2 提示词案例，欢迎联系我们，一起扩充 Evolink 的提示词库。",
    },
    "zh-TW": {
        "path": ROOT / "README_zh-TW.md",
        "logo_alt": "專案 Logo",
        "intro_heading": "簡介",
        "intro_title": "歡迎來到 awesome-gpt-image-2-prompts 倉庫！🤗",
        "intro_body": "**我們收錄了 GPT-Image-2 在人像、海報、角色設定、UI 原型與社群實驗等場景中的高品質提示詞與圖像案例。**",
        "intro_source": "本倉庫中的大多數案例整理自 X/Twitter、創作者社群、公開示範與社群分享實驗。",
        "intro_try": "在 Evolink 上體驗：[GPT-Image-2](https://evolink.ai/models?utm_source=github&utm_medium=picture&utm_campaign=awesome-gpt-image-2-prompts)",
        "intro_star": "如果你覺得這個倉庫有幫助，歡迎給個 Star。⭐",
        "note_1": "> 本倉庫專注於 GPT-Image-2 在 Evolink 上的可重用提示詞模式、參考案例與任務型示例。",
        "note_2": "> 最近僅含提示詞的更新也會同步記錄在 `gpt_image_2_prompt.json` 中。",
        "news_heading": "最新動態",
        "news": [
            "- **2026 年 4 月 21 日：** 已將 48 個新 prompt 案例整理歸入圖庫分區，並下載對應連結輸出圖像",
            "- **2026 年 4 月 21 日：** 新增 12 個 GPT-Image-2 prompts，涵蓋人像、海報、UI 與對比案例",
            "- **2026 年 4 月 20 日：** 新增 10 個精選 GPT-Image-2 prompts，並同步補充本地圖片資源與 README 更新。",
            "- **2026 年 4 月 19 日：** 新增 10 個 GPT-Image-2 prompts，涵蓋海報、UI 與對比案例",
            "- **2026 年 4 月 18 日：** 倉庫首次發佈，收錄精選 GPT-Image-2 案例集",
        ],
        "menu_heading": "目錄",
        "section_intro": "簡介",
        "section_news": "最新動態",
        "section_menu": "目錄",
        "section_portrait": "人像與攝影案例",
        "section_poster": "海報與插畫案例",
        "section_character": "角色設計案例",
        "section_ui": "UI 與社群媒體截圖案例",
        "section_comparison": "模型比較與社群案例",
        "section_ack": "致謝",
        "output": "輸出效果",
        "output_alt": "輸出圖像",
        "prompt": "提示詞",
        "ack_intro": "本倉庫受到優秀的開源提示詞集合以及社群分享的 GPT-Image-2 實驗案例啟發。",
        "ack_thanks": "感謝所有公開分享作品、讓這些案例研究得以成立的創作者與貢獻者。",
        "ack_note": "*我們無法保證每個案例都已準確歸屬於原始創作者。如需更正，請聯絡我們，我們會及時更新。*",
        "ack_more": "如果你還有更多有趣的 GPT-Image-2 提示詞案例，歡迎聯絡我們，一起擴充 Evolink 的提示詞庫。",
    },
}


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise ValueError(f"pattern not found: {old}")
    return text.replace(old, new, 1)


PROTECTED_SECTION_KEYS = ("news", "menu")


def heading_regex(title: str, emoji: Optional[str] = None) -> str:
    emoji_part = rf"(?:{re.escape(emoji)}\s+)?" if emoji else ""
    return rf"^##\s+{emoji_part}{re.escape(title)}\s*$"


def extract_section(text: str, heading_pattern: str) -> str:
    pattern = re.compile(rf"(?ms)({heading_pattern}\n.*?)(?=^##\s+|\Z)")
    match = pattern.search(text)
    if not match:
        raise ValueError(f"section not found for heading pattern: {heading_pattern}")
    return match.group(1).rstrip() + "\n"


def replace_section(text: str, heading_pattern: str, new_section: str) -> str:
    pattern = re.compile(rf"(?ms){heading_pattern}\n.*?(?=^##\s+|\Z)")
    updated, count = pattern.subn(new_section.rstrip() + "\n\n", text, count=1)
    if count != 1:
        raise ValueError(f"failed to replace section for heading pattern: {heading_pattern}")
    return updated


def protected_section_patterns(cfg: dict) -> dict[str, str]:
    return {
        "news": heading_regex(cfg["news_heading"]),
        "menu": heading_regex(cfg["menu_heading"], emoji="📑"),
    }


def protected_section_input_patterns(cfg: dict) -> dict[str, tuple[str, ...]]:
    return {
        # Some localized files historically kept the English headings even after
        # their bodies were translated. Keep those files safe too.
        "news": (heading_regex(cfg["news_heading"]), heading_regex("News")),
        "menu": (heading_regex(cfg["menu_heading"], emoji="📑"), heading_regex("Menu", emoji="📑")),
    }


def extract_first_matching_section(text: str, patterns: tuple[str, ...]) -> str:
    last_error = None
    for pattern in patterns:
        try:
            return extract_section(text, pattern)
        except ValueError as exc:
            last_error = exc
    raise last_error if last_error else ValueError("section not found")


def preserve_protected_sections(rendered: str, current: str, cfg: dict) -> tuple[str, dict[str, str]]:
    preserved = {}
    updated = rendered
    for key, output_pattern in protected_section_patterns(cfg).items():
        section = extract_first_matching_section(current, protected_section_input_patterns(cfg)[key])
        updated = replace_section(updated, output_pattern, section)
        preserved[key] = section
    return updated, preserved


def verify_protected_sections_unchanged(text: str, preserved: dict[str, str], cfg: dict) -> None:
    patterns = protected_section_input_patterns(cfg)
    for key, original in preserved.items():
        after = extract_first_matching_section(text, patterns[key])
        if after != original:
            raise ValueError(f"protected {key} section changed during sync for {cfg['path'].name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rewrite-protected-sections",
        action="store_true",
        help="Allow this script to regenerate localized News/Menu sections instead of preserving existing human-maintained content.",
    )
    return parser.parse_args()


def build_locale(base: str, cfg: dict) -> str:
    text = base
    text = replace_once(text, 'alt="Project logo"', f'alt="{cfg["logo_alt"]}"')

    text = replace_once(text, "## Introduction", f"## {cfg['intro_heading']}")
    text = replace_once(text, "Welcome to the awesome-gpt-image-2-prompts repository! 🤗", cfg["intro_title"])
    text = replace_once(text, "**We collect high-quality prompts and image examples for GPT-Image-2 across portraits, posters, character sheets, UI mockups, and community experiments.**", cfg["intro_body"])
    text = replace_once(text, "Most cases in this repository are curated from X/Twitter, creator communities, public demos, and shared experiments.", cfg["intro_source"])
    text = replace_once(text, "Try it on Evolink: [GPT-Image-2](https://evolink.ai/gpt-image-2-prompts?utm_source=github&utm_medium=readme&utm_campaign=awesome-gpt-image-2-prompts)", cfg["intro_try"])
    text = replace_once(text, "If you find this useful, consider giving it a star. ⭐", cfg["intro_star"])
    text = replace_once(text, "> This repository focuses on reusable prompt patterns, reference cases, and task-specific examples for GPT-Image-2 on Evolink.", cfg["note_1"])
    text = replace_once(text, "> Recent prompt-only updates are also tracked in `gpt_image_2_prompt.json`.", cfg["note_2"])

    text = replace_once(text, "## News", f"## {cfg['news_heading']}")
    for english, localized in zip(
        [
            "- **April 21, 2026:** Categorized 48 new prompt cases into the gallery sections and downloaded linked output images",
            "- **April 21, 2026:** Added 12 new GPT-Image-2 prompts across portrait, poster, UI, and comparison cases",
            "- **April 20, 2026:** Added 10 newly curated GPT-Image-2 prompts with local image assets and README updates.",
            "- **April 19, 2026:** Added 10 new GPT-Image-2 prompts across poster, UI, and comparison cases",
            "- **April 18, 2026:** First repository release with curated GPT-Image-2 case set",
        ],
        cfg["news"],
    ):
        text = replace_once(text, english, localized)

    text = replace_once(text, "## 📑 Menu", f"## {cfg['menu_heading']}")
    menu_pairs = [
        ("- [Introduction](#introduction)", f"- [{cfg['section_intro']}](#{cfg['section_intro'].lower().replace(' ', '-')})"),
        ("- [News](#news)", f"- [{cfg['section_news']}](#{cfg['section_news'].lower().replace(' ', '-')})"),
        ("- [Menu](#menu)", f"- [{cfg['section_menu']}](#{cfg['section_menu'].lower().replace(' ', '-')})"),
        ("- [Portrait & Photography Cases](#portrait-photography-cases)", f"- [{cfg['section_portrait']}](#{cfg['section_portrait'].lower().replace(' ', '-')})"),
        ("- [Poster & Illustration Cases](#poster-illustration-cases)", f"- [{cfg['section_poster']}](#{cfg['section_poster'].lower().replace(' ', '-')})"),
        ("- [Character Design Cases](#character-design-cases)", f"- [{cfg['section_character']}](#{cfg['section_character'].lower().replace(' ', '-')})"),
        ("- [UI & Social Media Mockup Cases](#ui-social-media-mockup-cases)", f"- [{cfg['section_ui']}](#{cfg['section_ui'].lower().replace(' ', '-')})"),
        ("- [Comparison & Community Examples](#comparison-community-examples)", f"- [{cfg['section_comparison']}](#{cfg['section_comparison'].lower().replace(' ', '-')})"),
        ("- [Acknowledge](#acknowledge)", f"- [{cfg['section_ack']}](#{cfg['section_ack'].lower().replace(' ', '-')})"),
    ]
    for old, new in menu_pairs:
        text = text.replace(old, new)

    section_pairs = [
        ("## Portrait & Photography Cases", f"## {cfg['section_portrait']}"),
        ("## Poster & Illustration Cases", f"## {cfg['section_poster']}"),
        ("## Character Design Cases", f"## {cfg['section_character']}"),
        ("## UI & Social Media Mockup Cases", f"## {cfg['section_ui']}"),
        ("## Comparison & Community Examples", f"## {cfg['section_comparison']}"),
        ("## Acknowledge", f"## {cfg['section_ack']}"),
    ]
    for old, new in section_pairs:
        text = text.replace(old, new)

    text = text.replace("| Output |", f"| {cfg['output']} |")
    text = text.replace('alt="Output image"', f'alt="{cfg["output_alt"]}"')
    text = text.replace("**Prompt:**", f"**{cfg['prompt']}：**")

    text = replace_once(text, "This repository was inspired by outstanding open prompt collections and community-shared GPT-Image-2 experiments.", cfg["ack_intro"])
    text = replace_once(text, "Thanks to the creators and contributors who shared their work publicly and made these case studies possible.", cfg["ack_thanks"])
    text = replace_once(text, "*We cannot guarantee that every case is attributed to the original creator. If anything needs to be corrected, please contact us and we will update it.*", cfg["ack_note"])
    text = replace_once(text, "If you have more interesting GPT-Image-2 prompt cases to share, feel free to reach out and help us expand the Evolink prompt library.", cfg["ack_more"])
    return text


def main() -> None:
    args = parse_args()
    base = README.read_text(encoding="utf-8")
    for cfg in LOCALES.values():
        rendered = build_locale(base, cfg)
        preserved = None
        if cfg["path"].exists() and not args.rewrite_protected_sections:
            current = cfg["path"].read_text(encoding="utf-8")
            rendered, preserved = preserve_protected_sections(rendered, current, cfg)
        if preserved is not None:
            verify_protected_sections_unchanged(rendered, preserved, cfg)
        cfg["path"].write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
