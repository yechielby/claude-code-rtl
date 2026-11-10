# Claude Code in VS Code - RTL Support for Hebrew & Arabic (+ Cursor + Kiro)

**Fixes reversed text and alignment issues in the "Claude Code in VS Code" extension for Hebrew and Arabic users. Works in VS Code, Cursor, and Kiro.**

---

## 🌍 בחר שפה | اختر اللغة

| 🇮🇱 עברית | 🇸🇦 العربية |
|:---:|:---:|
| [לקרוא בעברית ↓](#עברית) | [اقرأ بالعربية ↓](#عربية) |

---

## ✨ Key Features

- **Automatic RTL Detection** - Automatically detects Hebrew and Arabic text and applies right-to-left formatting
- **VS Code, Cursor & Kiro Support** - Works with the "Claude Code in VS Code" extension in all three editors
- **Zero Configuration** - Works out of the box with a simple toggle button (⇄) in the chat interface
- **Smart Text Handling** - Keeps code blocks and technical content in LTR for proper readability
- **Remembers Your Choice** - RTL mode stays on after reloading the window or restarting the editor
- **Translated Menus** - While RTL mode is on, the message menu (fork / rewind), the rewind confirmation dialog and the Agent map are shown in Arabic or Hebrew - whichever language you write in
- **Backup & Restore** - Automatically creates backups before modifications, easy rollback available
- **Safe Upgrades** - Detects installs made by older versions of the script and replaces them cleanly

---

## 🤔 Why This is Needed

The "Claude Code in VS Code" extension doesn't natively support RTL text direction. This causes:
- ❌ Hebrew and Arabic text appearing reversed and misaligned
- ❌ Chat conversations becoming hard to read for RTL language users
- ❌ Inconsistent text direction mixing with code blocks

**This tool solves these issues** by injecting CSS and JavaScript that intelligently handles RTL text while preserving code block formatting and maintaining compatibility with all versions of Claude Code.

---

## 🎯 Key Solutions

- **Fixes Text Reversal** - Ensures Hebrew and Arabic characters appear in the correct order and alignment
- **Terminal Alignment** - Automatically adjusts text direction in the Claude Code chat panel
- **Claude Code Integration** - Specifically tailored for the "Claude Code in VS Code" extension (works in Cursor and Kiro too)
- **Non-Invasive** - Works by extending the existing UI without modifying core functionality

---

## 🚀 Quick Start

```bash
git clone https://github.com/yechielby/claude-code-rtl.git
cd claude-code-rtl
python claude_code_rtl.py            # interactive menu
python claude_code_rtl.py --apply    # add RTL to every install (or update an older one)
python claude_code_rtl.py --remove   # remove RTL and restore the original files
python claude_code_rtl.py --status   # INSTALLED / OUTDATED / Not installed
```

Then reload the editor window (`Ctrl+Shift+P` → `Developer: Reload Window`) and click **⇄** at the top of the Claude Code chat.

### Translated menus

While RTL mode is on, the fixed English strings of these parts of the UI are translated:

- The menu on a message: *Fork conversation from here*, *Rewind code to here*, *Fork conversation and rewind code*
- The rewind confirmation dialog (title, buttons, notes)
- The Agent map dialog (title, subtitle, token counts)

The language is picked from your messages in the conversation: Arabic if you write in Arabic, Hebrew if you write in Hebrew. Text written by Claude (such as agent task names) is never translated. Turning RTL off brings the English back. If a Claude Code update rewords one of these strings, it simply stays in English.

### Running the tests

```bash
python -m unittest
```

---

<a name="עברית"></a>

<div dir="rtl" lang="he">

## 🇮🇱 עברית

### תיאור

כלי Python שמוסיף תמיכה ב-RTL (Right-to-Left) לתוסף **"Claude Code in VS Code"**, מאפשר עבודה נוחה עם שפות עברית וערבית בצ'אט של Claude. עובד ב-VS Code, ב-Cursor וגם ב-Kiro.

## מה הכלי עושה?

הסקריפט מבצע את הפעולות הבאות:
1. **מאתר אוטומטית** את תיקיות ההתקנה של Claude Code (תומך ב-VS Code, Cursor ו-Kiro על Windows, macOS ו-Linux)
2. **מזריק CSS** - מוסיף כללי עיצוב שהופכים את הטקסט לכיווניות RTL
3. **מוסיף כפתור Toggle** - יוצר כפתור (`⇄`) בממשק להפעלה/כיבוי של מצב RTL. הבחירה נשמרת גם אחרי טעינה מחדש של החלון
4. **מתרגם תפריטים** - במצב RTL, התפריט של הודעה, חלון אישור ההחזרה ו-Agent map מוצגים בעברית או בערבית
5. **שומר גיבויים** - יוצר עותקי גיבוי של הקבצים המקוריים לפני כל שינוי
6. **מאפשר הסרה** - אפשרות לשחזר את המצב המקורי בקלות

## דרישות מערכת

- **Python 3.6+**
- **"Claude Code in VS Code"** - התוסף חייב להיות מותקן (ב-VS Code או ב-Cursor או ב-Kiro)
- הרשאות לכתיבה לתיקיית ההרחבות (במקרה של Windows עשוי להידרש הרצה כמנהל)

## התקנה ושימוש

### שלב 1: הורדה
```bash
git clone https://github.com/yechielby/claude-code-rtl.git
cd claude-code-rtl
```

### שלב 2: הרצת הסקריפט

#### Windows
```cmd
python claude_code_rtl.py
```

#### macOS/Linux
```bash
python3 claude_code_rtl.py
```

### שלב 3: תפריט אינטראקטיבי

לאחר הרצת הסקריפט יופיע תפריט:

```
===============================================================
  Claude Code in VS Code - RTL Text Support (+ Cursor + Kiro)
===============================================================
  1. Add RTL support (all versions)
  2. Remove RTL support (all versions)
  3. Check status
  4. Exit
===============================================================
```

1. **הוספת תמיכה ב-RTL** - בחר אפשרות `1`
2. **הסרת תמיכה ב-RTL** - בחר אפשרות `2`
3. **בדיקת סטטוס** - בחר אפשרות `3` לראות האם RTL מותקן

#### הרצה בלי תפריט (שורת פקודה)

```bash
python claude_code_rtl.py --apply    # הוספת RTL לכל ההתקנות (או עדכון לגרסה האחרונה)
python claude_code_rtl.py --remove   # הסרת RTL ושחזור הקבצים המקוריים
python claude_code_rtl.py --status   # הצגת הסטטוס
```

הסקריפט מחזיר קוד יציאה `0` בהצלחה, `1` אם משהו נכשל או שלא נמצאה התקנה, ו-`2` לפרמטר לא מוכר.

> **שים לב:** עדכון של Claude Code מותקן בתיקייה חדשה ללא RTL - הרץ `--apply` שוב אחרי כל עדכון.

> **שדרוג מגרסה קודמת של הסקריפט:** `--status` יציג `OUTDATED` להתקנה ישנה. הרץ `--apply` והסקריפט יחליף אותה בגרסה החדשה, כולל התקנות שבוצעו בגרסה הראשונה.

### שלב 4: אתחול VS Code / Cursor / Kiro

לאחר ביצוע השינויים:
- **סגור וטען מחדש** את חלון VS Code / Cursor / Kiro (או לחץ `Ctrl+Shift+P` → `Developer: Reload Window`)
- הכפתור `⇄` יופיע בממשק הצ'אט של Claude

## איך להשתמש?

1. פתח את פאנל הצ'אט של Claude Code ב-VS Code / Cursor / Kiro
2. לחץ על הכפתור **⇄** בראש הצ'אט
3. הממשק יעבור למצב RTL - טקסט יישר לימין
4. לחץ שוב על הכפתור כדי לחזור למצב LTR

המצב נשמר: אם השארת את RTL פעיל, הוא יופעל שוב אוטומטית אחרי טעינה מחדש של החלון.

## תרגום תפריטים

במצב RTL, הטקסטים הקבועים באנגלית בחלקים הבאים מתורגמים:
- התפריט של הודעה: *Fork conversation from here*, *Rewind code to here*, *Fork conversation and rewind code*
- חלון אישור ההחזרה (Rewind) - כותרת, כפתורים והערות
- חלון Agent map - כותרת, שורת המשנה ומספר הטוקנים

השפה נבחרת לפי ההודעות שלך בשיחה: עברית אם אתה כותב בעברית, ערבית אם בערבית. טקסט ש-Claude כתב (כמו שמות המשימות של הסוכנים) לא מתורגם. כיבוי מצב RTL מחזיר את האנגלית. אם עדכון של Claude Code משנה את הניסוח של אחד הטקסטים, הוא פשוט יישאר באנגלית.

## מה משתנה במצב RTL?

### מה הופך ל-RTL:
- ✅ הודעות המשתמש
- ✅ תשובות של Claude (טקסט רגיל)
- ✅ רשימות ופסקאות
- ✅ שאלות ותשובות בממשק

### מה נשאר LTR:
- ✅ קוד (code blocks)
- ✅ כלים (tools) ותוצאותיהם
- ✅ בלוק Thinking
- ✅ פקודות slash
- ✅ כפתורים וממשק

## הסרת התמיכה ב-RTL

אם ברצונך להסיר את השינויים:
1. הרץ את הסקריפט שוב
2. בחר אפשרות `2` מהתפריט
3. הסקריפט ישחזר את הקבצים המקוריים מהגיבוי
4. אתחל את VS Code / Cursor / Kiro

## מבנה הפרויקט

```
claude-code-rtl/
├── claude_code_rtl.py        # הסקריפט הראשי
├── test_claude_code_rtl.py   # בדיקות (python -m unittest)
└── README.md                 # מדריך זה
```

## פתרון בעיות

### הסקריפט לא מוצא את הפלאגין
- **וודא שהפלאגין מותקן**: Extensions → חפש "Claude Code"
- **נסה הרצה כמנהל** (Windows): לחץ ימני → Run as Administrator

### השינויים לא נראים
- **אתחל את VS Code / Cursor / Kiro**: סגור לחלוטין ופתח מחדש
- **או טען חלון מחדש**: `Ctrl+Shift+P` → `Developer: Reload Window`

### שגיאת הרשאות (Permission Denied)
- **Windows**: הרץ את CMD/PowerShell כמנהל
- **macOS/Linux**: השתמש ב-`sudo python3 claude_code_rtl.py`

### RTL לא עובד טוב
- **נקה מטמון**: `Ctrl+Shift+P` → `Developer: Reload Window`
- **בדוק גרסה**: הסקריפט תומך בגרסאות עדכניות של Claude Code

## טכנולוגיות

- **Python 3** - שפת הסקריפט
- **CSS** - כללי עיצוב RTL
- **JavaScript** - לוגיקת כפתור ההחלפה
- **VS Code / Cursor / Kiro Extensions** - אינטגרציה עם התוסף

## תרומה לפרויקט

נשמח לתרומות! אפשר:
- 🐛 **לדווח על באגים** - פתח Issue
- ✨ **להציע פיצ'רים** - פתח Issue עם הצעה
- 🔧 **לשלוח Pull Request** - שפר את הקוד

## רישיון

פרויקט זה מופץ תחת רישיון MIT - ראה קובץ [LICENSE](LICENSE) לפרטים.

## יוצר

נוצר כדי לאפשר למשתמשי עברית וערבית לעבוד בצורה נוחה עם התוסף "Claude Code in VS Code" (ב-VS Code, ב-Cursor וב-Kiro).

## קישורים

- [Claude Code for VS Code](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code)
- [VS Code](https://code.visualstudio.com/)
- [Cursor](https://cursor.com/)
- [Kiro](https://kiro.dev/)

---

**אם הכלי עזר לך, תן ⭐ לפרויקט!**

</div>

---

<a name="عربية"></a>

<div dir="rtl" lang="ar">

## 🇸🇦 عربية

### الوصف

أداة Python تضيف دعم RTL (من اليمين إلى اليسار) لإضافة **"Claude Code in VS Code"**، مما يتيح العمل بسهولة مع اللغات العربية والعبرية في محادثة Claude. تعمل في VS Code و Cursor و Kiro.

## ماذا تفعل الأداة؟

يقوم البرنامج بتنفيذ العمليات التالية:
1. **يحدد تلقائيًا** مجلدات تثبيت Claude Code (يدعم VS Code و Cursor و Kiro على Windows و macOS و Linux)
2. **يحقن CSS** - يضيف قواعد تصميم تحول النص إلى اتجاه RTL
3. **يضيف زر Toggle** - ينشئ زرًا (`⇄`) في الواجهة لتفعيل/إيقاف وضع RTL، ويتذكّر اختيارك حتى بعد إعادة تحميل النافذة
4. **يعرّب القوائم** - في وضع RTL تظهر قائمة الرسالة ونافذة تأكيد الإرجاع ونافذة Agent map بالعربية أو العبرية
5. **يحفظ نسخًا احتياطية** - ينشئ نسخًا احتياطية من الملفات الأصلية قبل أي تعديل
6. **يسمح بالإزالة** - خيار لاستعادة الحالة الأصلية بسهولة

## متطلبات النظام

- **Python 3.6+**
- **"Claude Code in VS Code"** - يجب أن يكون مثبتًا (في VS Code أو Cursor أو Kiro)
- صلاحيات الكتابة لمجلد الإضافات (في حالة Windows قد يتطلب التشغيل كمسؤول)

## التثبيت والاستخدام

### الخطوة 1: التنزيل
```bash
git clone https://github.com/yechielby/claude-code-rtl.git
cd claude-code-rtl
```

### الخطوة 2: تشغيل البرنامج

#### Windows
```cmd
python claude_code_rtl.py
```

#### macOS/Linux
```bash
python3 claude_code_rtl.py
```

### الخطوة 3: القائمة التفاعلية

بعد تشغيل البرنامج ستظهر قائمة:

```
===============================================================
  Claude Code in VS Code - RTL Text Support (+ Cursor + Kiro)
===============================================================
  1. Add RTL support (all versions)
  2. Remove RTL support (all versions)
  3. Check status
  4. Exit
===============================================================
```

1. **إضافة دعم RTL** - اختر الخيار `1`
2. **إزالة دعم RTL** - اختر الخيار `2`
3. **فحص الحالة** - اختر الخيار `3` لمعرفة ما إذا كان RTL مثبتًا

#### التشغيل بدون قائمة (سطر الأوامر)

```bash
python claude_code_rtl.py --apply    # إضافة RTL لكل التثبيتات (أو التحديث لأحدث إصدار)
python claude_code_rtl.py --remove   # إزالة RTL واستعادة الملفات الأصلية
python claude_code_rtl.py --status   # عرض الحالة
```

يُرجع البرنامج رمز خروج `0` عند النجاح، و`1` إذا فشل شيء أو لم يُعثر على أي تثبيت، و`2` لمعامل غير معروف.

> **ملاحظة:** تحديث Claude Code يُثبَّت في مجلد جديد بدون RTL - شغّل `--apply` مرة أخرى بعد كل تحديث.

> **الترقية من إصدار قديم من البرنامج:** يُظهر `--status` الحالة `OUTDATED` للتثبيت القديم. شغّل `--apply` وسيستبدله البرنامج بالإصدار الجديد، بما في ذلك التثبيتات التي تمت بالإصدار الأول.

### الخطوة 4: إعادة تشغيل VS Code / Cursor / Kiro

بعد إجراء التغييرات:
- **أغلق وأعد تحميل** نافذة VS Code / Cursor / Kiro (أو اضغط `Ctrl+Shift+P` → `Developer: Reload Window`)
- سيظهر الزر `⇄` في واجهة محادثة Claude

## كيفية الاستخدام؟

1. افتح لوحة محادثة Claude Code في VS Code / Cursor / Kiro
2. اضغط على الزر **⇄** في أعلى المحادثة
3. ستتحول الواجهة إلى وضع RTL - سيتم محاذاة النص إلى اليمين
4. اضغط على الزر مرة أخرى للعودة إلى وضع LTR

يُحفظ الوضع تلقائيًا: إذا تركت RTL مفعّلًا، سيعود مفعّلًا بعد إعادة تحميل النافذة.

## تعريب القوائم

في وضع RTL تُترجم النصوص الإنجليزية الثابتة في الأجزاء التالية:
- قائمة الرسالة: *Fork conversation from here* و*Rewind code to here* و*Fork conversation and rewind code*
- نافذة تأكيد الإرجاع (Rewind): العنوان والأزرار والملاحظات
- نافذة Agent map: العنوان والسطر الفرعي وعدد التوكنات

تُختار اللغة حسب رسائلك في المحادثة: العربية إذا كنت تكتب بالعربية، والعبرية إذا كنت تكتب بالعبرية. النصوص التي يكتبها Claude (مثل أسماء مهام الوكلاء) لا تُترجم. إيقاف وضع RTL يعيد النصوص الإنجليزية. وإذا غيّر تحديث من Claude Code صياغة أحد هذه النصوص، فسيظهر بالإنجليزية فقط دون أي عطل.

## ماذا يتغير في وضع RTL؟

### ما يتحول إلى RTL:
- ✅ رسائل المستخدم
- ✅ إجابات Claude (نص عادي)
- ✅ القوائم والفقرات
- ✅ الأسئلة والأجوبة في الواجهة

### ما يبقى LTR:
- ✅ الكود (code blocks)
- ✅ الأدوات (tools) ونتائجها
- ✅ كتلة Thinking
- ✅ أوامر slash
- ✅ الأزرار والواجهة

## إزالة دعم RTL

إذا كنت ترغب في إزالة التغييرات:
1. شغّل البرنامج مرة أخرى
2. اختر الخيار `2` من القائمة
3. سيستعيد البرنامج الملفات الأصلية من النسخة الاحتياطية
4. أعد تشغيل VS Code / Cursor / Kiro

## هيكل المشروع

```
claude-code-rtl/
├── claude_code_rtl.py        # البرنامج الرئيسي
├── test_claude_code_rtl.py   # الاختبارات (python -m unittest)
└── README.md                 # هذا الدليل
```

## حل المشاكل

### البرنامج لا يجد الإضافة
- **تأكد من تثبيت الإضافة**: Extensions → ابحث عن "Claude Code"
- **جرب التشغيل كمسؤول** (Windows): انقر بزر الماوس الأيمن → Run as Administrator

### التغييرات لا تظهر
- **أعد تشغيل VS Code / Cursor / Kiro**: أغلق تمامًا وافتح من جديد
- **أو أعد تحميل النافذة**: `Ctrl+Shift+P` → `Developer: Reload Window`

### خطأ في الصلاحيات (Permission Denied)
- **Windows**: شغّل CMD/PowerShell كمسؤول
- **macOS/Linux**: استخدم `sudo python3 claude_code_rtl.py`

### RTL لا يعمل بشكل جيد
- **امسح الذاكرة المؤقتة**: `Ctrl+Shift+P` → `Developer: Reload Window`
- **تحقق من الإصدار**: يدعم البرنامج الإصدارات الحديثة من Claude Code

## التقنيات

- **Python 3** - لغة البرنامج
- **CSS** - قواعد تصميم RTL
- **JavaScript** - منطق زر التبديل
- **VS Code / Cursor / Kiro Extensions** - التكامل مع الإضافة

## المساهمة في المشروع

نرحب بالمساهمات! يمكنك:
- 🐛 **الإبلاغ عن الأخطاء** - افتح Issue
- ✨ **اقتراح ميزات** - افتح Issue مع الاقتراح
- 🔧 **إرسال Pull Request** - حسّن الكود

## الترخيص

يتم توزيع هذا المشروع تحت ترخيص MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## المؤلف

تم إنشاؤه لتمكين مستخدمي العربية والعبرية من العمل بشكل مريح مع إضافة "Claude Code in VS Code" (في VS Code و Cursor و Kiro).

## الروابط

- [Claude Code for VS Code](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code)
- [VS Code](https://code.visualstudio.com/)
- [Cursor](https://cursor.com/)
- [Kiro](https://kiro.dev/)

---

**إذا ساعدتك الأداة، امنح المشروع ⭐!**

</div>

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Contributing & Support:** Contributions, bug reports, and feature requests are welcome! Please open an Issue or Pull Request on GitHub.
