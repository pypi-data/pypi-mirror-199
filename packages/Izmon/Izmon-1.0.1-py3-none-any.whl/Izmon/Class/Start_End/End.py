class End:
	from ..Basic.Common_Function import Common_Function as co_f
	from ..Basic.Common_Variable import Common_Variable as co_v
	from ..Basic.Settings import Settings as st
	
	def save(self): #データをセーブする
		from ..Save_Code.Encode import Encode
		
		ty = self.co_f.typing("データをセーブしますか？ 0:する 1:しない", 1, 2)
		if ty == 0:
			code = Encode.encode()
			print("-" * self.st.SEPALATE_LEN)
			print("プレイヤー名と共に保管してください。")
			print(f"コード: {code}")
			print(f"プレイヤー名: {self.co_v.player_name}")
		else:
			ty = self.co_f.typing("本当にしないでよろしいですか? 0:する 1:しない", 1, 2)
			if ty == 0:
				code = Encode.encode()
				print("-" * self.st.SEPALATE_LEN)
				print("プレイヤー名と共に保管してください。")
				print(f"コード: {code}")
				print(f"プレイヤー名: {self.co_v.player_name}")
		print("=" * self.st.SEPALATE_LEN)
		return