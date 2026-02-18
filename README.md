# Claude Code RTL - תמיכה בעברית ל-VS Code

<div dir="rtl">

## תיאור

כלי Python שמוסיף תמיכה ב-RTL (Right-to-Left) לפלאגין **Claude Code for VS Code**, מאפשר עבודה נוחה עם שפות עברית וערבית בצ'אט של Claude.

## מה הכלי עושה?

הסקריפט מבצע את הפעולות הבאות:
1. **מאתר אוטומטית** את תיקיות ההתקנה של Claude Code (תומך ב-Windows, macOS ו-Linux)
2. **מזריק CSS** - מוסיף כללי עיצוב שהופכים את הטקסט לכיווניות RTL
3. **מוסיף כפתור Toggle** - יוצר כפתור (`ע`) בממשק להפעלה/כיבוי של מצב RTL
4. **שומר גיבויים** - יוצר עותקי גיבוי של הקבצים המקוריים לפני כל שינוי
5. **מאפשר הסרה** - אפשרות לשחזר את המצב המקורי בקלות

## דרישות מערכת

- **Python 3.6+**
- **Claude Code for VS Code** - חייב להיות מותקן
- הרשאות לכתיבה לתיקיית ההרחבות (במקרה של Windows עשוי להידרש הרצה כמנהל)

## התקנה ושימוש

### שלב 1: הורדה
```bash
git clone https://github.com/YOUR_USERNAME/claude-code-rtl.git
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
=========================================================
  Claude Code for VS Code - RTL Text Support
=========================================================
  1. Add RTL support (all versions)
  2. Remove RTL support (all versions)
  3. Check status
  4. Exit
=========================================================
```

1. **הוספת תמיכה ב-RTL** - בחר אפשרות `1`
2. **הסרת תמיכה ב-RTL** - בחר אפשרות `2`
3. **בדיקת סטטוס** - בחר אפשרות `3` לראות האם RTL מותקן

### שלב 4: אתחול VS Code

לאחר ביצוע השינויים:
- **סגור וטען מחדש** את חלון VS Code (או לחץ `Ctrl+Shift+P` → `Developer: Reload Window`)
- הכפתור `ע` יופיע בממשק הצ'אט של Claude

## איך להשתמש?

1. פתח את פאנל הצ'אט של Claude Code ב-VS Code
2. לחץ על הכפתור **ע** בראש הצ'אט
3. הממשק יעבור למצב RTL - טקסט יישר לימין
4. לחץ שוב על הכפתור כדי לחזור למצב LTR

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
4. אתחל את VS Code

## מבנה הפרויקט

```
claude-code-rtl/
├── claude_code_rtl.py    # הסקריפט הראשי
└── README.md             # מדריך זה
```

## פתרון בעיות

### הסקריפט לא מוצא את הפלאגין
- **וודא שהפלאגין מותקן**: Extensions → חפש "Claude Code"
- **נסה הרצה כמנהל** (Windows): לחץ ימני → Run as Administrator

### השינויים לא נראים
- **אתחל את VS Code**: סגור לחלוטין ופתח מחדש
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
- **VS Code Extensions API** - אינטגרציה עם הפלאגין

## תרומה לפרויקט

נשמח לתרומות! אפשר:
- 🐛 **לדווח על באגים** - פתח Issue
- ✨ **להציע פיצ'רים** - פתח Issue עם הצעה
- 🔧 **לשלוח Pull Request** - שפר את הקוד

## רישיון

פרויקט זה מופץ תחת רישיון MIT - ראה קובץ LICENSE לפרטים.

## יוצר

נוצר כדי לאפשר למשתמשי עברית וערבית לעבוד בצורה נוחה עם Claude Code ב-VS Code.

## קישורים

- [Claude Code for VS Code](https://marketplace.visualstudio.com/items?itemName=Anthropic.claude-code)
- [VS Code](https://code.visualstudio.com/)

---

**אם הכלי עזר לך, תן ⭐ לפרויקט!**

</div>
