# MAL Tier List BBCode Generator

![workflow](https://github.com/juliamarc/mal-tier-list-bbcode-gen/actions/workflows/mal-tier-list-bbcode-gen.yaml/badge.svg)

`mal-tier-list-bbcode-gen` generates BBCode for tier lists with custom images corresponding to entries in MAL (characters, anime, manga, people).
Each image is also a link to the respective entry's MAL page.

[Example character tier list](https://myanimelist.net/blog.php?eid=844887)

## Installation
```
pip install mal-tier-list-bbcode-gen
```
or
```
git clone https://github.com/juliamarc/mal-tier-list-bbcode-gen
cd mal-tier-list-bbcode-gen
```

## User guide

### Tiers
Each tier is represented by one sheet of the `tiers.ods` spreadsheet.

### Entries
Each entry consists of a link to MAL and a link to an image.

### Headers
Each tier has a header that's also an image.
Some example headers and the `.xcf` file (GIMP format) that was used to generate them can be found in `example-headers`.

### Image source
The images need to be hosted somewhere.
Currently there are two options:
* upload your images to an image hosting service like [Postimages](https://postimages.org/) and use the direct URL, or
* upload your images to Google Drive
    - create a folder for the images
    - make it public ("Anyone with the link can view")
    - use the generated share links ("Get sharable link" for each image)

### Image size
It's best for all the images to be the same size.
MAL's BBCode doesn't allow for resizing, so the desired image size needs to be set before upload.

Another tip on image size is to make the header width divisible by the entry image's width so they tile nicely.

### Settings
Basic settings can be found in the `SETTINGS` sheet.
Curretnly there are two settings:
* "Tier order" - list of the tier sheets that will be included in the BBCode and the order in which they will be displayed
* "Entries per row" - how many entries will be displayed in one row

## Usage

You can edit the `tiers.ods` file directly or create a copy of it.
I will show an example for `tiers.ods` here, but if your file is named differently then just replace `tiers` with your file's name.

1. Fill out the `tiers.ods` file
2. Run
    - `mal-tier-list-bbcode-gen tiers.ods` if you installed with pip
    - `python -m mal_tier_list_bbcode_gen tiers.ods` if you used `git clone`

The BBCode can be found in `tiers.bbcode.txt` and a preview of it is in `preview.html`.

### Adding a tier
Add a sheet to the spreadsheet and add its name to the "Tier order" in `SETTINGS`.

### Removing a tier
Delete the tier's name from the "Tier order" in `SETTINGS`.
The sheet doesn't have to be removed from the spreadsheet.
