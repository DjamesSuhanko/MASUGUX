dofile("config.lua")

local M = {}

function M.fast()
    gpio_16    = 0
    gpio_blink = false

    gpio.mode(gpio_16,gpio.OUTPUT)

    function toBlink()
        if not gpio_blink then
            gpio_blink = true
            gpio.write(gpio_16,gpio.HIGH)
        else
            gpio_blink = 0
            gpio.write(gpio_16.gpio.LOW)
        end
    end

    tmr.alarm(2,500,1,toBlink())

end

return M
