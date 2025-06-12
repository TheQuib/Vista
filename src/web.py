from flask import Flask, render_template, request
import logging
import os

logging.basicConfig(level=logging.DEBUG)

class Webserver:
    def __init__(self, refresh_display):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_directory, 'web', 'templates')
        static_dir = os.path.join(current_directory, 'web', 'static')
        self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
        self.refresh_display = refresh_display

        self.should_run = True # Server control loop flag

    def stop_server(self):
        self.should_run = False

    def start_server(self, planTotal, planRemaining, bonusTotal, bonusRemaining):
        planTotal = float(planTotal)
        planRemaining = float(planRemaining)
        planUsed = planTotal - planRemaining
        planUsed = round(planUsed, 2)
        planPercentageRemaining = round((planRemaining / planTotal) * 100, 2)  # Calculating percentage

        bonusTotal = float(bonusTotal)
        bonusRemaining = float(bonusRemaining)
        bonusUsed = bonusTotal - bonusRemaining
        bonusUsed = round(bonusUsed, 2)
        bonusPercentageRemaining = round((bonusRemaining / bonusTotal) * 100, 2)  # Calculating percentage

        @self.app.route('/')
        def home():  
            if not self.should_run:
                request.environ.get('werkzeug.server.shutdown')()          
            return render_template('home.html', regular_total=planTotal, regular_used=planUsed, regular_percentage=planPercentageRemaining, bonus_total=bonusTotal, bonus_used=bonusUsed, bonus_percentage=bonusPercentageRemaining)



        @self.app.route('/refresh-display', methods=['GET', 'POST'])
        def refresh_display_route():
            self.refresh_display()
            return "Display refreshed"
            

        if self.should_run:
            self.app.run(host="0.0.0.0", port=5000)
