from flask import Flask, render_template, jsonify
import redis
import json

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379, db=0)

@app.route('/')
def index():
    # A simple HTML page that will auto-refresh
    return """
    <html>
        <head>
            <title>Real-Time Dashboard</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <meta http-equiv="refresh" content="1">
        </head>
        <body class="bg-gray-900 text-white p-10">
            <h1 class="text-3xl font-bold mb-5">Real-Time Page Views</h1>
            <div id="data-container" class="grid grid-cols-2 gap-4"></div>
            <h2 class="text-2xl font-bold mt-10 mb-5">Latest Events</h2>
            <div id="events-container" class="bg-gray-800 p-4 rounded-lg font-mono text-sm"></div>
            <script>
                fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        // Page Counts
                        const container = document.getElementById('data-container');
                        container.innerHTML = '';
                        for (const [page, count] of Object.entries(data.page_counts)) {
                            container.innerHTML += `
                                <div class="bg-gray-700 p-4 rounded-lg">
                                    <div class="text-gray-400 text-sm">${page}</div>
                                    <div class="text-2xl font-bold">${count}</div>
                                </div>
                            `;
                        }
                        
                        // Latest Events
                        const eventsContainer = document.getElementById('events-container');
                        eventsContainer.innerHTML = '';
                        data.latest_events.forEach(event => {
                            eventsContainer.innerHTML += `<div>${JSON.stringify(event)}</div>`;
                        });
                    });
            </script>
        </body>
    </html>
    """

@app.route('/data')
def get_data():
    # Get all page counts from Redis
    page_counts = r.hgetall('page_counts')
    page_counts_decoded = {
        k.decode('utf-8'): int(v.decode('utf-8')) 
        for k, v in page_counts.items()
    }
    
    # Get latest 10 events
    latest_events = r.lrange('latest_events', 0, 9)
    latest_events_decoded = [
        json.loads(e.decode('utf-8')) 
        for e in latest_events
    ]
    
    return jsonify(
        page_counts=page_counts_decoded,
        latest_events=latest_events_decoded
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
