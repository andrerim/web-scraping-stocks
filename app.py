import dash
import dash_core_components as dcc
import dash_html_components as html


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Stock analyser'),

    html.Div(children='''
        A project for learning web scraping and dash.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Stock data'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)