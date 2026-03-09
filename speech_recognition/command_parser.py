
import re

def chinese_to_number(text):

    chinese_map = {
        "零":0,"一":1,"二":2,"三":3,"四":4,
        "五":5,"六":6,"七":7,"八":8,"九":9
    }

    if "十" in text:

        parts = text.split("十")

        if parts[0] == "":
            tens = 1
        else:
            tens = chinese_map.get(parts[0],0)

        if len(parts) > 1 and parts[1] != "":
            ones = chinese_map.get(parts[1],0)
        else:
            ones = 0

        return tens*10 + ones


    if text in chinese_map:
        return chinese_map[text]

    return None


def parse_command(text):

    action = None
    device = None
    value = None

    if "打开" in text:
        action = "open"

    if "关闭" in text:
        action = "close"

    if "空调" in text:
        device = "air_conditioner"

    numbers = re.findall(r'\d+', text)
    if numbers:
        value = numbers[0]
    else:
         match=re.search(r'[一二三四五六七八九十]+', text)
          if match:
              value= chinese_to_number(match.group())
    return action, device, value



