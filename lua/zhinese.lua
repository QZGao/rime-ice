-- This script is used to convert between simplified and traditional Chinese characters.
local F = {}

function F.init(env)
	F.traditionalize = Opencc('s2tw.json')
    F.taiwanize = Opencc('s2twp.json')
    F.simplify = Opencc('t2s.json')
end

function F.func(input, env)
    local trad_input = env.engine.context:get_option('traditionalization')
    for cand in input:iter() do
        if trad_input then
			-- traditional input mode
			local simplified = F.simplify:convert_word(cand.text) or {F.simplify:convert_text(cand.text)}
			if #simplified == 1 and simplified[1] == cand.text then
				-- simplified entry, convert to traditional + suggest Taiwanese
				local traditional = F.traditionalize:convert_word(cand.text) or {F.traditionalize:convert_text(cand.text)}
				for _, t in ipairs(traditional) do
					yield(cand:to_shadow_candidate(cand.type, t, "S→T"))
				end
				
				local taiwanese = F.taiwanize:convert_word(cand.text) or {F.taiwanize:convert_text(cand.text)}
				for _, t in ipairs(taiwanese) do
					yield(cand:to_shadow_candidate(cand.type, t, "S→TW"))
				end

			else
				-- traditional entry, no need to convert
				yield(cand)
			end
		else
			-- simplified input mode
			local simplified = F.simplify:convert_word(cand.text) or {F.simplify:convert_text(cand.text)}
			if #simplified == 1 and simplified[1] == cand.text then
				-- simplified entry, no need to convert
				yield(cand)
			else
				-- traditional entry, convert to simplified
				for _, s in ipairs(simplified) do
					yield(cand:to_shadow_candidate(cand.type, s, "T→S"))
				end
			end
		end
    end
end

return F
