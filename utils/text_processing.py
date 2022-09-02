import re

NUMBER_WORD_DICT = {
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

DEFAULT_POINT = 15


def extract_point(raw_str: str) -> int:
    l_raw = raw_str.lower()
    num_list = re.findall(r"(?<=for)(.*)(?=minutes|minute|hour|hours)", l_raw)
    unit_list = re.findall(r"minutes|minute|hour|hours", l_raw)
    if not num_list:
        return DEFAULT_POINT

    num_str = num_list[-1].strip()
    unit_str = unit_list[-1].strip()
    try:
        return int(num_str) * (60 if unit_str.startswith("h") else 1)
    except ValueError:
        if num_str in NUMBER_WORD_DICT:
            return NUMBER_WORD_DICT[num_str] * 60 if unit_str.startswith("h") else 1
        return DEFAULT_POINT


if __name__ == "__main__":
    print(extract_point("Sweep the floor for 15 minutes"))
