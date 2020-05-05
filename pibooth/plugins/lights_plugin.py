# -*- coding: utf-8 -*-

import time
import pibooth


class LightsPlugin(object):
    """Plugin to manage the lights via GPIO.
    """

    def __init__(self, plugin_manager):
        self._pm = plugin_manager
        self.blink_time = 0.3

    @pibooth.hookimpl
    def pibooth_startup(self, app):
        app.other_leds.start.on()

    @pibooth.hookimpl
    def state_wait_enter(self, cfg, app):
        if app.previous_picture_file and app.printer.is_installed() and not app.printer_unavailable\
                and app.nbr_duplicates < cfg.getint('PRINTER', 'max_duplicates'):
            app.leds.blink(on_time=self.blink_time, off_time=self.blink_time)
        else:
            app.leds.capture.blink(on_time=self.blink_time, off_time=self.blink_time)
            app.leds.printer.off()

    @pibooth.hookimpl
    def state_wait_do(self, cfg, app, events):
        if app.find_print_event(events) and app.previous_picture_file and app.printer.is_installed():
            if app.nbr_duplicates >= cfg.getint('PRINTER', 'max_duplicates') or app.printer_unavailable:
                app.leds.printer.off()
            else:
                app.leds.printer.on()
                time.sleep(1)  # Just to let the LED switched on
                app.leds.blink(on_time=self.blink_time, off_time=self.blink_time)

    @pibooth.hookimpl
    def state_wait_exit(self, app):
        app.leds.off()

    @pibooth.hookimpl
    def state_choose_enter(self, app):
        app.leds.blink(on_time=self.blink_time, off_time=self.blink_time)

    @pibooth.hookimpl
    def state_choose_exit(self, app):
        if app.capture_nbr == app.capture_choices[0]:
            app.leds.capture.on()
            app.leds.printer.off()
        elif app.capture_nbr == app.capture_choices[1]:
            app.leds.printer.on()
            app.leds.capture.off()

    @pibooth.hookimpl
    def state_chosen_exit(self, app):
        app.leds.off()

    @pibooth.hookimpl
    def state_preview_enter(self, app):
        app.other_leds.preview.on()

    @pibooth.hookimpl
    def state_capture_exit(self, app):
        app.other_leds.preview.off()

    @pibooth.hookimpl
    def state_print_enter(self, app):
        app.leds.blink(on_time=self.blink_time, off_time=self.blink_time)

    @pibooth.hookimpl
    def state_print_do(self, app, events):
        if app.find_print_event(events):
            app.leds.printer.on()
            app.leds.capture.off()

    @pibooth.hookimpl
    def state_finish_enter(self, app):
        app.leds.off()
