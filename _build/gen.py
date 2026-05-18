#!/usr/bin/env python3
"""One-off generator for FutureFlow sub-pages. Run from repo root: python3 _build/gen.py"""
import os, json, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- Shared chunks ----------
GFONTS = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://d8j0ntlcm91z4.cloudfront.net" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">'''

FAVICON = '''<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%234A86D8'/%3E%3Cstop offset='0.55' stop-color='%237C5CFF'/%3E%3Cstop offset='1' stop-color='%2300E5C7'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect x='7' y='7' width='18' height='18' rx='4' stroke='url(%23g)' stroke-width='2.4' fill='none'/%3E%3Cg stroke='url(%23g)' stroke-width='2' stroke-linecap='round'%3E%3Cline x1='12' y1='3' x2='12' y2='7'/%3E%3Cline x1='16' y1='3' x2='16' y2='7'/%3E%3Cline x1='20' y1='3' x2='20' y2='7'/%3E%3Cline x1='12' y1='25' x2='12' y2='29'/%3E%3Cline x1='16' y1='25' x2='16' y2='29'/%3E%3Cline x1='20' y1='25' x2='20' y2='29'/%3E%3Cline x1='3' y1='12' x2='7' y2='12'/%3E%3Cline x1='3' y1='16' x2='7' y2='16'/%3E%3Cline x1='3' y1='20' x2='7' y2='20'/%3E%3Cline x1='25' y1='12' x2='29' y2='12'/%3E%3Cline x1='25' y1='16' x2='29' y2='16'/%3E%3Cline x1='25' y1='20' x2='29' y2='20'/%3E%3C/g%3E%3C/svg%3E">'''

OG_DEFAULT = "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075056_b945567a-2797-4e82-a0ca-8d8bf54d3fce.png"

HEADER = '''<a href="#main" style="position:absolute;left:-9999px" onfocus="this.style.left='12px';this.style.top='12px';this.style.position='fixed';this.style.zIndex='9999';this.style.background='var(--bg-elev-1)';this.style.padding='10px 16px';this.style.border='1px solid var(--brand)';this.style.borderRadius='10px'">Перейти к контенту</a>

<header class="site-header">
  <div class="container nav">
    <a href="/" class="brand" aria-label="FutureFlow — на главную">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 32 32" fill="none">
          <rect x="7" y="7" width="18" height="18" rx="4" stroke="#fff" stroke-width="2.4"/>
          <g stroke="#fff" stroke-width="2" stroke-linecap="round">
            <line x1="12" y1="3" x2="12" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/><line x1="20" y1="3" x2="20" y2="7"/>
            <line x1="12" y1="25" x2="12" y2="29"/><line x1="16" y1="25" x2="16" y2="29"/><line x1="20" y1="25" x2="20" y2="29"/>
            <line x1="3" y1="12" x2="7" y2="12"/><line x1="3" y1="16" x2="7" y2="16"/><line x1="3" y1="20" x2="7" y2="20"/>
            <line x1="25" y1="12" x2="29" y2="12"/><line x1="25" y1="16" x2="29" y2="16"/><line x1="25" y1="20" x2="29" y2="20"/>
          </g>
        </svg>
      </span>
      FutureFlow
    </a>
    <nav class="nav-links" aria-label="Главное меню">
      <div class="nav-drop">
        <a href="/#services" class="nav-link" aria-haspopup="true">Услуги</a>
        <div class="nav-mega" role="menu">
          <div class="mega-grid">
            <a href="/services/ai-video/" class="mega-item"><span class="mega-ico">🎬</span><span class="mega-text"><span class="mega-title">AI / 3D генерация видео</span><span class="mega-desc">Higgsfield, Sora, Runway, Kling — ролики под ключ</span></span></a>
            <a href="/services/ai-agents/" class="mega-item"><span class="mega-ico">🤖</span><span class="mega-text"><span class="mega-title">AI-агенты и чат-боты</span><span class="mega-desc">Telegram, WhatsApp, сайт — GPT, Claude, YandexGPT</span></span></a>
            <a href="/services/voice-bots/" class="mega-item"><span class="mega-ico">🎙️</span><span class="mega-text"><span class="mega-title">Голосовые AI-боты и IVR</span><span class="mega-desc">SIP/VoIP, неотличимы от живого оператора</span></span></a>
            <a href="/services/web/" class="mega-item"><span class="mega-ico">🌐</span><span class="mega-text"><span class="mega-title">Разработка сайтов</span><span class="mega-desc">Лендинги, корпоративные, e-com, личные кабинеты</span></span></a>
            <a href="/services/seo/" class="mega-item"><span class="mega-ico">📈</span><span class="mega-text"><span class="mega-title">SEO и продвижение</span><span class="mega-desc">Топ Яндекс и Google, Дзен, контент-стратегия</span></span></a>
            <a href="/services/ads/" class="mega-item"><span class="mega-ico">🎯</span><span class="mega-text"><span class="mega-title">Контекстная реклама</span><span class="mega-desc">Яндекс Директ, Google Ads — снижаем CPL</span></span></a>
            <a href="/services/automation/" class="mega-item"><span class="mega-ico">⚡</span><span class="mega-text"><span class="mega-title">Автоматизация процессов</span><span class="mega-desc">Apps Script, API, Make / Zapier, RPA</span></span></a>
            <a href="/services/crm-bi/" class="mega-item"><span class="mega-ico">🔗</span><span class="mega-text"><span class="mega-title">CRM и BI-интеграции</span><span class="mega-desc">AmoCRM, Bitrix24, 1С, дашборды в реальном времени</span></span></a>
            <a href="/services/training/" class="mega-item"><span class="mega-ico">🧠</span><span class="mega-text"><span class="mega-title">AI-обучение персонала</span><span class="mega-desc">Симулятор переговоров и тренажёр продаж</span></span></a>
            <a href="/services/smm/" class="mega-item"><span class="mega-ico">📱</span><span class="mega-text"><span class="mega-title">SMM и AI-контент</span><span class="mega-desc">Ведение соцсетей, AI-генерация текста и медиа</span></span></a>
          </div>
        </div>
      </div>
      <a href="/cases/" class="nav-link">Кейсы</a>
      <a href="/industries/" class="nav-link">Отрасли</a>
      <a href="/about/" class="nav-link">О нас</a>
      <a href="/contacts/" class="nav-link">Контакты</a>
    </nav>
    <div class="nav-actions">
      <button class="theme-toggle" data-theme-toggle aria-label="Переключить тему" title="Светлая / тёмная тема">
        <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
        <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
      <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener" class="btn btn-primary btn-sm">Связаться</a>
      <button class="burger" data-drawer-open aria-label="Открыть меню"><span></span></button>
    </div>
  </div>
</header>

<div class="drawer" data-drawer aria-hidden="true">
  <div class="drawer-head">
    <a href="/" class="brand">
      <span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><rect x="7" y="7" width="18" height="18" rx="4" stroke="#fff" stroke-width="2.4"/></svg></span>
      FutureFlow
    </a>
    <button class="drawer-close" data-drawer-close aria-label="Закрыть меню">✕</button>
  </div>
  <div class="drawer-section">
    <div class="drawer-title">Услуги</div>
    <a href="/services/ai-video/" class="drawer-link">AI / 3D генерация видео</a>
    <a href="/services/ai-agents/" class="drawer-link">AI-агенты и чат-боты</a>
    <a href="/services/voice-bots/" class="drawer-link">Голосовые AI-боты</a>
    <a href="/services/web/" class="drawer-link">Разработка сайтов</a>
    <a href="/services/seo/" class="drawer-link">SEO-продвижение</a>
    <a href="/services/ads/" class="drawer-link">Контекстная реклама</a>
    <a href="/services/automation/" class="drawer-link">Автоматизация процессов</a>
    <a href="/services/crm-bi/" class="drawer-link">CRM и BI-интеграции</a>
    <a href="/services/training/" class="drawer-link">AI-обучение персонала</a>
    <a href="/services/smm/" class="drawer-link">SMM и контент</a>
  </div>
  <div class="drawer-section">
    <div class="drawer-title">Разделы</div>
    <a href="/cases/" class="drawer-link">Кейсы</a>
    <a href="/industries/" class="drawer-link">Отрасли</a>
    <a href="/about/" class="drawer-link">О компании</a>
    <a href="/contacts/" class="drawer-link">Контакты</a>
  </div>
  <div class="drawer-foot">
    <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener" class="btn btn-primary">Telegram</a>
    <a href="tel:+79259040111" class="btn btn-ghost">Позвонить</a>
  </div>
</div>'''

FOOTER = '''<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div class="foot-brand">
        <a href="/" class="brand">
          <span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none"><rect x="7" y="7" width="18" height="18" rx="4" stroke="#fff" stroke-width="2.4"/></svg></span>
          FutureFlow
        </a>
        <p>AI-агентство полного цикла. 3D-видео, AI-агенты, сайты, SEO, автоматизация и CRM. Делаем сложное — простым и измеримым.</p>
        <div class="foot-soc" style="margin-top:18px">
          <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener" title="Telegram">TG</a>
          <a href="https://wa.me/79661277767" target="_blank" rel="noopener" title="WhatsApp">WA</a>
          <a href="mailto:hello@futureflow.ru" title="Email">@</a>
        </div>
      </div>
      <div class="foot-col">
        <h4>Услуги</h4>
        <ul>
          <li><a href="/services/ai-video/">AI / 3D-видео</a></li>
          <li><a href="/services/ai-agents/">AI-агенты и чат-боты</a></li>
          <li><a href="/services/voice-bots/">Голосовые боты</a></li>
          <li><a href="/services/web/">Разработка сайтов</a></li>
          <li><a href="/services/seo/">SEO-продвижение</a></li>
          <li><a href="/services/ads/">Контекстная реклама</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h4>Ещё услуги</h4>
        <ul>
          <li><a href="/services/automation/">Автоматизация</a></li>
          <li><a href="/services/crm-bi/">CRM и BI</a></li>
          <li><a href="/services/training/">AI-обучение</a></li>
          <li><a href="/services/smm/">SMM и контент</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h4>Компания</h4>
        <ul>
          <li><a href="/cases/">Кейсы</a></li>
          <li><a href="/industries/">Отрасли</a></li>
          <li><a href="/about/">О нас</a></li>
          <li><a href="/contacts/">Контакты</a></li>
          <li><a href="/careers/">Вакансии</a></li>
        </ul>
      </div>
      <div class="foot-col">
        <h4>Контакты</h4>
        <ul>
          <li><a href="tel:+79259040111">+7 925 904-01-11</a></li>
          <li><a href="mailto:hello@futureflow.ru">hello@futureflow.ru</a></li>
          <li><a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener">@FutureFlowInc</a></li>
          <li><a href="https://wa.me/79661277767" target="_blank" rel="noopener">+7 966 127-77-67</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <p>© <span data-year>2026</span> FutureFlow · ИП Зайдель Адриан Патрик · Все права защищены</p>
      <p>
        <a href="/legal/privacy/">Политика обработки данных</a> ·
        <a href="/legal/terms/">Пользовательское соглашение</a>
      </p>
    </div>
  </div>
</footer>

<script src="/assets/js/site.js" defer></script>'''


CTA_BLOCK = '''<section class="section">
  <div class="container">
    <div class="cta-block rv">
      <h2>Обсудим вашу <span class="grad-text">задачу?</span></h2>
      <p>Опишите задачу удобным способом — пришлём смету и план за 1 рабочий день. Никаких форм с обязательным сбором данных: вы выбираете канал связи сами.</p>
      <div class="cta-ctas">
        <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener" class="btn btn-primary btn-arrow">Написать в Telegram</a>
        <a href="https://wa.me/79661277767" target="_blank" rel="noopener" class="btn btn-ghost">WhatsApp</a>
        <a href="mailto:hello@futureflow.ru" class="btn btn-ghost">Email</a>
        <a href="tel:+79259040111" class="btn btn-ghost">Позвонить</a>
      </div>
      <div class="cta-contacts">
        <a class="cc-item" href="tel:+79259040111"><span class="cc-lbl">Телефон</span><span class="cc-val">+7 925 904-01-11</span></a>
        <a class="cc-item" href="mailto:hello@futureflow.ru"><span class="cc-lbl">Email</span><span class="cc-val">hello@futureflow.ru</span></a>
        <a class="cc-item" href="https://t.me/FutureFlowInc" target="_blank" rel="noopener"><span class="cc-lbl">Telegram</span><span class="cc-val">@FutureFlowInc</span></a>
        <a class="cc-item" href="https://wa.me/79661277767" target="_blank" rel="noopener"><span class="cc-lbl">WhatsApp</span><span class="cc-val">+7 966 127-77-67</span></a>
      </div>
    </div>
  </div>
</section>'''


CRUMB_LABELS = {
    "services":"Услуги","ai-video":"AI / 3D-видео","ai-agents":"AI-агенты","voice-bots":"Голосовые боты",
    "web":"Разработка сайтов","seo":"SEO","ads":"Реклама","automation":"Автоматизация",
    "crm-bi":"CRM и BI","training":"AI-обучение","smm":"SMM",
    "cases":"Кейсы","industries":"Отрасли","about":"О компании","contacts":"Контакты",
    "careers":"Вакансии","legal":"Правовая информация","privacy":"Политика данных","terms":"Соглашение",
}

def page(title, description, url_path, body, og_image=OG_DEFAULT, extra_ld=None, keywords=""):
    """Render a full page. url_path is like '/services/ai-video/'."""
    canonical = f"https://futureflow.ru{url_path}"
    ld = []
    # Breadcrumb
    parts = [p for p in url_path.split('/') if p]
    crumb_items = [{"@type":"ListItem","position":1,"name":"Главная","item":"https://futureflow.ru/"}]
    acc = ""
    for i, p in enumerate(parts):
        acc += "/" + p
        crumb_items.append({"@type":"ListItem","position":i+2,"name": CRUMB_LABELS.get(p, p), "item": f"https://futureflow.ru{acc}/"})
    ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":crumb_items})
    if extra_ld:
        if isinstance(extra_ld, list):
            ld.extend(extra_ld)
        else:
            ld.append(extra_ld)
    ld_scripts = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    kw = f'<meta name="keywords" content="{html.escape(keywords)}">' if keywords else ""

    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
{kw}
<meta name="author" content="ИП Зайдель Адриан Патрик">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta name="theme-color" content="#06060F">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="ru" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="FutureFlow">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:image" content="{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="675">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(description)}">
<meta name="twitter:image" content="{og_image}">
{FAVICON}
{GFONTS}
{ld_scripts}
</head>
<body>
{HEADER}
<main id="main">
{body}
{CTA_BLOCK}
</main>
{FOOTER}
</body>
</html>'''


def crumbs(items):
    """items = [(href|None, label)]; last has aria-current."""
    out = ['<nav class="crumbs container" aria-label="Хлебные крошки">']
    for i, (href, label) in enumerate(items):
        if i:
            out.append('<span class="sep">›</span>')
        if href:
            out.append(f'<a href="{href}">{html.escape(label)}</a>')
        else:
            out.append(f'<span aria-current="page">{html.escape(label)}</span>')
    out.append('</nav>')
    return "\n".join(out)


def faq_block(title, items):
    """items = [(q, a_html)]. Returns (html, JSON-LD object)."""
    details = []
    qs = []
    for q, a in items:
        details.append(f'<details><summary>{html.escape(q)}</summary><div class="faq-a">{a}</div></details>')
        qs.append({"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text": re.sub(r"<[^>]+>", "", a)}})
    html_out = f'''<section class="section">
  <div class="container">
    <div class="section-head rv"><span class="eyebrow">FAQ</span><h2>{html.escape(title)}</h2></div>
    <div class="faq rv">
{chr(10).join(details)}
    </div>
  </div>
</section>'''
    ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity": qs}
    return html_out, ld


def service_ld(name, description, url, image=None):
    o = {
        "@context":"https://schema.org",
        "@type":"Service",
        "name": name,
        "description": description,
        "url": url,
        "provider": {"@type":"Organization","name":"FutureFlow","url":"https://futureflow.ru/"},
        "areaServed": {"@type":"Country","name":"Россия"}
    }
    if image:
        o["image"] = image
    return o


# ========================================
# SERVICES DATA
# ========================================
SERVICES = [
    {
        "slug": "ai-video",
        "title": "AI и 3D генерация видео — продакшн под ключ | FutureFlow",
        "h1": "AI и 3D генерация видео под ключ",
        "tagline": "Higgsfield · Sora · Runway · Kling · Veo",
        "description": "Заказать AI и 3D-видео под ключ. Производство рекламных роликов, продуктовых видео, аватаров, motion-графики на Higgsfield, Sora, Runway, Kling. Сценарий, генерация, монтаж и озвучка.",
        "keywords": "ai видео генерация, 3d видео генерация, заказать ai видео, higgsfield, sora, runway, kling, veo, ai motion дизайн, нейросеть видео, ai ролик",
        "lead": "От идеи до готового ролика — на нейросетях нового поколения. Делаем рекламные креативы, продуктовые видео, motion-графику, виртуальных аватаров и 3D-сцены в 5–10 раз быстрее и дешевле классической съёмки.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075059_a8c2f865-d746-429f-89c8-b20f3947ae8f.png",
        "includes": [
            ("🎬 Рекламные ролики", "Креативы для VK, Reels, Shorts, Stories — 5–30 секунд под конкретный оффер и аудиторию."),
            ("📦 Продуктовые видео", "Презентация товара или услуги с анимацией интерфейса, обзор фич, демо-сценарии."),
            ("👤 Виртуальные аватары и speakers", "Цифровые ведущие на 46+ языках для обучающих видео, новостей, объяснений."),
            ("✨ Motion и 3D-графика", "Анимированные логотипы, инфографика, переходы, заставки, шейдеры."),
            ("🎙️ Озвучка и саундтрек", "Голос диктора (TTS), музыка под лицензией, звуковой дизайн."),
            ("🎞️ Монтаж и постпродакшн", "Цветокоррекция, субтитры, адаптации под форматы и платформы, мастеринг."),
            ("📑 Юридическая чистота", "Контроль авторских прав на музыку и шрифты, отсутствие защищённых ТМ и образов в кадре."),
        ],
        "tech": ["Higgsfield","Sora","Runway","Kling","Veo","Pika","Nano Banana","Midjourney","Flux","ElevenLabs","SpeechKit","DaVinci","After Effects"],
        "faq": [
            ("Сколько времени занимает один ролик?", "Простой ролик 6–15 секунд — 1–2 дня. Сложный с уникальной 3D-сценой и сценарием — до 7 дней. Партии до 30 роликов делаем за неделю при шаблонной структуре."),
            ("В каких форматах сдаёте?", "MP4 / H.264 / H.265 для большинства платформ, WebM для веба, MOV ProRes для дальнейшего монтажа. Разрешение до 4K, частота до 60 fps. Аспекты 9:16, 1:1, 16:9, 21:9, 4:5 — под любую площадку."),
            ("Можно использовать референс или брендбук?", "Да. Передаём в модель ваш стайлгайд, палитру, типографику, логотип, шрифты. Можем обучить кастомный LoRA-стайл под бренд."),
            ("Получим ли мы исходники?", "Да: исходники проекта (After Effects / DaVinci), отдельные слои, превью разных длительностей, лицензии на музыку."),
            ("Что с авторскими правами?", "Все материалы выпускаются с лицензией для коммерческого использования, бренд получает права на использование без ограничений по медиа-каналам и регионам."),
            ("Сколько стоит?", "Простой ролик от 8 000 ₽, средний от 25 000 ₽, кастомный с 3D — от 60 000 ₽. Пакетные тарифы на 10/30/60 роликов с большой скидкой."),
        ]
    },
    {
        "slug": "ai-agents",
        "title": "AI-агенты и чат-боты для бизнеса под ключ | FutureFlow",
        "h1": "AI-агенты и чат-боты",
        "tagline": "OpenAI GPT · Claude · YandexGPT · RAG",
        "description": "Разработка AI-агентов и чат-ботов для Telegram, WhatsApp и сайта. GPT, Claude, YandexGPT, GigaChat. Знание базы клиента (RAG), интеграция с CRM, аналитика диалогов.",
        "keywords": "ai агент, чат бот, чат-бот telegram, whatsapp бот, gpt бот, бот для бизнеса, разработка ботов, rag бот, ai ассистент",
        "lead": "Делаем AI-агентов, которые реально работают: продают, поддерживают, квалифицируют лиды, помогают сотрудникам. Не «бот по сценарию», а умный ассистент со знанием вашей базы и понимаем контекста переписки.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075102_731a44e9-9fdf-406c-8cf3-64ecbdcbe6f0.png",
        "includes": [
            ("💬 Боты в Telegram, WhatsApp, на сайте", "Универсальный AI-агент во всех каналах, единая история переписки в CRM."),
            ("📚 Знание базы клиента (RAG)", "Загружаем PDF, базу знаний, прайсы, документы — бот отвечает по реальным данным, а не «галлюцинациям»."),
            ("🧩 Интеграции с CRM и сервисами", "AmoCRM, Bitrix24, 1С, IDENT, YClients, Sheets — бот создаёт сделки, обновляет статусы, бронирует время."),
            ("🛡️ Передача оператору", "Бот понимает, когда нужен человек, и плавно передаёт диалог с полным контекстом."),
            ("📊 Аналитика и dashboards", "Метрики: % автоответов, длительность диалога, NPS, темы обращений. Алерты по аномалиям."),
            ("🌐 Многоязычность", "GPT и Claude поддерживают 46+ языков — открываем международные рынки одним проектом."),
            ("🔒 Безопасность данных", "Маскирование персональных данных, журнал, опционально self-hosted LLM (Llama / Mistral / GigaChat)."),
        ],
        "tech": ["OpenAI GPT","Claude (Anthropic)","YandexGPT","GigaChat","Gemini","Llama","Mistral","LangChain","LlamaIndex","Pinecone","Qdrant","Telegram Bot API","WhatsApp Business","AmoCRM","Bitrix24"],
        "faq": [
            ("Чем AI-агент отличается от классического чат-бота?", "Классический бот работает по жёсткому сценарию (кнопкам), AI-агент — понимает любые формулировки, ведёт свободный диалог, использует базу знаний и принимает решения."),
            ("Бот будет «галлюцинировать»?", "Нет, если правильно настроить. Используем RAG (Retrieval-Augmented Generation): бот сначала ищет ответ в реальной базе, потом формулирует. Для критичных тем (цены, юридические) — строгие шаблоны без свободной генерации."),
            ("Что если бот не знает ответ?", "Передаёт оператору в указанные часы / в нужный канал с полным контекстом, в нерабочее время — фиксирует запрос и обещает связаться."),
            ("Сколько стоит запуск?", "Простой бот — от 80 000 ₽, бот со знанием базы и интеграциями — от 180 000 ₽, корпоративный AI-агент — от 400 000 ₽. Ежемесячно — стоимость API LLM (от 3 000 ₽/мес для среднего проекта)."),
            ("Сколько занимает запуск?", "Прототип за 1–2 недели, прод за 3–6 недель. Опционально — поддержка и развитие после запуска."),
            ("Работает ли с российскими LLM?", "Да. YandexGPT, GigaChat, Cotype, T-Pro, RuAdapt — для проектов с требованиями к локализации данных."),
        ]
    },
    {
        "slug": "voice-bots",
        "title": "Голосовые AI-боты и IVR для бизнеса | FutureFlow",
        "h1": "Голосовые AI-боты и IVR",
        "tagline": "SpeechKit · Whisper · SIP / VoIP · Mango",
        "description": "Заказать голосового AI-бота с SIP-интеграцией. Голос почти неотличим от живого. Приём и обзвоны, запись на услуги, поддержка 24/7. ElevenLabs, SpeechKit, Whisper.",
        "keywords": "голосовой бот, ai голосовой ассистент, ivr бот, голосовой бот заказать, voicebot, голосовая нейросеть, ai робот звонки, обзвон ботом",
        "lead": "Делаем голосовых AI-ассистентов, голос которых клиенты не отличают от живого оператора. Принимаем входящие звонки, делаем исходящие обзвоны, отвечаем на вопросы, записываем на услуги — 24/7 и без перерывов на обед.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075105_7d07a17a-6ba1-4a5f-9b28-d8a1822e8e02.png",
        "includes": [
            ("📞 Приём входящих звонков", "Бот отвечает мгновенно, проводит первичную консультацию, переключает на нужного оператора."),
            ("📲 Исходящие обзвоны", "Подтверждение записей, информирование клиентов, опросы NPS, реактивация спящей базы."),
            ("📅 Запись на услуги", "Подбор времени, проверка свободных слотов, занесение в CRM или систему записи."),
            ("🧠 Контекстные диалоги", "Бот помнит, что сказал клиент 30 секунд назад, переспрашивает, уточняет, не уходит в петлю."),
            ("🎚️ Подмена голоса под бренд", "ElevenLabs / собственный TTS — настраиваем тембр, скорость, эмоциональность."),
            ("🔗 SIP / VoIP интеграция", "Mango Office, UIS, Sipuni, Asterisk, FreePBX — подключаем к вашей телефонии."),
            ("📈 Аналитика звонков", "Транскрипция, оценка эмоций, теги тем, дашборд для руководителя, алерты."),
        ],
        "tech": ["SpeechKit (Yandex)","Whisper","ElevenLabs","Google TTS","Azure Speech","Mango ВАТС","UIS","Sipuni","Asterisk","FreePBX","Twilio","OpenAI GPT","Claude","SIP / VoIP"],
        "faq": [
            ("Клиенты точно не поймут, что это бот?", "В большинстве случаев — нет. Используем латентность ниже 800 мс, прерывание (barge-in), естественные паузы, эмоции. По закону «О рекламе» при холодных звонках обязаны представиться как робот — это делаем."),
            ("На каких языках работает?", "Русский, английский, испанский, немецкий, китайский, арабский, казахский и ещё 40+ языков. С разными акцентами и диалектами."),
            ("Какие задачи лучше всего автоматизировать?", "Запись/перенос/отмена визитов, FAQ-консультации, подтверждение заявок, информирование, опросы, лидогенерация по холодной базе, ретеншн."),
            ("Сколько стоит и от чего зависит?", "Запуск под ключ — от 250 000 ₽. Месячная стоимость — телефония + SaaS LLM (от 8 000 ₽/мес для 1000 минут). При большом объёме звонков выгоднее self-hosted."),
            ("Что с законом и согласием на запись?", "Перед стартом разговора предупреждаем о записи, делаем согласие записанным (юридически — конклюдентным). Все записи хранятся в защищённом облаке."),
            ("Можно подключить к существующей АТС?", "Да. Подключаемся по SIP-trunk, веб-хукам или API — без замены ваших номеров и оборудования."),
        ]
    },
    {
        "slug": "web",
        "title": "Разработка сайтов под ключ: лендинги, корпоративные, e-com | FutureFlow",
        "h1": "Разработка сайтов",
        "tagline": "React · Next.js · Node.js · WordPress · Tilda",
        "description": "Заказать разработку сайта: лендинг, корпоративный, e-commerce, личный кабинет. Современный дизайн, быстрая загрузка, адаптив, SEO-готовность. React, Next.js, WordPress.",
        "keywords": "разработка сайтов, заказать сайт, лендинг под ключ, корпоративный сайт, интернет-магазин, react next.js, wordpress, веб-разработка, создание сайта",
        "lead": "Создаём сайты, которые продают и быстро запускаются. Лендинги, корпоративные порталы, e-commerce, личные кабинеты и сложные SaaS — на современном стеке с заботой о скорости, SEO и удобстве.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075109_b020cc9e-5be8-4547-9af5-75401d3a5b01.png",
        "includes": [
            ("🚀 Лендинги и промо-сайты", "Одностраничники под товар или услугу с фокусом на конверсию. От 7 дней."),
            ("🏢 Корпоративные сайты", "Многостраничные сайты с каталогом услуг, новостями, кейсами, командой, отраслевыми лендингами."),
            ("🛒 Интернет-магазины", "Каталог, корзина, оплата, личный кабинет, интеграция с 1С, CDEK, Boxberry, СБП, ЮKassa, Robokassa."),
            ("🔐 Личные кабинеты и SaaS", "Авторизация, ролевая модель, дашборды, API, биллинг, мультитенантность."),
            ("⚡ Скорость и Core Web Vitals", "LCP < 2.5s, CLS < 0.1, оптимизация изображений, кеш CDN, лучшие практики Lighthouse."),
            ("🔎 SEO и Schema.org", "Семантическая разметка, Open Graph, Twitter Cards, JSON-LD, корректная hreflang."),
            ("📱 Адаптив и доступность", "Сайт удобен на любых экранах, проходит WCAG AA, поддерживает скринридеры."),
        ],
        "tech": ["React","Next.js","Vue.js","Nuxt","Astro","Svelte","Node.js","Express","NestJS","WordPress","WooCommerce","1С-Битрикс","Tilda","Webflow","PostgreSQL","MongoDB"],
        "faq": [
            ("Какой движок выбрать — React/Next или WordPress/Tilda?", "Зависит от задачи. Tilda — для одностраничника за 7 дней без программистов. WordPress — для контентного сайта с регулярными правками. Next.js — для маркетингового сайта с фокусом на скорость и SEO. Кастомный фуллстек — для SaaS, e-com со сложной логикой, личного кабинета."),
            ("Сколько стоит?", "Лендинг от 80 000 ₽, корпоративный сайт от 200 000 ₽, e-com от 350 000 ₽, SaaS — от 600 000 ₽. Точная смета — после брифа."),
            ("Сколько занимает?", "Лендинг — 7–14 дней. Корпоративный — 3–6 недель. E-com — 6–12 недель. SaaS — от 2 месяцев."),
            ("Хостинг и поддержка — кто делает?", "Можем взять на себя или передать вашему DevOps. Хостинг — Yandex Cloud, Selectel, Reg.ru, VK Cloud. SLA-поддержка с гарантией времени реакции."),
            ("А переделать существующий сайт?", "Да. Делаем редизайн без простоя: пилим новую версию рядом, переключаем по готовности. Сохраняем SEO-позиции через корректные 301-редиректы."),
            ("Сайт собирает персональные данные?", "По умолчанию делаем сайт без обязательных форм с ПДн — только кнопки в мессенджеры/email. Если форма нужна — оформляем как оператор ПДн с уведомлением Роскомнадзора и SSL/защитой данных."),
        ]
    },
    {
        "slug": "seo",
        "title": "SEO продвижение сайтов в Яндекс и Google под ключ | FutureFlow",
        "h1": "SEO-продвижение в Яндекс и Google",
        "tagline": "Яндекс · Google · Дзен · YMYL · GEO",
        "description": "SEO продвижение сайтов в Яндекс и Google под ключ. Технический аудит, семантика, контент-стратегия, ссылки, Дзен. SEO для YMYL, e-commerce, локального бизнеса.",
        "keywords": "seo продвижение, seo сайта, продвижение в яндексе, продвижение в google, поисковая оптимизация, технический seo, контент маркетинг, ссылочное продвижение",
        "lead": "Выводим сайты в ТОП-10 Яндекса и Google по коммерческим и информационным запросам. Работаем по KPI: позиции, трафик, заявки. Никаких «накруток» — только белые методы и качественный контент.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075112_46e4f828-fcc6-41c5-b2d3-6e860e4f88c5.png",
        "includes": [
            ("🔍 Технический SEO-аудит", "Сканирование Screaming Frog, проверка скорости, robots, sitemap, canonical, дублей, JS-рендеринга."),
            ("🧠 Семантика и кластеризация", "Сбор ядра через Key Collector / Wordstat / Ahrefs, кластеризация, распределение по страницам."),
            ("✍️ Контент-маркетинг и LSI", "Тексты от копирайтеров с экспертизой в нише, AI-расширение контента, оптимизация под LSI и YMYL."),
            ("🔗 Ссылочное продвижение", "Крауд, аутрич, гостевые посты, статьи-доноры. Только белые методы — без рисков под фильтр."),
            ("📰 Яндекс Дзен и платформы", "Каналы в Дзен, VC, Habr, Pikabu, Reddit — приводят трафик и поднимают авторитет домена."),
            ("📍 Локальное SEO и GEO", "Яндекс Карты, Google Maps, 2ГИС, региональные подкатегории."),
            ("📊 Аналитика и отчётность", "Метрика, GA4, GSC, Ahrefs, ежемесячный отчёт по позициям, трафику и заявкам."),
        ],
        "tech": ["Яндекс Вебмастер","Google Search Console","Яндекс Метрика","Google Analytics 4","Ahrefs","SE Ranking","SemRush","Screaming Frog","Key Collector","Pixel Tools","Topvisor","SimilarWeb"],
        "faq": [
            ("Как быстро виден результат?", "Первые движения по позициям — через 2–3 месяца, рост трафика — 4–6 месяцев, выход в ТОП-10 по конкурентным запросам — 6–12 месяцев. Молодые сайты — дольше. Долгосрочно SEO — самый дешёвый канал."),
            ("Даёте гарантии по позициям?", "Гарантируем выполнение работ по плану и движение по KPI (трафик, лиды). Конкретные позиции в выдаче никто честно гарантировать не может — алгоритмы меняются. Если кто-то обещает «ТОП-10 за месяц», это, скорее всего, накрутки или серые методы."),
            ("Сколько стоит?", "Стартовый аудит и стратегия — от 60 000 ₽ разово. Ежемесячное продвижение — от 80 000 ₽/мес для малого сайта, от 150 000 ₽/мес для среднего, от 250 000 ₽/мес для e-commerce."),
            ("Под Яндекс или под Google?", "Под оба сразу — в 90% случаев работы общие, отличия минимальны. Если нужна узкая специализация (например, только Google для зарубежных рынков) — обсуждаем отдельно."),
            ("Работаете с YMYL (медицина, финансы, юр.)?", "Да. Понимаем требования к E-E-A-T: автор статьи, ссылки на источники, реквизиты, лицензии, рецензии экспертов. Это даже строже в Яндексе через ИКС."),
            ("Можете писать контент сами?", "Да, у нас команда копирайтеров со специализацией в IT, медицине, юриспруденции, финансах, e-com, EdTech. Используем AI как помощника, но финальный контент — рукой эксперта."),
        ]
    },
    {
        "slug": "ads",
        "title": "Контекстная реклама: Яндекс Директ, Google Ads, ВК | FutureFlow",
        "h1": "Контекстная реклама",
        "tagline": "Яндекс Директ · Google Ads · ВК Реклама · ROAS",
        "description": "Настройка и ведение контекстной рекламы: Яндекс Директ, Google Ads, ВК Реклама. Снижаем CPL, поднимаем ROAS, работаем со сквозной аналитикой и автоматизацией ставок.",
        "keywords": "контекстная реклама, яндекс директ, google ads, вк реклама, ppc, настройка рекламы, агентство контекстной рекламы, снижение cpl, roas",
        "lead": "Настраиваем и ведём контекстную рекламу с прозрачным KPI и сквозной аналитикой. Не сливаем бюджет на нерелевантные клики — управляем стратегиями, ставками и аудиториями ежедневно.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075335_033c7d3a-9cf1-4ca3-97a8-49c72e708b61.png",
        "includes": [
            ("🎯 Стратегия и медиа-план", "Анализ конкурентов, выбор каналов и форматов, прогноз CPL и трафика."),
            ("🔧 Настройка и запуск", "Кампании в Яндекс Директ, Google Ads, VK Ads, MyTarget — поиск, РСЯ, КМС, ретаргет, динамические объявления."),
            ("📊 Сквозная аналитика", "Связка Метрики, GA4 и CRM. Видим путь от клика до сделки и LTV клиента."),
            ("🤖 Автостратегии и AI", "Мастер кампаний, Performance Max, Smart Bidding, кастомные оптимизаторы конверсий."),
            ("🎨 Креативы и A/B-тесты", "Тексты, баннеры, видео (в т.ч. AI-генерация на Higgsfield). Регулярные тесты гипотез."),
            ("🛡️ Защита от скликивания", "Antibot, чёрные списки IP, рефералов, операторов мобильной сети."),
            ("📈 Отчётность по KPI", "Еженедельный/ежемесячный отчёт: CPL, CR, ROAS, ROMI, LTV. Понятно собственнику бизнеса."),
        ],
        "tech": ["Яндекс Директ","Google Ads","VK Реклама","myTarget","TikTok Ads","Метрика","GA4","Roistat","K50","Calltouch","CoMagic","Marquiz","TargetHunter"],
        "faq": [
            ("Какой минимальный бюджет на контекст?", "Для теста ниши хватит 50 000 ₽ медиа-бюджета + 30 000 ₽ на настройку. Для стабильного потока заявок — от 100 000 ₽ медиа-бюджета в месяц."),
            ("Сколько стоит ведение?", "От 30 000 ₽/мес для малого бюджета, от 60 000 ₽/мес для среднего, % от оборота для крупных кампаний. Без скрытых наценок и накруток."),
            ("Как быстро будут заявки?", "Первые заявки — в день запуска. Стабильный поток с оптимальным CPL — обычно через 2–3 недели после прохождения стадии обучения автостратегий."),
            ("Что со сквозной аналитикой и атрибуцией?", "Настраиваем модель атрибуции (last-click / data-driven), связываем рекламу с CRM. Видим стоимость не клика, а реальной сделки и LTV."),
            ("Гарантируете заявки?", "Гарантируем выполнение KPI по верхней воронке (CTR, CPC, CR на сайте). Конверсия в продажу зависит от качества посадочной и работы отдела продаж — но мы и тут даём рекомендации."),
            ("Работаете с маркировкой ОРД?", "Да. Все креативы маркируем токенами через ОРД (operator рекламных данных) согласно 38-ФЗ. У клиента не возникает рисков по штрафам."),
        ]
    },
    {
        "slug": "automation",
        "title": "Автоматизация бизнес-процессов: Apps Script, Make, n8n | FutureFlow",
        "h1": "Автоматизация процессов",
        "tagline": "Apps Script · REST API · Make · n8n · RPA",
        "description": "Автоматизация бизнес-процессов под ключ: Apps Script, REST API, Make, Zapier, n8n, RPA. Уберём ручной труд, синхронизируем CRM, рекламу, документы, табели, складские системы.",
        "keywords": "автоматизация бизнеса, автоматизация процессов, apps script, make integromat, zapier, n8n, rpa, интеграция систем, автоматизация crm",
        "lead": "Уберём ручной труд из ваших процессов: синхронизация CRM, выгрузки в Google Sheets, отчёты, обновление цен, документооборот, табели сотрудников. Собираем экосистему из ваших инструментов без переплат за единую большую платформу.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075321_e9158e9e-ab9a-4b7c-898c-42d442249702.png",
        "includes": [
            ("🔄 Синхронизация систем", "CRM ↔ 1С ↔ маркетплейсы ↔ телефония ↔ email — единый источник правды без двойного ввода."),
            ("📥 Автоматический сбор данных", "Парсинг сайтов конкурентов, маркетплейсов, выгрузки из рекламных кабинетов, банков."),
            ("📤 Генерация документов", "Договоры, акты, счета, КП — из шаблонов с подстановкой данных из CRM. Подписи через КЭП."),
            ("📲 Уведомления и алерты", "Telegram-уведомления о событиях: новый лид, просроченная задача, аномалия в продажах."),
            ("🗂️ Документооборот", "Электронные акты, ОС, согласования. Интеграция с Контур.Диадок, СБИС."),
            ("🤖 RPA для legacy-систем", "Если у системы нет API — автоматизируем через эмуляцию пользователя (UiPath, RoboCorp)."),
            ("📅 Планирование и таски", "Автосоздание задач, напоминания, эскалации, ритейн на свободные слоты."),
        ],
        "tech": ["Google Apps Script","REST API","GraphQL","Webhooks","Make (Integromat)","Zapier","n8n","Albato","ApiX-Drive","Power Automate","UiPath","RoboCorp","Python","Node.js"],
        "faq": [
            ("С чего начать автоматизацию?", "С самого «больного» процесса: который занимает больше часов в неделю, чаще всего ломается или приводит к ошибкам. Сделаем экспресс-аудит и подскажем приоритеты."),
            ("Сколько стоит?", "Простая интеграция (например, AmoCRM ↔ Sheets ↔ Telegram) — от 30 000 ₽. Сложная мультисистемная — от 150 000 ₽. Ежемесячно — только подписки сервисов (Make/n8n) и поддержка."),
            ("Что если API нет?", "Используем парсинг, RPA (эмуляция действий пользователя), email-парсинг, либо разрабатываем плагин/расширение. Решаем любую задачу."),
            ("Это надёжно? Что если сломается?", "Делаем мониторинг и алертинг — узнаем о падении быстрее вас. Логирование, ретраи, очереди. SLA на исправление."),
            ("Можно сделать через no-code?", "Да, если процесс простой. Для сложных или высоконагруженных лучше Apps Script / Python — дешевле и стабильнее в долгосрочной перспективе."),
            ("А безопасность?", "Данные не покидают вашу инфраструктуру без необходимости. Используем секреты, токены с минимальными правами, шифрование. Аудит доступов."),
        ]
    },
    {
        "slug": "crm-bi",
        "title": "Внедрение CRM и BI-аналитики: AmoCRM, Bitrix24, 1С | FutureFlow",
        "h1": "CRM и BI-интеграции",
        "tagline": "AmoCRM · Bitrix24 · 1С · ETL · Dashboards",
        "description": "Внедрение CRM и настройка BI-аналитики под ключ. AmoCRM, Bitrix24, 1С, Google Sheets, Notion. Дашборды в реальном времени, сквозная аналитика, ETL, прогнозы.",
        "keywords": "внедрение crm, amocrm, bitrix24, 1с интеграция, bi аналитика, сквозная аналитика, дашборд, etl, datalens, power bi, tableau",
        "lead": "Внедряем и кастомизируем CRM, связываем их с источниками данных, строим BI-дашборды, по которым реально принимают решения. От «как у всех» к «как нам нужно для нашей бизнес-модели».",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075325_9420818d-e477-4eb5-81da-d336af58f1af.png",
        "includes": [
            ("📞 Внедрение CRM", "AmoCRM, Bitrix24 или собственный кастом. Воронки, поля, права доступа, виджеты."),
            ("🔌 Интеграции", "Сайт, лендинги, телефония, email, маркетплейсы, 1С, мессенджеры — все источники лидов в одной CRM."),
            ("📊 BI-дашборды", "DataLens, Power BI, Tableau, Metabase. Дашборды для руководства, продажников, маркетинга."),
            ("🔁 ETL и хранилище", "ClickHouse / PostgreSQL / BigQuery + Airflow / dbt — собираем данные из десятков систем в одно место."),
            ("📈 Сквозная аналитика", "Reklama → клик → лид → сделка → LTV. Реальный ROI каждого канала и креатива."),
            ("🤖 AI-аналитика", "Предсказание оттока, рекомендации товаров, скоринг лидов, выявление аномалий."),
            ("👥 Обучение команды", "Документация, видео-инструкции, очное обучение, поддержка после внедрения."),
        ],
        "tech": ["AmoCRM","Bitrix24","1С","HubSpot","Notion","Google Sheets","Yandex DataLens","Power BI","Tableau","Metabase","ClickHouse","PostgreSQL","BigQuery","Airflow","dbt"],
        "faq": [
            ("Какую CRM выбрать?", "AmoCRM — для продажников, кому важна простота и фокус на сделках. Bitrix24 — для компаний, где CRM + задачи + документы + связь в одном окне. 1С — если уже есть. Кастом — если уникальная бизнес-логика."),
            ("Сколько стоит внедрение?", "Базовое (CRM + 2-3 интеграции + обучение) — от 120 000 ₽. Среднее (CRM + BI + телефония + аналитика) — от 250 000 ₽. Сложное с кастомом и ETL — от 600 000 ₽."),
            ("Уже есть CRM, но в ней бардак. Что делать?", "Делаем аудит, чистим дубли, перепроектируем воронки и поля. Часто после такой «чистки» CRM начинает работать как новая, без замены."),
            ("Как часто обновляются данные на дашборде?", "Реальное время (для критичных метрик) или раз в 5–15 минут (для остальных). Зависит от системы-источника и нагрузки."),
            ("Будет ли всё работать после ухода ваших специалистов?", "Да. Документируем всё, обучаем команду, передаём пароли и доступы. Готовы оставаться на саппорте, но не привязываем."),
            ("Сквозная аналитика — это сложно/дорого?", "Нет, если делать прагматично. Минимальный сетап с одной CRM + Метрикой + парой источников — за 2 недели, под 80 000 ₽."),
        ]
    },
    {
        "slug": "training",
        "title": "AI-обучение сотрудников: тренажёр продаж и переговоров | FutureFlow",
        "h1": "AI-обучение персонала",
        "tagline": "GPT · TTS · 46 языков · LMS",
        "description": "AI-тренажёр продаж и переговоров на ИИ. Менеджеры отрабатывают возражения с виртуальным клиентом 24/7, получают разбор и оценку. Снижение срока адаптации в 2-3 раза.",
        "keywords": "тренажёр продаж, ai обучение, симулятор переговоров, обучение менеджеров, lms, корпоративное обучение, ai тренажёр, обучение операторов",
        "lead": "AI-симулятор клиента, на котором отрабатывают навыки операторы колл-центров, продавцы, рекрутёры, врачи. 24/7, на 46 языках, с автоматической оценкой и разбором ошибок. Срок адаптации новичка сокращается в 2-3 раза.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075338_d690fdce-d2ef-4e48-b813-13a75acf9e0c.png",
        "includes": [
            ("🎭 Виртуальный клиент", "AI имитирует разных типов клиентов: спокойного, агрессивного, торгующегося, технически подкованного, недоверчивого."),
            ("🎙️ Голос или текст", "Тренировка в чате или в реальном звонке через гарнитуру — как удобнее обучаемому."),
            ("📋 Сценарии из вашей жизни", "Грузим ваши скрипты, базу возражений, продуктовые знания — бот «говорит» как реальный покупатель вашей ниши."),
            ("📊 Автоматическая оценка", "AI оценивает по 20+ критериям: следование скрипту, работа с возражениями, обработка эмоций, закрытие."),
            ("🎓 Разбор полётов", "После каждой сессии — расшифровка диалога, подсветка ошибок, конкретные рекомендации."),
            ("🏆 Геймификация и рейтинги", "Уровни, бейджи, командные рейтинги. Соревновательный элемент повышает мотивацию."),
            ("📈 Прогресс для руководителя", "Дашборд: кто и сколько тренируется, как растут навыки, кто готов к боевым звонкам."),
        ],
        "tech": ["OpenAI GPT","Claude","YandexGPT","Whisper","ElevenLabs","SpeechKit","Google TTS","React","Node.js","PostgreSQL","WebRTC","Socket.io"],
        "faq": [
            ("Кому это нужно?", "Колл-центры, отделы продаж от 10 человек, медицинские координаторы, рекрутёры (отработка интервью), HR (онбординг), любые B2C-операции с большим количеством однотипных диалогов."),
            ("Это правда работает?", "Да. По нашим внедрениям — срок адаптации новичка падает на 50–60%, конверсия в продажу растёт на 20–30%, текучка снижается. Кейс MCC AI Trainer — 400+ операторов используют ежедневно."),
            ("Сколько стоит?", "Запуск под вашу нишу с базовыми сценариями — от 350 000 ₽. С интеграцией в LMS и сложной геймификацией — от 800 000 ₽. Подписка SaaS — от 1 500 ₽/мес за пользователя."),
            ("Сколько занимает внедрение?", "Готовый MVP — 2–3 недели. Полная кастомизация под ваши скрипты и базу — 4–6 недель."),
            ("Можно подключить к нашей LMS?", "Да. SCORM, xAPI, REST API, виджет — интегрируемся с iSpring, Mirapolis, Moodle, GetCourse, Talent Rocks."),
            ("А если у нас узкая ниша — медицина, страхование?", "Тренируем модель на ваших скриптах и базе возражений. Через 2 недели бот говорит как реальный пациент / клиент вашего профиля."),
        ]
    },
    {
        "slug": "smm",
        "title": "SMM и AI-контент: ведение соцсетей, генерация креативов | FutureFlow",
        "h1": "SMM и AI-контент",
        "tagline": "VK · Telegram · Дзен · AI-контент",
        "description": "Ведение соцсетей и AI-генерация контента для бизнеса. ВКонтакте, Telegram, Дзен. Стратегия, контент-план, тексты, дизайн, AI-видео. Рост охватов и подписчиков.",
        "keywords": "smm, ведение соцсетей, smm агентство, контент маркетинг, ai контент, telegram канал, вконтакте продвижение, дзен, контент-план",
        "lead": "Превращаем соцсети в полноценный канал привлечения и удержания клиентов. Стратегия, регулярный контент, дизайн, AI-генерация видео и текстов, аналитика и реклама — всё в одной команде.",
        "image": "https://d8j0ntlcm91z4.cloudfront.net/user_3Di09CVa1BatdZIdE0tir1KKUxw/hf_20260518_075328_1c107a5a-e78a-421c-94a8-bc77286bbf75.png",
        "includes": [
            ("🎯 Стратегия и контент-план", "Анализ конкурентов, целевая аудитория, рубрики, периодичность, цели по охвату/лидам."),
            ("✍️ Тексты и сторителлинг", "Экспертные посты, истории клиентов, новости, юмор — миксуем рубрики под алгоритмы платформ."),
            ("🎨 Дизайн и AI-визуал", "Карточки, обложки, инфографика, AI-генерация изображений и видео под бренд (Higgsfield, MJ, Flux)."),
            ("📅 Регулярные публикации", "5-15 постов в неделю на одной площадке, синхронные публикации в нескольких сетях."),
            ("💬 Комьюнити-менеджмент", "Ответы на комментарии и сообщения, модерация, общение в личке, мониторинг репутации."),
            ("📰 Яндекс Дзен и блог-платформы", "Каналы на Дзене, VC, Habr — приводят SEO-трафик и формируют экспертный имидж."),
            ("📊 Аналитика и отчётность", "Охват, ER, переходы на сайт, заявки. Ежемесячный отчёт и план на следующий месяц."),
        ],
        "tech": ["ВКонтакте","Telegram","Яндекс Дзен","Одноклассники","Pinterest","RuTube","VK Видео","Higgsfield","Midjourney","Flux","Canva","Figma","DaVinci","Capcut"],
        "faq": [
            ("Сколько стоит ведение?", "Базовый пакет (одна площадка, 8 постов/мес, дизайн, копирайтинг) — от 35 000 ₽/мес. Расширенный (3 площадки, 30+ постов, дизайн, видео, реклама) — от 90 000 ₽/мес."),
            ("Какие площадки сейчас работают?", "ВКонтакте, Telegram, Яндекс Дзен — основные. RuTube и VK Видео — для видеоконтента. Pinterest — для визуальных ниш (декор, одежда, рукоделие). Instagram* — только если есть VPN-аудитория."),
            ("Сколько ждать первых результатов?", "Рост охватов — с первого месяца. Стабильный приток подписчиков — 2–3 месяца. Заявки и продажи через соцсети — обычно 3–6 месяцев системной работы."),
            ("Можете писать как эксперт в моей нише?", "Согласовываем темы и тезисы с вами, чтобы посты звучали экспертно и не врали в фактах. Часто берём интервью у вас раз в неделю и из него генерируем 5-10 постов."),
            ("Используете ли AI-генерацию?", "Да, как помощника. Тексты и дизайн проходят через эксперта-человека. AI-видео и AI-визуал — это мощный инструмент для масштабирования контента (см. услугу AI-видео)."),
            ("Гарантируете результат?", "Гарантируем выполнение работ по плану и метрики верхней воронки (охват, рост подписчиков, ER). Лиды и продажи — зависят от ниши, оффера и работы отдела продаж, но и здесь даём рекомендации."),
        ]
    },
]


def render_service(s):
    url = f"/services/{s['slug']}/"
    canonical = f"https://futureflow.ru{url}"
    includes = "\n".join(
        f'<div class="card rv" style="padding:24px"><h3 style="font-size:18px;margin-bottom:8px">{t}</h3><p style="font-size:14.5px;color:var(--text-soft);margin:0">{html.escape(d)}</p></div>'
        for t, d in s["includes"]
    )
    pills = "\n".join(f'<span class="pill">{html.escape(t)}</span>' for t in s["tech"])
    faq_html, faq_ld = faq_block("Часто спрашивают", s["faq"])
    svc_ld = service_ld(s["h1"], s["description"], canonical, s.get("image"))

    body = f'''
{crumbs([("/", "Главная"), ("/#services", "Услуги"), (None, s["h1"])])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv" style="display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:48px;align-items:center">
      <div>
        <span class="eyebrow">{html.escape(s["tagline"])}</span>
        <h1 style="margin-top:18px">{html.escape(s["h1"])}</h1>
        <p class="lead mt-md">{html.escape(s["lead"])}</p>
        <div class="hero-ctas" style="margin-top:28px">
          <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener" class="btn btn-primary btn-arrow">Обсудить проект</a>
          <a href="/cases/" class="btn btn-ghost">Смотреть кейсы</a>
        </div>
      </div>
      <div class="rv">
        <div class="card" style="padding:0;overflow:hidden;aspect-ratio:16/9;border-radius:var(--r-lg)">
          <img src="{s.get('image', OG_DEFAULT)}" alt="{html.escape(s['h1'])}" style="width:100%;height:100%;object-fit:cover" loading="eager">
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head rv">
      <span class="eyebrow">Что входит в услугу</span>
      <h2>Полный <span class="grad-text">пакет</span> работ</h2>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px">
      {includes}
    </div>
  </div>
</section>

<section class="section-tight" style="background:var(--bg-elev-1);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
  <div class="container">
    <div class="section-head rv">
      <span class="eyebrow">Технологии и инструменты</span>
      <h2>Работаем со <span class="grad-text">всем рынком</span></h2>
    </div>
    <div class="card rv" style="padding:32px">
      <div class="pill-wrap">{pills}</div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="section-head rv">
      <span class="eyebrow">5 шагов</span>
      <h2>Как мы <span class="grad-text">работаем</span></h2>
    </div>
    <div class="steps">
      <div class="card step rv"><h3>Бриф</h3><p>30–60 мин обсуждаем задачу, цели, ограничения, дедлайны. Бесплатно.</p></div>
      <div class="card step rv"><h3>Смета и план</h3><p>За 1 рабочий день после брифа — детальная смета, план, состав команды.</p></div>
      <div class="card step rv"><h3>Прототип</h3><p>За 1–2 недели — работающий MVP, который можно показать и протестировать.</p></div>
      <div class="card step rv"><h3>Запуск</h3><p>Финальная сборка, интеграции, документация, обучение команды.</p></div>
      <div class="card step rv"><h3>Поддержка</h3><p>SLA, мониторинг, обновления, развитие. По подписке или по запросу.</p></div>
    </div>
  </div>
</section>

{faq_html}

<section class="section-tight">
  <div class="container">
    <div class="section-head rv">
      <span class="eyebrow">Связанные услуги</span>
      <h2>Часто <span class="grad-text">берут вместе</span></h2>
    </div>
    <div class="svc-grid">
      <a href="/services/ai-agents/" class="card svc-card rv"><div class="svc-ico">🤖</div><div class="svc-title">AI-агенты и чат-боты</div><p class="svc-desc">Дополним проект умным ассистентом во всех каналах.</p></a>
      <a href="/services/web/" class="card svc-card rv"><div class="svc-ico">🌐</div><div class="svc-title">Разработка сайтов</div><p class="svc-desc">Сделаем посадочную, которая конвертирует трафик в заявки.</p></a>
      <a href="/services/seo/" class="card svc-card rv"><div class="svc-ico">📈</div><div class="svc-title">SEO-продвижение</div><p class="svc-desc">Приведём органический трафик из Яндекса и Google.</p></a>
    </div>
  </div>
</section>
'''
    return page(s["title"], s["description"], url, body, og_image=s.get("image", OG_DEFAULT), extra_ld=[svc_ld, faq_ld], keywords=s["keywords"])


def write_file(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


# ========================================
# Render all services
# ========================================
for s in SERVICES:
    write_file(f"services/{s['slug']}/index.html", render_service(s))


# ========================================
# CASES page
# ========================================
CASES = [
    ("AI-видео · DTC-бренд", "🎬", "3D-видеогенерация: 60 рекламных роликов за неделю",
     "Для бренда товаров для дома сделали 60 коротких рекламных видео под VK, Reels и Shorts. Higgsfield + Runway + автоматический монтаж. Стоимость одного ролика снизилась в 12 раз vs. съёмка.",
     [("×12","дешевле"),("60","роликов / 7 дней"),("+42%","CTR")]),
    ("AI-агент · Медицина", "🦷", "AI-администратор стоматологии в Telegram",
     "Бот отвечает на вопросы, подбирает врача, бронирует время в IDENT, шлёт напоминания. Снял с ресепшна 70% рутины.",
     [("−70%","нагрузки"),("24/7","приём"),("×3","скорость")]),
    ("Голос · Логистика", "📞", "Голосовой IVR-бот для сети АЗС",
     "Голос неотличим от оператора. Объясняет, как оплатить, решает проблемы у колонки. Заменил часть колл-центра.",
     [("94%","авторешение"),("−3 FTE","в КЦ"),("4.8/5","CSI")]),
    ("EdTech", "🎓", "MCC AI Trainer — симулятор продаж на 400+ операторов",
     "Виртуальный клиент с 46 языками и эмоциями. Менеджеры отрабатывают возражения, RTM ставит оценку.",
     [("400+","операторов"),("+28%","конверсия"),("−60%","адаптация")]),
    ("AI-агент · QC", "📊", "MCC Monitoring — AI-контроль качества звонков",
     "AI слушает 100% разговоров колл-центра, оценивает по чек-листу, выявляет аномалии. До этого ОТК прослушивал 5%.",
     [("100%","покрытия"),("×20","рост"),("−40%","жалоб")]),
    ("E-com · БАД", "💊", "Магазин БАД с AI-консультантом",
     "Бот подбирает добавки по симптомам и целям, ссылается на исследования, оформляет заказ. CR x2, средний чек +35%.",
     [("×2","CR"),("+35%","средний чек"),("90%","автоответов")]),
    ("EdTech · LMS", "🎓", "LMS с AI-тьютором и автопроверкой",
     "Платформа онлайн-обучения: AI-тьютор отвечает на вопросы, проверяет домашки, ставит оценки и комментарии.",
     [("1500+","учеников"),("−80%","нагрузка"),("+40%","NPS")]),
    ("Недвижимость", "🏗️", "AI-лид-менеджер для застройщика",
     "AI квалифицирует лиды, подбирает планировки, бронирует показы, эскалирует горячих менеджеру.",
     [("×3","скорость"),("+25%","конверсия"),("−50%","трудозатраты")]),
    ("HoReCa", "🍽️", "Система онлайн-бронирования и AI-меню",
     "Бот в Telegram: бронирование столиков, меню с фото, заказ навынос, оплата СБП.",
     [("+60%","броней"),("4.9","рейтинг"),("×2","ретеншн")]),
    ("Финансы", "📈", "AI-бот для анализа предсказательных рынков",
     "Бот собирает данные с Polymarket/Kalshi, анализирует, формирует сигналы и стратегии для подписчиков.",
     [("24/7","анализ"),("87%","точность"),("12 рынков","покрытие")]),
    ("Логистика", "🚛", "AI-диспетчер для грузоперевозок",
     "AI принимает заявки, подбирает водителей и машины, оптимизирует маршруты, контролирует выполнение.",
     [("×2","оборачиваемость"),("−30%","холостые пробеги"),("4.7/5","NPS")]),
    ("Legal-tech", "⚖️", "AI-юрист: автоматическая проверка договоров",
     "AI сравнивает поступивший договор с эталоном, подсвечивает риски, формирует протокол разногласий.",
     [("×10","скорость"),("90%","покрытие рисков"),("−65%","junior часов")]),
    ("HR-tech", "👥", "AI-HR: найм, проверка, онбординг",
     "AI скринит резюме, проводит первичные интервью голосом, ставит оценку, ведёт онбординг новичков.",
     [("×5","скорость найма"),("+30%","retention"),("400+","CV в нед.")]),
    ("E-com · Pricing", "💰", "Динамическое ценообразование с мониторингом",
     "Парсинг цен конкурентов на маркетплейсах, автокорректировка цен в магазине под правила.",
     [("24/7","мониторинг"),("+18%","маржа"),("12 маркетплейсов","")]),
    ("CRM", "🔗", "CRM с нуля: разработка под уникальные процессы",
     "Кастомная CRM, когда AmoCRM/Bitrix не подходят: отраслевые поля, сложные воронки, особый документооборот.",
     [("100%","под клиента"),("×3","скорость работы"),("0","лишних модулей")]),
    ("BI / ETL", "📊", "Централизованная платформа данных: ETL, аналитика, BI",
     "Собрали данные из 12 источников в ClickHouse, построили DataLens-дашборды для топ-менеджмента.",
     [("12","источников"),("Real-time","обновление"),("4","роли доступа")]),
]
cases_grid = "\n".join(
    f'''<article class="card case-card rv">
  <div class="case-cover" style="background:linear-gradient(135deg,#4A86D8,#7C5CFF)">{e}</div>
  <div class="case-body">
    <span class="case-tag">{html.escape(tag)}</span>
    <h3 class="case-title">{html.escape(title)}</h3>
    <p class="case-desc">{html.escape(desc)}</p>
    <div class="case-metrics">
{chr(10).join(f'      <div class="case-metric"><div class="num">{html.escape(n)}</div><div class="lbl">{html.escape(l)}</div></div>' for n,l in metrics)}
    </div>
  </div>
</article>'''
    for tag, e, title, desc, metrics in CASES
)
cases_body = f'''
{crumbs([("/", "Главная"), (None, "Кейсы")])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv">
      <span class="eyebrow">15+ внедрений в проде</span>
      <h1 style="margin-top:18px">Реальные <span class="grad-text">кейсы</span> FutureFlow</h1>
      <p class="lead mt-md">От запуска первого AI-агента до полной цифровой трансформации отрасли. Каждый кейс — с конкретными цифрами, технологиями и сроками.</p>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="case-grid">
{cases_grid}
    </div>
  </div>
</section>
'''
write_file("cases/index.html", page(
    "Кейсы FutureFlow: 15+ AI-проектов в проде — стоматология, АЗС, e-com, LMS",
    "Реальные кейсы внедрений FutureFlow: AI-видео, голосовые боты для АЗС, AI-администратор стоматологии, симулятор продаж MCC, AI-юрист, BI-платформа. С цифрами и метриками.",
    "/cases/", cases_body,
    keywords="кейсы ai, ai проекты, ai кейсы, портфолио ai агентства, ai в бизнесе, внедрение ai"
))


# ========================================
# INDUSTRIES page
# ========================================
INDUSTRIES = [
    ("medicine","🏥","Медицина и клиники",
     "Запись и переносы визитов через Telegram-бота, AI-консультант по симптомам с грамотной маршрутизацией, голосовые ассистенты для ресепшна, AI-видео для медицинского контент-маркетинга, SEO для частной практики с учётом E-E-A-T и YMYL. Соблюдение требований 152-ФЗ и врачебной тайны.",
     ["AI-администратор клиники (Telegram, WhatsApp)","Голосовой бот для ресепшн и колл-центра","Запись через сайт + интеграция с YClients / IDENT / Universe","AI-консультации по симптомам с эскалацией","SEO для клиник и врачей частной практики","AI-видео для соцсетей и YouTube"]),
    ("ecom","🛒","E-commerce и ретейл",
     "AI-консультант на сайте с реальным знанием каталога, динамическое ценообразование, продуктовые AI-видео для маркетплейсов, автоворонки в мессенджерах, SEO для интернет-магазинов на 10 000+ товаров.",
     ["AI-консультант с RAG по каталогу","AI-видео для карточек товара (Higgsfield, Sora)","Динамическое ценообразование и мониторинг конкурентов","Автоворонки в Telegram / WhatsApp","SEO для крупных каталогов","Интеграция с маркетплейсами"]),
    ("realestate","🏗️","Недвижимость и девелопмент",
     "AI-квалификация лидов и подбор объектов, видео-туры по квартирам через AI, голосовой обзвон базы, CRM для агентств, AI-3D визуализация проектов.",
     ["AI-лид-менеджер для застройщика","3D-туры и AI-визуализации проектов","Голосовой обзвон с подбором показа","AmoCRM с отраслевыми воронками","SEO с лонгридами о ЖК и районах","AI-юрист для проверки договоров ДДУ"]),
    ("legal","⚖️","Юридические услуги",
     "AI-юрист для первичной проверки договоров и поиска рисков, AI-консультации с эскалацией к живому юристу, автогенерация типовых документов, SEO для юридических услуг.",
     ["AI-анализ договоров и протокол разногласий","Первичный консультант для клиентов","Автогенерация типовых документов","SEO для юр.услуг с E-E-A-T","CRM для юридической фирмы","AI-видео объяснения правовых вопросов"]),
    ("edu","🎓","EdTech и образование",
     "LMS с AI-тьютором, автопроверкой и персонализацией, симуляторы навыков на ИИ, AI-видеокурсы с виртуальным преподавателем, продвижение в Яндекс Дзене.",
     ["LMS с AI-тьютором и автопроверкой","Тренажёры soft и hard skills","AI-видеолекции и аватары преподавателей","Боты для онбординга студентов","SEO и Дзен для EdTech","Сквозная аналитика по когортам"]),
    ("horeca","🍽️","HoReCa и доставка",
     "Боты для бронирования и меню, голосовые ассистенты для приёма заказов, AI-видео для соцсетей, программа лояльности, SEO для ресторанов и кафе.",
     ["Бот-бронирование столиков","Голосовой приём заказов","AI-меню в Telegram с фото","Лояльность и реактивация спящих","SEO для локальной выдачи","AI-видео блюд и атмосферы"]),
    ("logistics","🚛","Логистика и транспорт",
     "AI-диспетчеры, маршрутизация, голосовые подтверждения заявок, дашборды для управления автопарком, BI для финансовых показателей.",
     ["AI-диспетчер заказов и подбор машин","Голосовые подтверждения и уведомления","Оптимизация маршрутов и снижение пробегов","BI-дашборды по парку и финансам","Интеграция с 1С Управление автотранспортом","Чат-боты для водителей"]),
    ("finance","💰","Финансы и страхование",
     "AI-скоринг клиентов, чат-боты с консультацией по продуктам, расчёт ОСАГО/КАСКО ботом, BI для управленческих решений, мониторинг рисков.",
     ["Скоринг клиентов на ML-моделях","Боты-консультанты по продуктам","Голосовой расчёт страховых полисов","BI-дашборды для управления","Мониторинг рынка и сигналы","Чат-боты для саппорта клиентов"]),
]
ind_html = "\n".join(
    f'''<section id="{slug}" class="section-tight" style="{('background:var(--bg-elev-1);border-top:1px solid var(--border);border-bottom:1px solid var(--border)' if i%2 else '')}">
  <div class="container">
    <div class="rv" style="display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:48px;align-items:start">
      <div>
        <div class="ind-emoji" style="font-size:48px;margin-bottom:14px">{e}</div>
        <h2>{html.escape(title)}</h2>
        <p class="lead">{html.escape(desc)}</p>
      </div>
      <div>
        <h3 style="font-size:14px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-mute);margin-bottom:14px">Что делаем</h3>
        <ul style="display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:0;list-style:none">
{chr(10).join(f'          <li style="display:flex;gap:10px;font-size:14.5px;color:var(--text-soft);padding:12px 14px;background:var(--bg-elev-1);border:1px solid var(--border);border-radius:12px"><span style="color:var(--brand-3);font-weight:700">✓</span><span>{html.escape(item)}</span></li>' for item in items)}
        </ul>
      </div>
    </div>
  </div>
</section>'''
    for i, (slug, e, title, desc, items) in enumerate(INDUSTRIES)
)
ind_body = f'''
{crumbs([("/", "Главная"), (None, "Отрасли")])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv">
      <span class="eyebrow">Опыт в 8 отраслях</span>
      <h1 style="margin-top:18px">Работаем в <span class="grad-text">каждой</span> сфере бизнеса</h1>
      <p class="lead mt-md">От медицины до девелопмента и страхования. В каждой нише — десятки внедрений и понимание специфики, регуляторики, цикла принятия решения у клиента.</p>
    </div>
  </div>
</section>

{ind_html}
'''
write_file("industries/index.html", page(
    "Отрасли FutureFlow: AI для медицины, e-com, недвижимости, EdTech, HoReCa",
    "AI и цифровые услуги для медицины, e-commerce, недвижимости, юридических услуг, EdTech, HoReCa, логистики, финансов. Опыт в каждой нише.",
    "/industries/", ind_body,
    keywords="ai для медицины, ai для e-commerce, ai для недвижимости, ai для юристов, ai для edtech, отраслевые ai решения"
))


# ========================================
# ABOUT page
# ========================================
about_body = f'''
{crumbs([("/", "Главная"), (None, "О компании")])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv">
      <span class="eyebrow">О FutureFlow</span>
      <h1 style="margin-top:18px">Команда, которая делает <span class="grad-text">завтра</span> сегодня</h1>
      <p class="lead mt-md">FutureFlow — AI-агентство полного цикла. Мы соединяем глубокую инженерную экспертизу с прагматичным подходом: не «делаем модно», а решаем реальные задачи бизнеса в измеримых метриках.</p>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="prose rv">
      <h2>Кто мы</h2>
      <p>FutureFlow — независимая распределённая команда AI-инженеров, разработчиков, маркетологов и продактов. Юридически работаем как <strong>ИП Зайдель Адриан Патрик</strong> (Россия) — это удобная и прозрачная форма для договорных отношений с бизнесом.</p>
      <p>Мы стартовали в 2023 году с одного направления — AI-агентов для клиник и колл-центров. За три года выросли в полноценную команду, закрывающую весь цифровой стек: от 3D-видеогенерации до сквозной BI-аналитики.</p>

      <h2>Во что верим</h2>
      <ul>
        <li><strong>Технология ради результата.</strong> Никаких «AI ради AI». Если задачу проще решить таблицей в Google Sheets — делаем таблицу.</li>
        <li><strong>Прозрачность.</strong> Открытые сметы, прямой доступ к команде, регулярные отчёты, документация ко всему.</li>
        <li><strong>Без вендор-лока.</strong> Используем лучшие инструменты под задачу, а не самые маржинальные для агентства. Передаём вам полные права на код и данные.</li>
        <li><strong>Юридическая чистота.</strong> Договоры, акты, корректное налогообложение, маркировка рекламы, соблюдение 152-ФЗ.</li>
        <li><strong>Долгие отношения.</strong> 80% клиентов работают с нами от года и больше — это лучший показатель качества.</li>
      </ul>

      <h2>Как мы устроены</h2>
      <p>Каждый проект ведёт продакт + 1–3 специалиста (AI-инженер, разработчик, дизайнер, копирайтер — по необходимости). Клиент общается напрямую с продактом и в общем чате в Telegram. Никаких 5 уровней менеджмента и «отписок аккаунт-менеджера».</p>
      <p>Технологический стек подбираем под задачу — от no-code (Tilda, Make, n8n) до кастомной разработки на React/Node/Python с self-hosted LLM.</p>

      <h2>Юридическая чистота и работа с данными</h2>
      <p>Работаем как ИП Зайдель Адриан Патрик. Договоры с обеими сторонами, акты выполненных работ, счета — для любой системы налогообложения у клиента. NDA подписываем по запросу до начала работ.</p>
      <p>Сайт <strong>futureflow.ru</strong> не собирает персональные данные пользователей через обязательные формы — для связи используются мессенджеры, e-mail и телефон, которые посетитель сам выбирает. Поэтому ИП не подлежит регистрации в Реестре операторов персональных данных Роскомнадзора (152-ФЗ). Подробнее — в <a href="/legal/privacy/">Политике обработки данных</a>.</p>

      <h2>Контакты</h2>
      <p>ИП Зайдель Адриан Патрик<br>
      Телефон: <a href="tel:+79259040111">+7 925 904-01-11</a><br>
      Email: <a href="mailto:hello@futureflow.ru">hello@futureflow.ru</a><br>
      Telegram: <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener">@FutureFlowInc</a><br>
      WhatsApp: <a href="https://wa.me/79661277767" target="_blank" rel="noopener">+7 966 127-77-67</a></p>
    </div>
  </div>
</section>
'''
write_file("about/index.html", page(
    "О компании FutureFlow — AI-агентство полного цикла",
    "FutureFlow — независимая команда AI-инженеров, разработчиков и маркетологов. Работаем как ИП с 2023 года. Юридически чисто, прозрачно, без вендор-лока.",
    "/about/", about_body,
    keywords="о компании futureflow, ai агентство о нас, ип зайдель"
))


# ========================================
# CONTACTS page
# ========================================
contacts_body = f'''
{crumbs([("/", "Главная"), (None, "Контакты")])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv">
      <span class="eyebrow">Связь с командой</span>
      <h1 style="margin-top:18px">Напишите нам — <span class="grad-text">удобным способом</span></h1>
      <p class="lead mt-md">На сайте нет форм с обязательным сбором данных. Вы выбираете канал связи сами — мессенджер, e-mail или телефон. Отвечаем в течение 1 рабочего дня (обычно — за пару часов).</p>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px">
      <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener" class="card rv" style="padding:32px;text-decoration:none;display:block">
        <div class="b-icon" style="width:54px;height:54px;border-radius:14px;background:var(--brand-grad-soft);border:1px solid var(--border-2);display:grid;place-items:center;font-size:24px;margin-bottom:18px">💬</div>
        <h3 style="font-size:18px;margin-bottom:6px">Telegram</h3>
        <p style="color:var(--text-mute);font-size:13px;margin-bottom:14px">Рекомендуем: быстрее всего отвечаем</p>
        <div style="font-family:var(--font-display);font-weight:700;color:var(--text);font-size:17px">@FutureFlowInc</div>
      </a>
      <a href="https://wa.me/79661277767" target="_blank" rel="noopener" class="card rv" style="padding:32px;text-decoration:none;display:block">
        <div class="b-icon" style="width:54px;height:54px;border-radius:14px;background:var(--brand-grad-soft);border:1px solid var(--border-2);display:grid;place-items:center;font-size:24px;margin-bottom:18px">📱</div>
        <h3 style="font-size:18px;margin-bottom:6px">WhatsApp</h3>
        <p style="color:var(--text-mute);font-size:13px;margin-bottom:14px">Если удобнее общаться через WA</p>
        <div style="font-family:var(--font-display);font-weight:700;color:var(--text);font-size:17px">+7 966 127-77-67</div>
      </a>
      <a href="mailto:hello@futureflow.ru" class="card rv" style="padding:32px;text-decoration:none;display:block">
        <div class="b-icon" style="width:54px;height:54px;border-radius:14px;background:var(--brand-grad-soft);border:1px solid var(--border-2);display:grid;place-items:center;font-size:24px;margin-bottom:18px">✉️</div>
        <h3 style="font-size:18px;margin-bottom:6px">E-mail</h3>
        <p style="color:var(--text-mute);font-size:13px;margin-bottom:14px">Для официальной переписки и КП</p>
        <div style="font-family:var(--font-display);font-weight:700;color:var(--text);font-size:17px">hello@futureflow.ru</div>
      </a>
      <a href="tel:+79259040111" class="card rv" style="padding:32px;text-decoration:none;display:block">
        <div class="b-icon" style="width:54px;height:54px;border-radius:14px;background:var(--brand-grad-soft);border:1px solid var(--border-2);display:grid;place-items:center;font-size:24px;margin-bottom:18px">📞</div>
        <h3 style="font-size:18px;margin-bottom:6px">Телефон</h3>
        <p style="color:var(--text-mute);font-size:13px;margin-bottom:14px">С 10:00 до 20:00 МСК</p>
        <div style="font-family:var(--font-display);font-weight:700;color:var(--text);font-size:17px">+7 925 904-01-11</div>
      </a>
    </div>

    <div class="card rv" style="margin-top:32px;padding:32px">
      <h3 style="font-size:18px;margin-bottom:14px">Реквизиты</h3>
      <p style="color:var(--text-soft);font-size:14.5px;line-height:1.7">
        <strong style="color:var(--text)">ИП Зайдель Адриан Патрик</strong><br>
        Россия<br>
        Email: <a href="mailto:hello@futureflow.ru" style="color:var(--brand)">hello@futureflow.ru</a><br>
        Полные реквизиты (ИНН, ОГРНИП, расчётный счёт) — предоставляются по запросу для заключения договора.
      </p>
    </div>

    <div class="card rv" style="margin-top:18px;padding:32px;background:var(--brand-grad-soft);border-color:var(--border-2)">
      <h3 style="font-size:18px;margin-bottom:10px">📝 Что прислать сразу для расчёта</h3>
      <ul style="display:flex;flex-direction:column;gap:6px;padding:0;list-style:none;margin:0">
        <li style="font-size:14.5px;color:var(--text-soft)">✓ Краткое описание задачи (1-2 абзаца)</li>
        <li style="font-size:14.5px;color:var(--text-soft)">✓ Желаемый срок запуска</li>
        <li style="font-size:14.5px;color:var(--text-soft)">✓ Бюджет (хотя бы порядок)</li>
        <li style="font-size:14.5px;color:var(--text-soft)">✓ Ссылки на текущие сайты / системы (если есть)</li>
        <li style="font-size:14.5px;color:var(--text-soft)">✓ Удобный канал и время для созвона</li>
      </ul>
    </div>
  </div>
</section>
'''
write_file("contacts/index.html", page(
    "Контакты FutureFlow: Telegram, WhatsApp, e-mail, телефон",
    "Контакты FutureFlow: Telegram @FutureFlowInc, WhatsApp +7 966 127-77-67, email hello@futureflow.ru, телефон +7 925 904-01-11. Без форм с обязательным сбором данных.",
    "/contacts/", contacts_body,
    keywords="контакты futureflow, написать в futureflow, телефон футурфлоу, telegram футурфлоу"
))


# ========================================
# LEGAL: privacy
# ========================================
privacy_body = f'''
{crumbs([("/", "Главная"), ("/about/", "О компании"), (None, "Политика обработки данных")])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv">
      <span class="eyebrow">Юридический документ</span>
      <h1 style="margin-top:18px">Политика обработки <span class="grad-text">данных</span></h1>
      <p class="lead mt-md">Документ описывает, какие данные собирает сайт futureflow.ru, как они обрабатываются и почему ИП не подлежит регистрации в Реестре операторов персональных данных Роскомнадзора.</p>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="prose rv">
      <p><strong>Редакция от 18.05.2026.</strong> Сайт: <strong>futureflow.ru</strong>. Владелец сайта: <strong>ИП Зайдель Адриан Патрик</strong> (далее — «ИП»).</p>
      <p>Контакты для запросов по этой Политике:<br>
      Телефон: <a href="tel:+79259040111">+7 925 904-01-11</a><br>
      Email: <a href="mailto:hello@futureflow.ru">hello@futureflow.ru</a><br>
      Telegram: <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener">@FutureFlowInc</a><br>
      WhatsApp: <a href="https://wa.me/79661277767" target="_blank" rel="noopener">+7 966 127-77-67</a></p>

      <h2>1. Кто и на основании чего</h2>
      <p>ИП ведёт деятельность на территории Российской Федерации. Настоящая Политика разработана в соответствии с Федеральным законом от 27.07.2006 № 152-ФЗ «О персональных данных», иными нормативными актами РФ и отражает добросовестную практику обращения с данными посетителей.</p>

      <h2>2. Что сайт НЕ делает</h2>
      <p>Сайт <strong>futureflow.ru</strong> построен по принципу <strong>минимизации обработки данных</strong>:</p>
      <ul>
        <li>На сайте <strong>отсутствуют формы обратной связи</strong> с обязательными полями для имени, телефона, email, паспорта или иных персональных данных;</li>
        <li>ИП <strong>не использует</strong> на сайте инструменты онлайн-чатов, всплывающие формы захвата лидов, поля ввода персональных данных, callback-формы, формы записи или формы подписки;</li>
        <li>Сайт не использует пиксели, скрипты ретаргетинга и трекинговые cookie, целенаправленно собирающие персональные данные. Cookies используются только техническими сервисами (Google Fonts, GitHub Pages) для штатной работы — IP-адреса фиксируются на стороне их инфраструктуры, ИП к этим логам доступа не имеет;</li>
        <li>ИП <strong>не собирает</strong> данные о посетителях через сторонние счётчики и системы веб-аналитики (Яндекс Метрика, Google Analytics) на этом сайте. Технические серверные логи хостинга (GitHub Pages / Cloudflare) хранятся у инфраструктурных провайдеров и не содержат данных, идентифицирующих физическое лицо в значении 152-ФЗ.</li>
      </ul>
      <p>Таким образом, сайт <strong>не осуществляет действий по сбору, записи, систематизации, накоплению, хранению, уточнению, извлечению, использованию, передаче, обезличиванию, блокированию, удалению или уничтожению персональных данных</strong> в значении ст. 3 152-ФЗ.</p>

      <h2>3. Сторонние сервисы и логирование</h2>
      <p>Сайт подгружает шрифты с серверов <strong>Google Fonts</strong> (fonts.googleapis.com / fonts.gstatic.com). При обращении за шрифтом инфраструктура Google технически фиксирует IP-адрес запроса согласно своей политике: <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">policies.google.com/privacy</a>. ИП эти сведения не получает и не имеет к ним доступа.</p>
      <p>Изображения для оформления сайта подгружаются с CDN-серверов <strong>Amazon CloudFront</strong>. Те же замечания применимы.</p>
      <p>Сайт размещается на платформе <strong>GitHub Pages</strong> (GitHub, Inc.). Серверные логи доступа (IP, user-agent) хранятся у GitHub согласно его политике <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">политике конфиденциальности</a>. ИП не имеет доступа к этим логам.</p>

      <h2>4. Если вы сами связались с нами</h2>
      <p>Если посетитель сайта <strong>по собственной инициативе</strong> отправил сообщение в Telegram, WhatsApp, на электронную почту ИП или совершил телефонный звонок — в момент такого обращения возникает гражданско-правовое отношение, в рамках которого ИП обрабатывает минимально необходимые данные (имя, контакт, содержание обращения) исключительно <strong>для исполнения договора или подготовки к его заключению</strong> в соответствии с п. 5 ч. 1 ст. 6 152-ФЗ.</p>
      <p>В этом случае ИП:</p>
      <ul>
        <li>обрабатывает данные на правовом основании «исполнение договора, стороной которого является субъект персональных данных» (без отдельного согласия);</li>
        <li>не передаёт данные третьим лицам, кроме исполнителей по поручению (например, для отправки счёта в банк) и государственных органов в случаях, предусмотренных законом;</li>
        <li>хранит данные не дольше, чем это необходимо для оказания услуг и в сроки, установленные налоговым и архивным законодательством РФ;</li>
        <li>обеспечивает конфиденциальность и применяет организационные и технические меры защиты.</li>
      </ul>

      <h2>5. Уведомление Роскомнадзора</h2>
      <p>В соответствии с ч. 2 ст. 22 152-ФЗ оператор вправе осуществлять обработку персональных данных <strong>без уведомления уполномоченного органа по защите прав субъектов персональных данных</strong> (Роскомнадзора), если обработка ведётся в рамках заключения и исполнения договора, стороной которого является субъект персональных данных. Именно в этом режиме обрабатываются обращения посетителей, направленные ими по собственной инициативе после изучения сайта.</p>
      <p>Поскольку сам сайт <strong>не осуществляет сбора</strong> персональных данных через формы и инструменты, на него такая обязанность также не распространяется. ИП готов предоставить подтверждение указанной позиции уполномоченному органу по запросу.</p>

      <h2>6. Передача через мессенджеры, e-mail и операторов связи</h2>
      <p>При обращении через Telegram, WhatsApp, по электронной почте или по телефону ваше сообщение проходит через инфраструктуру соответствующего сервиса связи (Telegram FZ-LLC, WhatsApp LLC / Meta Platforms Inc., почтовый провайдер ИП и провайдер вашей почты, оператор сотовой связи). Эти сервисы обрабатывают передаваемые через них данные на основании собственных условий и политик; ИП не отвечает за их действия и рекомендует ознакомиться с их политиками до начала переписки.</p>

      <h2>7. Ваши права</h2>
      <p>В отношении персональных данных, переданных вами в адрес ИП по собственной инициативе, вы имеете права, предусмотренные гл. 3 152-ФЗ: получать сведения об их обработке, требовать уточнения, блокирования, уничтожения, обращаться с жалобой в Роскомнадзор и в суд.</p>
      <p>Для реализации прав отправьте запрос на e-mail <a href="mailto:hello@futureflow.ru">hello@futureflow.ru</a>, в Telegram <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener">@FutureFlowInc</a>, на WhatsApp <a href="https://wa.me/79661277767" target="_blank" rel="noopener">+7 966 127-77-67</a> или по телефону <a href="tel:+79259040111">+7 925 904-01-11</a>. Срок ответа — не более 10 рабочих дней.</p>

      <h2>8. Защита данных</h2>
      <p>ИП применяет организационные и технические меры защиты данных: разграничение доступа, антивирусную защиту, шифрование каналов передачи, регулярные обновления ПО, бэкапы.</p>

      <h2>9. Несовершеннолетние</h2>
      <p>Услуги ориентированы на бизнес (B2B). Сайт не предназначен для лиц младше 18 лет, и ИП намеренно не обрабатывает данные несовершеннолетних.</p>

      <h2>10. Изменения</h2>
      <p>ИП вправе вносить изменения в настоящую Политику. Новая редакция вступает в силу с момента её публикации на сайте по адресу <a href="https://futureflow.ru/legal/privacy/">https://futureflow.ru/legal/privacy/</a>, если иное не предусмотрено новой редакцией.</p>

      <h2>11. Контакты</h2>
      <p>ИП Зайдель Адриан Патрик<br>
      Телефон: <a href="tel:+79259040111">+7 925 904-01-11</a><br>
      Email: <a href="mailto:hello@futureflow.ru">hello@futureflow.ru</a><br>
      Telegram: <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener">@FutureFlowInc</a><br>
      WhatsApp: <a href="https://wa.me/79661277767" target="_blank" rel="noopener">+7 966 127-77-67</a></p>
    </div>
  </div>
</section>
'''
write_file("legal/privacy/index.html", page(
    "Политика обработки данных — FutureFlow",
    "Политика обработки персональных данных FutureFlow. Сайт не собирает ПДн через формы, поэтому ИП не подлежит регистрации в Реестре операторов ПДн Роскомнадзора.",
    "/legal/privacy/", privacy_body
))


# ========================================
# LEGAL: terms
# ========================================
terms_body = f'''
{crumbs([("/", "Главная"), ("/about/", "О компании"), (None, "Пользовательское соглашение")])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv">
      <span class="eyebrow">Юридический документ</span>
      <h1 style="margin-top:18px">Пользовательское <span class="grad-text">соглашение</span></h1>
      <p class="lead mt-md">Условия использования сайта futureflow.ru. Использование сайта означает полное и безоговорочное принятие условий настоящего Соглашения.</p>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="prose rv">
      <p><strong>Редакция от 18.05.2026.</strong></p>

      <h2>1. Общие положения</h2>
      <p>Настоящее Соглашение (далее — «Соглашение») регулирует условия использования сайта <strong>futureflow.ru</strong> (далее — «Сайт»), принадлежащего ИП Зайдель Адриан Патрик (далее — «Компания»). Использование Сайта означает полное и безоговорочное принятие условий Соглашения.</p>

      <h2>2. Характер информации на сайте</h2>
      <p>Вся информация на Сайте носит ознакомительный характер, не является публичной офертой в значении ст. 437 ГК РФ и может быть изменена в любой момент без предварительного уведомления. Точные условия оказания услуг, состав работ и стоимость определяются в индивидуальном порядке и фиксируются в договоре между Компанией и Заказчиком.</p>

      <h2>3. Интеллектуальная собственность</h2>
      <p>Все объекты, размещённые на Сайте (тексты, изображения, графика, дизайн, программный код), являются объектами интеллектуальной собственности их правообладателей и охраняются законодательством РФ. Использование любых материалов Сайта без письменного согласия правообладателя запрещено.</p>
      <p>Используемые на Сайте товарные знаки и логотипы третьих лиц упомянуты исключительно для идентификации соответствующих платформ, технологий и сервисов, с которыми Компания работает в рамках своих услуг.</p>

      <h2>4. Допустимое использование</h2>
      <p>Пользователь обязуется не использовать Сайт для:</p>
      <ul>
        <li>распространения вредоносного ПО и иной запрещённой законом информации;</li>
        <li>попыток несанкционированного доступа к Сайту или связанным системам;</li>
        <li>автоматизированного сбора данных в ущерб работоспособности Сайта;</li>
        <li>любых иных действий, нарушающих законодательство РФ или права третьих лиц.</li>
      </ul>

      <h2>5. Ограничение ответственности</h2>
      <p>Сайт предоставляется «как есть». Компания не гарантирует бесперебойной работы Сайта, отсутствия ошибок, а также соответствия Сайта ожиданиям и целям конкретного Пользователя. Компания не несёт ответственности за прямые или косвенные убытки, возникшие в результате использования или невозможности использования Сайта.</p>

      <h2>6. Внешние ссылки</h2>
      <p>Сайт может содержать ссылки на сайты и сервисы третьих лиц. Компания не отвечает за содержание, политики и действия таких ресурсов; переход осуществляется на риск Пользователя.</p>

      <h2>7. Изменения Соглашения</h2>
      <p>Компания вправе в любой момент изменить условия Соглашения. Новая редакция вступает в силу с момента её публикации на Сайте по адресу <a href="https://futureflow.ru/legal/terms/">https://futureflow.ru/legal/terms/</a>, если иное не предусмотрено новой редакцией.</p>

      <h2>8. Применимое право и разрешение споров</h2>
      <p>К Соглашению применяется законодательство Российской Федерации. Споры, не урегулированные путём переговоров, подлежат разрешению в суде по месту нахождения Компании.</p>

      <h2>9. Реквизиты и контакты</h2>
      <p>ИП Зайдель Адриан Патрик<br>
      Тел.: <a href="tel:+79259040111">+7 925 904-01-11</a><br>
      Email: <a href="mailto:hello@futureflow.ru">hello@futureflow.ru</a><br>
      Telegram: <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener">@FutureFlowInc</a><br>
      WhatsApp: <a href="https://wa.me/79661277767" target="_blank" rel="noopener">+7 966 127-77-67</a><br>
      Реквизиты ИП предоставляются по запросу.</p>
    </div>
  </div>
</section>
'''
write_file("legal/terms/index.html", page(
    "Пользовательское соглашение — FutureFlow",
    "Пользовательское соглашение сайта futureflow.ru. Условия использования сайта ИП Зайдель Адриан Патрик.",
    "/legal/terms/", terms_body
))


# ========================================
# SERVICES HUB
# ========================================
svc_cards = "\n".join(
    f'''<a href="/services/{s["slug"]}/" class="card card-glow svc-card rv">
      <div class="svc-ico">{ico}</div>
      <div class="svc-title">{html.escape(s["h1"])}</div>
      <p class="svc-desc">{html.escape(s["lead"][:140])}…</p>
      <span class="svc-link">Подробнее</span>
    </a>'''
    for s, ico in zip(SERVICES, ["🎬","🤖","🎙️","🌐","📈","🎯","⚡","🔗","🧠","📱"])
)
services_body = f'''
{crumbs([("/", "Главная"), (None, "Услуги")])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv">
      <span class="eyebrow">10 равноценных направлений</span>
      <h1 style="margin-top:18px">Все <span class="grad-text">услуги</span> FutureFlow</h1>
      <p class="lead mt-md">От 3D-видеогенерации до сквозной BI-аналитики. Берём одно направление или собираем под вас полный AI-отдел на аутсорсе.</p>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="svc-grid">
{svc_cards}
    </div>
  </div>
</section>
'''
write_file("services/index.html", page(
    "Услуги FutureFlow — AI-видео, агенты, сайты, SEO, автоматизация",
    "Все услуги FutureFlow: AI и 3D-видео, AI-агенты и чат-боты, голосовые боты, разработка сайтов, SEO, реклама, автоматизация, CRM и BI, AI-обучение, SMM.",
    "/services/", services_body,
    keywords="услуги ai агентства, ai видео генерация, чат боты, разработка сайтов, seo, контекстная реклама, автоматизация"
))


# ========================================
# CAREERS (updated style, same vacancy)
# ========================================
careers_body = f'''
{crumbs([("/", "Главная"), (None, "Вакансии")])}

<section class="page-hero">
  <div class="page-hero-bg"></div>
  <div class="container">
    <div class="rv">
      <span class="eyebrow">Открытая вакансия · Удалённо · Комиссия</span>
      <h1 style="margin-top:18px">Менеджер по <span class="grad-text">привлечению клиентов</span></h1>
      <p class="lead mt-md">Команда из 10+ AI-инженеров, маркетологов и дизайнеров ищет коммерческого специалиста, который умеет находить клиентов на услуги цифровой трансформации: AI-видео, агенты, сайты, SEO. Комиссия 10–20% с каждого закрытого договора, без фиксированной ставки.</p>
      <div class="hero-ctas" style="margin-top:28px">
        <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener" class="btn btn-primary btn-arrow">Откликнуться в Telegram</a>
        <a href="mailto:hello@futureflow.ru?subject=Вакансия%20Менеджер%20по%20привлечению" class="btn btn-ghost">Написать на e-mail</a>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="prose rv">
      <h2>Кто мы и что делаем</h2>
      <p>FutureFlow — AI-агентство полного цикла. Помогаем бизнесу автоматизировать рутину, ускорять продажи и снижать затраты с помощью искусственного интеллекта. Кейсы — от стоматологии до сети АЗС, от EdTech до девелопмента.</p>
      <p>Наш чек — от 80 000 ₽ за разовый проект до 600 000+ ₽ за комплексное внедрение и от 180 000 ₽/мес за подписку на AI-команду.</p>

      <h2>Что нужно делать</h2>
      <ul>
        <li>Искать и привлекать новых клиентов: входящий маркетинг, исходящий, нетворк, мероприятия;</li>
        <li>Проводить первичные брифы и квалифицировать запросы;</li>
        <li>Передавать продакт-менеджеру для сметы, согласовывать с клиентом;</li>
        <li>Сопровождать сделку до подписания договора и оплаты;</li>
        <li>Поддерживать связь с клиентом в первый месяц после запуска и собирать обратную связь.</li>
      </ul>

      <h2>Кого мы ищем</h2>
      <ul>
        <li>Опыт продаж B2B-услуг (digital, IT, маркетинг, AI — будет плюсом, но не обязательно);</li>
        <li>Умение проводить экспертный диалог: задать правильные вопросы, перевести «хочу автоматизацию» в понятную задачу;</li>
        <li>Самостоятельность и проактивность — мы не контролируем график, контролируем результат;</li>
        <li>Грамотная русская речь и письменная коммуникация;</li>
        <li>Готовность учиться технической стороне (что такое RAG, чем GPT отличается от Claude, как устроена интеграция CRM).</li>
      </ul>

      <h2>Ваша комиссия</h2>
      <ul>
        <li><strong>10–20%</strong> от стоимости каждого закрытого договора в зависимости от типа клиента и сложности;</li>
        <li>На подписке (AI-команда на ретейнер) — комиссия в первые 3 месяца;</li>
        <li>Без верхнего потолка по сумме сделок;</li>
        <li>Выплата — после поступления оплаты от клиента, обычно в течение 5 рабочих дней.</li>
      </ul>

      <h2>Почему это выгодно</h2>
      <ul>
        <li><strong>Высокий чек.</strong> Средний договор — от 200 000 ₽, ваш доход с одной сделки — от 20 000 до 100 000 ₽;</li>
        <li><strong>Тёплый рынок.</strong> AI — то, о чём сейчас говорят все, входящий интерес высокий;</li>
        <li><strong>Сильный продукт.</strong> 50+ кейсов в проде, высокий уровень повторных обращений и рекомендаций;</li>
        <li><strong>Свобода.</strong> Полностью удалённо, гибкий график, без микроменеджмента;</li>
        <li><strong>Поддержка команды.</strong> Маркетолог, дизайнер, продакт, AI-инженеры — на вашей стороне для подготовки КП и брифов.</li>
      </ul>

      <h2>Как откликнуться</h2>
      <p>Напишите в <a href="https://t.me/FutureFlowInc" target="_blank" rel="noopener">Telegram @FutureFlowInc</a> или на <a href="mailto:hello@futureflow.ru?subject=Вакансия%20Менеджер%20по%20привлечению">hello@futureflow.ru</a> пару абзацев о себе и опыте. Если есть кейсы / LinkedIn / резюме — приложите. Ответим в течение 1 рабочего дня.</p>
    </div>
  </div>
</section>
'''
write_file("careers/index.html", page(
    "Вакансия: Менеджер по привлечению клиентов — FutureFlow",
    "Открытая вакансия в FutureFlow: менеджер по привлечению клиентов на услуги AI-агентства. Удалённо, комиссия 10–20% с каждого договора, без фиксированной ставки.",
    "/careers/", careers_body,
    keywords="вакансии futureflow, менеджер по привлечению клиентов, работа в ai агентстве, удалённая работа, b2b продажи, sales manager"
))


# ========================================
# robots.txt and sitemap.xml
# ========================================
ROBOTS = """User-agent: *
Allow: /
Disallow: /_backup/
Disallow: /_build/

Sitemap: https://futureflow.ru/sitemap.xml
Host: https://futureflow.ru
"""
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(ROBOTS)

URLS = [
    ("/", 1.0, "weekly"),
    ("/services/ai-video/", 0.9, "monthly"),
    ("/services/ai-agents/", 0.9, "monthly"),
    ("/services/voice-bots/", 0.9, "monthly"),
    ("/services/web/", 0.9, "monthly"),
    ("/services/seo/", 0.9, "monthly"),
    ("/services/ads/", 0.9, "monthly"),
    ("/services/automation/", 0.9, "monthly"),
    ("/services/crm-bi/", 0.9, "monthly"),
    ("/services/training/", 0.9, "monthly"),
    ("/services/smm/", 0.9, "monthly"),
    ("/services/", 0.85, "monthly"),
    ("/cases/", 0.8, "monthly"),
    ("/industries/", 0.8, "monthly"),
    ("/about/", 0.7, "monthly"),
    ("/contacts/", 0.7, "monthly"),
    ("/careers/", 0.6, "monthly"),
    ("/legal/privacy/", 0.3, "yearly"),
    ("/legal/terms/", 0.3, "yearly"),
]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, prio, freq in URLS:
    sm.append(f'  <url><loc>https://futureflow.ru{path}</loc><changefreq>{freq}</changefreq><priority>{prio}</priority></url>')
sm.append('</urlset>')
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sm))

print("done")
