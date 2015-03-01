from flask import render_template, Flask
import numpy as np
from collections import OrderedDict

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.resources import Resources
from bokeh.templates import RESOURCES
from bokeh.utils import encode_utf8
from bokeh.models import HoverTool

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def test_plot():
    p = create_plot()
    plot_script, plot_div = components(p, CDN)

    resources = Resources("inline")
    plot_resources = RESOURCES.render(
        js_raw=resources.js_raw,
        css_raw=resources.css_raw,
        js_files=resources.js_files,
        css_files=resources.css_files,
    )

    html = render_template('bokeh_plot.html', plot_resources=plot_resources,
                           plot_script=plot_script, plot_div=plot_div)
    return encode_utf8(html)


def create_plot():
    #Make data
    N = 100
    x = np.linspace(0, 4*np.pi, N)
    y = np.sin(x)

    #output_file("legend.html", title="legend.py example")

    TOOLS = "pan,box_zoom,reset,save,crosshair,hover"

    p = figure(title="An Example", tools=TOOLS, plot_width=900, plot_height=500)
    p.circle(x, y, radius=.05, legend="sin(x)")
    p.line(x, y, legend="sin(x)")

    p.line(x, 2*y, legend="2*sin(x)",
            line_dash=[4, 4], line_color="orange", line_width=2)

    p.square(x, 3*y, legend="3*sin(x)",
            fill_color=None, line_color="green")
    p.line(x, 3*y, legend="3*sin(x)",
            fill_color=None, line_color="green")

    p.xaxis.axis_label = 'Index'
    p.yaxis.axis_label = 'Signal'
    hover = p.select(dict(type=HoverTool))

    hover.tooltips = OrderedDict([
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("fill color", "$color[hex, swatch]:fill_color"),
        ("foo", "@foo"),
        ("bar", "@bar")
    ])

    return p

if __name__ == '__main__':
    # debug=True allows the server to listen for changes in the code and
    # updates in realtime, use only in development
    PORT = 5005
    HOST = 'localhost'
    app.run(debug=True, host=HOST, port=PORT)