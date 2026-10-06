"""
Harness FME SDK - Python Example (Flask Web App)
Feature Flag: show-discount-banner

Run in localhost mode for local testing (no Harness connection needed).
Replace SDK_KEY with your real key to connect to Harness FME.
"""

from flask import Flask
from splitio import get_factory
from splitio.exceptions import TimeoutException

app = Flask(__name__)

# Replace with your real Server-side SDK key
SDK_KEY = "YOUR_SERVER_SIDE_SDK_KEY"

# The user key to evaluate the flag for
USER_KEY = "user_anonymous"

# The feature flag name
FLAG_NAME = "show-discount-banner"

# Localhost mode config — reads treatments from a local flags.yaml file
LOCALHOST_CONFIG = {
    "splitFile": "flags.yaml"
}

# Initialize the SDK
print("Initializing Harness FME Python SDK...")
if SDK_KEY == "YOUR_SERVER_SIDE_SDK_KEY" or SDK_KEY == "localhost":
    factory = get_factory("localhost", config=LOCALHOST_CONFIG)
else:
    factory = get_factory(SDK_KEY)

try:
    factory.block_until_ready(10)
    print("SDK initialized successfully.")
except TimeoutException:
    print("SDK initialization timed out. Check your SDK key.")

split_client = factory.client()


@app.route("/")
def home():
    treatment = split_client.get_treatment(USER_KEY, FLAG_NAME)

    if treatment == "on":
        banner = """
        <div style="
            background: #1565C0;
            color: white;
            padding: 16px;
            border-radius: 8px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 16px 0;
        ">
            🎉 10% off today! Use code <strong>HARNESS10</strong> at checkout.
        </div>
        """
    else:
        banner = ""

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Harness E-Commerce Store — Python</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            .sdk-badge {{
                display: inline-block;
                background: #306998;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 8px;
            }}
            .products {{ background: #f5f5f5; padding: 20px; border-radius: 8px; margin-top: 20px; }}
            .flag-status {{ font-size: 12px; color: #888; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="sdk-badge">🐍 Python SDK — port 5001</div>
        <h1>🛍️ Harness E-Commerce Store</h1>
        <p>Welcome to our store! Check out our latest products.</p>

        {banner}

        <div class="products">
            <h2>Featured Products</h2>
            <p>Product 1 — $49.99</p>
            <p>Product 2 — $29.99</p>
            <p>Product 3 — $99.99</p>
        </div>

        <p class="flag-status">
            Flag: <strong>{FLAG_NAME}</strong> | Treatment: <strong>{treatment}</strong>
        </p>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
