import SCBPOP
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

#app settings
external_CSS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_CSS)

#Get stats from SCB by querying API
regionCodes = ["01","03","04","05","06","07","08","09","10","12","13","14","17","18","19","20","21","22","23","24","25"]
SCBData= SCBPOP.SCB(regionCodes).getPop()

#Multi Dropdown component
dropDown = dcc.Dropdown(
    options= [{'label': key, 'value': key} for key in SCBData.keys() if key != 'Year'],
    multi=True,
    value=['Stockholm','Uppsala'],
    id='menu'
)

#Bar Chart component
barColors = ['#003f5c','#d45087','#2f4b7c','#f95d6a','#665191','#a05195','#ff7c43','#ffa600','#003f5c','#d45087','#2f4b7c','#f95d6a','#665191','#a05195','#ff7c43','#ffa600','#003f5c','#d45087','#2f4b7c','#f95d6a','#665191','#a05195','#ff7c43','#ffa600']
barChart = dcc.Graph(
    figure="",
    style={'height': 300},
    id='barryBar'
)

#Slider component
startYear = min(SCBData['Year'])
endYear = max(SCBData['Year'])
print(10-startYear%10)
markers = {}

if startYear%10 == 0:
    markerList = list(range(startYear, endYear + 1, 5))
else:
    markerList = list(range(startYear+(10-(startYear%10)),endYear+1,5))

markers[startYear] = startYear
for item in markerList:
    markers[item] = item
markers[endYear] = endYear

slider = dcc.RangeSlider(
        id='dateSlider',
        min=startYear,
        max=endYear,
        step=1,
        value=[startYear, endYear],
        marks=markers
    )

#HTML Creation
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('SCB DATA', style={'text-align':'center', 'font-size':40, 'color':'white', 'margin':15, 'font-weight':'bold', 'font-family': 'Arial, serif', 'text-shadow': '0px 3px 0 #3a50d9'})
        ],className="twelve columns")
    ],className="row", style={'backgroundColor':'#003f5c', 'margin-bottom':15 , 'box-shadow':'0px 10px 22px 1px #888888'}),
    html.Div([
        html.Div([
            html.Div([dropDown], style={'margin-top':10,'margin-bottom':10,'margin-left':100,'margin-right':100})
        ],className="twelve columns"),
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([barChart], style={'margin-top':10,'margin-bottom':10,'margin-left':100,'margin-right':100})
        ],className="twelve columns"),
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([slider], style={'margin-top':10,'margin-bottom':10,'margin-left':100,'margin-right':100})
        ],className="twelve columns"),
    ], className="row")
])

#Update BarChart when user interacts with Dropdown or Slider
@app.callback(
    Output(component_id='barryBar', component_property='figure'),
    [Input(component_id='menu', component_property='value'),
     Input(component_id='dateSlider', component_property='value')])

def update_output(regions,dateRange):
    barData = []
    for index,region in enumerate(regions):
        barData.append(go.Bar(
                x=list(range(dateRange[0],dateRange[1]+1,1)),
                y=SCBData[region],name=region,
                marker=go.bar.Marker(color=barColors[index])))

    return go.Figure(
            data= barData,
            layout=go.Layout(
                title='Population i Sverige',
                showlegend=True,
                legend=go.layout.Legend(
                x=0,
                y=1.0
            ),
            margin=go.layout.Margin(l=40, r=0, t=40, b=30)))

if __name__ == '__main__':
    app.run_server(debug=True)
