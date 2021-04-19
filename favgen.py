from urllib.parse import unquote

import bbcode

# this list determines the order in which the tiers will be displayed
tier_files = [
    "S_tier.txt",
    "A_tier.txt",
    "B_tier.txt",
    "C_tier.txt",
    "D_tier.txt",
    "E_tier.txt",
    "F_tier.txt",
]
output_file = "favbbcode.txt"

title = "MAL Favorites BBCode Generator"
print(f"\t|{len(title)*'-'}|\n\t|{title}|\n\t|{len(title)*'-'}|")

with open(output_file, "w") as output:
    for i, tier_file in enumerate(tier_files, start=1):
        try:
            with open(tier_file, "r") as f:
                lines = f.read().splitlines()
                tier_banner = lines[0].strip()
                tier_characters_lines = lines[1:]

                output.write(f"[img]{tier_banner}[/img]\n")

                tier_characters = []
                for character in tier_characters_lines:
                    img, mal = map(lambda x: x.strip(), character.split(","))
                    tier_characters.append(
                        "\t" + unquote(mal.split("/")[-1]).replace("_", " "))
                    output.write(f"[url={mal}][img]{img}[/img][/url]")

                output.write("\n")

            print(f"[{i}/{len(tier_files)}] BBCode for file {tier_file} "
                  f"generated successfuly.")

            if tier_characters:
                print("\n".join(tier_characters))

        except FileNotFoundError:
            print(f"[!][{i}/{len(tier_files)}] File {tier_file} not found! "
                  "No BBCode was generated.")

with open(output_file, "r") as f:
    file_data = f.read()
    with open("preview.html", "w") as f2:
        parser = bbcode.Parser(replace_links=False)
        parser.add_simple_formatter('img', '<img src=%(value)s>')
        html = parser.format(file_data)
        f2.write(html)

print(f"Generated BBCode is in file {output_file}")
