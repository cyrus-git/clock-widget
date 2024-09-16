import objc
from AppKit import NSWindowCollectionBehaviorCanJoinAllSpaces  # 追加
from AppKit import (NSApp, NSApplication, NSBackingStoreBuffered, NSColor,
                    NSFont, NSObject, NSRunningApplication, NSScreen,
                    NSTextField, NSWindow, NSWindowStyleMaskBorderless)
from Foundation import NSDate, NSDateFormatter, NSTimer, NSTimeZone
from PyObjCTools import AppHelper
from Quartz import kCGDesktopIconWindowLevel


class AppDelegate(NSObject):
    def applicationSupportsSecureRestorableState_(self, app):
        return True


class ClockWindow:
    def __init__(self):
        # ウィンドウのサイズと位置を設定
        self.width = 900  # 幅を900に設定
        self.height = 450  # 高さを450に設定
        self.screen = NSScreen.mainScreen().frame()

        x = (self.screen.size.width - self.width) / 2
        y = (self.screen.size.height - self.height) / 2
        frame = ((x, y), (self.width, self.height))

        # NSWindowの初期化、スタイルマスクやウィンドウ設定を修正
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            frame,
            NSWindowStyleMaskBorderless,  # ウィンドウスタイルマスクをボーダーレスに設定
            NSBackingStoreBuffered,        # バッキングストアの種類
            False                          # ウィンドウ作成時にディレイしない
        )
        self.window.setCollectionBehavior_(
            NSWindowCollectionBehaviorCanJoinAllSpaces)

        # ウィンドウのレベルをデスクトップ上に設定
        self.window.setLevel_(kCGDesktopIconWindowLevel)

        # ウィンドウの背景色を透明に設定
        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())

        # 1段目のラベル（曜日と日付）
        self.date_label = NSTextField.alloc().initWithFrame_(
            ((0, self.height / 2 - 40), (self.width, self.height / 2 - 50)))
        self.date_label.setFont_(
            NSFont.boldSystemFontOfSize_(60))  # フォントサイズを60に設定
        self.date_label.setTextColor_(NSColor.whiteColor())
        self.date_label.setBezeled_(False)
        self.date_label.setDrawsBackground_(False)
        self.date_label.setEditable_(False)
        self.date_label.setSelectable_(False)
        self.date_label.setAlignment_(1)  # NSTextAlignmentCenter
        self.window.contentView().addSubview_(self.date_label)

        # 2段目のラベル（時間）
        self.time_label = NSTextField.alloc().initWithFrame_(
            ((0, 100), (self.width, self.height / 2 - 30)))
        self.time_label.setFont_(
            NSFont.boldSystemFontOfSize_(150))  # フォントサイズを150に設定
        self.time_label.setTextColor_(NSColor.whiteColor())
        self.time_label.setBezeled_(False)
        self.time_label.setDrawsBackground_(False)
        self.time_label.setEditable_(False)
        self.time_label.setSelectable_(False)
        self.time_label.setAlignment_(1)  # NSTextAlignmentCenter
        self.window.contentView().addSubview_(self.time_label)

        # ウィンドウを常に表示
        self.window.makeKeyAndOrderFront_(None)
        self.update_time_(None)

        # タイマーで毎分時間を更新
        self.timer = NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, "update_time:", None, True
        )
        NSApp.activateIgnoringOtherApps_(True)

    def update_time_(self, timer):
        # 日付を取得して1段目に表示
        date_formatter = NSDateFormatter.alloc().init()
        date_formatter.setDateFormat_("EEEE, MMM d")  # 曜日、月、日を表示
        date_formatter.setTimeZone_(NSTimeZone.timeZoneWithName_("Asia/Tokyo"))
        current_date = date_formatter.stringFromDate_(NSDate.date())
        self.date_label.setStringValue_(current_date)

        # 時間を取得して2段目に表示
        time_formatter = NSDateFormatter.alloc().init()
        time_formatter.setDateFormat_("HH:mm")  # 時間と分を表示
        time_formatter.setTimeZone_(NSTimeZone.timeZoneWithName_("Asia/Tokyo"))
        current_time = time_formatter.stringFromDate_(NSDate.date())
        self.time_label.setStringValue_(current_time)


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    clock_window = ClockWindow()
    AppHelper.runEventLoop()
