from flask import Flask, render_template, request
import logging
import os

logging.basicConfig(level=logging.DEBUG)

class Webserver:
    def __init__(self, clear_display):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(current_directory, 'web', 'templates')
        static_dir = os.path.join(current_directory, 'web', 'static')
        self.app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
        self.clear_display = clear_display

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
            return render_template('home.html', regular_total=planTotal, regular_used=planUsed, regular_percentage=planPercentageRemaining, bonus_total=bonusTotal, bonus_used=bonusUsed, bonus_percentage=bonusPercentageRemaining)

        @self.app.route('/settings')
        def settings():
            return render_template('settings.html')
        
        @self.app.route('/clear-display', methods=['POST'])
        def clear_display_route():
            result = self.clear_display()
            return result
            

        self.app.run()
