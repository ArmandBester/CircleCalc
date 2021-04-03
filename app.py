

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Circle'
server = app.server



## Layout
#####################################################################################
app.layout = html.Div(children=[
    html.H4(["Circle segment calculator"], 
            style={'justify-content': 'center', 'text-align': 'center', 'margin-top': '1vw'}),

    html.Div([

        html.Div(["Radius: ",
        html.Br(),
        #Radius
        dcc.Input(
                id="radius", type="number", 
                min=0, step=1, value=100),
                ]),
        
        html.Div(["Dist. from center: ",
        html.Br(),
        # Lenght
        dcc.Input(
                id="len", type="number",
                min=0, step=1, value=70),
        
         html.Div(["Value to scale up: ",
        html.Br(),
        #Scale
        dcc.Input(
                id="scaleUp", type="number", 
                min=0, step=1, value=0),
                ]),        
        
        ]),
        
        html.Br(),
        html.P("Your results:"),

        dcc.Textarea(
            id='result',  
            readOnly=False,  
            contentEditable=False,     
            disabled=True,   
            style={'width': '90%', 'height': 140}
            
        ),
                
        ],style= {'width': '30%', 'display': 'inline-block', 'vertical-align': 'top','margin-left': '3vw', 'margin-top': '3vw'}),
        
        ## Graphics
        html.Div([
        # Circle
            dcc.Graph(id='circle')
        ],style= {'width': '60%', 'display': 'inline-block'}),      
])


# Plot
#####################################################################################
@app.callback(
    [Output('circle', 'figure'),
    Output('result', 'value'),
    Output('len', component_property='max'),
    Output('radius', component_property='min')],
    [Input('radius', 'value'),
    Input('len', 'value'),
    Input('scaleUp', 'value')])

def callback_result(r_value, l_value, toScale):
    r = r_value
    l = l_value
    d = r*2
    k = r - l
    c = np.sqrt(r**2 - l**2)
    A = np.round(np.pi*r**2, 2)

    # calculations 
    phix2 = np.rad2deg(np.arcsin(c/r))*2
    ratio = phix2/360.0
    pizzaSlice = ratio * A
    triangle = 2*c*0.5*l
    segment = pizzaSlice - triangle

    ratio = segment/A
    per = np.round(ratio * 100, 2)
    atScale = np.round(ratio**-1 * toScale)

    # Figure layout
    my_layout = go.Layout({"showlegend": False})    
    fig = go.Figure(layout=my_layout)
    fig.update_layout(width=800, height=800,template='plotly_dark')

    s = 1.2
    # Set axes properties
    fig.update_xaxes(range=[-r*s, r*s], zeroline=False)
    fig.update_yaxes(range=[-r*s, r*s])

    # Create scatter trace of text labels
    fig.add_trace(go.Scatter(
        x=[0.5*l],
        y=[0.03*r],
        text=[l],
        mode="text",
    ))
    fig.add_trace(go.Scatter(
        x=[0.45*l],
        y=[0.55*c],
        text=[r],
        mode="text",
    ))
    fig.add_trace(go.Scatter(
        x=[l*1.1],
        y=[0.5*c],
        text=[np.round(c,1)],
        mode="text",
    ))
    fig.add_trace(go.Scatter(
        x=[l - l * 0.12],
        y=[-0.1 * r],
        text=[f'Area: {np.round(segment,2)}'],
        mode="text"   
    ))
    # Add circle
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=-r, y0=-r, x1=r, y1=r,
        line_color="LightSeaGreen",
    )
    # Add lines
    fig.add_shape(type="line",
        xref="x", yref="y",
        x0=0, y0=0, x1=l, y1=0,
        line=dict(
            color="orange",
            dash='dash',
            width=2,
        ))
    fig.add_shape(type="line",
        xref="x", yref="y",
        x0=l, y0=0, x1=l, y1=c,
        line=dict(
            color="orange",
            dash='dot',
            width=1,
        ))
    fig.add_shape(type="line",
        xref="x", yref="y",
        x0=l, y0=0, x1=l, y1=-c,
        line=dict(
            color="orange",
            dash='dot',
            width=1,
        ))
    fig.add_shape(type="line",
        xref="x", yref="y",
        x0=0, y0=0, x1=l, y1=c,
        line=dict(
            color="orange",
            dash='dash',
            width=2,
        ))

    result = f'Circumference: {np.round(2*r*np.pi, 2):,}\nLength of segment {np.round(2*c,2):,}\nArea of segment: {np.round(segment, 2):,}\nArea of circle: {np.round(A, 2):,}\nPercentage: {per}\nValue at scale: {atScale}'

    
    return fig, result, r, l





if __name__ == '__main__':
    app.run_server()
