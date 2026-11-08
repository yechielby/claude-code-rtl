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

/* End RTL Text Support for Claude Code VS Code / Cursor Extension */
"""

RTL_JS_CODE = """
/* RTL Toggle Button - Added by script */
(function() {
    var BTN_ID = 'yby-rtl-btn';
    var ROOT_CLASS = 'YBYrtl';

    /* The history and new-chat buttons in the header are rendered by the
       extension's shared icon-button component. Anchoring to the last of them
       puts our button in the same flex row, so nothing is pushed out of view. */
    function findAnchor() {
        var headers = document.querySelectorAll('[class*="header_"]');
        for (var i = 0; i < headers.length; i++) {
            var header = headers[i];
            /* Skip per-message headers, which carry icon buttons of their own. */
            if (header.closest('[class*="messagesContainer_"]')) continue;
            var buttons = header.querySelectorAll('[class*="iconButton_"]');
            if (buttons.length) return buttons[buttons.length - 1];
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
        btn.textContent = '\\u21C4';
        btn.title = 'Toggle RTL mode';
        btn.setAttribute('aria-label', 'Toggle RTL mode');
        btn.addEventListener('click', function() {
            var root = document.getElementById('root');
            if (!root) return;
            root.classList.toggle(ROOT_CLASS);
            paint(btn);
        });
        return btn;
    }

    function tryInsertButton() {
        if (document.getElementById(BTN_ID)) return;

        var anchor = findAnchor();
        var btn = makeButton();

        if (anchor) {
            /* Copy the neighbour's classes so size, padding, hover and colours
               match the native buttons exactly. */
            btn.className = anchor.className;
            anchor.parentNode.insertBefore(btn, anchor.nextSibling);
        } else {
            var header = document.querySelector('[class*="header_"]');
            if (!header) return;
            btn.classList.add('yby-standalone');
            header.appendChild(btn);
        }

        /* A re-render may have dropped an earlier button while RTL was on, so
           restore the pressed state from the root element rather than assuming
           the button starts off. */
        paint(btn);
    }

    /* React re-renders drop the button, so re-insert on mutation - but coalesce
       the many mutations a streaming reply fires into one check per frame. */
    var scheduled = false;
    function schedule() {
        if (scheduled) return;
        scheduled = true;
        requestAnimationFrame(function() {
            scheduled = false;
            tryInsertButton();
        });
    }

    new MutationObserver(schedule).observe(document.body, {
        childList: true,
        subtree: true
    });

    if (document.readyState !== 'loading') {
        tryInsertButton();
    } else {
        document.addEventListener('DOMContentLoaded', tryInsertButton);
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


def _has_marker(path, marker):
    if not path:
        return False
    try:
        return marker in _read(path)
    except Exception:
        return False


def is_rtl_installed(css_path):
    """Check if RTL CSS is already injected"""
    return _has_marker(css_path, RTL_START_MARKER)


def is_js_installed(js_path):
    """Check if RTL JS button is already injected"""
    return _has_marker(js_path, JS_START_MARKER)


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


def _inject(path, block, start_marker, end_marker, label, name):
    """Append block to path, or replace an outdated copy of it. Returns success."""
    try:
        content = _read(path)
        if start_marker in content:
            if block in content:
                print(f"  {label} Already up to date in {name}")
                return True
            # Injected by an older version of this script - swap in the current
            # block. The existing .bak still holds the untouched original.
            content = _strip_block(content, start_marker, end_marker)
            _write(path, content + "\n" + block)
            print(f"  {label} Updated to the latest version in {name}")
            return True

        backup_path = path + '.bak'
        if not os.path.exists(backup_path):
            shutil.copy2(path, backup_path)
            print(f"  {label} Backup created: {backup_path}")
        _write(path, content + "\n" + block)
        print(f"  {label} Added to {name}")
        return True
    except PermissionError:
        print(f"  {label} Permission denied: {path}")
        print(f"       Try running with elevated privileges")
    except Exception as e:
        print(f"  {label} Error: {e}")
    return False


def _remove(path, start_marker, end_marker, label, name):
    """Restore path from its .bak, or strip the block if that fails. Returns success."""
    if not _has_marker(path, start_marker):
        print(f"  {label} Not installed in {name}")
        return True

    backup_path = path + '.bak'
    if os.path.exists(backup_path):
        try:
            shutil.copy2(backup_path, path)
            os.remove(backup_path)
            print(f"  {label} Restored from backup: {name}")
            return True
        except Exception as e:
            print(f"  {label} Backup restore failed: {e}, trying manual removal...")

    try:
        _write(path, _strip_block(_read(path), start_marker, end_marker))
        print(f"  {label} Removed from {name}")
        return True
    except Exception as e:
        print(f"  {label} Error removing: {e}")
    return False


def add_rtl_support(ext_info):
    """Add RTL CSS and JS toggle button to a Claude Code extension. Returns success."""
    name = ext_info['name']
    ok = _inject(ext_info['css_path'], RTL_CSS_RULES,
                 RTL_START_MARKER, RTL_END_MARKER, "CSS:", name)
    if not ext_info['js_path']:
        print(f"  JS:  index.js not found, skipping button injection")
        return ok
    return _inject(ext_info['js_path'], RTL_JS_CODE,
                   JS_START_MARKER, JS_END_MARKER, "JS: ", name) and ok


def remove_rtl_support(ext_info):
    """Remove RTL CSS and JS toggle button from a Claude Code extension. Returns success."""
    name = ext_info['name']
    ok = _remove(ext_info['css_path'], RTL_START_MARKER, RTL_END_MARKER, "CSS:", name)
    if not ext_info['js_path']:
        return ok
    return _remove(ext_info['js_path'], JS_START_MARKER, JS_END_MARKER, "JS: ", name) and ok


def check_status(extensions):
    """Show status of all found extensions"""
    if not extensions:
        print("\nNo Claude Code extensions found!")
        return

    print(f"\nFound {len(extensions)} Claude Code extension(s):\n")
    for ext in extensions:
        css_installed = is_rtl_installed(ext['css_path'])
        js_installed = is_js_installed(ext['js_path'])
        css_backup = os.path.exists(ext['css_path'] + '.bak')
        js_backup = ext['js_path'] and os.path.exists(ext['js_path'] + '.bak')
        print(f"  {ext['name']}")
        print(f"    CSS: {'INSTALLED' if css_installed else 'Not installed'}  |  {'Backup exists' if css_backup else 'No backup'}")
        print(f"    JS:  {'INSTALLED' if js_installed else 'Not installed'}  |  {'Backup exists' if js_backup else 'No backup'}")
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
            input("\nPress Enter to exit...")
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
        choice = input("\n  Select option (1-4): ").strip()

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

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}")
        # Keep a double-clicked console window open, but never block a script.
        if len(sys.argv) == 1 and sys.stdin.isatty():
            input("Press Enter to close...")
        sys.exit(1)
