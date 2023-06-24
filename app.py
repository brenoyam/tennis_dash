from dash import html, dcc
import dash
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from app import *
from clear_base import filter_player_dash, dash_base_preparation,dir_serv_perc
import plotly.graph_objects as go
import requests
import json
import pandas as pd


estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.COSMO]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"


# app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])



# load data from local or api later

# df = pd.read_csv('database/charting-m-points-from-2017-enriched_small.csv')




# First Service Graph


def dash_pie_chart(df, title_name):
    # df_service_1st = df[(df['Service']=='1st') & (df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
    fig_service_1 = px.pie(df, values='count', names='dir_srv', hole=.6,color='dir_srv',
                category_orders={'dir_srv':['Wide','Body','Down the T']},
                color_discrete_map={'Wide':'darkblue','Body':'lightblue','Down the T':'MediumPurple'})
    fig_service_1.update_layout(
        title={
            'text': title_name,
            'y':0.93,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(color='gray'),)

    fig_service_1.update_layout(
        paper_bgcolor='rgba(255, 255, 255,0)',
        plot_bgcolor='rgba(0, 0, 0,0)',

    )
    fig_service_1.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)'))

    fig_service_1.update_layout(legend=dict(
        yanchor="middle",
        y=0.50,
        xanchor="center",
        x=0.50,

    ))
    fig_service_1.add_annotation(text="44.2%",
                  xref="paper", yref="paper",
                  x=0.5, y=0.30, showarrow=False,
                  font=dict(
            family="Arial Black",
            size=13,
            color="black"
            ))



    return fig_service_1


# Second Service Graph
# df_service_2nd = df[(df['Service']=='2nd') & (df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
# fig_service_2nd = px.pie(df_service_2nd, values='count', names='dir_srv', hole=.6,color='dir_srv',
#              category_orders={'dir_srv':['Wide','Body','Down the T']},
#              color_discrete_map={'Wide':'darkblue','Body':'lightblue','Down the T':'MediumPurple'})
# fig_service_2nd.update_layout(
#     title={
#         'text': "2nd Service Direction",
#         'y':0.93,
#         'x':0.5,
#         'xanchor': 'center',
#         'yanchor': 'top'})

# fig_service_2nd.update_layout(legend=dict(
#     yanchor="middle",
#     y=0.50,
#     xanchor="center",
#     x=0.50
# ))


# Bar Chart

def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_layout(
        paper_bgcolor='rgba(255, 255, 255,255)',
        plot_bgcolor='rgba(255, 255, 255,255)',

    )

    return fig


def fig_serv_dir(down_t, body, wide, title_name):
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0,0)',
        plot_bgcolor='rgba(0, 0, 0,0)',
    )
    fig.add_annotation(text= '<b>' + down_t + '</b>',
                    xref="paper", yref="paper",
                    x=0.47, y=0.22, showarrow=False,
                    bgcolor='lightblue',
                    width = 40,
                    borderpad = 3)

    fig.add_annotation(text='<b>' + body + '</b>',
                    xref="paper", yref="paper",
                    x=0.60, y=0.25, showarrow=False,
                    bgcolor='lightblue',
                    width = 40,
                    borderpad = 3)

    fig.add_annotation(text='<b>' + wide + '</b>',
                   xref="paper", yref="paper",
                   x=0.77, y=0.25, showarrow=False,
                    bgcolor='lightblue',
                    width = 40,
                    borderpad = 3)


    fig.update_layout(
            title={
                'text': "<b>"+ title_name+"</b>",
                'y':0.9,
                'x':0.95,
                'xanchor': 'right',
                'yanchor': 'top',
                'font_color':'white',
                'font_size':20})



    return fig

def dash_bar_chart(df):
    # df_bar = df[(df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
    fig = px.histogram(df, x='Service',y = 'count',barnorm='percent',color='Win',facet_col="Surface",
                    category_orders={"Service": ["1st", "2nd"],
                                "Win": ["Win", "Loss"],
                                "Surface": ["Clay","Grass","Hard"]},
                    color_discrete_map={'Win':'darkblue','Loss':'mediumpurple'},text_auto=True,)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(
        yaxis=dict(
            showgrid=True,
            showline=True,
            showticklabels=True,
            zeroline=True,
        ),
        paper_bgcolor='rgba(255, 255, 255,0.6)',#fundo
        plot_bgcolor='rgba(0, 0, 0,0)', # fundo do plot
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False, texttemplate='%{y:.1f}',)
    fig.update_layout(
        title="Performance by Service",
        legend_title="",
        font=dict(color='black')
    )
    fig.update_yaxes(showgrid=False)

    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)'))
    fig.update_layout(yaxis_title=None)
    fig.update_layout(xaxis_title="Service")

    return fig


def dash_bar_service(df):
    fig = px.bar(df, y='Return',x = 'Weight(%)',text_auto=True,orientation='h')
    fig.update_layout(
            yaxis=dict(
                showgrid=True,
                showline=True,
                showticklabels=True,
                zeroline=True,
            ),
            paper_bgcolor='rgba(255, 255, 255,0.6)',#fundo
            plot_bgcolor='rgba(0, 0, 0,0)', # fundo do plot
        )
    fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False, texttemplate='%{x:.1f}',)
    fig.update_layout(
            title="Top 5 - Service Returning Weight (%)",
            legend_title="",
            font=dict(color='black')
        )
    fig.update_yaxes(showgrid=False)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(marker_color='MediumPurple')

    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)'))
    fig.update_layout(yaxis_title=None)
    fig.update_layout(xaxis_title="Return")

    return fig

def dash_win(df):
    fig = px.pie(df, values='Count', names='Win', hole=.6,color='Win',
             category_orders={'Win':['Win','Loss']},
             color_discrete_map={'Win':'darkblue','Loss':'MediumPurple'})
    fig.update_layout(
        title={
            'xanchor': 'center',
            'yanchor': 'top',
            'font_color':'Black',
            'font_size':20})
    fig.update_layout(title_text='Win Status', title_x=0.5)
    fig.update_layout(margin=dict(t=70, b=60, l=10, r=10))
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.001,
        xanchor="center",
        x=0.5
    ))
    return fig


# Dash Layout

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Img(src='https://github.com/brenoyam/tennis_dash/blob/main/assets/le_wagon.png?raw=true', id='logo_2',
                    className='perfil_avatar'),
            html.Br(),
            html.P('Tennis Analytics', className="text-info"),
            html.Hr(),

            # Carregar Logo
            # dbc.Button(id = "img_player",children=[], style={'background-color':'transparent','border-color':'transparent'}),

            dbc.Button(id = "botao_logo",
                    children=[html.Img(src='https://github.com/brenoyam/tennis_dash/blob/main/assets/tennis_logo.png?raw=true', id='logo',
                    className='perfil_avatar')], style={'background-color':'transparent','border-color':'transparent'}),



            dbc.Select(
                    id="select_player",
                    options=[
                        {"label": "Novak Djokovic", "value": "Novak Djokovic"},
                        {"label": "Rafael Nadal", "value": "Rafael Nadal"},
                        {"label": "Roger Federer", "value": "Roger Federer"},
                    ]),

            html.Br(),

            dbc.Button("Run", id = 'btn_run',size="lg", className="me-1"),

        ], md=2, style={'height':'1080px'}),



        dbc.Col([
            dbc.Row([
                    dbc.Col(dbc.Button(id = "img_player",children=[], style={'background-color':'transparent','border-color':'transparent'}),width=2),
                    dbc.Col(dbc.Card(dcc.Graph(id='graph_1',figure = blank_fig()),style={'padding':'0px','background-color':'transparent','background-image':"url('https://github.com/brenoyam/tennis_dash/blob/main/assets/court_final.jpeg?raw=true')",'background-repeat': 'no-repeat','background-size': '1800px 1800px','background-size': 'cover'}),width=5),
                    dbc.Col(dbc.Card(dcc.Graph(id='graph_2',figure = blank_fig()),style={'padding':'0px','background-color':'transparent','background-image':"url('https://github.com/brenoyam/tennis_dash/blob/main/assets/court_final.jpeg?raw=true')",'background-repeat': 'no-repeat','background-size': '1800px 1800px','background-size': 'cover'}),width=5),
                ],style={'margin':'10px'}),

            # dbc.Row([
            #         dbc.Col(dbc.Card(dcc.Graph(id='graph_1',figure=fig_service_1),style={'padding':'10px'}),width=6),
            #         dbc.Col(dbc.Card(dcc.Graph(id='graph_2',figure=fig_service_2nd),style={'padding':'10px'}),width=6),
            #     ],style={'margin':'10px'}),


            dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='graph_5',figure = blank_fig()),style={'padding':'10px','background-color':'transparent'}),width=2),
                    dbc.Col(dbc.Card(dcc.Graph(id='graph_3',figure = blank_fig()),style={'padding':'10px','background-color':'transparent'}),width=5),
                    dbc.Col(dbc.Card(dcc.Graph(id='graph_4',figure = blank_fig()),style={'padding':'10px','background-color':'transparent'}),width=5),




                ],style={'margin':'10px'})

            # ],md=10,style={'height':'1080px','background-image':"url('/assets/wimbledon.jpg')",'background-repeat': 'no-repeat','background-size': '1800px 1800px','background-size': 'cover'})
            ],md=10,style={'height':'1080px','background-repeat': 'no-repeat','background-size': '1800px 1800px','background-size': 'cover'})

    ])

], fluid=True)


@app.callback([
    Output('graph_1', 'figure'),
    Output('graph_2', 'figure'),
    Output('graph_3', 'figure'),
    Output('graph_4', 'figure'),
    Output('graph_5', 'figure'),
    Output('img_player', 'children')],
    [Input('btn_run', 'n_clicks'),
     State('select_player','value')])


def multi_output(btn, selection):

    # selection = 'Rafael Nadal'

    df = pd.read_csv('https://raw.githubusercontent.com/brenoyam/tennis_dash/main/charting-m-points-from-2017-enriched_small.csv',low_memory=False)
    df_tmp = filter_player_dash(df,selection)


    url = 'https://alvespublico.com:8001/player_summary/'
    url_2 = 'https://alvespublico.com:8001/player_top5/'
    # url_3 = 'https://alvespublico.com:8001/player_wins/'

    # url_player = url + selection
    # response = requests.get(url=url_player).json()
    # df_tmp = pd.DataFrame.from_records(response)


    url_player_2 = url_2 + selection
    response_2 = requests.get(url=url_player_2).json()
    df_tmp_2 = pd.DataFrame.from_records(response_2)
    df_tmp_2 = df_tmp_2.rename(columns={'ds_return':'Return','serve_return':'Weight(%)'})



    # url_wins = url_3 + selection
    # response_wins = requests.get(url=url_wins).json()
    # response_wins= response_wins.replace('[', '').replace(']','')
    # response_wins = response_wins.split(', ')

    # data_win = [['Win', response_wins[0]],['Loss', response_wins[1]]]
    # data_win = pd.DataFrame(data_win, columns=['Win', 'Count'])
    # fig_win = dash_win(data_win)

    df_wins = pd.read_csv('https://raw.githubusercontent.com/brenoyam/tennis_dash/main/win_loss_table.csv', low_memory=False)
    df_wins = df_wins[df_wins['Player'] == selection]
    data_win = [['Win', df_wins['Win'].item()],['Loss', df_wins['Loss'].item()]]
    data_win = pd.DataFrame(data_win, columns=['Win', 'Count'])

    fig_win = dash_win(data_win)


    # First Service Graph
    # df_1st = df_tmp[(df_tmp['Service']=='1st') & (df_tmp['Serving']=='Serving') & (df_tmp['isAce'] == 0)]
    # fig_1st = dash_pie_chart(df_1st,'1st Service Direction')
    first_down, first_body, first_wide, second_down, second_body, second_wide = dir_serv_perc(df_tmp)
    fig_1st = fig_serv_dir(first_down,first_body,first_wide,'1st Service')


    # df_2nd = df_tmp[(df_tmp['Service']=='2nd') & (df_tmp['Serving']=='Serving') & (df_tmp['isAce'] == 0)]
    fig_2nd = fig_serv_dir(second_down,second_body,second_wide,'2nd Service')


    df_bar = df_tmp[(df_tmp['Serving']=='Serving') & (df_tmp['isAce'] == 0)]
    fig_bar = dash_bar_chart(df_bar)
    # df_bar = df[(df['Serving']=='Serving') & (df['isAce'] == 0)].copy()

    fig_bar_service = dash_bar_service(df_tmp_2)

    image_player = 'https://raw.githubusercontent.com/brenoyam/tennis_dash/main/assets/' + selection + '.png'
    # player_img = html.Img(src='/assets/' + selection + '.png', id='logo',className='perfil_avatar')
    player_img = html.Img(src=image_player, id='logo',className='perfil_avatar')

    return fig_1st,fig_2nd,fig_bar ,fig_bar_service, fig_win,player_img



if __name__ == '__main__':
    app.run_server(port=9001, debug=True)
