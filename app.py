from shiny import App

# Import modular components
from modules.ui import create_app_ui
from modules.server import create_server_function

# Create the app
app = App(
    ui=create_app_ui(),
    server=create_server_function()
)

# The app will be launched when running "shiny run app.py"