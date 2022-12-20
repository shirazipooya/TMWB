import base64
import os
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from p import *


image_filename = os.getcwd() + "/static/images/Method.png" # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

image_filename2 = os.getcwd() + "/static/images/Workflow.png" # replace with your own image
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())


external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    # "/static/vendor/fontawesome/v6.1.1/css/all.css",
    # "/static/vendor/bootstrap/v5.2.0/css/bootstrap.min.css",
    # "/static/vendor/bootstrap-icons/v1.9.1/bootstrap-icons.css",
    # "/static/vendor/animate/v4.1.1/animate.min.css",
    "/static/css/main.css",
]

external_scripts=[
    # "/static/vendor/jquery/v3.6.0/jquery.min.js",
    # "/static/vendor/popper/v2.9.2/popper.min.js",
    # "/static/vendor/bootstrap/v5.2.0/js/bootstrap.min.js",
]

app = Dash(
    name=__name__,
    url_base_pathname='/',
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    title='تورنت وایت - ماتر',
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True
)

form = html.Div(
    className="col-lg-6 col-md-12 px-5 mx-auto",
    children=[
        html.Div(
            className='form-group p-3', 
            children=[
                dcc.Upload(
                    id="upload_data",
                    accept=".xlsx",
                    children=[
                        html.A('انتخاب فایل داده‌های ورودی')
                    ], 
                    className="select_file_button"
                ),
                html.Div(
                    id='file_name_upload',
                    children=[
                        "فایلی انتخاب نشده است!"
                    ],
                    className='text-center pt-2 text-danger',
                )
            ]
        ),
        html.Div(
            dbc.FormFloating(
                [
                    dbc.Input(type="number", placeholder="عرض جغرافیایی (Lat)", id="lat"),
                    dbc.Label(
                        [
                            html.Span("*", className="text-danger px-1"),
                            "عرض جغرافیایی (Lat)",
                        ],
                        class_name="text-dark",
                    ),
                ],
            ),
            className="py-2"
        ),
        html.Div(
            dbc.FormFloating(
                [
                    dbc.Input(type="number", placeholder="ظرفیت ذخیره رطوبت خاک (SM) [mm]", id="sm"),
                    dbc.Label(
                        [
                            html.Span("*", className="text-danger px-1"),
                            "ظرفیت ذخیره رطوبت خاک (SM) [mm]",
                        ],
                        class_name="text-dark",
                    ),
                ],
            ),
            className="py-2"
        ),
        html.Div(
            dbc.FormFloating(
                [
                    dbc.Input(type="number", placeholder="ضریب رواناب (beta) [%]", id="beta"),
                    dbc.Label(
                        [
                            html.Span("*", className="text-danger px-1"),
                            "ضریب رواناب (beta) [%]",
                        ],
                        class_name="text-dark",
                    ),
                ],
            ),
            className="py-2"
        ),
        html.Div(
            dbc.FormFloating(
                [
                    dbc.Input(type="number", placeholder="آستانه دمای بارش برف (SRT) [C°]", id="srt"),
                    dbc.Label(
                        [
                            html.Span("*", className="text-danger px-1"),
                            "آستانه دمای بارش برف (SRT) [C°]",
                        ],
                        class_name="text-dark",
                    ),
                ],
            ),
            className="pt-2 pb-4"
        ),
        dmc.Button("محاسبه بیلان ماهانه", fullWidth=True, id="calculate", n_clicks=0)
    ]
)


home = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            dmc.Text("محاسبه بیلان ماهانه آب خاک به روش مدل توزیعی تورنت وایت - ماتر",  weight=600, align="right"),
                            className="text-primary m-0 pt-3",
                        ),
                        html.P(
                            dmc.Text(
                                "برنامه توسعه داده شده توانایی محاسبه بیلان آب خاک با استفاده از مدل توزیعی تورنت وایت - ماتر را دارد. این مدل از یک روش حسابداری برای تجزیه و تحلیل تخصیص آب در میان اجزای مختلف یک سیستم هیدرولوژیکی استفاده می کند.",
                                align="right"),
                            className="m-0 pt-3",
                        ),
                    ],
                    md=12
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            dmc.Text("محاسبه بیلان",  weight=600, align="right"),
                            className="text-primary m-0 pt-5",
                        ),
                        html.P(
                            dmc.Text(
                                "لطفا مراحل زیر را به ترتیب دنبال کنید تا به نتیجه نهایی برسید!",
                                align="right"),
                            className="m-0 py-3",
                        ),
                        dmc.Accordion(
                            disableChevronRotation=False,
                            variant="separated",
                            children=[
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(
                                            dmc.Text("گام اول - دریافت الگوی داده‌های ورودی", size="lg", weight=700, className="px-2"),
                                            icon=DashIconify(icon="file-icons:microsoft-excel", height=24, width=24, color="green"),
                                        ),
                                        dmc.AccordionPanel(
                                            children=[
                                                dmc.Text("دانلود الگوی داده‌های ورودی - پارامترهای سال، ماه، دما و بارش مورد نیاز است.", size="md", align="right", className="px-5"),
                                                html.Div(
                                                    children=[
                                                        dbc.Button(
                                                            "از اینجا دانلود کنید!",
                                                            id="template",
                                                            color="link"
                                                        ),
                                                        dcc.Download(
                                                            id="download_template"
                                                        )
                                                    ],
                                                    className="px-5"
                                                )
                                            ]
                                        ),
                                    ],
                                    value="info",
                                ),
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(
                                            dmc.Text("گام دوم - بارگزاری داده‌های ورودی و تکمیل اطلاعات مورد نیاز", size="lg", weight=700, className="px-2"),
                                            icon=DashIconify(icon="material-symbols:edit-square", height=28, width=28, color="green"),
                                        ),
                                        dmc.AccordionPanel(form),
                                    ],
                                    value="addr",
                                ),
                                dmc.AccordionItem(
                                    [
                                        dmc.AccordionControl(
                                            dmc.Text("گام سوم - دانلود نتایج", size="lg", weight=700, className="px-2"),
                                            icon=DashIconify(icon="simple-icons:plotly", height=24, width=24, color="green"),
                                        ),
                                        dmc.AccordionPanel(
                                             children=[
                                                 html.Div(
                                                     children=[
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    children=[
                                                                        dbc.Button(
                                                                            "دانلود فایل نمودار نتایج",
                                                                            id="pic",
                                                                            color="link"
                                                                        ),
                                                                        dcc.Download(
                                                                            id="download_pic"
                                                                        )
                                                                    ],
                                                                ),    
                                                            ],
                                                            className="col-4 d-flex justify-content-center"
                                                        ),
                                                        html.Div(
                                                            children=[
                                                                dmc.Button("نمایش نتایج", fullWidth=False, id="show", n_clicks=0)
                                                            ],
                                                            className="col-4 d-flex justify-content-center"
                                                        ),
                                                        html.Div(
                                                            children=[
                                                                html.Div(
                                                                    children=[
                                                                        dbc.Button(
                                                                            "دانلود فایل اکسل نتایج",
                                                                            id="result",
                                                                            color="link"
                                                                        ),
                                                                        dcc.Download(
                                                                            id="download_result"
                                                                        )
                                                                    ],
                                                                ),    
                                                            ],
                                                            className="col-4 d-flex justify-content-center"
                                                        ),      
                                                    ],
                                                     className="row"
                                                 ), 
                                                html.Div(
                                                    children=[
                                                        dcc.Graph(
                                                            id='GRAPH',
                                                            figure=NO_MATCHING_GRAPH_FOUND
                                                        )
                                                    ],
                                                    dir="rtl"
                                                )
                                             ]              
                                        ),
                                    ],
                                    value="focus",
                                ),
                            ],
                        )
                    ],
                    md=12
                )
            ]
        ),
    ]
)



methods = html.Div(
    [
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            dmc.Text("روش",  weight=600, align="right"),
                            className="text-primary m-0 pt-3",
                        ),
                        html.Div(
                            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), width=1000),
                            className="text-center"
                        ),
                    ],
                    md=12
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            dmc.Text("جریان کاری",  weight=600, align="right"),
                            className="text-primary m-0 pt-3",
                        ),
                        html.Div(
                            html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), width=1000),
                            className="text-center"
                        ),
                    ],
                    md=12
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            dmc.Text("ورودی‌ها",  weight=600, align="right"),
                            className="text-primary m-0 pt-3",
                        ),
                        html.P(
                            [
                                dmc.Text(
                                    "P = monthly precipitation (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "Tm = mean monthly temperature (°C)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "LAT = latitude",
                                    align="left",
                                ),
                                dmc.Text(
                                    "SM = soil moisture storage capacity value (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "beta = dimensionless runoff coefficient (percent)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "SRT = snowfall rainfall threshold (°C)",
                                    align="left",
                                ),
                            ],
                            className="m-0 pt-3",
                        ),
                    ],
                    md=12
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            dmc.Text("خروجی‌ها",  weight=600, align="right"),
                            className="text-primary m-0 pt-3",
                        ),
                        html.P(
                            [
                                dmc.Text(
                                    "PET = monthly potential evapotranspiration (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "delta = P-PET (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "AET = monthly actual evapotranspiration (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "ST = monthly soil moisture (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "S = monthly water surplus (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "RO = monthly runoff (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "RES = dynamic water storage available for the next month (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "SMRO = monthly snow melt runoff (mm)",
                                    align="left",
                                ),
                                dmc.Text(
                                    "TOT RO = monthly total runoff (mm)",
                                    align="left",
                                ),
                            ],
                            className="m-0 pt-3",
                        ),
                    ],
                    md=12
                )
            ]
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4(
                            dmc.Text("منابع",  weight=600, align="right"),
                            className="text-primary m-0 pt-3",
                        ),
                        html.P(
                            [
                                dmc.Text(
                                    "Mammoliti, E.; Fronzi, D.; Mancini, A.; Valigi, D.; Tazioli, A. (2021). WaterbalANce, a WebApp for Thornthwaite–Mather Water Balance Computation: Comparison of Applications in Two European Watersheds. Hydrology 2021, 8, 34",
                                    align="left",
                                    className="py-2"
                                ),
                                dmc.Text(
                                    "McCabe, G.J.; and Markstrom, S.L. (2007). A monthly water-balance model driven by a graphical user interface: U.S. Geological Survey Open-File report 2007-1088, 6 p",
                                    align="left",
                                    className="py-2"
                                ),
                                dmc.Text(
                                    "Thornthwaite, C. W.; & Mather, J. R. (1957). Instructions and tables for computing potential evapotraspiration and the water balance. Johns Hopkins Univ., Laboratory in Climatology, 10 (3) 181-311",
                                    align="left",
                                    className="py-2"
                                ),
                                dmc.Text(
                                    "Thornthwaite, C. W.; Mather, J. R. (1955). The water balance. Johns Hopkins Univ., Laboratory in Climatology, 8 (1), 1-104",
                                    align="left",
                                    className="py-2"
                                ),
                            ],
                            className="m-0 pt-3",
                        ),
                    ],
                    md=12
                )
            ]
        ),
    ]
)


app.layout = dmc.NotificationsProvider(
    html.Div(
        className="container",
        children=[
            html.Div(
                style={
                    "font-family": "Vazir-Bold-FD",
                },
                children=[
                    html.H4(
                        dmc.Text("دانشگاه فردوسی مشهد",  weight=300, align="center"),
                        className="text-dark m-0 pt-3",
                    ),
                    html.H2(
                        dmc.Text("پژوهشکده آب و محیط‌زیست",  weight=700, align="center"),
                        className="text-success m-0 pb-1",
                    ),
                ]    
            ),
            html.Div(
                id='ALERTS',
            ),
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.Tab(
                                dmc.Text("خانه", size="xl", weight=700, className="px-1"),
                                icon=DashIconify(icon="tabler:home", height=24, width=24),
                                value="home",
                            ),
                            dmc.Tab(
                                dmc.Text("روش‌ها", size="xl", weight=700, className="px-1"),
                                icon=DashIconify(icon="tabler:copy", height=24, width=24),
                                value="methods",
                            ),
                        ]
                    ),
                    dmc.TabsPanel(home, value="home"),
                    dmc.TabsPanel(methods, value="methods"),
                ],
                value="home",
                color="blue",
            ),

            dcc.Store(
                id='storage',
                storage_type='memory'
            ),
            dcc.Interval(
                id='interval',
                interval=1000,
                n_intervals=0,
                max_intervals=1
            )
        ]
    )
)





@app.callback(
    Output("file_name_upload", "children"),
    Output("file_name_upload", "className"),
    Input('upload_data', 'contents'),        
    State('upload_data', 'filename')
)
def name_file_show(
    file_content,
    file_name
):
    if (file_content is None):
        
        result = [
            "فایلی انتخاب نشده است!",
            'text-center pt-2 text-danger',
        ]
        
        return result
    
    else:
        
        result = [
            file_name,
            'text-center pt-2 text-success',
        ]
        
        return result





@app.callback(
    Output("download_template", "data"),
    Input("template", "n_clicks"),
    prevent_initial_call=True,
)
def download_template(
    n
):
    return dcc.send_file(
        "./assets/template.xlsx"
    )

@app.callback(
    Output("download_pic", "data"),
    Input("pic", "n_clicks"),
    prevent_initial_call=True,
)
def download_pic(
    n
):
    return dcc.send_file(
        "./result/result.png"
    )

@app.callback(
    Output("download_result", "data"),
    Input("result", "n_clicks"),
    prevent_initial_call=True,
)
def download_result(
    n
):
    return dcc.send_file(
        "./result/result.xlsx"
    )
     
    
@app.callback(
    Output("calculate", "n_clicks"),
    Output("ALERTS", "children"),
    Input("calculate", "n_clicks"),
    Input("lat", "value"),
    Input("sm", "value"),
    Input("beta", "value"),
    Input("srt", "value"),
    Input('upload_data', 'contents'),        
    State('upload_data', 'filename'), 
    prevent_initial_call=True,
)
def calculate_tmwb(
    n, lat, sm, beta, srt, file_content, file_name
):
    if n != 0:
        d, nn = read_data_from_spreadsheet(file_content, file_name)
        data = pd.DataFrame.from_dict(d[nn[0]])
        
        CONFIG_ALG = dict()

        CONFIG_ALG = {
            "source_data_path": data,
            "LAT": round(lat, 0),
            "SM": sm,
            "beta": beta / 100,
            "SRT": srt,
            "dest_data_path": "./result/result.xlsx",
            "dest_img_path": "./result/result.png",
            "mean_calc": False
        }
        
        thorntw_mater_proc(
            source_path=CONFIG_ALG["source_data_path"],
            LAT=CONFIG_ALG["LAT"],
            SM=CONFIG_ALG["SM"],
            SRT=CONFIG_ALG["SRT"],
            beta=CONFIG_ALG["beta"],
            mean_calc=CONFIG_ALG["mean_calc"],
            file_out=CONFIG_ALG["dest_data_path"],
            img_out=CONFIG_ALG["dest_img_path"],
        )
        
        notify = dmc.Notification(
            id="notify",
            title = "خبر",
            message = ["محاسبات با موفقیت انجام شد."],
            color="green",
            action = "show",
        )

        return 0, notify
    
    else:
        
        notify = dmc.Notification(
            id="notify",
            title = "خبر",
            message = ["محاسبات با موفقیت انجام شد."],
            color="red",
            action = "hide",
        )
        
        return 0, notify


@app.callback(
    Output("show", "n_clicks"),
    Output('GRAPH', 'figure'),
    Input("show", "n_clicks"), 
    prevent_initial_call=True,
)
def show_result(
    n,
):
    if n != 0:
        
        data = pd.read_excel("./result/result.xlsx")
        data["date"] = data["year"].astype(str) + "-" + data["month"].astype(str) + "-" + "1"
        data["date"] = pd.to_datetime(data["date"])
        
        fig = make_subplots(
            rows=5,
            cols=2,
            shared_xaxes=False,
            vertical_spacing=0.02
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['Tm'],
                mode='lines+markers',
                name='Temp. °C',
                marker=dict(
                    color='black',
                    size=4,
                ),
                line=dict(
                    color='black',
                    width=1
                )  
            ),
            row=1,
            col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=data['date'],
                y=data['P'],
                name='Rainfall [mm]',
                marker_color="blue"
 
            ),
            row=1,
            col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['P'],
                mode='lines+markers',
                name='PET [mm]',
                marker=dict(
                    color='magenta',
                    size=4,
                ),
                line=dict(
                    color='magenta',
                    width=1
                )  
            ),
            row=2,
            col=1
        )
        
        fig.add_trace(
            go.Bar(
                x=data['date'],
                y=data['delta'],
                name='P-PET [mm]',
                marker_color="black"
            ),
            row=2,
            col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['AET'],
                mode='lines+markers',
                name='AET [mm]',
                marker=dict(
                    color='orange',
                    size=4,
                ),
                line=dict(
                    color='orange',
                    width=1
                )  
            ),
            row=3,
            col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['ST'],
                mode='lines+markers',
                name='ST [mm]',
                marker=dict(
                    color='red',
                    size=4,
                ),
                line=dict(
                    color='red',
                    width=1
                )  
            ),
            row=3,
            col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['S'],
                mode='lines+markers',
                name='S [mm]',
                marker=dict(
                    color='darkblue',
                    size=4,
                ),
                line=dict(
                    color='darkblue',
                    width=1
                )  
            ),
            row=4,
            col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['RO'],
                mode='lines+markers',
                name='RO [mm]',
                marker=dict(
                    color='green',
                    size=4,
                ),
                line=dict(
                    color='green',
                    width=1
                )  
            ),
            row=4,
            col=2
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['SMRO'],
                mode='lines+markers',
                name='SMRO [mm]',
                marker=dict(
                    color='black',
                    size=4,
                ),
                line=dict(
                    color='black',
                    width=1
                )  
            ),
            row=5,
            col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=data['date'],
                y=data['TOT_RO'],
                mode='lines+markers',
                name='tot RO [mm]',
                marker=dict(
                    color='blue',
                    size=4,
                ),
                line=dict(
                    color='blue',
                    width=1
                )  
            ),
            row=5,
            col=2
        )
        
               
        fig.update_yaxes(title_text='Temp. [°C]', row=1, col=1)
        fig.update_yaxes(title_text='Rainfall [mm]', row=1, col=2)
        fig.update_yaxes(title_text='PET [mm]', row=2, col=1)
        fig.update_yaxes(title_text='P-PET [mm]', row=2, col=2)
        fig.update_yaxes(title_text='AET [mm]', row=3, col=1)
        fig.update_yaxes(title_text='ST [mm]', row=3, col=2)
        fig.update_yaxes(title_text='S [mm]', row=4, col=1)
        fig.update_yaxes(title_text='RO [mm]', row=4, col=2)
        fig.update_yaxes(title_text='SMRO [mm]', row=5, col=1)
        fig.update_yaxes(title_text='tot RO [mm]', row=5, col=2)
        
        fig.update_xaxes(title_text='Time [months]', row=5, col=1)
        fig.update_xaxes(title_text='Time [months]', row=5, col=2)

        
        
        fig.update_layout(
            showlegend=False,
            height=1000,
            xaxis=dict(
                tickformat="%Y-%m",
            ),
        )        
        
        
        return 0, fig
    
    else:
        
        return 0, NO_MATCHING_GRAPH_FOUND


if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=50505,
        debug=True
    )