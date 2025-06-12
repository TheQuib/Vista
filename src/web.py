from flask import Flask, render_template, request
import logging
import os
import json

logging.basicConfig(level=logging.DEBUG)

class Webserver:
    def __init__(self, refresh_display):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_directory, 'web', 'templates')
        static_dir = os.path.join(current_directory, 'web', 'static')
        self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
        self.refresh_display = refresh_display

        self.should_run = True # Server control loop flag
        self.data_file = os.path.abspath(os.path.join(current_directory, '..', 'latest_data.json'))

    def _read_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def stop_server(self):
        self.should_run = False

    def start_server(self):
        # Generate an initial display and data file
        self.refresh_display()

        @self.app.route('/')
        def home():
            if not self.should_run:
                request.environ.get('werkzeug.server.shutdown')()
            data = self._read_data()
            planTotal = float(data.get('plan_total', 0))
            planRemaining = float(data.get('plan_remaining', 0))
            planUsed = round(planTotal - planRemaining, 2)
            planPercentageRemaining = float(data.get('plan_percentage', 0))
            bonusTotal = float(data.get('bonus_total', 0))
            bonusRemaining = float(data.get('bonus_remaining', 0))
            bonusUsed = round(bonusTotal - bonusRemaining, 2)
            bonusPercentageRemaining = float(data.get('bonus_percentage', 0))
            fun_fact = data.get('fun_fact', [])
            return render_template(
                'home.html',
                regular_total=planTotal,
                regular_used=planUsed,
                regular_percentage=planPercentageRemaining,
                bonus_total=bonusTotal,
                bonus_used=bonusUsed,
                bonus_percentage=bonusPercentageRemaining,
                fun_fact=fun_fact
            )



        @self.app.route('/refresh-display', methods=['GET', 'POST'])
        def refresh_display_route():
            self.refresh_display()
            return "Display refreshed"
            

        if self.should_run:
            self.app.run(host="0.0.0.0", port=5000)
