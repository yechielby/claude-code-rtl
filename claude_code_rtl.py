#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"Claude Code in VS Code" - RTL Text Support Script
Adds RTL (Right-to-Left) text support for the "Claude Code in VS Code" extension (works in VS Code, Cursor, and Kiro)

Approach:
  - Injects CSS into webview/index.css (RTL rules scoped to .YBYrtl class)
  - Injects JS  into webview/index.js  (toggle button that adds/removes .YBYrtl on #root)
"""

import os
import shutil
import sys
import platform
import glob
from pathlib import Path

RTL_CSS_RULES = """
/* RTL Text Support for Claude Code VS Code / Cursor Extension - Added by script */

/* ==========================================
   Toggle button - sits in the header next to
   the history / new-chat buttons
   ========================================== */

/* The button copies the class list of a neighbouring header button, so the
   extension's own rules supply the box model. Only the glyph and the state
   colours are set here - defining a width or padding would make the button
   wider than its neighbours and squeeze them out of a narrow panel. */
#yby-rtl-btn {
    font-size: 13px;
    font-weight: bold;
    line-height: 1;
    cursor: pointer;
    opacity: 0.7;
    transition: opacity 0.15s, background 0.15s;
}

/* Fallback box, applied only when no native header button was found to copy.
   Declared before the state rules below so those still win on equal
   specificity. */
#yby-rtl-btn.yby-standalone {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    padding: 4px;
    border: none;
    border-radius: 4px;
    background: transparent;
    color: var(--vscode-foreground);
    flex-shrink: 0;
}

#yby-rtl-btn:hover {
    opacity: 1;
    background: var(--app-hover-background, rgba(128, 128, 128, 0.15));
}

#yby-rtl-btn.yby-active {
    opacity: 1;
    background: var(--app-secondary-background, rgba(128, 128, 128, 0.3));
    color: var(--app-primary-foreground, var(--vscode-foreground));
}

/* ==========================================
   RTL - Hebrew/Arabic content (active when .YBYrtl is on #root)
   ========================================== */

/* Messages container + user messages */
.YBYrtl [class*="messagesContainer_"] {
    direction: rtl;
}

.YBYrtl [class*="userMessage_"],
.YBYrtl [class*="userMessageContainer_"] {
    direction: rtl;
    unicode-bidi: plaintext;
    text-align: right !important;
    align-items: flex-end !important;
    margin-left: auto !important;
    margin-right: 0 !important;
}

.YBYrtl [class*="content_"][class*="xGDvVg"],
.YBYrtl [class*="content_"] > span {
    unicode-bidi: plaintext;
}

/* Claude's markdown responses (excluding thinking block) */
.YBYrtl [class*="root_"]:not([class*="thinkingContent_"] [class*="root_"]) {
    direction: rtl;
    unicode-bidi: plaintext;
}

.YBYrtl [class*="root_"]:not([class*="thinkingContent_"] [class*="root_"]) > :is(p, ul, ol, h1, h2, h3, h4, blockquote),
.YBYrtl [class*="root_"]:not([class*="thinkingContent_"] [class*="root_"]) > :is(ul, ol) li {
    text-align: right;
}

.YBYrtl [class*="root_"]:not([class*="thinkingContent_"] [class*="root_"]) a {
    unicode-bidi: plaintext;
}

/* Question/answer blocks */
.YBYrtl [class*="questionBlock_"],
.YBYrtl [class*="questionHeader_"],
.YBYrtl [class*="answerText_"],
.YBYrtl [class*="optionText_"],
.YBYrtl [class*="optionContent_"] {
    direction: rtl;
    unicode-bidi: plaintext;
}

/* ==========================================
   LTR overrides - Code, Tools, UI
   ========================================== */

.YBYrtl [class*="slashCommandMessage_"],
.YBYrtl [class*="slashCommandResultMessage_"],
.YBYrtl [class*="header_"][class*="aqhumA"],
.YBYrtl [class*="sessionsButtonText_"],
.YBYrtl [class*="dotSuccess_"],
.YBYrtl [class*="dotFailure_"],
.YBYrtl [class*="dotProgress_"],
.YBYrtl [class*="dotWarning_"],
.YBYrtl [class*="progressContent_"],
.YBYrtl [class*="inputContainer_"][class*="cKsPxg"],
.YBYrtl [class*="messageInput_"],
.YBYrtl [class*="inputWrapper_"],
.YBYrtl [class*="iconButton_"],
.YBYrtl [class*="copyButton_"],
.YBYrtl [class*="actionButton_"],
.YBYrtl [class*="selectionAttachment_"],
.YBYrtl [class*="attachmentInfo_"],
.YBYrtl [class*="attachmentText_"],
.YBYrtl [class*="permissionRequest"],
.YBYrtl [class*="errorMessage_"],
.YBYrtl [class*="secondaryLine_"],
.YBYrtl [class*="todoListContainer_"],
.YBYrtl [class*="todoList_"],
.YBYrtl [class*="todoItem_"],
.YBYrtl [class*="auth_"],
.YBYrtl [class*="authUrl"] {
    direction: ltr !important;
}

/* Code blocks - LTR + alignment */
.YBYrtl pre,
.YBYrtl code,
.YBYrtl [class*="codeBlockWrapper_"] {
    direction: ltr !important;
    unicode-bidi: isolate !important;
    text-align: left !important;
}

/* Tool containers - LTR + alignment */
.YBYrtl [class*="toolUse_"],
.YBYrtl [class*="toolSummary_"],
.YBYrtl [class*="toolBody_"],
.YBYrtl [class*="toolBodyGrid_"],
.YBYrtl [class*="toolBodyRow_"],
.YBYrtl [class*="toolBodyRowContent_"],
.YBYrtl [class*="toolBodyRowLabel_"],
.YBYrtl [class*="toolResult_"],
.YBYrtl [class*="toolNameText_"],
.YBYrtl [class*="toolReference_"] {
    direction: ltr !important;
    unicode-bidi: isolate !important;
    text-align: left !important;
}

/* Thinking block - LTR + alignment */
.YBYrtl [class*="thinking_"],
.YBYrtl [class*="thinkingContent_"],
.YBYrtl [class*="thinkingContainer_"],
.YBYrtl [class*="thinkingHeader_"],
.YBYrtl [class*="spinnerRow_"],
.YBYrtl [class*="timelineMessage_"]:has([class*="thinking_"]) {
    direction: ltr !important;
    unicode-bidi: isolate !important;
    text-align: left !important;
}

.YBYrtl [class*="thinkingContent_"] [class*="root_"] :is(ul, ol, li) {
    direction: ltr !important;
    text-align: left !important;
}

/* ==========================================
   Translated menus and dialogs - the toggle script sets dir on them
   ========================================== */

/* The extension hard-codes left alignment on menu items */
[class*="popupOption_"][dir="rtl"] {
    text-align: right;
}

/* Agent map rows: the extension hard-codes left alignment, and indents the
   meta line on the left to sit under the title text */
[role="dialog"] [class*="row_"][dir="rtl"] {
    text-align: right;
}

[role="dialog"] [class*="row_"][dir="rtl"] [class*="rowMeta_"] {
    padding-left: 0;
    padding-right: 14px;
}

/* Agent map tree: the connector lines are placed with left offsets - mirror
   them so they still join the main row to its agents */
[role="dialog"][dir="rtl"] [class*="children_"] {
    margin-left: 0;
    margin-right: 32px;
}

[role="dialog"][dir="rtl"] [class*="children_"]::before {
    left: auto;
    right: -32px;
}

[role="dialog"][dir="rtl"] [class*="child_"]::before,
[role="dialog"][dir="rtl"] [class*="child_"]::after {
    left: auto;
    right: -16px;
}

[role="dialog"][dir="rtl"] [class*="rowMain_"]::after {
    left: auto;
    right: calc(100% + 1px);
}

/* Rewind dialog: file paths stay left-to-right */
[role="dialog"][dir="rtl"] [class*="fileItem_"] {
    direction: ltr;
    text-align: left;
}

/* End RTL Text Support for Claude Code VS Code / Cursor Extension */
"""

RTL_JS_CODE = r"""
/* RTL Toggle Button - Added by script */
(function() {
    var BTN_ID = 'yby-rtl-btn';
    var ROOT_CLASS = 'YBYrtl';
    var STORAGE_KEY = 'yby-rtl-enabled';

    /* ------------------------------------------------------------------
       Translation of fixed UI strings
       ------------------------------------------------------------------ */

    /* Applied only while RTL mode is on. The language follows the
       conversation: whichever of Arabic or Hebrew the user writes in. A string
       missing here, or reworded by an extension update, stays in English.
       Each language has one table per scope (see SCOPES). */
    var STRINGS = {
        ar: {
            ui: {
                /* Message action menu */
                'Fork conversation from here': 'تفريع المحادثة من هنا',
                'Rewind code to here': 'إرجاع الكود إلى هذه النقطة',
                'Fork conversation and rewind code': 'تفريع المحادثة وإرجاع الكود',
                /* Rewind confirmation dialog */
                'Rewind': 'إرجاع',
                'Rewind code': 'إرجاع الكود',
                'Fork and rewind': 'تفريع وإرجاع',
                'Restore': 'استعادة',
                'Continue': 'متابعة',
                'Never mind': 'إلغاء',
                'A new forked conversation will be created after rewinding.': 'ستُنشأ محادثة مفرّعة جديدة بعد الإرجاع.',
                'Checking code changes…': 'جارٍ فحص تغييرات الكود…',
                'Restored files go back whole, losing later changes by anyone. Bash changes to other files are not undone.':
                    'تُستعاد الملفات كاملة، فتضيع أي تغييرات لاحقة عليها مهما كان مصدرها. ولا تُلغى تغييرات أوامر Bash على الملفات الأخرى.',
                'Restore code and conversation': 'استعادة الكود والمحادثة',
                'Restore conversation': 'استعادة المحادثة',
                'Restore code': 'استعادة الكود',
                'The conversation will be forked.': 'ستُفرَّع المحادثة.',
                'The conversation will be forked. The code will be unchanged.': 'ستُفرَّع المحادثة، ولن يتغير الكود.',
                'The conversation will be unchanged.': 'لن تتغير المحادثة.',
                'The code ': 'الكود ',
                'has not changed': 'لم يتغير',
                ', so no code will be restored.': '، لذلك لن يُستعاد أي كود.',
                /* Agent map dialog */
                'Agent map': 'خريطة الوكلاء',
                'This session': 'هذه الجلسة'
            },
            /* "3 lines will be removed and 5 lines will be added across 2 files:" -
               the extension builds it from fragments around the numbers. */
            summary: {
                ' line': ' سطر',
                's': '',
                'will be removed and': 'سيُحذف و',
                'will be added across ': 'سيُضاف في ',
                ' file': ' ملف'
            },
            /* "10 agents · click an agent for details" */
            agents: {
                'agent': 'وكيل',
                'agents': 'وكلاء',
                ' · click an agent for details': ' · اضغط على وكيل لعرض تفاصيله'
            },
            /* "2m 23s · 80.0k tokens", "345.6k tokens in context" */
            tokens: [
                [/ tokens in context$/, ' توكن في السياق'],
                [/ tokens$/, ' توكن']
            ]
        },
        he: {
            ui: {
                'Fork conversation from here': 'פיצול השיחה מכאן',
                'Rewind code to here': 'החזרת הקוד לנקודה זו',
                'Fork conversation and rewind code': 'פיצול השיחה והחזרת הקוד',
                'Rewind': 'החזרה',
                'Rewind code': 'החזרת הקוד',
                'Fork and rewind': 'פיצול והחזרה',
                'Restore': 'שחזור',
                'Continue': 'המשך',
                'Never mind': 'ביטול',
                'A new forked conversation will be created after rewinding.': 'לאחר ההחזרה תיווצר שיחה מפוצלת חדשה.',
                'Checking code changes…': 'בודק שינויים בקוד…',
                'Restored files go back whole, losing later changes by anyone. Bash changes to other files are not undone.':
                    'קבצים משוחזרים חוזרים במלואם, וכל שינוי מאוחר יותר בהם יאבד, לא משנה מי ביצע אותו. שינויים של Bash בקבצים אחרים אינם מבוטלים.',
                'Restore code and conversation': 'שחזור הקוד והשיחה',
                'Restore conversation': 'שחזור השיחה',
                'Restore code': 'שחזור הקוד',
                'The conversation will be forked.': 'השיחה תפוצל.',
                'The conversation will be forked. The code will be unchanged.': 'השיחה תפוצל. הקוד לא ישתנה.',
                'The conversation will be unchanged.': 'השיחה לא תשתנה.',
                'The code ': 'הקוד ',
                'has not changed': 'לא השתנה',
                ', so no code will be restored.': ', ולכן שום קוד לא ישוחזר.',
                'Agent map': 'מפת סוכנים',
                'This session': 'הסשן הנוכחי'
            },
            summary: {
                ' line': ' שורות',
                's': '',
                'will be removed and': 'יוסרו ו-',
                'will be added across ': 'יתווספו ב-',
                ' file': ' קבצים'
            },
            agents: {
                'agent': 'סוכן',
                'agents': 'סוכנים',
                ' · click an agent for details': ' · לחצו על סוכן לפרטים'
            },
            tokens: [
                [/ tokens in context$/, ' טוקנים בהקשר'],
                [/ tokens$/, ' טוקנים']
            ]
        }
    };

    /* The only places text is ever replaced, each with the table it uses.
       Messages, code and file names are outside all of them. */
    var SCOPES = [
        ['[class*="popupOption_"]', 'ui'],
        ['[role="dialog"] h3', 'ui'],
        ['[role="dialog"] [class*="actions_"] button', 'ui'],
        ['[role="dialog"] [class*="forkNote_"]', 'ui'],
        ['[role="dialog"] [class*="loading_"]', 'ui'],
        ['[role="dialog"] [class*="warning_"]', 'ui'],
        ['[role="dialog"] [class*="choiceGroup_"]', 'ui'],
        ['[role="dialog"] [class*="noChanges_"]', 'ui'],
        ['[role="dialog"] [class*="summary_"]', 'summary'],
        ['[role="dialog"] [class*="subtitle_"]', 'agents'],
        ['[role="dialog"] [class*="rowMain_"] [class*="rowTitle_"]', 'ui'],
        ['[role="dialog"] [class*="rowMeta_"]', 'tokens']
    ];

    /* Dialogs whose layout follows the translation: right-to-left when
       translated, left-to-right otherwise (they would inherit RTL from the
       chat and scramble English text). Keyed by their English title. */
    var DIALOG_TITLES = {
        'Agent map': true,
        'Rewind': true,
        'Rewind code': true,
        'Fork and rewind': true
    };

    var WATCHED = '[class*="popupOption_"], [role="dialog"]';

    /* Text node -> {en, tr}: the English it had and what we replaced it with.
       Lets a node be translated again, or restored, without losing the
       original - and spots when the extension has written new text into it. */
    var originals = new WeakMap();
    var touched = false;

    function lookup(text, table) {
        if (Array.isArray(table)) {
            for (var i = 0; i < table.length; i++) {
                if (table[i][0].test(text)) return text.replace(table[i][0], table[i][1]);
            }
            return text;
        }
        if (Object.prototype.hasOwnProperty.call(table, text)) return table[text];
        /* Match ignoring surrounding whitespace, but keep that whitespace. */
        var m = /^(\s*)([\s\S]*?)(\s*)$/.exec(text);
        if (m[2] && Object.prototype.hasOwnProperty.call(table, m[2])) {
            return m[1] + table[m[2]] + m[3];
        }
        return text;
    }

    /* The English a text node holds, even if we have translated it. */
    function sourceOf(node) {
        var seen = originals.get(node);
        return seen && node.nodeValue === seen.tr ? seen.en : node.nodeValue;
    }

    function sourceText(el) {
        var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        var text = '', node;
        while ((node = walker.nextNode())) text += sourceOf(node);
        return text;
    }

    /* Translate el's text with table, or restore English when table is null.
       Only nodeValue is changed, so the extension keeps the same text nodes it
       rendered and can still update them. */
    function localizeTree(el, table) {
        var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
        var node;
        while ((node = walker.nextNode())) {
            var source = sourceOf(node);
            var text = table ? lookup(source, table) : source;
            if (text === node.nodeValue) continue;
            originals.set(node, { en: source, tr: text });
            node.nodeValue = text;
            touched = true;
        }
    }

    function localize(lang) {
        for (var i = 0; i < SCOPES.length; i++) {
            var table = lang ? STRINGS[lang][SCOPES[i][1]] : null;
            var els = document.querySelectorAll(SCOPES[i][0]);
            for (var j = 0; j < els.length; j++) localizeTree(els[j], table);
        }
    }

    /* Direction of the first letter in text: 'rtl', 'ltr', or null. */
    function textDir(text) {
        var m = /[A-Za-zÀ-ɏ֐-ࣿ]/.exec(text);
        if (!m) return null;
        return /[֐-ࣿ]/.test(m[0]) ? 'rtl' : 'ltr';
    }

    /* Set dir on an element, marking it so it can be cleaned up; null removes
       a dir this script set and leaves any other alone. */
    function setDir(el, dir) {
        if (!dir) {
            if (el.hasAttribute('data-yby-dir')) {
                el.removeAttribute('dir');
                el.removeAttribute('data-yby-dir');
            }
            return;
        }
        if (el.getAttribute('dir') !== dir) el.setAttribute('dir', dir);
        if (!el.hasAttribute('data-yby-dir')) el.setAttribute('data-yby-dir', '');
        touched = true;
    }

    function orient(on, lang) {
        var i;
        if (!on) {
            var marked = document.querySelectorAll('[data-yby-dir]');
            for (i = 0; i < marked.length; i++) setDir(marked[i], null);
            return;
        }
        var options = document.querySelectorAll('[class*="popupOption_"]');
        for (i = 0; i < options.length; i++) setDir(options[i], lang ? 'rtl' : null);

        var dialogs = document.querySelectorAll('[role="dialog"]');
        for (i = 0; i < dialogs.length; i++) {
            var title = dialogs[i].querySelector('h3');
            if (!title || !DIALOG_TITLES[sourceText(title).trim()]) continue;
            setDir(dialogs[i], lang ? 'rtl' : 'ltr');
            /* Agent rows hold free text (task names) - lay each one out in
               the direction of its own text. */
            var rows = dialogs[i].querySelectorAll('[class*="rowTitle_"]');
            for (var j = 0; j < rows.length; j++) {
                setDir(rows[j].parentNode, textDir(rows[j].textContent));
            }
        }
    }

    /* Arabic or Hebrew, by which script the user's messages use most; falls
       back to the editor's display language. Re-checked at most once a second. */
    var langCache = null, langCheckedAt = 0;
    function conversationLang() {
        var now = Date.now();
        if (now - langCheckedAt < 1000) return langCache;
        langCheckedAt = now;
        var text = '';
        var msgs = document.querySelectorAll('[class*="userMessage_"]');
        for (var i = 0; i < msgs.length; i++) text += msgs[i].textContent;
        var ar = (text.match(/[؀-ۿ]/g) || []).length;
        var he = (text.match(/[֐-׿]/g) || []).length;
        if (ar || he) {
            langCache = ar >= he ? 'ar' : 'he';
        } else {
            var ui = (navigator.language || '').slice(0, 2).toLowerCase();
            langCache = STRINGS[ui] ? ui : null;
        }
        return langCache;
    }

    /* ------------------------------------------------------------------
       RTL state and toggle button
       ------------------------------------------------------------------ */

    function loadState() {
        try { return localStorage.getItem(STORAGE_KEY) === '1'; } catch (e) { return false; }
    }

    function saveState(on) {
        try { localStorage.setItem(STORAGE_KEY, on ? '1' : '0'); } catch (e) { /* not available */ }
    }

    /* Skip headers that belong to a message or to a dialog. */
    function isMainHeader(header) {
        return !header.closest('[class*="messagesContainer_"], [role="dialog"]');
    }

    /* The history and new-chat buttons in the header are rendered by the
       extension's shared icon-button component. Anchoring to the last of them
       puts our button in the same flex row, so nothing is pushed out of view. */
    function findAnchor() {
        var headers = document.querySelectorAll('[class*="header_"]');
        for (var i = 0; i < headers.length; i++) {
            if (!isMainHeader(headers[i])) continue;
            var buttons = headers[i].querySelectorAll('[class*="iconButton_"]');
            if (buttons.length) return buttons[buttons.length - 1];
        }
        return null;
    }

    function findHeader() {
        var headers = document.querySelectorAll('[class*="header_"]');
        for (var i = 0; i < headers.length; i++) {
            if (isMainHeader(headers[i])) return headers[i];
        }
        return null;
    }

    function isRtlOn() {
        var root = document.getElementById('root');
        return !!root && root.classList.contains(ROOT_CLASS);
    }

    function paint(btn) {
        var active = isRtlOn();
        btn.classList.toggle('yby-active', active);
        btn.setAttribute('aria-pressed', active ? 'true' : 'false');
    }

    function makeButton() {
        var btn = document.createElement('button');
        btn.id = BTN_ID;
        btn.type = 'button';
        btn.textContent = '⇄';
        btn.title = 'Toggle RTL mode';
        btn.setAttribute('aria-label', 'Toggle RTL mode');
        btn.addEventListener('click', function() {
            var root = document.getElementById('root');
            if (!root) return;
            root.classList.toggle(ROOT_CLASS);
            saveState(root.classList.contains(ROOT_CLASS));
            paint(btn);
            schedule();
        });
        return btn;
    }

    function tryInsertButton() {
        var existing = document.getElementById(BTN_ID);
        var anchor;
        if (existing) {
            /* A fallback button moves next to the native ones once they
               render; otherwise it would stay in the fallback spot for good. */
            if (!existing.classList.contains('yby-standalone')) return;
            anchor = findAnchor();
            if (!anchor) return;
            existing.parentNode.removeChild(existing);
        } else {
            anchor = findAnchor();
        }

        var btn = makeButton();
        if (anchor) {
            /* Copy the neighbour's classes so size, padding, hover and colours
               match the native buttons exactly. */
            btn.className = anchor.className;
            anchor.parentNode.insertBefore(btn, anchor.nextSibling);
        } else {
            var header = findHeader();
            if (!header) return;
            btn.classList.add('yby-standalone');
            header.appendChild(btn);
        }

        /* A re-render may have dropped an earlier button while RTL was on, so
           restore the pressed state from the root element rather than assuming
           the button starts off. */
        paint(btn);
    }

    /* Turn RTL back on if it was on last time. Returns false until #root exists. */
    function restoreState() {
        var root = document.getElementById('root');
        if (!root) return false;
        if (loadState()) root.classList.add(ROOT_CLASS);
        return true;
    }

    var restored = restoreState();

    function update() {
        if (!restored) restored = restoreState();
        tryInsertButton();
        if (!document.querySelector(WATCHED)) return;
        var on = isRtlOn();
        if (!on && !touched) return;
        var lang = on ? conversationLang() : null;
        localize(lang);
        orient(on, lang);
    }

    /* React re-renders drop the button and bring back English text, so check
       again on mutation - but coalesce the many mutations a streaming reply
       fires into one check per frame. */
    var scheduled = false;
    function schedule() {
        if (scheduled) return;
        scheduled = true;
        requestAnimationFrame(function() {
            scheduled = false;
            update();
        });
    }

    new MutationObserver(schedule).observe(document.body, {
        childList: true,
        characterData: true,
        subtree: true
    });

    if (document.readyState !== 'loading') {
        update();
    } else {
        document.addEventListener('DOMContentLoaded', update);
    }
})();
/* End RTL Toggle Button */
"""

# Markers to identify injected CSS
RTL_START_MARKER = "/* RTL Text Support for Claude Code VS Code / Cursor Extension - Added by script */"
RTL_END_MARKER = "/* End RTL Text Support for Claude Code VS Code / Cursor Extension */"

# Markers to identify injected JS
JS_START_MARKER = "/* RTL Toggle Button - Added by script */"
JS_END_MARKER = "/* End RTL Toggle Button */"

# Every (start, end) pair a block may carry, current one first. Markers written
# by earlier versions of this script stay listed so an old install is still
# detected, upgraded and removed.
CSS_MARKERS = [
    (RTL_START_MARKER, RTL_END_MARKER),
    ("/* RTL Text Support for Claude Code VS Code Extension - Added by script */",
     "/* End RTL Text Support for Claude Code VS Code Extension */"),
]
JS_MARKERS = [(JS_START_MARKER, JS_END_MARKER)]


def _is_wsl():
    """Detect if running inside Windows Subsystem for Linux"""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except Exception:
        return False


def _get_wsl_windows_homes():
    """Get Windows user home directories accessible from WSL (e.g. /mnt/c/Users/John)"""
    homes = []
    # Check common mount points for Windows drives
    for drive_letter in ('c', 'd'):
        users_dir = f"/mnt/{drive_letter}/Users"
        if not os.path.isdir(users_dir):
            continue
        try:
            for entry in os.listdir(users_dir):
                if entry.lower() in ("public", "default", "default user", "all users"):
                    continue
                user_home = os.path.join(users_dir, entry)
                if os.path.isdir(user_home):
                    homes.append(user_home)
        except PermissionError:
            continue
    return homes


# Editor data directories that may contain a Claude Code extension install.
# Each editor has a local dir and a remote counterpart (VS Code Remote / WSL / SSH).
EDITOR_LABELS = {
    ".vscode": "VS Code",
    ".vscode-server": "VS Code (Remote)",
    ".cursor": "Cursor",
    ".cursor-server": "Cursor (Remote)",
    ".kiro": "Kiro",
    ".kiro-server": "Kiro (Remote)",
}
EDITOR_DIRS = tuple(EDITOR_LABELS)


def _extension_dirs(home):
    """Extension search paths for every supported editor under a home directory"""
    return [os.path.join(home, editor, "extensions") for editor in EDITOR_DIRS]


def _editor_label(ext_path):
    """Name of the editor an extension directory belongs to"""
    for part in os.path.normpath(ext_path).replace(os.sep, "/").lower().split("/"):
        if part in EDITOR_LABELS:
            return EDITOR_LABELS[part]
    return "Unknown editor"


def _get_wsl_linux_homes():
    """Get Linux home directories inside WSL distros, accessible from Windows via \\\\wsl$\\"""
    homes = []
    skip_users = {"root"}
    # Try both UNC paths that Windows uses to access WSL filesystems
    for wsl_root in (r"\\wsl$", r"\\wsl.localhost"):
        try:
            distros = os.listdir(wsl_root)
        except (OSError, PermissionError):
            continue
        for distro in distros:
            home_dir = os.path.join(wsl_root, distro, "home")
            if not os.path.isdir(home_dir):
                continue
            try:
                for user in os.listdir(home_dir):
                    if user in skip_users:
                        continue
                    user_home = os.path.join(home_dir, user)
                    if os.path.isdir(user_home):
                        homes.append(user_home)
            except (OSError, PermissionError):
                continue
        # Both UNC roots expose the same distros - one working root is enough,
        # otherwise every WSL extension would be discovered twice.
        if homes:
            break
    return homes


def find_claude_extensions():
    """Find all installed Claude Code extension directories"""
    system = platform.system().lower()
    wsl = system == "linux" and _is_wsl()

    search_dirs = []

    if system == "windows":
        userprofile = os.getenv("USERPROFILE")
        if userprofile:
            search_dirs.extend(_extension_dirs(userprofile))

        # Also search inside WSL distros (\\wsl$\Ubuntu\home\user\...)
        for wsl_home in _get_wsl_linux_homes():
            search_dirs.extend(_extension_dirs(wsl_home))
    elif system == "darwin":
        home = str(Path.home())
        search_dirs.extend(_extension_dirs(home))
    elif system == "linux":
        home = str(Path.home())
        search_dirs.extend(_extension_dirs(home))

        # Also search other users' home directories (e.g. running as root)
        if os.path.isdir("/home"):
            try:
                for user in os.listdir("/home"):
                    user_home = os.path.join("/home", user)
                    if user_home == home or not os.path.isdir(user_home):
                        continue
                    search_dirs.extend(_extension_dirs(user_home))
            except PermissionError:
                pass

        # WSL: also search Windows-side VS Code extensions
        if wsl:
            for win_home in _get_wsl_windows_homes():
                search_dirs.extend(_extension_dirs(win_home))

    # Homes can overlap between roots; keep first occurrence of each path
    search_dirs = list(dict.fromkeys(search_dirs))

    found = []
    for ext_dir in search_dirs:
        if not os.path.exists(ext_dir):
            continue
        # Find all anthropic.claude-code-* directories
        pattern = os.path.join(ext_dir, "anthropic.claude-code-*")
        matches = glob.glob(pattern)
        for match in sorted(matches):
            css_path = os.path.join(match, "webview", "index.css")
            js_path = os.path.join(match, "webview", "index.js")
            if os.path.exists(css_path):
                found.append({
                    'dir': match,
                    'css_path': css_path,
                    'js_path': js_path if os.path.exists(js_path) else None,
                    'name': _editor_label(match) + " - " + os.path.basename(match)
                })

    return found


def _read(path):
    # newline='' keeps the file's own line endings; text mode would otherwise
    # rewrite every LF in the bundle as CRLF on Windows.
    with open(path, 'r', encoding='utf-8', newline='') as f:
        return f.read()


def _write(path, content):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(content)


def _contains_block(content, markers):
    return any(start in content for start, _ in markers)


def _has_marker(path, markers):
    if not path:
        return False
    try:
        return _contains_block(_read(path), markers)
    except Exception:
        return False


def is_rtl_installed(css_path):
    """Check if RTL CSS is already injected (by this or an older version)"""
    return _has_marker(css_path, CSS_MARKERS)


def is_js_installed(js_path):
    """Check if RTL JS button is already injected (by this or an older version)"""
    return _has_marker(js_path, JS_MARKERS)


def _install_state(path, block, markers):
    """'installed', 'outdated' or 'missing' for one injected file"""
    try:
        content = _read(path) if path else ""
    except Exception:
        return "missing"
    if not _contains_block(content, markers):
        return "missing"
    clean, ok = _strip_blocks(content, markers)
    return "installed" if ok and clean + "\n" + block == content else "outdated"


def _strip_block(content, start_marker, end_marker):
    """Remove a marked block from content string"""
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return content
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        return content
    end_idx += len(end_marker)
    # _inject appends "\n" + block, and each block opens and closes with a
    # newline - take those back too so a strip leaves the file as it was.
    for _ in range(2):
        if start_idx > 0 and content[start_idx - 1] == '\n':
            start_idx -= 1
    if content[end_idx:end_idx + 1] == '\n':
        end_idx += 1
    return content[:start_idx] + content[end_idx:]


def _strip_blocks(content, markers):
    """Remove every marked block, current or legacy, including duplicates.

    Returns (content, ok). ok is False when a start marker has no end marker
    after it: the block's extent is unknown, so nothing can be cut safely.
    """
    for start, end in markers:
        while start in content:
            stripped = _strip_block(content, start, end)
            if stripped == content:
                return content, False
            content = stripped
    return content, True


def _report_damaged(path, label, name):
    print(f"  {label} The injected block in {name} is damaged (its end marker is missing)")
    print(f"       Reinstall the Claude Code extension to get a clean {os.path.basename(path)}")


def _inject(path, block, markers, label, name):
    """Append block to path, replacing any older copy of it. Returns success."""
    try:
        content = _read(path)
        clean, ok = _strip_blocks(content, markers)
        if not ok:
            _report_damaged(path, label, name)
            return False
        patched = clean + "\n" + block
        if patched == content:
            print(f"  {label} Already up to date in {name}")
            return True

        # The backup must hold the unpatched file. Earlier versions could copy
        # an already patched file into it, so such a backup is replaced too.
        backup_path = path + '.bak'
        if not os.path.exists(backup_path) or _has_marker(backup_path, markers):
            _write(backup_path, clean)
            print(f"  {label} Backup created: {backup_path}")

        _write(path, patched)
        if clean == content:
            print(f"  {label} Added to {name}")
        else:
            print(f"  {label} Updated to the latest version in {name}")
        return True
    except PermissionError:
        print(f"  {label} Permission denied: {path}")
        print(f"       Try running with elevated privileges")
    except Exception as e:
        print(f"  {label} Error: {e}")
    return False


def _remove(path, markers, label, name):
    """Restore path from its .bak, or strip the block if that fails. Returns success."""
    if not _has_marker(path, markers):
        print(f"  {label} Not installed in {name}")
        return True

    backup_path = path + '.bak'
    backup_clean = os.path.exists(backup_path) and not _has_marker(backup_path, markers)
    if backup_clean:
        try:
            shutil.copy2(backup_path, path)
            os.remove(backup_path)
            print(f"  {label} Restored from backup: {name}")
            return True
        except Exception as e:
            print(f"  {label} Backup restore failed: {e}, trying manual removal...")

    try:
        clean, ok = _strip_blocks(_read(path), markers)
        if not ok:
            _report_damaged(path, label, name)
            return False
        _write(path, clean)
        # A backup that itself holds the patch would only bring it back later.
        if os.path.exists(backup_path) and not backup_clean:
            os.remove(backup_path)
        print(f"  {label} Removed from {name}")
        return True
    except Exception as e:
        print(f"  {label} Error removing: {e}")
    return False


def add_rtl_support(ext_info):
    """Add RTL CSS and JS toggle button to a Claude Code extension. Returns success."""
    name = ext_info['name']
    ok = _inject(ext_info['css_path'], RTL_CSS_RULES, CSS_MARKERS, "CSS:", name)
    if not ext_info['js_path']:
        print(f"  JS:  index.js not found, skipping button injection")
        return ok
    return _inject(ext_info['js_path'], RTL_JS_CODE, JS_MARKERS, "JS: ", name) and ok


def remove_rtl_support(ext_info):
    """Remove RTL CSS and JS toggle button from a Claude Code extension. Returns success."""
    name = ext_info['name']
    ok = _remove(ext_info['css_path'], CSS_MARKERS, "CSS:", name)
    if not ext_info['js_path']:
        return ok
    return _remove(ext_info['js_path'], JS_MARKERS, "JS: ", name) and ok


def check_status(extensions):
    """Show status of all found extensions"""
    if not extensions:
        print("\nNo Claude Code extensions found!")
        return

    labels = {
        "installed": "INSTALLED",
        "outdated": "OUTDATED (run --apply to update)",
        "missing": "Not installed",
    }
    print(f"\nFound {len(extensions)} Claude Code extension(s):\n")
    for ext in extensions:
        css_state = _install_state(ext['css_path'], RTL_CSS_RULES, CSS_MARKERS)
        js_state = _install_state(ext['js_path'], RTL_JS_CODE, JS_MARKERS)
        css_backup = os.path.exists(ext['css_path'] + '.bak')
        js_backup = ext['js_path'] and os.path.exists(ext['js_path'] + '.bak')
        print(f"  {ext['name']}")
        print(f"    CSS: {labels[css_state]}  |  {'Backup exists' if css_backup else 'No backup'}")
        print(f"    JS:  {labels[js_state]}  |  {'Backup exists' if js_backup else 'No backup'}")
        print(f"    Path: {ext['css_path']}")
        print()


def show_menu():
    print("\n" + "=" * 63)
    print("  Claude Code in VS Code - RTL Text Support (+ Cursor + Kiro)")
    print("=" * 63)
    print("  1. Add RTL support (all versions)")
    print("  2. Remove RTL support (all versions)")
    print("  3. Check status")
    print("  4. Exit")
    print("=" * 63)


USAGE = "Usage: python claude_code_rtl.py [--apply | --remove | --status]"


def _pause(prompt):
    """Wait for Enter in an interactive console; never block or fail a script."""
    if not sys.stdin.isatty():
        return
    try:
        input(prompt)
    except EOFError:
        pass


def _run_all(action, verb, extensions):
    """Run action on every extension. Returns True only if all succeeded."""
    print(f"\n{verb} RTL support...\n")
    results = [action(ext) for ext in extensions]
    print("\nRestart VS Code / Cursor / Kiro / reload window to see changes!")
    return all(results)


def main():
    """Returns the process exit code."""
    args = sys.argv[1:]
    flag = args[0] if args else None
    if len(args) > 1 or flag not in (None, "--apply", "--remove", "--status"):
        print(USAGE)
        return 0 if flag in ("-h", "--help") else 2

    system_info = f"{platform.system()} {platform.release()}"
    if _is_wsl():
        system_info += " (WSL)"
    print(f"System: {system_info}")

    extensions = find_claude_extensions()

    if not extensions:
        print("\nNo Claude Code extensions found!")
        print("Make sure the 'Claude Code in VS Code' extension is installed in VS Code, Cursor, or Kiro.")
        if not flag:
            _pause("\nPress Enter to exit...")
        return 1

    print(f"Found {len(extensions)} extension(s)")

    if flag == "--apply":
        return 0 if _run_all(add_rtl_support, "Adding", extensions) else 1
    if flag == "--remove":
        return 0 if _run_all(remove_rtl_support, "Removing", extensions) else 1
    if flag == "--status":
        check_status(extensions)
        return 0

    while True:
        show_menu()
        try:
            choice = input("\n  Select option (1-4): ").strip()
        except EOFError:
            # Input ran out (e.g. piped) - nothing more to do.
            return 0

        if choice == "1":
            _run_all(add_rtl_support, "Adding", extensions)

        elif choice == "2":
            _run_all(remove_rtl_support, "Removing", extensions)

        elif choice == "3":
            check_status(extensions)

        elif choice == "4":
            print("\nGoodbye!")
            return 0
        else:
            print("\nInvalid choice")

        _pause("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        # Keep a double-clicked console window open, but never block a script.
        if len(sys.argv) == 1:
            _pause("Press Enter to close...")
        sys.exit(1)
