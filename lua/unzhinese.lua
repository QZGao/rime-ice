-- This script is used to suggest Taiwanese variants of Chinese phrases.
local M = {}

function M.init(env)
    M.taiwanize = Opencc('s2twp.json')
end

function M.func(input, env)
    local do_convert = env.engine.context:get_option('traditionalization')
    if not do_convert then
        for cand in input:iter() do
            yield(cand)
        end
        return
    end
    for cand in input:iter() do
        yield(cand)  -- already converted by simplifier@traditionalize

        local taiwanized_text = M.taiwanize:convert(cand.text)
        if taiwanized_text ~= cand.text then
            yield(cand:to_shadow_candidate(cand.type, taiwanized_text, 'ᵀᵂ'))
        end
    end
end

return M
