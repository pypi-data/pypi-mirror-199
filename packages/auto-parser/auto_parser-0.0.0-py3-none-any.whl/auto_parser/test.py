
# オートマトンによる構文解析 [auto_parser]
# 【動作確認 / 使用例】

import sys
import fies
from sout import sout
from ezpip import load_develop
# オートマトンによる構文解析 [auto_parser]
auto_parser = load_develop("auto_parser", "../", develop_flag = True)

# 構文解析 [auto_parser]
res = auto_parser.parse(
	target_str = fies["test_input.txt"],	# 解析対象の文字列
	rules = fies["test_rules.yml"],	# 遷移規則一覧
	init_state = {"state": "args_start"},	# 初期state
	init_stack = [["lines"]],	# 初期stack
)
sout(res, None)
