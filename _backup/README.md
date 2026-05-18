# Бэкап сайта FutureFlow перед редизайном (2026-05-18)

Снимок текущей версии сайта futureflow.ru до запуска нового редизайна
(SEO-усиление, 3D/AI видео-генерация, светлая/тёмная тема).

## Как откатиться

### Вариант 1 — целиком на снимок (рекомендуется)
```
git checkout main
git reset --hard backup/pre-redesign-2026-05-18
git push --force-with-lease origin main
```

### Вариант 2 — переключиться на ветку-бэкап
```
git checkout backup/site-pre-redesign
git push -u origin backup/site-pre-redesign
```

### Вариант 3 — взять файлы из папки `_backup/`
```
cp _backup/index.html ./index.html
cp -r _backup/careers ./careers
cp _backup/CNAME ./CNAME
git add -A && git commit -m "Откат на бэкап от 2026-05-18"
```

## Что входит
- `index.html` — главная (3006 строк)
- `careers/index.html` — страница вакансий (698 строк)
- `CNAME` — домен `futureflow.ru`

## Git-метки
- Тег: `backup/pre-redesign-2026-05-18`
- Ветка: `backup/site-pre-redesign`
