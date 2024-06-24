-- This script is used to suggest Taiwanese variants of Chinese phrases.
local F = {}

function F.init(env)
    F.simplify = Opencc('t2s.json')
    F.taiwanize = Opencc('s2twp.json')
end

function F.func(input, env)
    local do_convert = env.engine.context:get_option('traditionalization')
    if not do_convert then
        for cand in input:iter() do
            yield(cand)
        end
        return
    end
    for cand in input:iter() do
        yield(cand)  -- already converted by simplifier@traditionalize

        local reverted_text = F.simplify:convert(cand.text)
        local taiwanized_text = F.taiwanize:convert(reverted_text)
        if taiwanized_text ~= cand.text then
            yield(cand:to_shadow_candidate(cand.type, taiwanized_text, 'ᵀᵂ'))
        end
    end
end

return F
