import bbcode
import pyexcel_ods as pods

# ods test
data = pods.get_data("tiers.fods")
# print(data.keys())

# bbcode html rendering test
with open("favbbcode.txt", "r") as f:
    file_data = f.read()
    with open("out.html", "w") as f2:
        parser = bbcode.Parser(replace_links=False)
        parser.add_simple_formatter('img', '<img src=%(value)s>')
        html = parser.format(file_data)
        f2.write(html)
