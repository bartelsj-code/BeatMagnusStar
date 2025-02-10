from flask import Blueprint, render_template, request
from path_finding import api_requests, control_variables, data_access, format_conversion, game, get_path, path_finder, player_node

main = Blueprint('main', __name__)

# Simulate the pathfinding task (this is where your pathfinding logic would go)
def find_shortest_path(username, goal):
    # Simulate a delay while calculating the path
    import time
    time.sleep(3)  # Simulate a delay (replace with actual pathfinding logic)
    
    players = get_path.main(username, goal)
    # Simulated result
    return players

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/find_path', methods=['POST'])
def find_path():
    username = request.form['username']
    goal = request.form['goal']
    
    # Simulate finding the path
    players = find_shortest_path(username, goal)

    # Return the results to be displayed
    return render_template('results.html', players=players)

@main.route('/results')
def results():
    return render_template('results.html')
