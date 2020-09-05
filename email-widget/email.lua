local wibox = require("wibox")
local awful = require("awful")
local naughty = require("naughty")
local watch = require("awful.widget.watch")
local os = require("os")

local path_to_icons = "/home/mrtommy/Imágenes/icons/"

email_widget = wibox.widget.textbox()
email_widget:set_font('Play 9')

email_icon = wibox.widget.imagebox()
email_icon:set_image(path_to_icons .. "/mail.png")

function sleep(n)
    if n > 0 then
        os.execute("ping -n " .. tonumber(n + 1) .. " localhost > NUL")
    end  
end

watch(
    "python /home/mrtommy/.config/awesome/awesome-wm-widgets/email-widget/count_unread_emails.py", 20,
    function(widget, stdout, stderr, exitreason, exitcode)
        local unread_emails_num = tonumber(stdout) or 0
        if (unread_emails_num > 0) then
        	email_icon:set_image(path_to_icons .. "/mail.png")
	        email_widget:set_text(stdout)
        elseif (unread_emails_num == 0) then
        	email_icon:set_image(path_to_icons .. "/mail.png")
   	        email_widget:set_text("")
        end	
    end
)


function show_emails()
    awful.spawn.easy_async("[[bash -c 'python /home/mrtommy/.config/awesome/awesome-wm-widgets/email-widget/read_unread_emails.py']]",
        function(stdout, stderr, reason, exit_code)
            naughty.notify{
                text = stdout,
                title = "Unread Emails",
                timeout = 5, hover_timeout = 0.5,
                width = 400,
            }
        end
    )
end

email_widget:connect_signal("mouse::enter", function() show_emails() end)

return email_widget