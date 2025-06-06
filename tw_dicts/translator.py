from opencc import OpenCC
from rich.progress import Progress
import os
import re


progress = None


class Translator:
    def __init__(self, convert_method: str):
        self.convert_method = convert_method
        self.converter = OpenCC(convert_method)
        self.translation_dict_checked_filename = f"trans_dict_{convert_method}_checked"
        self.translation_dict = self.__load_translation_dict()
        self.translation_dict_filtered = {}
        self.translation_dict_unchecked_filename = (
            f"trans_dict_{convert_method}_unchecked"
        )
        self.translation_dict_unchecked = {}

    def save(self):
        self.__save_translation_dict(
            self.translation_dict_checked_filename, self.translation_dict_filtered
        )
        self.__save_translation_dict(
            self.translation_dict_unchecked_filename, self.translation_dict_unchecked
        )

    def __load_translation_dict(self) -> dict:
        translation_dict_checked_files = list(
            filter(
                lambda x: x.startswith(self.translation_dict_checked_filename),
                os.listdir("tw_dicts"),
            )
        )
        translation_dict = {}
        task0 = progress.add_task(
            "[cyan]Loading dictionaries...", total=len(translation_dict_checked_files)
        )
        for translation_dict_file in translation_dict_checked_files:
            with open(
                f"tw_dicts/{translation_dict_file}", "r", encoding="utf-8-sig"
            ) as f:
                task = progress.add_task(
                    f"{os.path.basename(translation_dict_file)}",
                    total=os.path.getsize(f"tw_dicts/{translation_dict_file}"),
                )
                for line in f:
                    if not line.strip() or line.startswith("#"):
                        continue
                    key, val = line.strip().split("\t")
                    translation_dict[key] = val
                    progress.update(task, advance=len(line.encode("utf-8")))
                progress.remove_task(task)
            progress.update(task0, advance=1)
        progress.remove_task(task0)
        return translation_dict

    def __save_translation_dict(self, dict_filename: str, dict_obj: dict):
        file_index = 1
        current_file = open(
            f"tw_dicts/{dict_filename}_{file_index}.txt", "w", encoding="utf-8-sig"
        )
        task = progress.add_task(
            f"[cyan]Saving to {dict_filename}{file_index}", total=len(dict_obj)
        )
        for i, (key, val) in enumerate(sorted(dict_obj.items())):
            current_file.write(key + "\t" + val + "\n")
            progress.update(task, advance=1)

            if i % 10000000 == 0 and i > 0:
                current_file.close()
                file_index += 1
                current_file = open(
                    f"tw_dicts/{dict_filename}_{file_index}.txt",
                    "w",
                    encoding="utf-8-sig",
                )
                progress.update(
                    task,
                    description=f"[cyan]Saving to {dict_filename}{file_index}",
                )
        current_file.close()
        progress.remove_task(task)

        # Check if there are more files undeleted
        translation_dict_files = list(
            filter(
                lambda x: x.startswith(dict_filename),
                os.listdir("tw_dicts"),
            )
        )
        for translation_dict_file in translation_dict_files:
            index = int(
                translation_dict_file.removeprefix(f"{dict_filename}_").removesuffix(
                    ".txt"
                )
            )
            if index > file_index:
                os.remove(f"tw_dicts/{translation_dict_file}")
                print(f"Removed {translation_dict_file} as it is not needed anymore.")

    def __load_file_by_line(self, from_dict_file: str):
        with open(from_dict_file, "r", encoding="utf-8-sig") as f:
            task = progress.add_task(
                os.path.basename(from_dict_file), total=os.path.getsize(from_dict_file)
            )
            for line in f:
                yield line
                progress.update(task, advance=len(line.encode("utf-8")))
            progress.remove_task(task)

    def __load_file_lines(self, from_dict_file: str) -> list:
        from_dict_lines = []
        for line in self.__load_file_by_line(from_dict_file):
            from_dict_lines.append(line)
        return from_dict_lines

    def __write_file(self, to_dict_file: str, to_dict_lines: list):
        with open(to_dict_file, "w", encoding="utf-8-sig") as f:
            task = progress.add_task("Writing...", total=1)
            f.writelines(to_dict_lines)
            progress.remove_task(task)

    def __contains_cjk(self, s: str) -> bool:
        # CJK Unified Ideographs
        if re.search(r"[\u4E00-\u9FFF]", s):
            return True

        # CJK Unified Ideographs Extension A
        if re.search(r"[\u3400-\u4DBF]", s):
            return True

        # CJK Unified Ideographs Extension B
        if re.search(r"[\U00020000-\U0002A6DF]", s):
            return True

        # CJK Unified Ideographs Extension C
        if re.search(r"[\U0002A700-\U0002B73F]", s):
            return True

        # CJK Unified Ideographs Extension D
        if re.search(r"[\U0002B740-\U0002B81F]", s):
            return True

        # CJK Unified Ideographs Extension E
        if re.search(r"[\U0002B820-\U0002CEAF]", s):
            return True

        # CJK Unified Ideographs Extension F
        if re.search(r"[\U0002CEB0-\U0002EBEF]", s):
            return True

        # CJK Unified Ideographs Extension G
        if re.search(r"[\U00030000-\U0003134F]", s):
            return True

        # CJK Unified Ideographs Extension H
        if re.search(r"[\U00031350-\U000323AF]", s):
            return True

        # CJK Unified Ideographs Extension I
        if re.search(r"[\U0002EBF0-\U0002EE5F]", s):
            return True

        # CJK Compatibility Ideographs
        if re.search(r"[\uF900-\uFAFF]", s):
            return True

        # CJK Compatibility Ideographs Supplement
        if re.search(r"[\U0002F800-\U0002FA1F]", s):
            return True

        # # CJK Radicals / Kangxi Radicals
        # if re.search(r'[\u2F00-\u2FDF]', s):
        # 	return True

        # # CJK Radicals Supplement
        # if re.search(r'[\u2E80-\u2EFF]', s):
        # 	return True

        # # CJK Strokes
        # if re.search(r'[\u31C0-\u31EF]', s):
        # 	return True

        # # CJK Symbols and Punctuation
        # if re.search(r'[\u3000-\u303F]', s):
        # 	return True

        return False

    def __convert(self, key: str) -> str:
        if not self.__contains_cjk(key):
            return key

        if key in self.translation_dict:
            self.translation_dict_filtered[key] = self.translation_dict[key]
            return self.translation_dict[key]
        elif key in self.translation_dict_unchecked:
            return self.translation_dict_unchecked[key]
        else:
            translation = self.converter.convert(key)
            self.translation_dict_unchecked[key] = translation
            return translation

    def translate(self, from_dict_file: str, to_dict_file: str):
        if from_dict_file.endswith("emoji.txt"):
            self.translate_emoji_txt(from_dict_file, to_dict_file)
            return
        if from_dict_file.endswith("others.txt"):
            self.translate_others_txt(from_dict_file, to_dict_file)
            return

        to_dict_lines = []
        file_iter = self.__load_file_by_line(from_dict_file)

        # header lines
        if from_dict_file.endswith(".dict.yaml"):
            for line in file_iter:
                if line.startswith("name:"):
                    line = line.strip() + "_tw\n"
                to_dict_lines.append(line)
                if line == "...\n":
                    break

        # entries
        for line in file_iter:
            if line == "3D打印	sanDdayin\n":  # Temporary fix for 3D列印
                line = "3D打印	sanDdayin\n3D列印	sanDlieyin\n"
            elif line == "3D打印	sanddayin\n":
                line = "3D打印	sanddayin\n3D列印	sandlieyin\n"
            elif not line.startswith("#"):  # skip comments
                if "\t" in line:
                    key, val = line.split("\t")[0], "\t".join(line.split("\t")[1:])
                    key = key.strip()
                    val = val.strip()
                    translation = self.__convert(key)
                    line = translation + "\t" + val + "\n"
                elif line.strip():
                    key = line.strip()
                    translation = self.__convert(key)
                    line = translation + "\n"
            to_dict_lines.append(line)

        self.__write_file(to_dict_file, to_dict_lines)

    def translate_emoji_txt(self, from_dict_file: str, to_dict_file: str):
        to_dict_lines = []

        for line in self.__load_file_by_line(from_dict_file):
            key, vals = line.split("\t")
            val0 = vals.split(" ")[0]
            try:
                assert key == val0  # should be same as key
            except AssertionError:
                print(f"Error in {from_dict_file}: `{key}` != `{val0}`")
                raise
            val_rest = vals[len(val0) :]
            translation = self.__convert(key)
            line = translation + "\t" + translation + val_rest
            to_dict_lines.append(line)

        self.__write_file(to_dict_file, to_dict_lines)

    def translate_others_txt(self, from_dict_file: str, to_dict_file: str):
        from_dict_lines = self.__load_file_lines(from_dict_file)

        # Split by sections, with each section starting with a line containing caption
        def split_sections(from_dict_lines: list) -> list:
            sections = []
            section = []
            for line in from_dict_lines:
                if line.startswith("----"):
                    if section:
                        sections.append(section)
                        section = []
                section.append(line)
            if section:
                sections.append(section)
            return sections

        def unique(lst: list) -> list:
            seen = set()
            return [x for x in lst if not (x in seen or seen.add(x))]

        # Translate each section
        def translate_section(section_lines: list) -> str:
            if len(section_lines) < 2:
                return "".join(section_lines)

            caption = section_lines[0].replace("--", "").strip()

            if caption == "其他" or caption == "生活大爆炸&老友记":
                for i in range(1, len(section_lines)):
                    key, vals = section_lines[i].split("\t")
                    vals = vals.strip().split(" ")

                    key = self.__convert(key.strip())
                    vals = [self.__convert(val.strip()) for val in vals]
                    vals = unique(vals)  # remove duplicates
                    section_lines[i] = key + "\t" + " ".join(vals) + "\n"

            # elif caption.endswith("叠字"):
            # 	for i in range(1, len(section_lines)):
            # 		key, vals = section_lines[i].split("\t")
            # 		val0 = vals.split(" ")[0]
            # 		try:
            # 			assert key == val0  # should be same as key
            # 		except AssertionError:
            # 			print(f"Error in {from_dict_file}: `{key}` != `{val0}`")
            # 			raise
            # 		val_rest = vals[len(val0):]
            # 		if len(key) == 3 and key[1] == '个':
            # 			# temporary: manual conversion for 叠字
            # 			translation = self.__convert(key[0]) + "個" + key[2]
            # 			self.translation_dict_unchecked[key] = translation
            # 		else:
            # 			translation = self.__convert(key)
            # 		line = translation + "\t" + translation + val_rest

            else:
                for i in range(1, len(section_lines)):
                    try:
                        key, vals = section_lines[i].split("\t")
                    except ValueError:
                        continue  # skip that line
                    val0 = vals.split(" ")[0]
                    try:
                        assert key == val0  # should be same as key
                    except AssertionError:
                        print(f"Error in {from_dict_file}: `{key}` != `{val0}`")
                        raise
                    val_rest = vals[len(val0) :]
                    translation = self.__convert(key)
                    line = translation + "\t" + translation + val_rest
                    section_lines[i] = line

            return "".join(section_lines)

        sections = split_sections(from_dict_lines)
        to_dict_lines = [translate_section(section) for section in sections]

        self.__write_file(to_dict_file, to_dict_lines)


def generate_dict_list(from_dir: str, to_dir: str):
    from_dict_files = []
    for root, dirs, files in os.walk(from_dir):
        for file in files:
            if file.endswith(".dict.yaml") and not file.endswith("_tw.dict.yaml"):
                from_dict_files.append(os.path.join(root, file))
    dict_list = []
    for from_dict_file in from_dict_files:
        to_dict_file = from_dict_file.replace(from_dir, to_dir)
        to_dict_file = to_dict_file.replace(".dict.yaml", "_tw.dict.yaml")
        dict_list.append((from_dict_file, to_dict_file))
    return dict_list


if __name__ == "__main__":
    with Progress() as progress:
        translator = Translator("s2tw")

        dict_list = generate_dict_list("cn_dicts", "tw_dicts")
        dict_list.append(("en_dicts/cn_en.txt", "en_dicts/tw_en.txt"))
        dict_list.append(("opencc/emoji.txt", "opencc/emoji_tw.txt"))
        dict_list.append(("opencc/others.txt", "opencc/others_tw.txt"))

        task = progress.add_task("[cyan]Translating...", total=len(dict_list))
        for from_dict_file, to_dict_file in dict_list:
            translator.translate(from_dict_file, to_dict_file)
            progress.update(task, advance=1)
        progress.remove_task(task)

        translator.save()
        print("All done.")
