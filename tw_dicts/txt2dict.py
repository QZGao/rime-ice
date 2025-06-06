from pypinyin import lazy_pinyin
from pypinyin_dict.pinyin_data import kxhc1983
from pypinyin_dict.phrase_pinyin_data import cc_cedict
from pathlib import Path
from datetime import datetime
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

cc_cedict.load()
kxhc1983.load()


def txt2dict(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
    ) as progress:
        words = file_path.read_text(encoding="utf-8").strip()

        task2 = progress.add_task("Inferencing pinyin...")
        pinyin_res = lazy_pinyin(words)
        pinyin_str = " ".join(pinyin_res).strip()
        pinyin_list = pinyin_str.split(" \n ")
        progress.update(task2, completed=True)

    with Progress() as progress:
        words_split = words.splitlines()
        task3 = progress.add_task(
            "Writing to output file...", total=len(words_split) + 1
        )
        with file_path.with_suffix(".dict.yaml").open(
            "w", encoding="utf-8"
        ) as output_file:
            date_str = datetime.now().strftime("%Y-%m-%d")
            output_file.write(
                f"""# Rime dictionary
# encoding: utf-8
---
name: {file_path.stem}
version: "{date_str}"
sort: origin
use_preset_vocabulary: true
...
"""
            )
            progress.update(task3, advance=1)

            for word, pinyin in zip(words_split, pinyin_list):
                output_file.write(f"{word}\t{pinyin}\t1\n")
                progress.update(task3, advance=1)
            progress.update(task3, completed=True)


if __name__ == "__main__":
    print("Model loaded.")

    import argparse

    parser = argparse.ArgumentParser(
        description="Convert a text file of words to a Rime dictionary format."
    )
    parser.add_argument("file_path", type=str, help="Path to the input text file.")

    args = parser.parse_args()

    if not Path(args.file_path).is_file():
        print(f"Error: The file {args.file_path} does not exist.")
        exit(1)
    print(f"Processing file: {args.file_path}")

    try:
        txt2dict(args.file_path)
        print(
            f"Dictionary created successfully: {Path(args.file_path).with_suffix('.dict.yaml')}"
        )
    except Exception as e:
        print(f"Error: {e}")
