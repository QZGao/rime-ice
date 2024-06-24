-- This script is mainly used to simplify the traditional Chinese characters in the poetry dictionary.
local F = {}

function F.init(env)
    F.simplify = Opencc('t2s.json')
end

function F.func(input, env)
    local do_convert = env.engine.context:get_option('traditionalization')
    for cand in input:iter() do
        if cand.text:find("⬚") then
            local text = cand.text:gsub("⬚", "")

            if do_convert then
                yield(cand:to_shadow_candidate(cand.type, text, cand.comment))
            else
                local simplified_text = F.simplify:convert(text)
                yield(cand:to_shadow_candidate(cand.type, simplified_text, cand.comment))
            end
        else
            yield(cand)
        end
    end
end

return F
