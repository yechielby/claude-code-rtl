#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"Claude Code in VS Code" - RTL Text Support Script
Adds RTL (Right-to-Left) text support for the "Claude Code in VS Code" extension (works in VS Code and Cursor)

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
   Toggle button - always visible
   ========================================== */

#yby-rtl-btn {
    font-size: 14px;
    font-weight: bold;
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    background: transparent;
    color: var(--vscode-foreground);
    opacity: 0.5;
    transition: opacity 0.2s, background 0.2s;
    flex-shrink: 0;
}

#yby-rtl-btn:hover {
    opacity: 1;
}

#yby-rtl-btn.yby-active {
    opacity: 1;
    background: var(--vscode-button-background, rgba(128, 128, 128, 0.3));
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

    function tryInsertButton() {
        if (document.getElementById(BTN_ID)) return;
        var header = document.querySelector('[class*="header_"]');
        if (!header) return;

        var btn = document.createElement('button');
        btn.id = BTN_ID;
        btn.textContent = '\\u21C4';
        btn.title = 'Toggle RTL mode';

        btn.addEventListener('click', function() {
            var root = document.getElementById('root');
            if (!root) return;
            var isActive = root.classList.toggle(ROOT_CLASS);
            btn.classList.toggle('yby-active', isActive);
        });

        header.appendChild(btn);
    }

    // Wait for React to render the header
    var observer = new MutationObserver(function() {
        tryInsertButton();
    });
    observer.observe(document.body, { childList: true, subtree: true });

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
    return homes


def find_claude_extensions():
    """Find all installed Claude Code extension directories"""
    system = platform.system().lower()
    wsl = system == "linux" and _is_wsl()

    search_dirs = []

    if system == "windows":
        userprofile = os.getenv("USERPROFILE")
        if userprofile:
            search_dirs.append(os.path.join(userprofile, ".vscode", "extensions"))
            search_dirs.append(os.path.join(userprofile, ".vscode-server", "extensions"))
            search_dirs.append(os.path.join(userprofile, ".cursor", "extensions"))
            search_dirs.append(os.path.join(userprofile, ".cursor-server", "extensions"))

        # Also search inside WSL distros (\\wsl$\Ubuntu\home\user\...)
        for wsl_home in _get_wsl_linux_homes():
            search_dirs.append(os.path.join(wsl_home, ".vscode-server", "extensions"))
            search_dirs.append(os.path.join(wsl_home, ".cursor-server", "extensions"))
    elif system == "darwin":
        home = str(Path.home())
        search_dirs.append(os.path.join(home, ".vscode", "extensions"))
        search_dirs.append(os.path.join(home, ".vscode-server", "extensions"))
        search_dirs.append(os.path.join(home, ".cursor", "extensions"))
        search_dirs.append(os.path.join(home, ".cursor-server", "extensions"))
    elif system == "linux":
        home = str(Path.home())
        search_dirs.append(os.path.join(home, ".vscode", "extensions"))
        search_dirs.append(os.path.join(home, ".vscode-server", "extensions"))
        search_dirs.append(os.path.join(home, ".cursor", "extensions"))
        search_dirs.append(os.path.join(home, ".cursor-server", "extensions"))

        # Also search other users' home directories (e.g. running as root)
        if os.path.isdir("/home"):
            try:
                for user in os.listdir("/home"):
                    user_home = os.path.join("/home", user)
                    if user_home == home or not os.path.isdir(user_home):
                        continue
                    search_dirs.append(os.path.join(user_home, ".vscode", "extensions"))
                    search_dirs.append(os.path.join(user_home, ".vscode-server", "extensions"))
                    search_dirs.append(os.path.join(user_home, ".cursor", "extensions"))
                    search_dirs.append(os.path.join(user_home, ".cursor-server", "extensions"))
            except PermissionError:
                pass

        # WSL: also search Windows-side VS Code extensions
        if wsl:
            for win_home in _get_wsl_windows_homes():
                search_dirs.append(os.path.join(win_home, ".vscode", "extensions"))
                search_dirs.append(os.path.join(win_home, ".vscode-server", "extensions"))
                search_dirs.append(os.path.join(win_home, ".cursor", "extensions"))
                search_dirs.append(os.path.join(win_home, ".cursor-server", "extensions"))

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
                    'name': os.path.basename(match)
                })

    return found


def is_rtl_installed(css_path):
    """Check if RTL CSS is already injected"""
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return RTL_START_MARKER in content
    except Exception:
        return False


def is_js_installed(js_path):
    """Check if RTL JS button is already injected"""
    if not js_path:
        return False
    try:
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return JS_START_MARKER in content
    except Exception:
        return False


def add_rtl_support(ext_info):
    """Add RTL CSS and JS toggle button to a Claude Code extension"""
    css_path = ext_info['css_path']
    js_path = ext_info['js_path']

    # --- CSS ---
    if is_rtl_installed(css_path):
        print(f"  CSS: RTL already installed in {ext_info['name']}")
    else:
        try:
            backup_path = css_path + '.bak'
            if not os.path.exists(backup_path):
                shutil.copy2(css_path, backup_path)
                print(f"  CSS: Backup created: {backup_path}")

            with open(css_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(content + "\n" + RTL_CSS_RULES)

            print(f"  CSS: RTL support added to {ext_info['name']}")
        except PermissionError:
            print(f"  CSS: Permission denied: {css_path}")
            print(f"       Try running with elevated privileges")
        except Exception as e:
            print(f"  CSS: Error: {e}")

    # --- JS ---
    if not js_path:
        print(f"  JS:  index.js not found, skipping button injection")
        return

    if is_js_installed(js_path):
        print(f"  JS:  Button already installed in {ext_info['name']}")
    else:
        try:
            backup_path = js_path + '.bak'
            if not os.path.exists(backup_path):
                shutil.copy2(js_path, backup_path)
                print(f"  JS:  Backup created: {backup_path}")

            with open(js_path, 'r', encoding='utf-8') as f:
                content = f.read()
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(content + "\n" + RTL_JS_CODE)

            print(f"  JS:  Toggle button added to {ext_info['name']}")
        except PermissionError:
            print(f"  JS:  Permission denied: {js_path}")
            print(f"       Try running with elevated privileges")
        except Exception as e:
            print(f"  JS:  Error: {e}")


def _strip_block(content, start_marker, end_marker):
    """Remove a marked block from content string"""
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        return content
    end_idx += len(end_marker)
    if start_idx > 0 and content[start_idx - 1] == '\n':
        start_idx -= 1
    return content[:start_idx] + content[end_idx:]


def remove_rtl_support(ext_info):
    """Remove RTL CSS and JS toggle button from a Claude Code extension"""
    css_path = ext_info['css_path']
    js_path = ext_info['js_path']

    # --- CSS ---
    if not is_rtl_installed(css_path):
        print(f"  CSS: RTL not installed in {ext_info['name']}")
    else:
        backup_path = css_path + '.bak'
        restored = False
        if os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, css_path)
                os.remove(backup_path)
                print(f"  CSS: Restored from backup: {ext_info['name']}")
                restored = True
            except Exception as e:
                print(f"  CSS: Backup restore failed: {e}, trying manual removal...")

        if not restored:
            try:
                with open(css_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                cleaned = _strip_block(content, RTL_START_MARKER, RTL_END_MARKER)
                with open(css_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                print(f"  CSS: RTL removed from {ext_info['name']}")
            except Exception as e:
                print(f"  CSS: Error removing RTL: {e}")

    # --- JS ---
    if not js_path or not is_js_installed(js_path):
        print(f"  JS:  Button not installed in {ext_info['name']}")
    else:
        backup_path = js_path + '.bak'
        restored = False
        if os.path.exists(backup_path):
            try:
                shutil.copy2(backup_path, js_path)
                os.remove(backup_path)
                print(f"  JS:  Restored from backup: {ext_info['name']}")
                restored = True
            except Exception as e:
                print(f"  JS:  Backup restore failed: {e}, trying manual removal...")

        if not restored:
            try:
                with open(js_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                cleaned = _strip_block(content, JS_START_MARKER, JS_END_MARKER)
                with open(js_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                print(f"  JS:  Toggle button removed from {ext_info['name']}")
            except Exception as e:
                print(f"  JS:  Error removing button: {e}")


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
    print("\n" + "=" * 55)
    print("  Claude Code in VS Code - RTL Text Support (+ Cursor)")
    print("=" * 55)
    print("  1. Add RTL support (all versions)")
    print("  2. Remove RTL support (all versions)")
    print("  3. Check status")
    print("  4. Exit")
    print("=" * 55)


def main():
    system_info = f"{platform.system()} {platform.release()}"
    if _is_wsl():
        system_info += " (WSL)"
    print(f"System: {system_info}")

    extensions = find_claude_extensions()

    if not extensions:
        print("\nNo Claude Code extensions found!")
        print("Make sure the 'Claude Code in VS Code' extension is installed.")
        input("\nPress Enter to exit...")
        return

    print(f"Found {len(extensions)} extension(s)")

    while True:
        show_menu()
        choice = input("\n  Select option (1-4): ").strip()

        if choice == "1":
            print("\nAdding RTL support...\n")
            for ext in extensions:
                add_rtl_support(ext)
            print("\nRestart VS Code / Cursor / reload window to see changes!")

        elif choice == "2":
            print("\nRemoving RTL support...\n")
            for ext in extensions:
                remove_rtl_support(ext)
            print("\nRestart VS Code / Cursor / reload window to see changes!")

        elif choice == "3":
            check_status(extensions)

        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        input("Press Enter to close...")
