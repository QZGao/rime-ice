-- This script is mainly used to simplify the traditional Chinese characters in the poetry dictionary.
local F = {}

function F.init(env)
    F.simplify = Opencc('t2s.json')
end

function F.func(input, env)
    local do_convert = env.engine.context:get_option('traditionalization')
    for cand in input:iter() do
        if do_convert then
            yield(cand)
        else
            local simplified_text = F.simplify:convert(cand.text)
            if simplified_text == cand.text then
                yield(cand)
            else
                yield(cand:to_shadow_candidate(cand.type, simplified_text, cand.comment))
            end
        end
    end
end

return F
