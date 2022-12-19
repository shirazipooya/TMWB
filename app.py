from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from p import *


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
                                                        dbc.Button(
                                                            "دانلود فایل نمودار نتایج",
                                                            id="pic",
                                                            color="link"
                                                        ),
                                                        dcc.Download(
                                                            id="download_pic"
                                                        )
                                                    ],
                                                    className="px-5"
                                                ),
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
                                                    className="px-5"
                                                ),
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
                    dmc.TabsPanel("2", value="methods"),
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





if __name__ == '__main__':
    app.run(
        host="127.0.0.1",
        port=13631,
        debug=True
    )