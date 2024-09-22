
import objc
from AppKit import (NSApp, NSApplication,
                    NSApplicationDidChangeScreenParametersNotification,
                    NSBackingStoreBuffered, NSColor, NSFont, NSObject,
                    NSRunningApplication, NSScreen, NSTextField, NSWindow,
                    NSWindowCollectionBehaviorCanJoinAllSpaces,
                    NSWindowStyleMaskBorderless)
from Foundation import (NSDate, NSDateFormatter, NSNotificationCenter,
                        NSTimeZone)
from PyObjCTools import AppHelper
from Quartz import kCGDesktopIconWindowLevel


class AppDelegate(NSObject):
    def applicationSupportsSecureRestorableState_(self, app):
        return True


class ClockWindow(NSObject):
    def init(self):
        self = objc.super(ClockWindow, self).init()
        if self is None:
            return None

        # ウィンドウのサイズを設定
        self.width = 900
        self.height = 450

        # ウィンドウを初期化
        self.window = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(
            ((0, 0), (self.width, self.height)),
            NSWindowStyleMaskBorderless,
            NSBackingStoreBuffered,
            False
        )

        self.window.setLevel_(kCGDesktopIconWindowLevel)
        self.window.setOpaque_(False)
        self.window.setBackgroundColor_(NSColor.clearColor())
        self.window.setCollectionBehavior_(
            NSWindowCollectionBehaviorCanJoinAllSpaces)

        # ラベルを設定
        self.setup_labels()

        # ウィンドウを中央に配置
        self.center_window()

        # ウィンドウを表示
        self.window.makeKeyAndOrderFront_(None)

        # タイマーを使わず手動で時間を更新
        self.update_time()
        self.schedule_update()

        # スクリーン変更の通知を監視
        NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
            self,
            "screenParametersChanged:",
            NSApplicationDidChangeScreenParametersNotification,
            None
        )

        return self

    def setup_labels(self):
        # 日付ラベルを作成
        self.date_label = NSTextField.alloc().initWithFrame_(
            ((0, self.height / 2 - 40), (self.width, self.height / 2 - 50)))
        self.date_label.setFont_(NSFont.boldSystemFontOfSize_(60))
        self.date_label.setTextColor_(NSColor.whiteColor())
        self.date_label.setBezeled_(False)
        self.date_label.setDrawsBackground_(False)
        self.date_label.setEditable_(False)
        self.date_label.setSelectable_(False)
        self.date_label.setAlignment_(1)  # NSTextAlignmentCenter
        self.window.contentView().addSubview_(self.date_label)

        # 時間ラベルを作成
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

    def center_window(self):
        # 現在のメインスクリーンを取得
        self.screen = NSScreen.mainScreen().frame()

        # ウィンドウの位置を再計算
        x = (self.screen.size.width - self.width) / 2
        y = (self.screen.size.height - self.height) / 2
        frame = ((x, y), (self.width, self.height))

        # ウィンドウのフレームを更新
        self.window.setFrame_display_(frame, True)

    def screenParametersChanged_(self, notification):
        # スクリーンが変更されたときにウィンドウを再配置
        self.center_window()

    def update_time(self):
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

    def schedule_update(self):
        # 1秒後に次の時間更新を呼び出す
        AppHelper.callLater(1.0, self.update_time)
        AppHelper.callLater(1.0, self.schedule_update)


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    clock_window = ClockWindow.alloc().init()
    AppHelper.runEventLoop()
