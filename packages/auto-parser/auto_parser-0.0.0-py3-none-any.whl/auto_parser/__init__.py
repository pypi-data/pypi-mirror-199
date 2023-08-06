
# オートマトンによる構文解析 [auto_parser]

import sys
from sout import sout

# target_strを分解 (末尾に"@end"を付記)
def div_target_str(target_str):
	div_target = list(target_str)
	div_target.append("@end")
	return div_target

# stateがcondを満たすかどうかを確認
def judge_match(state, cond):
	for key in cond:
		# OKなパターン一覧
		or_ls = cond[key]
		if type(or_ls) == type(""): or_ls = [or_ls]
		# stateのkey包含条件
		if key not in state:
			raise Exception("[auto_parser error] state must have key('%s')."%key)
		# 満たすかどうかの確認
		if state[key] not in or_ls: return False
	return True

# 現状のstateに適合するruleを引き当て
def match_rule(state, rules):
	for rule in rules:
		# stateがcondを満たすかどうかを確認
		flag = judge_match(state, rule["cond"])
		if flag is True: return rule
	# どれも当てはまらない場合
	raise Exception("[auto_parser error] There is no rule to match the pattern.")

# stack操作: pop
def stack_pop(stack, pop_n):
	pop_ls = []
	for _ in range(pop_n):
		pop_ls.append(stack.pop())
	return pop_ls

# @+の構文の解決
def resolve_at_plus(at_plus_args, head, pop_ls):
	ret_ls = []
	for arg in at_plus_args:
		# 相互再帰
		resolved = resolve_push_value(arg, head, pop_ls)
		# 型チェック
		if type(resolved) != type([]): raise Exception("[auto_parser error] The type of @+ syntax args is invalid.")
		# 追記
		for e in resolved: ret_ls.append(e)
	return ret_ls

# pushする内容の作成
def resolve_push_value(blueprint, head, pop_ls):
	# 再帰終了条件
	if type(blueprint) == type(""):
		if blueprint == "@head": return head
		if blueprint.startswith("@p"):
			p_idx = int(blueprint.replace("@p", ""))
			return pop_ls[p_idx]
		return blueprint	# 通常の文字列の場合
	elif type(blueprint) == type([]):
		if len(blueprint) > 0 and blueprint[0] == "@+":
			# @+の構文の解決
			return resolve_at_plus(blueprint[1:], head, pop_ls)
		return [
			resolve_push_value(e, head, pop_ls)
			for e in blueprint
		]
	else:
		raise Exception("[auto_parser error] invalid blueprint syntax.")

# stack操作: push (複数)
def stack_push_ls(stack, rule, head, pop_ls):
	push_idx = 0
	while True:
		key = "push_%d"%push_idx
		if key not in rule: break
		# pushする内容の作成
		value = resolve_push_value(rule[key], head, pop_ls)
		# push
		stack.append(value)
		# push_idxのインクリメント
		push_idx += 1

# stateの変更
def update_state(state, overwrite_state):
	for key in overwrite_state:
		state[key] = overwrite_state[key]

# 構文解析
def parse(
	target_str,	# 解析対象の文字列
	rules,	# 遷移規則一覧
	init_state,	# 初期state
	init_stack	# 初期stack
):
	# 初期状態の設定
	state = init_state	# 初期state
	stack = init_stack	# 初期stack
	# target_strを分解 (末尾に"@end"を付記)
	div_target = div_target_str(target_str)
	for head in div_target:
		# headを現在のstateに書き込む
		state["@head"] = head
		# 現状のstateに適合するruleを引き当て
		rule = match_rule(state, rules)
		# stack操作: pop
		pop_ls = stack_pop(stack, rule["pop_n"])
		# stack操作: push (複数)
		stack_push_ls(stack, rule, head, pop_ls)
		# stateの変更
		update_state(state, rule["post_state"])
		# # debug
		# sout(stack)
		# sout(state)
		# input(">>>")
	# stackの最終状態の確認
	if len(stack) != 1: raise Exception("[auto_parser error] The stack must have an element count of 1 in its final state.")
	return stack[0]
