local wibox = require("wibox")
local awful = require("awful")
local watch = require("awful.widget.watch")
local beautiful = require("beautiful")

rhythmbox_widget = wibox.widget {
    font = 'Play 9',
    widget = wibox.widget.textbox
}

rhythmbox_icon = wibox.widget 

watch(
    "rhythmbox-client --no-start --print-playing", 1,
    function(widget, stdout, stderr, exitreason, exitcode)
        if string.len(stdout) > 33 then
            stdout = string.sub(stdout, 0, 30) .. "..."
        end
        rhythmbox_widget:set_text(stdout)
    end
)

widget = wibox.widget {
    {
        {
            image  = "/usr/share/icons/Adwaita/16x16/devices/audio-speakers-symbolic.symbolic.png",
            resize = false,
            widget = wibox.widget.imagebox
        },
        rhythmbox_widget,
        layout = wibox.layout.fixed.horizontal
    },
    widget = wibox.container.background
}

return widget