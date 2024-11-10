import re
import os


def validate_txt(lines: list[str]):
	key_dict = {}
	for line in lines:
		if "\t" not in line:
			continue

		try:
			key, values = line.split("\t")
		except ValueError:
			print(f"Invalid line: {line}")  # supposed to be that one certain line
			continue

		values = values.strip().split(" ")

		if key in key_dict:
			raise ValueError(f"Duplicate key: {key}")
		key_dict[key] = values


def load_txt(path: str) -> list[str]:
	if not os.path.exists(path):
		raise FileNotFoundError(f"File not found: {path}")

	with open(path, "r", encoding="utf-8-sig") as f:
		lines = f.readlines()
	return lines


if __name__ == "__main__":
	paths = ["opencc/emoji_tw.txt", "opencc/others_tw.txt"]
	for path in paths:
		lines = load_txt(path)
		validate_txt(lines)
		print(f"Validation passed: {path}")
