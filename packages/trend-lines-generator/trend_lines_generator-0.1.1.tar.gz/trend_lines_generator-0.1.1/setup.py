# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trend_lines', 'trend_lines.factories', 'trend_lines.models']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0']

setup_kwargs = {
    'name': 'trend-lines-generator',
    'version': '0.1.1',
    'description': 'Trend lines generator.',
    'long_description': '# Trend lines generator\n\nUsage example:\n```python\n#! pip install trend-lines-generator\nimport requests\nimport mplfinance as mpf\nfrom pandas import DataFrame, to_datetime\n\nfrom trend_lines import generate_trend_lines, Side\n\n\ndef main():\n    columns = [\n        ("ts", "int"),\n        ("volume_quote", "float64"),\n        ("open", "float64"),\n        ("high", "float64"),\n        ("low", "float64"),\n        ("close", "float64"),\n    ]\n    url = "https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair=MOVR_USDT&interval=1h&limit=100"\n    response = requests.get(url)\n\n    rows = response.json()\n\n    df = (\n        DataFrame([r[: len(columns)] for r in rows], columns=[i[0] for i in columns])\n        .astype(dict(columns))\n        .set_index("ts")\n    )\n    df.index = to_datetime(df.index, unit="s")\n\n    lines = generate_trend_lines(low_series=df["low"], high_series=df["high"])\n\n    x1 = df.index[0]\n    x2 = df.index[-1]\n\n    mpf.plot(\n        df,\n        type="candle",\n        tight_layout=True,\n        alines={\n            "alines": [((x1, line.get_y(x1)), (x2, line.get_y(x2))) for line in lines],\n            "colors": ["g" if line.side == Side.LOW else "r" for line in lines],\n        },\n    )\n\n\nif __name__ == "__main__":\n    main()\n```\n\n![trend lines](https://github.com/nanvel/trend-lines/raw/master/docs/trend_lines.png)\n',
    'author': 'Oleksandr Polieno',
    'author_email': 'polyenoom@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nanvel/trend-lines-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
