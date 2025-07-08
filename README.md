**task_workmate**

Тестовое задание для workmate

**Установка**

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/EugenePycharm/task_workmate.git
   ```

2. Перейдите в директорию проекта:

   ```bash
   cd task_workmate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```


**## Запуск тестов**

Запустите тесты из корневой папки программы:

```bash
python -m pytest tests/ -v
```


**## Использование**

Перейдите в директорию `csv_processor`:

```bash
cd csv_processor
```

Запустите CLI с параметрами:

```bash
py .\cli.py test.csv [--where "условие"] [--aggregate "агрегация"] [--order "сортировка"]
```

**Пример использования:**

```bash
py .\cli.py test.csv --order-by "rating=asc" --where "rating>4.4"
```
