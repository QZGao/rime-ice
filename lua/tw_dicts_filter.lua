local M = {}

function M.init(env)
	env.tran = Component.Translator(env.engine, "", "table_translator@tw_dicts")
end

function M.func(input, seg, env)
	local t = env.tran:query(input, seg)
    for cand in t:iter() do
		cand.type = "A_" .. cand.type
		yield(cand)
	end
end

return M
