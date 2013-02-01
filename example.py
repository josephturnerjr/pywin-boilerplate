import md5
import sys
try:
    import winxpgui as wingui
except ImportError:
    import win32gui as wingui
import os 
import win32con
import win32api


from win32gui_struct import commctrl
import win32con

import os
import win32con
import win32api
try:
    import _resources
except ImportError:
    print "Error loading the frozen resource file. You may need to run 'make resources'."
    sys.exit(0)


def open_webpage(url):
    win32api.ShellExecute(0, "open", url, "", "", 0)


class Example(object):
    RESOURCE_NAME = "IDD_EXAMPLE"

    def __init__(self):
        self.started = False
        self.hicon = self.get_icon()
        self.rc_dict = _resources.Parse(None)
        self.starting = False
        self.created = False
        self.started = False
        self.template = self.rc_dict.dialogs[self.RESOURCE_NAME]
        self.ids = self.rc_dict.ids
        self.dlg_msg_handler = {
                                win32con.WM_CLOSE: self._OnClose,
                                win32con.WM_INITDIALOG: self._OnCreate,
                                win32con.WM_COMMAND: self._OnCommand,
                                win32con.WM_DESTROY: self._OnDestroy
                               }
        self.start()

    def start(self):
        if not self.started:
            self.starting = True
            wingui.DialogBoxIndirect(wingui.GetModuleHandle(None), self.template, 0, self.dlg_msg_handler)
        else:
            if not self.starting:
                self.bring_to_top()

    def _OnDestroy(self, hwnd, msg, wparam, lparam):
        self.started = False
        self.created = False

    def _OnClose(self, hwnd, msg, wparam, lparam):
        self.OnClose(hwnd, msg, wparam, lparam)

    def OnClose(self, hwnd, msg, wparam, lparam):
        wingui.EndDialog(hwnd, 0)
        wingui.PostQuitMessage(0) # Terminate the app.
        
    def _OnCreate(self, hwnd, msg, wparam, lparam):
        try:
            wingui.SetForegroundWindow(hwnd)
        except Exception, e:
            logging.log("Error setting foreground window: %s" % e)
        self.OnCreate(hwnd, msg, wparam, lparam)
        self.created = True
        self.started = True
        self.starting = False

    def OnCreate(self, hwnd, msg, wparam, lparam):
        self.hwnd = hwnd
        wingui.SendMessage(self.hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, self.hicon)
        wingui.SendMessage(self.hwnd, win32con.WM_SETICON, win32con.ICON_BIG, self.hicon)

    def _OnCommand(self, hwnd, msg, wparam, lparam):
        self.OnCommand(hwnd, msg, wparam, lparam)

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = wingui.LOWORD(wparam)
        if id == win32con.IDOK:
            self.OnClose(hwnd, msg, wparam, lparam)
        elif id == win32con.IDCANCEL:
            self.OnClose(hwnd, msg, wparam, lparam)
        elif id == self.ids['IDC_WEBSITE']:
            open_webpage("http://thejosephturner.com")
        elif id == self.ids['IDC_GET_HASH']:
            h = wingui.GetDlgItem(self.hwnd, self.ids["IDC_MD5"])
            wingui.SendMessage(h, win32con.WM_SETTEXT, 0, md5.new(self.get_edit_val("IDC_PHRASE")).hexdigest())

    def get_edit_val(self, name):
        h = wingui.GetDlgItem(self.hwnd, self.ids[name])
        MAX_LENGTH = 1024
        buffer = wingui.PyMakeBuffer(MAX_LENGTH)
        length = wingui.SendMessage(h, win32con.WM_GETTEXT, MAX_LENGTH, buffer)
        return buffer[:length]

    def bring_to_top(self):
        wingui.BringWindowToTop(self.hwnd)

    def get_icon(self):
        return wingui.LoadIcon(0, win32con.IDI_APPLICATION)
        
    def run(self):
        wingui.PumpMessages()

if __name__ == "__main__":
    example = Example()
    example.run()
