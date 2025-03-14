import wifi
import socketpool
import microcontroller
import time
from adafruit_httpserver import Server, Request, Response, POST

# Wi-Fi Access Point Settings
SSID = "PicoW Hotspot"
PASSWORD = "password"  # Must be at least 8 characters

# Start Pico W as an Access Point
print("Starting Access Point...")
wifi.radio.start_ap(SSID, PASSWORD)
print("AP started! IP:", wifi.radio.ipv4_address_ap)

# Create a socket pool and server
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, str(wifi.radio.ipv4_address_ap))

# Variable to store data
data = "Default"

@server.route("/", methods=["GET", "POST"])
def index(request: Request):
    global data
    if request.method == POST:
        form_data = request.form
        if "value" in form_data:
            data = form_data["value"]

    html = f"""
    <html>
        <head><title>Pico W Server</title></head>
        <body>
            <h1>Update Variable</h1>
            <form method="POST">
                <input type="text" name="value" value="{data}"/>
                <input type="submit" value="Update"/>
            </form>
            <p>Current Value: {data}</p>
        </body>
    </html>
    """
    return Response(request, html, content_type="text/html")

# Start the web server
server.start()
print("Server started! Connect to:", wifi.radio.ipv4_address_ap)

while True:
    try:
        server.poll()
    except Exception as e:
        print("Error:", e)
        time.sleep(5)
        microcontroller.reset()