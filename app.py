import dash
from dash import Dash, Input, Output, callback, html, dcc, dash_table
import dash_bootstrap_components as dbc
from PIL import Image, ImageOps, ImageDraw
import pillow_avif
from dash.dependencies import Input, Output, State
import io
import os
import boto3
from botocore.exceptions import NoCredentialsError
import base64
import sqlite3
from datetime import datetime
from web3 import Web3
import dash_daq as daq
import json

# Amazon S3 configuration
S3_BUCKET = ''
S3_REGION = ''
S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''
s3_client = boto3.client('s3', region_name=S3_REGION, aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY)

# Global email for filtering
DEFAULT_EMAIL = "test@testmail.com"

# SQLite database setup
DB_NAME = 'nfts-ings-db.sqlite'


##############################################
# Sample device data
devices = [
    {
        "name": "NFTag K",
        "lat": -0.274288,
        "lon": 36.069253,
        "uuid": "opf4b1e2-53c8-45f2-9f1a-972e07c92f4d",
        "email": DEFAULT_EMAIL,
        "nft_value": 100.00,
        "owner_contact": "+65 1234567433",
        "custom_message": "I'm fun and track assets",
        "owner": "John Doe",
        "image_url": "https://nftag.s3.us-east-2.amazonaws.com/.png",
        "unique_code": "1234",
        "status": "not connected",
        "toggle_status": "normal"
    },
    {
        "name": "NFTag B",
        "lat": -0.274294,
        "lon": 36.069287,
        "uuid": "b3d4f4c2-8b2b-4c1a-9d4b-8b92f0b1d97e",
        "email": DEFAULT_EMAIL,
        "nft_value": 150.00,
        "owner_contact": "+65 1234567433",
        "custom_message": "I'm fun and track assets",
        "owner": "John Doe",
        "image_url": "https://nftag.s3.us-east-2.amazonaws.com/6265.png",
        "unique_code": "1234",
        "status": "not connected",
        "toggle_status": "normal"
    },
    {
        "name": "NFTag C",
        "lat": -0.274294,
        "lon": 36.069287,
        "uuid": "b5d4f4c2-8b2b-4cha-9d4b-8b92f0b1d97e",
        "email": DEFAULT_EMAIL,
        "nft_value": 150.00,
        "owner_contact": "+65 1234567433",
        "custom_message": "I'm fun and track assets",
        "owner": "John Doe",
        "image_url": "https://nftag.s3.us-east-2.amazonaws.com/6265.png",
        "unique_code": "1234",
        "status": "not connected",
        "toggle_status": "normal"
    }    
]

# Function to initialize the database
def initialize_db():
    db_exists = os.path.isfile('nftag-devices.db')
    conn = sqlite3.connect('nftag-devices.db')
    cursor = conn.cursor()

    if not db_exists:
        cursor.execute('''
            CREATE TABLE devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                lat REAL,
                lon REAL,
                uuid TEXT UNIQUE,
                email TEXT,
                nft_value REAL,
                owner_contact TEXT,
                custom_message TEXT,
                owner TEXT,
                image_url TEXT,
                unique_code TEXT,
                status TEXT,
                toggle_status TEXT
            )
        ''')
        conn.commit()
    
    # Check for existing data and insert if not present
    for device in devices:
        cursor.execute('''
            SELECT * FROM devices WHERE uuid = ?
        ''', (device['uuid'],))
        
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO devices (name, lat, lon, uuid, email, nft_value, owner_contact, custom_message, owner, image_url, unique_code, status, toggle_status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (device['name'], device['lat'], device['lon'], device['uuid'], device['email'], device['nft_value'], device['owner_contact'], device['custom_message'], device['owner'], device['image_url'], device['unique_code'], device['status'], device['toggle_status']))
            conn.commit()
    
    conn.close()

# Initialize the database
initialize_db()




#############################################
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE image_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                filename TEXT UNIQUE,
                image BLOB
            )
        ''')
        conn.commit()
        conn.close()

def get_device_names(default_email):
    conn = sqlite3.connect('nftag-devices.db')
    cursor = conn.cursor()
    query = "SELECT name FROM devices WHERE email = ?"
    cursor.execute(query, (default_email,))
    device_names = cursor.fetchall()
    conn.close()
    return [{'label': name[0], 'value': name[0]} for name in device_names]

def get_image_urls(device_name):
    conn = sqlite3.connect('nftag-devices.db')
    cursor = conn.cursor()
    query = "SELECT image_url FROM devices WHERE name = ?"
    cursor.execute(query, (device_name,))
    image_urls = cursor.fetchall()
    conn.close()
    return [{'label': url[0], 'value': url[0]} for url in image_urls]

def update_device_image(device_name, image_url):
    conn = sqlite3.connect('nftag-devices.db')
    cursor = conn.cursor()
    query = "UPDATE devices SET image_url = ? WHERE name = ?"
    cursor.execute(query, (image_url, device_name))
    conn.commit()
    conn.close()

def save_to_db(email, filename, image_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO image_data (email, filename, image) 
            VALUES (?, ?, ?)
        ''', (email, filename, image_data))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # File name already exists
    conn.close()

def upload_to_s3(file_content, file_name):
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=file_name,
            Body=file_content,
            ContentType='image/png'
        )
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_name}"
        return file_url
    except NoCredentialsError:
        return "Credentials not available"

def list_s3_images():
    try:
        image_links = []
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        if 'Contents' in response:
            files = response['Contents']
            image_links = [
                f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file['Key']}" 
                for file in files
            ]
        return image_links
    except NoCredentialsError:
        return []
    except Exception as e:
        print(f"Error fetching S3 images: {str(e)}")
        return []

# Initialize database
init_db()



# Initialize the Dash app
FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, FA], title="nftagapp.io", assets_folder ="assets", assets_url_path="assets",
                    meta_tags=[
                        {
                            'charset': 'utf-8',
                        },
                        {
                            'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1, shrink-to-fit=yes'
                        }
                    ]

)

# Define image URLs
image_urls = {
    'nftag-a': 'https://nftag.s3.us-east-2.amazonaws.com/1178.png',
    'nftag-b': 'https://nftag.s3.us-east-2.amazonaws.com/6265.png'
}

# Create a formatted string with the image URLs
image_urls_js = ', '.join(f"'{key}': '{url}'" for key, url in image_urls.items())


# Choose center coordinates (e.g., NFTag A)
map_center = devices[0]  # Center map on NFTag A
center_lon = map_center['lon']
center_lat = map_center['lat']

# Function to initialize the database
def initialize_db():
    # Check if the database file exists
    if not os.path.isfile('button_presses.db'):
        # Connect to SQLite database (this will create the file)
        conn = sqlite3.connect('button_presses.db')
        cursor = conn.cursor()

        # Create a table to store button press counts with a unique constraint on email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS button_presses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                press_count INTEGER DEFAULT 0,
                last_updated TIMESTAMP
            )
        ''')

        # Insert an initial row with email and press count if not exists
        email = DEFAULT_EMAIL
        cursor.execute('''
            INSERT INTO button_presses (email, press_count, last_updated)
            VALUES (?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET press_count = press_count, last_updated = last_updated
        ''', (email, 0, datetime.now()))

        conn.commit()
        conn.close()

# Initialize the database
initialize_db()

# Define the layout of the Dash app
app.layout = html.Div([
    html.Div([
            dbc.Row(
            [
                dbc.Col(html.Div([
                    dbc.Row(                        
                        ),
                    dbc.Row([
                        daq.BooleanSwitch(
                        id='bluetooth-switch',
                        on=False,
                        label='Turn On Bluetooth'
                    ),
                        # Interval component for delay
                        dcc.Interval(
                            id='delay-interval',
                            interval=10*1000,  # 10 seconds
                            n_intervals=0,
                            disabled=True
                        ),
                    ]),
                    dbc.Row(
                        daq.BooleanSwitch(
                        id='location-switch',
                        on=False,
                        label='Turn On Location'
                    )
                        )
                    ]), md=4),
                    
                html.Br(),
                html.Br(), 
                
                dbc.Col(html.Div(
                    dbc.Container(
                            [
                                dbc.Row(
                                    dbc.Col(
                                        html.Div([
                                            html.Div([
                                                # Profile Icon
                                                html.Img(
                                                    src="https://via.placeholder.com/150",  # Placeholder for profile icon
                                                    style={
                                                        "width": "100px",
                                                        "height": "100px",
                                                        "border-radius": "50%",
                                                        "border": "2px solid #ccc",
                                                        "margin": "auto",
                                                        "display": "block"
                                                    }
                                                ),
                                                html.H6("Welcome: User"),                                    
                                            ], style={"text-align": "center"})
                                        ])
                                    )
                                )
                            ],
                            fluid=True
                        )
                    ), md=4),
                    
                html.Br(), 
                html.Br(), 
                
                dbc.Col(html.Div([
                    dbc.Row(
                    [
                        dbc.Row([
                            html.H6("Total Mined $NFTag Tokens", style={'textAlign':'center', 'width':'100%'}),
                            html.Div(id="output", style={
                            "font-size": "24px",  # Increase font size
                            "font-weight": "bold",
                            "textAlign":"center",
                            "color": "#007bff"  # Optional: set text color
                        }),
                        ]),
                        dbc.Row(
                            html.Button("Mining Button", id="button",style={'textAlign':'center', 'width':'100%'},  n_clicks=0),
                        ),
                    ]
                ),
                ]), md=4),
            ]
        ),
        ]),
    html.Hr(),    
       dbc.Row([
            dbc.Col(html.Div([
                html.H6("NFTag Tracking", style={'textAlign': 'center'}),
                html.Iframe(
                    id='map-iframe',
                    srcDoc=f'''
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="utf-8">
                            <title>Add markers with images and owner information</title>
                            <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
                            <link href="https://api.mapbox.com/mapbox-gl-js/v2.11.0/mapbox-gl.css" rel="stylesheet">
                            <script src="https://api.mapbox.com/mapbox-gl-js/v2.11.0/mapbox-gl.js"></script>
                            <style>
                                body {{
                                    margin: 0;
                                    padding: 0;
                                }}
                                #map {{
                                    position: absolute;
                                    top: 0;
                                    bottom: 0;
                                    width: 100%;
                                    height: 100%;
                                }}
                                .mapboxgl-popup-content {{
                                    font-size: 14px;
                                }}
                            </style>
                        </head>
                        <body>
                            <div id="map"></div>
                            <script>
                                mapboxgl.accessToken = 'MAPBOX TOKEN KEY';
                                const map = new mapboxgl.Map({{
                                    container: 'map',
                                    style: 'mapbox://styles/mapbox/streets-v12',
                                    center: [{center_lon}, {center_lat}],
                                    zoom: 15
                                }});

                                function loadImages(callback) {{
                                    const images = {{{image_urls_js}}};
                                    let imagesLoaded = 0;
                                    const totalImages = Object.keys(images).length;

                                    for (const [id, url] of Object.entries(images)) {{
                                        map.loadImage(url, (error, image) => {{
                                            if (error) {{
                                                console.error('Error loading image for ' + id + ':', error);
                                                return;
                                            }}
                                            map.addImage(id, image);
                                            imagesLoaded++;
                                            if (imagesLoaded === totalImages) {{
                                                callback();
                                            }}
                                        }});
                                    }}
                                }}

                                function addPopup(coordinates, title, owner, value) {{
                                    new mapboxgl.Popup()
                                        .setLngLat(coordinates)
                                        .setHTML(`
                                            <h3>${{title}}</h3>
                                            <p>Owner: ${{owner}}</p>
                                            <p>Value: $${{value.toFixed(2)}}</p>
                                        `)
                                        .addTo(map);
                                }}

                                map.on('load', () => {{
                                    loadImages(() => {{
                                        map.addSource('points', {{
                                            'type': 'geojson',
                                            'data': {{
                                                'type': 'FeatureCollection',
                                                'features': [
                                                    {{
                                                        'type': 'Feature',
                                                        'geometry': {{
                                                            'type': 'Point',
                                                            'coordinates': [36.069253, -0.274288]
                                                        }},
                                                        'properties': {{
                                                            'title': 'NFTag A',
                                                            'icon': 'nftag-a',
                                                            'owner': 'John Doe',
                                                            'value': 100.00
                                                        }}
                                                    }},
                                                    {{
                                                        'type': 'Feature',
                                                        'geometry': {{
                                                            'type': 'Point',
                                                            'coordinates': [36.069287, -0.274294]
                                                        }},
                                                        'properties': {{
                                                            'title': 'NFTag B',
                                                            'icon': 'nftag-b',
                                                            'owner': 'John Doe',
                                                            'value': 150.00
                                                        }}
                                                    }}
                                                ]
                                            }}
                                        }});

                                        map.addLayer({{
                                            'id': 'points-layer',
                                            'type': 'symbol',
                                            'source': 'points',
                                            'layout': {{
                                                'icon-image': ['get', 'icon'],
                                                'icon-size': 0.5,
                                                'text-field': ['get', 'title'],
                                                'text-font': [
                                                    'Open Sans Semibold',
                                                    'Arial Unicode MS Bold'
                                                ],
                                                'text-offset': [0, 1.25],
                                                'text-anchor': 'top'
                                            }}
                                        }});

                                        // Add popups on marker click
                                        map.on('click', 'points-layer', (e) => {{
                                            const coordinates = e.features[0].geometry.coordinates.slice();
                                            const title = e.features[0].properties.title;
                                            const owner = e.features[0].properties.owner;
                                            const value = e.features[0].properties.value;

                                            addPopup(coordinates, title, owner, value);
                                        }});

                                        map.on('mouseenter', 'points-layer', () => {{
                                            map.getCanvas().style.cursor = 'pointer';
                                        }});

                                        map.on('mouseleave', 'points-layer', () => {{
                                            map.getCanvas().style.cursor = '';
                                        }});
                                    }});
                                }});
                            </script>
                        </body>
                        </html>
                    ''',
                    style={'height': '600px', 'width': '100%'}
                )
            ]), width=12, lg=8),
          dbc.Col([
              dbc.Row([
                # web3 wallet integration and NFT cuustomization
                dbc.Col([
                    html.H6("Link Wallet", style={'textAlign':'center'}),
                    dbc.Row([
                        dbc.Container(
                                [                            
                                    html.Div(id='wallet-address-output', style={'textAlign': 'center'}),
                                    dbc.Row(
                                        dcc.Input(id='wallet-address-input', type='text', placeholder='Enter MetaMask Wallet Address', style={'textAlign': 'center', 'width': '100%'}),
                                        ),
                                    dbc.Row(
                                        html.Button('Link Wallet', id='wallet-submit-button', style={'textAlign': 'center', 'width': '100%'}, n_clicks=0)
                                        ),
                                    html.Script(src="https://cdnjs.cloudflare.com/ajax/libs/web3/1.6.1/web3.min.js"),
                                    html.Script(children='''
                                        async function connectMetaMask() {
                                            if (window.ethereum) {
                                                const web3 = new Web3(window.ethereum);
                                                try {
                                                    // Request account access
                                                    await window.ethereum.request({ method: 'eth_requestAccounts' });
                                                    const accounts = await web3.eth.getAccounts();
                                                    document.getElementById('wallet-address-input').value = accounts[0];
                                                } catch (error) {
                                                    console.error("User denied account access");
                                                }
                                            } else {
                                                alert("MetaMask is not installed. Please install it to use this feature.");
                                            }
                                        }
                                        document.addEventListener('DOMContentLoaded', function() {
                                            connectMetaMask();
                                        });
                                    ''')
                                ],
                                fluid=True
                            )
                    ]),
                    dbc.Row([
                        html.H6("Change PFP Name", style={'textAlign':'center'}),
                        dcc.Input(id="nft-customization", type="text", placeholder="Enter Name", style={'textAlign': 'center', 'width': '100%'}),
                        html.Div(id="nft-customization-result", style={'textAlign':'center'}),
                    ]),
                    dbc.Row(
                        html.Button("Rename PFP", id="customize-nft-button"),
                        )     
                    ], width=12, lg=12),
                  ]),
                  html.Br(),
                  
                  ################### PFP NFTs Upload
    
                  dbc.Row([
                      dcc.Interval(
                        id='interval-component',
                        interval=5*1000,  # Refresh every 5 seconds
                        n_intervals=0
                    ),

                    html.H6("Upload PFP", style={'textAlign': 'center'}),
                    dcc.Upload(
                        id='upload-image',
                        children=html.Button('Choose PFT'),
                        multiple=False,
                        
                    ),
                    html.Br(),
                    html.H6("Name your PFP:", style={'textAlign': 'center'}),
                    dcc.Input(id='filename-input', type='text', value='NFTag.png'),
                    html.Br(),
                    html.Button('Upload PFP', id='upload-button'),
                    html.Div(id='image-output', style={'display': 'none'}),
                    html.Div(id='image-list', style={'display': 'none'}),
                    html.Div(id='image-output'),

                  ], style={'textAlign': 'center', 'width': '100%'}), 
                  
                  html.Br(),
                  html.Br(),
                ############### NFTag Controls
                dbc.Row([
                    html.H6("NFTag Control", style={'textAlign': 'center'}),
                    dcc.Dropdown(
                        id='nftag-device-dropdown',
                        options=[],
                        placeholder="Select a device",
                        style={'color': 'black'}
                    ),
                    dbc.Row([
                        dbc.Button("Connect NFTag", id='link-button', n_clicks=0, color="primary"),
                        html.Br(),
                         ]),
                    dbc.Row([
                        dbc.Button("Disconnect NFTag", id='disconnect-button', n_clicks=0, color="danger"),
                        html.Br(),
                         ]),
                    dbc.Row([
                        dbc.Button("Lost NFTag Alert", id='lost-button', n_clicks=0, color="warning"),
                        html.Br(),
                        ]),
                    dbc.Row([
                        dbc.Button("Found NFTag Alert", id='normal-button', n_clicks=0, color="success"),
                        html.Br(),
                        ]),
               ]),

              ], width=12, lg=4),
            ]
        ),   
    html.Hr(),

    ########################## NFTag Management and Customization
    
    dbc.Row(
        [ 
            dbc.Col(html.Div([  
                dbc.Row([
                    html.H6("NFTag List", style={'textAlign': 'center'}),
                    html.Div(id="devices-table-container", style={'color': 'black', 'overflowX': 'auto'}),
                ]),
                html.Br(),
                dbc.Row(
                        [
                            ####### Changing PFP info for NFTag
                            dbc.Col(html.Div([                               
                                html.H6("Change NFTag Name/Message", style={'textAlign': 'center'}),
                                dcc.Dropdown(
                                    id='customization-device-dropdown',
                                    options=[],
                                    placeholder="Select a device for customization",
                                    style={'color': 'black'}
                                ),
                                dcc.Dropdown(
                                    id='customization-column-dropdown',
                                    options=[
                                        {'label': 'Name', 'value': 'name'},
                                        {'label': 'Custom Message', 'value': 'custom_message'}
                                    ],
                                    placeholder="Select a column to update",
                                    style={'color': 'black'}
                                ),
                                dbc.Row(
                                     dcc.Input(
                                        id='customization-input',
                                        type='text',
                                        placeholder="Enter new info",
                                        style={'color': 'black', 'width': '100%'}
                                    ),                                    
                                    ),
                                dbc.Row([
                                    dbc.Button("Submit Changes", id='customization-submit-button',style={'textAlign': 'center', 'width': '100%'},  n_clicks=0, color="primary"),
                                    html.Div(id='customization-output', style={'color': 'black'}),                                    
                                    ]),

                            ]), md=6),
                            dbc.Col(html.Div([
                                html.H6("Select PFP Link:", style={'textAlign': 'center'}),
                                html.Div(id='database-contents', style={'color': 'black', 'width': '100%'}),
                                dbc.Row([
                                    dbc.Col(
                                        dcc.Dropdown(
                                            id='device-dropdown'
                                            # options will be set by the callback
                                        ),
                                        style={'color': 'black', 'width': '100%'}
                                    )
                                ]),
                                dcc.Dropdown(
                                    id='image-dropdown',
                                    options=[],
                                    value=None,
                                    style={'color': 'black', 'width': '100%'}
                                ),
                                dbc.Button("Submit Link", id="submit-button", style={'width': '100%'}, n_clicks=0)
                
                    ########### End PFP for NFTag                               
                            ]), md=6),
                        ]
                    ),               

            ]), width=12, lg=12),
            ######### end
        ], className="g-0",
        ),

        ############################## End NFTag Management and Customization

        ############## List of Uploaded NFTs
        html.H6("Uploaded PFPs", style={'textAlign': 'center'}),
        html.Hr(),
            dbc.Container(
            [
                html.Div(id='s3-image-list', style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'gap': '10px'})
            ],
            fluid=True
            ) 
         ############# end

])

# Callbacks
# Callback to display list of images
@app.callback(
    Output('s3-image-list', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def display_images(n_intervals):
    images = list_s3_images()
    if images:
        image_links = [
            html.Div([
                html.Img(
                    src=f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{img}", 
                    style={'width': '100px', 'height': 'auto'}
                ),
                html.P(f"{img}: https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{img}")
            ], style={'flex': '1 0 16%', 'boxSizing': 'border-box', 'textAlign': 'center'})  # 6 items per row approximately
            for img in images
        ]
        return image_links
    return html.Div("No images found.")


def list_s3_images():
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        if 'Contents' in response:
            files = response['Contents']
            return [file['Key'] for file in files]
        return []
    except NoCredentialsError:
        return []

# Callback for Web3 wallet linkiing and NFT customization
# Metamask wallet linking
@app.callback(
    Output('wallet-address-output', 'children'),
    [Input('wallet-submit-button', 'n_clicks')],
    [dash.dependencies.State('wallet-address-input', 'value')]
)
def update_wallet_address(n_clicks, wallet_address):
    if wallet_address:
        # Connect to web3 Ethereum node 
        infura_url = 'https://mainnet.infura.io/v3/7bf521618cad48c88d3e34d43a15e19d'
        web3 = Web3(Web3.HTTPProvider(infura_url))

        # Check if connected
        print("Connected:", web3.is_connected())
        return f"Wallet: {wallet_address} Linked successfully"
    return ""

@app.callback(
    Output("nft-customization-result", "children"),
    Input("customize-nft-button", "n_clicks"),
    State("nft-customization", "value")
)
def customize_nft(n_clicks, customization):
    if n_clicks:
        return f"PFP Renamed to : {customization}"
    return ""

# Callback for mining $NFTag tokens
@app.callback(
    Output("output", "children"),
    [Input("button", "n_clicks")]
)
def update_output(n_clicks):
    # Connect to SQLite database
    conn = sqlite3.connect('button_presses.db')
    cursor = conn.cursor()

    email = DEFAULT_EMAIL
    now = datetime.now()

    # Check last update time and update if necessary
    cursor.execute('''
        SELECT last_updated FROM button_presses WHERE email = ?
    ''', (email,))
    row = cursor.fetchone()
    
    if row:
        last_updated = row[0]
        # Increment only if the last update was not in the same session
        if last_updated is None or (now - datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S.%f")).total_seconds() > 0:
            cursor.execute('''
                UPDATE button_presses
                SET press_count = press_count + 1,
                    last_updated = ?
                WHERE email = ?
            ''', (now, email))
            conn.commit()

    # Query the total press count
    cursor.execute('SELECT press_count FROM button_presses WHERE email = ?', (email,))
    total_presses = cursor.fetchone()[0]

    # Close the connection
    conn.close()

    return f"Bal: {total_presses}"

# Get nearby NFtag devices callback
@app.callback(
    Output('delay-interval', 'disabled'),
    [Input('bluetooth-switch', 'on'),
     Input('location-switch', 'on')]
)
def start_interval(bluetooth_on, location_on):
    if bluetooth_on or location_on:
        return False  # Enable interval
    return True  # Disable interval


# UPLOAD CALLBACKS
# Combined callback to update dropdowns and image list
@app.callback(
    [Output('device-dropdown', 'options'),
     Output('image-dropdown', 'options'),
     Output('image-list', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('device-dropdown', 'value')]
)
def update_dropdowns_and_images(n_intervals, selected_device):
    device_options = get_device_names(DEFAULT_EMAIL)
    
    image_options = []
    if selected_device:
        image_options = get_image_urls(selected_device)
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT filename FROM image_data WHERE email = ?', (DEFAULT_EMAIL,))
        filenames = [record[0] for record in cursor.fetchall()]
        conn.close()
        
        if filenames:
            all_links = list_s3_images()
            filtered_links = [
                link for link in all_links if any(filename in link for filename in filenames)
            ]
            if filtered_links:
                dropdown_options = [{'label': link, 'value': link} for link in filtered_links]
                link_elements = [html.Div(html.P(link)) for link in filtered_links]
                return device_options, image_options, html.Div(link_elements)
            else:
                return device_options, image_options, html.Div("No matching images found in S3.")
        else:
            return device_options, image_options, html.Div("No filenames found for the default email.")
    except Exception as e:
        return device_options, image_options, html.Div(f"Error: {str(e)}")

# Callback to process and upload image
@app.callback(
    Output('image-output', 'children'),
    [Input('upload-button', 'n_clicks')],
    [State('upload-image', 'contents'),
     State('filename-input', 'value')]
)
def process_image(n_clicks, file_content, filename):
    if n_clicks is not None and file_content is not None:
        try:
            content_type, content_string = file_content.split(',')
            decoded = base64.b64decode(content_string)
            image_data = io.BytesIO(decoded)
            image = Image.open(image_data)
            size = (32, 40)
            image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, size[0], size[1]), fill=255)
            image.putalpha(mask)
            output = io.BytesIO()
            image.save(output, format='PNG')
            output.seek(0)
            save_to_db(DEFAULT_EMAIL, filename, output.getvalue())
            s3_url = upload_to_s3(output.getvalue(), filename)
            return html.Div([
                html.H6("Image Uploaded Successfully"),
                html.Img(src=s3_url, style={'width': '32px', 'height': '40px'}),
                html.P(f"Image URL: {s3_url}")
            ])
        except Exception as e:
            return html.Div(f"Error: {str(e)}")
    return html.Div("")

# Callback to update device image URL
@app.callback(
    Output('image-dropdown', 'value'),
    [Input('submit-button', 'n_clicks')],
    [State('device-dropdown', 'value'),
     State('image-dropdown', 'value')]
)
def update_device_image_url(n_clicks, device_name, image_url):
    if n_clicks > 0 and device_name and image_url:
        update_device_image(device_name, image_url)
        return image_url
    return dash.no_update


######################################NFT MANAGEMENT CALLBACKS
@app.callback(
    Output('nftag-device-dropdown', 'options'),
    Output("devices-table-container", "children"),
    Input('link-button', 'n_clicks'),
    Input('disconnect-button', 'n_clicks'),
    Input('lost-button', 'n_clicks'),
    Input('normal-button', 'n_clicks'),
    State('nftag-device-dropdown', 'value')
)
def update_device_status(n_clicks_link, n_clicks_disconnect, n_clicks_lost, n_clicks_normal, selected_device):
    email = DEFAULT_EMAIL
    conn = sqlite3.connect('nftag-devices.db')
    cursor = conn.cursor()

    if n_clicks_link > 0 and selected_device:
        # Update the status of the selected device to 'connected'
        cursor.execute('''
            UPDATE devices 
            SET status = ? 
            WHERE name = ? AND email = ?
        ''', ('connected', selected_device, email))
        conn.commit()
    
    if n_clicks_disconnect > 0 and selected_device:
        # Update the status of the selected device to 'disconnected'
        cursor.execute('''
            UPDATE devices 
            SET status = ? 
            WHERE name = ? AND email = ?
        ''', ('disconnected', selected_device, email))
        conn.commit()
    
    if n_clicks_lost > 0 and selected_device:
        # Update the toggle status of the selected device to 'lost'
        cursor.execute('''
            UPDATE devices 
            SET toggle_status = ? 
            WHERE name = ? AND email = ?
        ''', ('lost', selected_device, email))
        conn.commit()

    if n_clicks_normal > 0 and selected_device:
        # Update the toggle status of the selected device to 'normal'
        cursor.execute('''
            UPDATE devices 
            SET toggle_status = ? 
            WHERE name = ? AND email = ?
        ''', ('normal', selected_device, email))
        conn.commit()
    
    # Fetch updated device data
    cursor.execute('''
        SELECT name, status, owner, nft_value, toggle_status, custom_message 
        FROM devices 
        WHERE email = ?
    ''', (email,))
    rows = cursor.fetchall()
    
    # Fetch device names for the dropdown
    cursor.execute('''
        SELECT DISTINCT name 
        FROM devices 
        WHERE email = ?
    ''', (email,))
    device_names = cursor.fetchall()
    
    conn.close()
    
    # Create a DataFrame for the table
    columns = ["name", "status", "owner", "nft_value", "toggle_status", "custom_message"]
    
    if not rows:
        return [{'label': name[0], 'value': name[0]} for name in device_names], html.P("No devices found for the default email.")
    
    table = dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in columns],
        data=[{columns[i]: row[i] for i in range(len(columns))} for row in rows],
        style_table={'width': '100%', 'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    )
    
    # Return device names and the table
    return [{'label': name[0], 'value': name[0]} for name in device_names], table


@app.callback(
    Output('customization-device-dropdown', 'options'),
    Input('interval-component', 'n_intervals')
)
def update_customization_device_dropdown(n_intervals):
    email = DEFAULT_EMAIL
    conn = sqlite3.connect('nftag-devices.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT name 
        FROM devices 
        WHERE email = ? AND status = ?
    ''', (email, 'connected'))
    
    device_names = cursor.fetchall()
    conn.close()
    
    return [{'label': name[0], 'value': name[0]} for name in device_names]

@app.callback(
    Output('customization-output', 'children'),
    Input('customization-submit-button', 'n_clicks'),
    State('customization-device-dropdown', 'value'),
    State('customization-column-dropdown', 'value'),
    State('customization-input', 'value')
)
def update_device_customization(n_clicks, selected_device, selected_column, new_value):
    if n_clicks > 0 and selected_device and selected_column and new_value:
        conn = sqlite3.connect('nftag-devices.db')
        cursor = conn.cursor()
        
        # Update the specified column for the selected device
        cursor.execute(f'''
            UPDATE devices 
            SET {selected_column} = ? 
            WHERE name = ? AND email = ?
        ''', (new_value, selected_device, DEFAULT_EMAIL))
        conn.commit()
        conn.close()
        
        return f"Updated {selected_column} for device {selected_device} to '{new_value}'"

    return ""
##########################################

# Run the app
if __name__ == '__main__':
    app.run_server('0.0.0.0', port=8050, use_reloader=False, use_debugger=False)
