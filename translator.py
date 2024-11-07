from opencc import OpenCC
from rich.progress import Progress
import os


progress = None


class Translator:
	def __init__(self, convert_method: str):
		self.convert_method = convert_method
		self.converter = OpenCC(convert_method)
		self.translation_dict_file = f"trans_dict_{convert_method}.txt"
		self.translation_dict = self.__load_translation_dict()
		self.translation_dict_unchecked_file = f"trans_dict_{convert_method}_unchecked.txt"
		self.translation_dict_unchecked = {}

	def save(self):
		self.__save_translation_dict(self.translation_dict_file, self.translation_dict)
		self.__save_translation_dict(self.translation_dict_unchecked_file, self.translation_dict_unchecked)

	def __load_translation_dict(self) -> dict:
		if not os.path.exists(self.translation_dict_file):
			with open(self.translation_dict_file, 'w', encoding="utf-8-sig") as f:
				f.write("")
		translation_dict = {}
		with open(self.translation_dict_file, 'r', encoding="utf-8-sig") as f:
			for line in f:
				if not line.strip() or line.startswith("#"):
					continue
				key, val = line.strip().split("\t")
				translation_dict[key] = val
		return translation_dict

	def __save_translation_dict(self):
		with open(self.translation_dict_file, 'w', encoding="utf-8-sig") as f:
			identical = []
			for key, val in self.translation_dict.items():
				if key == val:
					identical.append(key)
				else:
					f.write(key + "\t" + val + "\n")
			if identical:
				f.write("\n# Identical translations\n")
				for key in identical:
					f.write(key + "\t" + key + "\n")

	def translate(self, from_dict_file: str, to_dict_file: str):
		to_dict_lines = []
		with open(from_dict_file, 'r', encoding="utf-8-sig") as f:
			task = progress.add_task(os.path.basename(from_dict_file), total=os.path.getsize(from_dict_file))

			# header lines
			if from_dict_file.endswith(".dict.yaml"):
				for line in f:
					if line.startswith("name:"):
						line = line.strip() + "_translated\n"
					to_dict_lines.append(line)
					progress.update(task, advance=len(line.encode("utf-8")))
					if line == "...\n":
						break
			
			# entries
			for line in f:
				if not line.startswith("#"):  # skip comments
					if "\t" in line:
						key, val = line.split("\t")[0], "\t".join(line.split("\t")[1:])
						key = key.strip()
						val = val.strip()
						if key in self.translation_dict:
							translation = self.translation_dict[key]
						elif key in self.translation_dict_unchecked:
							translation = self.translation_dict_unchecked[key]
						else:
							translation = self.converter.convert(key)
							self.translation_dict_unchecked[key] = translation
						line = translation + "\t" + val + "\n"
					elif line.strip():
						key = line.strip()
						if key in self.translation_dict:
							translation = self.translation_dict[key]
						elif key in self.translation_dict_unchecked:
							translation = self.translation_dict_unchecked[key]
						else:
							translation = self.converter.convert(key)
							self.translation_dict_unchecked[key] = translation
						line = translation + "\n"
				to_dict_lines.append(line)
				progress.update(task, advance=len(line.encode("utf-8")))
			progress.remove_task(task)

		with open(to_dict_file, 'w', encoding="utf-8-sig") as f:
			task = progress.add_task("Writing...", total=1)
			f.writelines(to_dict_lines)
			progress.remove_task(task)
	

def generate_dict_list(from_dir: str, to_dir: str):
	from_dict_files = []
	for root, dirs, files in os.walk(from_dir):
		for file in files:
			if file.endswith('.dict.yaml') and not file.endswith('_translated.dict.yaml'):
				from_dict_files.append(os.path.join(root, file))
	dict_list = []
	for from_dict_file in from_dict_files:
		to_dict_file = from_dict_file.replace(from_dir, to_dir)
		to_dict_file = to_dict_file.replace(".dict.yaml", "_translated.dict.yaml")
		dict_list.append((from_dict_file, to_dict_file))
	return dict_list


if __name__ == "__main__":
	with Progress() as progress:
		translator = Translator("s2tw")
		
		dict_list = generate_dict_list("cn_dicts", "tw_dicts")
		dict_list.append(("en_dicts/cn_en.txt", "tw_dicts/cn_en.txt"))

		task = progress.add_task("[cyan]Translating...", total=len(dict_list))
		for from_dict_file, to_dict_file in dict_list:
			translator.translate(from_dict_file, to_dict_file)
			progress.update(task, advance=1)
