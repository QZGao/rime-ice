-- Additional dictionaries

local function translator(input, seg, env)
	env.mem_sp = Memory(env.engine, Schema('dicts_sp'))
	env.mem_td = Memory(env.engine, Schema('dicts_td'))

	
end