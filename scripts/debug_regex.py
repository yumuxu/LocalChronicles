import re

line_667 = "八闽通志卷之一"
line_1548 = "八闽通志卷之二"

JUAN_PATTERN = re.compile(r"^\s*八?闽?通?志?卷之([一二三四五六七八九十百]+)(.*)$")

m1 = JUAN_PATTERN.match(line_667)
print(f"Line 667 match: {m1}")
if m1:
    print(m1.groups())

m2 = JUAN_PATTERN.match(line_1548)
print(f"Line 1548 match: {m2}")
if m2:
    print(m2.groups())
