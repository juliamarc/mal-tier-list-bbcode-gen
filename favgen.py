# list of tier files
# this list determines the order in which the tiers will be displayed
# you can remove or add files if you want
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

with open(output_file, "w") as output:
    for tier_file in tier_files:
        with open(tier_file, "r") as f:
            lines = f.read().splitlines()
            tier_banner = lines[0]
            tier_characters = lines[1:]

            output.write(f"[img]{tier_banner}[/img]\n")

            for character in tier_characters:
                img, mal = character.split(",")
                output.write(f"[url={mal}][img]{img}[/img][/url]")

            output.write("\n")
