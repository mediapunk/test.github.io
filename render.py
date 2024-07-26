#!/usr/bin/env python
import json
import yaml
import os
from jinja2 import Environment, FileSystemLoader, DebugUndefined

from pathlib import Path
import traceback
import datetime
from glob import glob  # Add this line for importing glob
from tqdm import tqdm

# Create an empty dictionary to store template variables to be passed
data = dict()

# Add today's date, properly formatted, to the data dict to display at the bottom
# of the page
data['today'] = datetime.date.today().strftime('%Y-%m-%d')

# Load assets that can be used by templates. Assets are yaml files with data
for pathname in tqdm(glob('content/*.y*ml'), desc='Loading content'):
    path = Path(pathname)
    fname = path.stem
    with path.open('r') as f:
        assetdata = yaml.safe_load(f)
    if type(assetdata) is not dict:
        assetdata = {fname: assetdata}
    data.update(assetdata)

# Scan sections in the sections directory; there will be a section header for
# each one of these
data['sections'] = []
sectionfiles = glob('sections/*.html')
try:
    order = yaml.safe_load(Path('sections/order.yaml').open('r'))
    comparator = lambda key: (order + [Path(key).stem]).index(Path(key).stem)
except FileNotFoundError:
    comparator = lambda key: key

# for sectionfile in tqdm(sorted(sectionfiles, key=comparator), 
#                         desc='Processing sections'):
#     sectionfile = Path(sectionfile)
#     fname = sectionfile.stem
#     sectionenv = Environment(loader=FileSystemLoader('sections'), 
#                              extensions=['jinja_markdown2.MarkdownExtension'],
#                              undefined=DebugUndefined)
#     sectiontempl = sectionenv.get_template(sectionfile.name)
#     data['sections'] += [dict(name=fname, content=sectiontempl.render(**data))]

# Create a Jinja2 environment instance
jinja_env = Environment(loader=FileSystemLoader('templates'),
                        undefined=DebugUndefined)

# template
tfile = "index.html"
# Get template
template = jinja_env.get_template(tfile)

# Render template and output it to index.html, the default page to show
output_path = Path('output')  #change path as needed
output_path.mkdir(exist_ok=True)

output_file_path = output_path.joinpath(tfile)
with output_file_path.open('w') as out:
    out.write(template.render(**data))

print(f"index.html saved at: {output_file_path}")