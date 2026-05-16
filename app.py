from flask import Flask, jsonify, render_template
import logging

from services.dynamodb_service import get_metrics

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/')
def dashboard():

    logger.info("Dashboard page accessed")

    return render_template('index.html')

@app.route('/health')
def health_check():

    logger.info("Health endpoint accessed")

    return jsonify({
        "status": "healthy"
    })

@app.route('/api/metrics')
def api_metrics():

    logger.info("Metrics endpoint accessed")

    try:

        metrics = get_metrics()

        return jsonify({
            "status": "success",
            "count": len(metrics),
            "data": metrics
        })

    except Exception as e:

        logger.exception(f"Failed to retrieve metrics: {str(e)}")

        return jsonify({
            "status": "error",
            "message": "Unable to retrieve metrics"
        }), 500
    
if __name__ == '__main__':

    logger.info("Starting Flask dashboard application")

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )