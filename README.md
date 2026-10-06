# BioForge

یه ابزار خط فرمانی برای پردازش توالی‌های DNA با پایتون. یه فایل FASTA می‌گیره، توالی‌ها رو اعتبارسنجی می‌کنه، تو هر ۶ تا reading frame دنبال ORF می‌گرده، ترجمه‌شون می‌کنه به پروتئین، فیلترشون می‌کنه و آخرش یه گزارش و لاگ تحویل می‌ده.

```
FASTA → Parsing → Validation → ORF Detection → Translation → Filtering → Annotation → Reporting → Logging
```

## فهرست

- [نصب و اجرا](#نصب-و-اجرا)
- [ساختار پروژه](#ساختار-پروژه)
- [ورودی و خروجی](#ورودی-و-خروجی)
- [رفتار برنامه](#رفتار-برنامه)
- [طراحی و OOP](#طراحی-و-oop)
- [تصمیم‌های طراحی](#تصمیم‌های-طراحی)

## اجرا

برنامه رو از **داخل پوشه‌ی `BioForge`** اجرا کن — چون مسیر `data/` نسبت به پوشه‌ی جاری حساب می‌شه:

```bash
git clone https://github.com/titiianna/BioForge.git
cd BioForge
python main.py --input input/input.fasta --out output/ --min-length 4 --min-weight 500
```

هر چهار تا آرگومان اجبارین:

| آرگومان | توضیح |
|---|---|
| `--input` | مسیر فایل FASTA |
| `--out` | پوشه‌ی خروجی (اگه نباشه ساخته می‌شه) |
| `--min-length` | حداقل طول پروتئین؛ فقط اونایی می‌مونن که `طول >= ورودی` باشه |
| `--min-weight` | حداقل وزن مولکولی؛ فقط اونایی می‌مونن که `وزن >= ورودی` باشه |

## ساختار پروژه

```
BioForge/
├── main.py          # CLI و هماهنگ‌کننده‌ی مراحل
├── parsers.py       # خواندن FASTA (read_fasta, FastaRecord)
├── models.py        # DNASequence, ORF, DataDirLoad
├── pipeline.py      # پیدا کردن ORF، ترجمه، فیلتر، Annotation
├── filters.py       # BaseFilter, LengthFilter, WeightFilter
├── report.py        # نوشتن report.txt
├── logger.py        # لاگ
├── exceptions.py    # اکسپشن‌های سفارشی
├── data/
│   ├── codon_table.txt
│   └── amino_weights.txt
├── input/
│   └── input.fasta
└── output/          # خروجی‌ها (report.txt و bioforge.log)
```

## ورودی و خروجی

### ورودی

یه فایل FASTA چندرکوردی. هر رکورد شامل ID (اولین تکه‌ی Header)، Description (بقیه‌ش) و Sequence هست. اگه تو Description چیزی مثل `organism=...` باشه، استخراج می‌شه و تو گزارش کنار ID میاد. خطوط خالی نادیده گرفته می‌شن و حروف کوچیک هم قبولن (خودشون به بزرگ تبدیل می‌شن).

### خروجی

- **`output/report.txt`** — برای هر رکورد، ORFهایی که از فیلتر رد شدن: ID، Strand، Frame، Start Position، وضعیت (Complete / Incomplete) و Protein.
- **`output/bioforge.log`** — لاگ اجرا. به صورت **Append** باز می‌شه، یعنی اجرای بعدی لاگ قبلی رو پاک نمی‌کنه. Warning و Error هم تو فایل میان هم رو کنسول.

### نمونه

ورودی:

```
>seq001 organism=E_coli sample=A
ATGCTTTCATAG

>seq002 organism=Human sample=B
CCCATGGGGTAA
```

اجرا با `--min-length 1 --min-weight 0`، خروجی `report.txt`:

```
Report
===================
Record: seq001 (organism=E_coli)
ID Strand Frame Start Status Protein
BFG_001 Forward 0 1 Complete MLS
BFG_002 Reverse 2 10 InComplete MKA

Record: seq002 (organism=Human)
ID Strand Frame Start Status Protein
BFG_003 Forward 0 4 Complete MG
BFG_004 Reverse 1 5 InComplete M
```

## رفتار برنامه

### Parsing

چندرکورد، خط خالی و حروف کوچیک پشتیبانی می‌شن. فایل خالی، Sequence قبل از اولین `>`، Header خالی و Header بدون Sequence با `FastaFormatError` رد می‌شن. اگه ID تکراری باشه تو `main.py` یه Warning تو لاگ ثبت می‌شه ولی رکورد حذف نمی‌شه.

### Validation

توالی فقط می‌تونه `A`, `C`, `G`, `T` داشته باشه. هر چیز دیگه → `InvalidSequenceError`. توالی **هیچ‌وقت** خودکار اصلاح نمی‌شه (نه حذف، نه جایگزینی). رکوردی که توالی نامعتبر داره تو لاگ ثبت و رد می‌شه، ولی بقیه‌ی رکوردها ادامه پیدا می‌کنن.

### ORF Detection

- هر ۳ تا Frame (0, 1, 2) رو Strand اصلی (Forward) و روی Reverse Complement (Reverse) — جمعاً ۶ تا.
- ORF از `AUG` شروع می‌شه و کدون‌ها سه‌تا سه‌تا تو همون Frame خونده می‌شن تا به `UAA`، `UAG` یا `UGA` برسن. Stop از خود `codon_table.txt` تشخیص داده می‌شه (مقدار `*`).
- اگه Stop تو همون Frame پیدا نشه، ORF حذف نمی‌شه و به عنوان **Incomplete** ثبت می‌شه (`complete_incomplete = False`).
- بعد از یه ORF کامل، جست‌وجو تو همون Frame از کدون بعد از Stop ادامه پیدا می‌کنه. یعنی `AUG`هایی که داخل یه ORF هستن، ORF جدا حساب نمی‌شن.

### مختصات (Start Position)

- **۱-مبناست** (اولین نوکلئوتید شماره‌ی ۱).
- **Forward:** موقعیت `A` تو `AUG` روی DNA اصلی.
- **Reverse:** موقعیت روی Reverse Complement به مختصات DNA اصلی تبدیل می‌شه (`طول توالی - موقعیت ۰-مبنا`). این همون نوکلئوتیدی از DNA اصلیه که مکمل `A` تو `AUG`ه (انتهای `CAT` تو توالی اصلی).
- `Frame` برای Reverse نسبت به Reverse Complement شمرده می‌شه.

### Translation

جدول کدون از `data/codon_table.txt` خونده می‌شه، تو کد hardcode نشده. Stop Codon هیچ‌وقت وارد پروتئین نمی‌شه — مثلاً برای `AUG GCU AAA UGA CCU` خروجی `MAK`ه.

### Filtering

- `LengthFilter`: `len(protein) >= min_length`
- `WeightFilter`: `sum(وزن residueها) + 18.015 >= min_weight`؛ وزن‌ها از `data/amino_weights.txt`.

یه ORF فقط وقتی تو خروجی می‌مونه که از **همه‌ی** فیلترها رد بشه.

### Annotation

ORFهای نهایی (بعد از فیلتر) به ترتیب `BFG_001`, `BFG_002`, … می‌گیرن. شمارنده بین رکوردها ادامه پیدا می‌کنه و هر اجرا از ۱ شروع می‌شه.

### مدیریت خطا

```
BioForgeError
├── FastaFormatError      # خطای ساختار FASTA
├── InvalidSequenceError  # DNA نامعتبر
└── DataFileError         # خطای فایل‌های data (با شماره‌ی خط خراب)
```

- فایل‌ها با `with open(..., encoding="utf-8")` باز می‌شن.
- فایل FASTA ناموجود یا خالی، و Data File ناموجود یا خراب مدیریت می‌شن و تو لاگ میان.
- خطای یه رکورد (توالی نامعتبر) کل Pipeline رو متوقف نمی‌کنه.

## طراحی و OOP

### چرا کلاس؟

| کلاس | دلیل |
|---|---|
| `DNASequence` | داده (رشته‌ی توالی) و رفتارهای مربوط بهش (`validate`, `complement`, `reverse_complement`, `to_rna`, `gc_content`) کنار هم. اعتبارسنجی تو سازنده انجام می‌شه، پس هیچ‌وقت یه `DNASequence` نامعتبر تو برنامه وجود نداره. |
| `FastaRecord` | سه بخش ID، Description و Sequence یه رکورد رو کنار هم نگه می‌داره. |
| `ORF` | یه ظرف داده برای اطلاعات هر ORF (Protein, Strand, Frame, Start, Complete) که بین Pipeline، فیلترها و گزارش دست‌به‌دست می‌شه. |
| `BaseFilter` / `LengthFilter` / `WeightFilter` | هر فیلتر State داره (`min_length`، `min_weight` و جدول وزن‌ها) و همه یه رابط مشترک دارن (`filter(orf)`). |
| `Pipeline` | جدول کدون، لیست فیلترها و شمارنده‌ی Annotation رو به عنوان State نگه می‌داره و مراحل ORF → Translation → Filter → Annotation رو انجام می‌ده. |
| `DataDirLoad` | دو تا تابع بارگذاری فایل‌های data رو یه جا جمع می‌کنه (با `@staticmethod`، بدون State). |
| سلسله‌مراتب `BioForgeError` | می‌شه همه‌ی خطاها رو با یه `except BioForgeError` گرفت و در عین حال نوع خطا رو تفکیک کرد. |

### چرا فانکشن؟

| فانکشن | دلیل |
|---|---|
| `read_fasta` | فقط مسیر فایل (و logger) می‌گیره و لیست رکورد برمی‌گردونه؛ بین فراخوانی‌ها State نداره. |
| `_add_record` | یه مرحله‌ی کوچیک و بدون State (ساخت رکورد، و ثبت تو لاگ اگه توالی نامعتبر بود). |
| `get_organism` | پردازش یه رشته‌ی Description؛ ورودی ← خروجی، بدون State. |
| `get_args` | فقط `argparse` رو راه‌اندازی می‌کنه. |
| `setup_logging` | یه‌بار تو شروع اجرا صدا زده می‌شه و logger رو برمی‌گردونه. |
| `write_report` | لیست نتایج و مسیر رو می‌گیره و فایل می‌نویسه؛ State نداره. |
| `main` | ترتیب مراحل رو هماهنگ می‌کنه. |

### مفاهیم OOP

- **Encapsulation:** منطق اعتبارسنجی و تبدیل‌های DNA داخل `DNASequence` پنهانه و بیرون فقط متدها رو صدا می‌زنه. جزئیات داخلی `Pipeline` (`_translator_codon`, `_passes_filters`) و `_add_record` با پیشوند `_` به عنوان Private علامت‌گذاری شدن (به قرارداد پایتون). جزئیات خوندن و اعتبارسنجی فایل‌های data داخل `DataDirLoad`ه و بیرون فقط دیکشنری نهایی رو می‌گیره.
- **Inheritance:** `LengthFilter` و `WeightFilter` از `BaseFilter` ارث می‌برن؛ `FastaFormatError`، `InvalidSequenceError` و `DataFileError` از `BioForgeError`.
- **Polymorphism:** `Pipeline` یه لیست از فیلترها داره و بدون اینکه نوع هرکدوم رو بدونه `f.filter(orf)` رو صدا می‌زنه. اضافه کردن فیلتر جدید نیازی به تغییر `Pipeline` نداره.
- **Composition:** `FastaRecord` یه `DNASequence` تو خودش داره؛ `Pipeline` جدول کدون و لیست فیلترها رو تو خودش داره؛ `main` هم فیلترها رو می‌سازه و به `Pipeline` می‌ده.

## تصمیم‌های طراحی

1. **اعتبارسنجی تو سازنده‌ی `DNASequence`.** به جای اینکه هرکس توالی رو می‌گیره خودش چک کنه، شیء نامعتبر اصلاً ساخته نمی‌شه. بقیه‌ی کد (ORF، Reverse Complement) می‌تونه فرض کنه ورودی فقط `ACGT`ه. طبق سند، توالی نامعتبر خودکار اصلاح نمی‌شه و `InvalidSequenceError` می‌ده.

2. **رکورد نامعتبر Log و رد می‌شه، ولی خطای ساختاری FASTA اجرا رو متوقف می‌کنه.** سند می‌گه در صورت امکان یه رکورد خراب نباید کل Pipeline رو متوقف کنه؛ پس `_add_record` خطای `InvalidSequenceError` رو می‌گیره و تو لاگ می‌نویسه. خطاهای ساختاری (فایل خالی، Sequence قبل از Header، Header بدون Sequence) نشون می‌دن خود فایل مشکل داره، پس با `FastaFormatError` متوقف می‌شه.

3. **`logger` به صورت پارامتر به `read_fasta` داده می‌شه** (Dependency Injection) به جای اینکه `parsers.py` خودش logger بسازه یا با یه اسم رشته‌ای پیداش کنه. وابستگی صریحه، به یه اسم ثابت وابسته نیستیم و تستش راحت‌تره.

4. **فیلترها Class با رابط مشترکن.** هر فیلتر پارامتر خودش رو داره و `Pipeline` فقط `filter(orf)` رو می‌شناسه. اضافه کردن فیلتر جدید (مثلاً فیلتر روی Strand) فقط یه کلاس جدید می‌خواد. فیلترها تو `main` ساخته می‌شن چون مقدارشون از CLI میاد.

5. **داده‌های زیستی Hardcode نشدن.** جدول کدون و وزن آمینواسیدها تو زمان اجرا از `data/` خونده می‌شن. تشخیص Stop Codon هم از خود جدول (`*`) انجام می‌شه، نه از لیست ثابت تو کد. خط خراب تو این فایل‌ها `DataFileError` با شماره‌ی خط می‌ده.

6. **`Pipeline` همه‌ی مراحل ORF تا Annotation رو نگه می‌داره.** تو این مقیاس کوچیک، جدا کردن هر مرحله به یه کلاس جداگانه Over-Engineering بود. فقط چیزهایی که State دارن (جدول کدون، فیلترها، شمارنده) تو `Pipeline` هستن و بقیه‌ی کارها فانکشن‌های ساده‌ان.

7. **Annotation بعد از Filter انجام می‌شه.** پس شناسه‌های `BFG_xxx` پشت‌سرهم و بدون شکاف هستن و فقط برای ORFهای نهایی میان.

8. **تبدیل مختصات Reverse داخل `find_orfs`.** موقعیت روی Reverse Complement فوراً به مختصات DNA اصلی تبدیل می‌شه تا هیچ بخشی از برنامه با مختصات نسبت به Strand معکوس سروکار نداشته باشه.

9. **آداپتور برای گزارش (`prepare_for_report`).** `report.py` اسم‌های `sequence_id` و `is_complete` رو انتظار داره، در حالی که مدل‌ها `id` و `complete_incomplete` دارن. به جای تغییر مدل‌ها، `main.py` این دو تا attribute رو قبل از گزارش اضافه می‌کنه. اگه اسم‌ها یکی بشن این تابع حذف می‌شه.
