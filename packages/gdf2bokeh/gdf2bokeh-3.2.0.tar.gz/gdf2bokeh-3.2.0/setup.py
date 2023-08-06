# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdf2bokeh']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=3.1.0,<4.0.0', 'geopandas>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'gdf2bokeh',
    'version': '3.2.0',
    'description': 'An easy way to map geodataframes on bokeh',
    'long_description': '# Gdf2Bokeh\nAn easy way to map your geographic data (from a GeoDataFrame, a DataFrame and a list of dictionaries containing wkt or shapely geometries).\n\nYeah! Because it\'s boring to convert shapely geometry to bokeh format each time I need to map something !!\n\nAlso, this library let you to build complex Bokeh dashboard: no limitations to use Bokeh mecanisms.\n\n[![CI](https://github.com/amauryval/gdf2bokeh/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/amauryval/gdf2bokeh/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/amauryval/gdf2bokeh/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/gdf2bokeh)\n\n[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/version.svg)](https://anaconda.org/amauryval/gdf2bokeh)\n[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/latest_release_date.svg)](https://anaconda.org/amauryval/gdf2bokeh)\n[![Anaconda-Server Badge](https://anaconda.org/amauryval/gdf2bokeh/badges/platforms.svg)](https://anaconda.org/amauryval/gdf2bokeh)\n\n[![PyPI version](https://badge.fury.io/py/gdf2bokeh.svg)](https://badge.fury.io/py/gdf2bokeh)\n\nCheck the demo [here](https://amauryval.github.io/gdf2bokeh/)\n\n\n## How to install it ?\n\n### with pip\n\n```bash\npip install gdf2bokeh\n```\n\n### With Anaconda\n\n```bash\nconda install -c amauryval gdf2bokeh\n```\n\n## How to use it ?\n\nGdf2Bokeh is able to map your data from various format. About data, you must be aware to use compliant geometry types:\n\nIt supports Geo/DataFrame/List of dict/List of geometry containing these 4 geometries families:\n\n* Point data with Point geometry\n* MultiPoint data with MultiPoint geometry\n* Line data with LineString and/or MultiLineString geometries\n* Polygon data with Polygon and/or MultiPolygon geometries\n\nGeometryCollection data are not supported, so explode it to use it. So the best practice consists to split your input \ndata by geometry type. \n\nAnd you\'ll be able, optionally, to style your data thanks to the bokeh arguments :\nCheck bokeh documentation in order to style your data :\n    \n* Point / MultiPoint families: [bokeh marker style options](https://docs.bokeh.org/en/latest/docs/reference/models/markers.html)\n* Line family: [bokeh multi_line style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_line)\n* Polygon family: [bokeh multi_polygon style options](https://docs.bokeh.org/en/latest/docs/reference/plotting.html?highlight=multi_polygons#bokeh.plotting.figure.Figure.multi_polygons)\n\n\n### A simple example\n\n```python\nfrom bokeh.plotting import show\nimport geopandas as gpd\nimport paandas as pd\nfrom gdf2bokeh import Gdf2Bokeh\n\nmap_session = Gdf2Bokeh()\n\n# add your layer from your data\n\n# Map a points GeoDataFrame. You can see marker style arguments, so we suppose that input_data contains Point geometry\nmap_session.add_layer_from_geodataframe("layer1", gpd.GeoDataFrame.from_file("your_poins_data.geojson"),\n                                        size=6, fill_color="red", line_color="blue")\n\n# Map from a DataFrame. Style parameters are not required\nmap_session.add_layer_from_dataframe("layer2", pd.DataFrame.from_file("your_data.json"),\n                                     geom_column="geometry", geom_format="shapely")\n\n# Map from a list of dictionnaries\nmap_session.add_layer_from_dict_list("layer3", \n                                     [\n                                         {"geometry": "POINT(0 0)", "col1": "value1"},\n                                         {"geometry": "POINT(1 1)", "col1": "value2"}\n                                     ],\n                                     geom_column="geometry", geom_format="wkt")\n\n# Map from a geometry (shapely, wkt...) list\nmap_session.add_layer_from_geom_list("layer4", ["Point(0 0)", "Point(5 5)"], geom_format="wkt")\n\n# Let\'s go to register them on bokeh\nmap_session.add_layers_on_map()\n\n# Next, the map is displayed\nshow(map_session.figure)\n```\n\n\nHere a bokeh basic example.\nOn the terminal, run :\n\n```bash\npython examples/bokeh_simple_case_example.py\n```\n\nOr you can use the jupyter notebook \'example.ipynb\'\n\n### An advanced example\n\nHere a bokeh serve example with a slider widget.\nOn the terminal, run :\n\n```bash\nbokeh serve --show examples/bokeh_serve_example.py\n```\n',
    'author': 'amauryval',
    'author_email': 'amauryval@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.0',
}


setup(**setup_kwargs)
