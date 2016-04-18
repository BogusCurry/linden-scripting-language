import os
import plistlib
import shutil
import stat
import sublime
import sublime_plugin

SETTINGS_FILE = "LSL.sublime-settings"
INDENT_STYLE = "LSL_indent_style.tmPreferences"
INDENT_STYLE_ALLMAN = "LSL_indent_style.tmPreferences.allman"
INDENT_STYLE_KANDR = "LSL_indent_style.tmPreferences.kandr"

def chmod_lslint():
    binaryPath = os.path.join(sublime.packages_path(), "LSL/bin/osx/lslint")
    os.chmod(binaryPath, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
    binaryPath = os.path.join(sublime.packages_path(), "LSL/bin/linux/lslint")
    os.chmod(binaryPath, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)

def set_default_lsl_indent_style():
    srcdir = os.path.join(sublime.packages_path(), "LSL/metadata")
    destdir = os.path.join(sublime.packages_path(), "User")
    destfile = os.path.join(destdir, INDENT_STYLE)
    if not os.path.exists(destfile):
        shutil.copyfile(os.path.join(srcdir, INDENT_STYLE_ALLMAN), destfile)

if sublime.version().startswith('2'):
    chmod_lslint()
    set_default_lsl_indent_style()

def plugin_loaded():
    chmod_lslint()
    set_default_lsl_indent_style()

class OpenLslDefaultSettingsCommand(sublime_plugin.WindowCommand):
    def __init__(self, *args, **kwargs):
        super(OpenLslDefaultSettingsCommand, self).__init__(*args, **kwargs)
        self.view = None

    def run(self):
        self.view = sublime.active_window().open_file(
            os.path.join(
                sublime.packages_path(),
                "LSL",
                "settings",
                "LSL.sublime-settings"
            )
        )

        sublime.set_timeout(self.set_view_readonly, 1)

    def set_view_readonly(self):
        if self.view is None or self.view.is_loading():
            sublime.set_timeout(self.set_view_readonly, 1)
            return

        self.view.set_read_only(True)

class ChangeEditorSchemeCommand(sublime_plugin.WindowCommand):
    _is_checked = False

    def __init__(self, view):
        settings = sublime.load_settings(SETTINGS_FILE)
        self._is_checked = settings.has("color_scheme")

    def run(self):
        settings = sublime.load_settings(SETTINGS_FILE)
        if self._is_checked:
            settings.erase("color_scheme")
            self._is_checked = False
        else:
            settings.set("color_scheme", "Packages/LSL/color-schemes/LSL.hidden-tmTheme")
            self._is_checked = True
        sublime.save_settings(SETTINGS_FILE)

    def is_checked(self):
        return self._is_checked

class ChangeStyleCommand(sublime_plugin.WindowCommand):
    """
        Changing the indent style is only being done via the *.tmPreferences
        files, not via the LSL.sublime-settings file.
    """

    _is_checked = False

    def __init__(self, view):
        srcdir = os.path.join(sublime.packages_path(), "LSL/metadata")
        destdir = os.path.join(sublime.packages_path(), "User")
        destfile = os.path.join(destdir, INDENT_STYLE)
        if os.path.exists(destfile):
            pl = plistlib.readPlist(destfile)
            self._is_checked = (pl['uuid'] == "a775771f-1a8d-4741-a1a3-6f6dc0b01ab4")
#       else:
#           shutil.copyfile(os.path.join(srcdir, INDENT_STYLE_ALLMAN), destfile)
#       settings = sublime.load_settings(SETTINGS_FILE)
#       if self._is_checked:
#           settings.set("lsl-indent-style", "kandr")
#       else:
#           settings.erase("lsl-indent-style")
#       sublime.save_settings(SETTINGS_FILE)

    def run(self):
        srcdir = os.path.join(sublime.packages_path(), "LSL/metadata")
        destdir = os.path.join(sublime.packages_path(), "User")
        destfile = os.path.join(destdir, INDENT_STYLE)
#       settings = sublime.load_settings(SETTINGS_FILE)
        if self._is_checked:
            shutil.copyfile(os.path.join(srcdir, INDENT_STYLE_ALLMAN), destfile)
#           settings.erase("lsl-indent-style")
            self._is_checked = False
        else:
            shutil.copyfile(os.path.join(srcdir, INDENT_STYLE_KANDR), destfile)
#           settings.set("lsl-indent-style", "kandr")
            self._is_checked = True
#       sublime.save_settings(SETTINGS_FILE)

    def is_checked(self):
        return self._is_checked
