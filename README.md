# l3-data-match
# How to use
The program has the following CLI flags -
* -t Switch execution from normal mode to training mode
* -r Enable raw data (reading from pretrained dict file)
* -d \<path> use path as dictionary file(s)
* -m \<path> use path as file/dir to match with
* -o \<path> use path as output file, if not provided, python will print to STDOUT

There are also two tweakable parameters in settings.json -
* -keep_special Setting this to true will make it so that special characters are **not** replaced by S DEFAULT=true
* -pad_str This value is used to pad the pattern string DEFAULT=" "
