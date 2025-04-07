from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="autosprinter"
    )

# Fetch cars with optional filters
def fetch_cars(filters=None, limit=None, offset=0):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT cars.*, GROUP_CONCAT(car_images.image_url) AS images
    FROM cars
    LEFT JOIN car_images ON cars.id = car_images.car_id
    WHERE 1=1
    """
    params = []

    if filters:
        if filters.get('brand'):
            query += " AND name = %s"
            params.append(filters['brand'])
        if filters.get('model'):
            query += " AND model = %s"
            params.append(filters['model'])
        if filters.get('year'):
            query += " AND year = %s"
            params.append(filters['year'])
        if filters.get('seats'):
            query += " AND seats = %s"
            params.append(filters['seats'])

    query += " GROUP BY cars.id ORDER BY cars.id DESC"

    if limit is not None:
        query += f" LIMIT {limit} OFFSET {offset}"

    cursor.execute(query, tuple(params))
    cars = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert the comma-separated image URLs into a list
    for car in cars:
        car['images'] = car['images'].split(',') if car['images'] else []

    return cars

# Fetch filter options (brands, models, years, seats)
def get_filter_options():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM cars")
    brands = [row[0] for row in cursor.fetchall() if row[0] is not None]
    cursor.execute("SELECT DISTINCT model FROM cars")
    models = [row[0] for row in cursor.fetchall() if row[0] is not None]
    cursor.execute("SELECT DISTINCT year FROM cars ORDER BY year DESC")
    years = [row[0] for row in cursor.fetchall() if row[0] is not None]
    cursor.execute("SELECT DISTINCT seats FROM cars ORDER BY seats")
    seats = [row[0] for row in cursor.fetchall() if row[0] is not None]
    cursor.close()
    conn.close()
    return {
        'brands': brands,
        'models': models,
        'years': years,
        'seats': seats
    }

# Home page route
@app.route('/')
def index():
    cars = fetch_cars(limit=5)
    return render_template('index.html', cars=cars)

# Catalog page route with filters
@app.route('/catalog')
def catalog():
    filters = {
        'brand': request.args.get('brand'),
        'model': request.args.get('model'),
        'year': request.args.get('year'),
        'seats': request.args.get('seats')
    }
    cars = fetch_cars(filters=filters)

    filter_options = get_filter_options()
    return render_template('catalog.html', cars=cars, filter_options=filter_options)

# Car details page route
@app.route('/car/<slug>')
def car_detail(slug):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT cars.*, GROUP_CONCAT(car_images.image_url) AS images
    FROM cars
    LEFT JOIN car_images ON cars.id = car_images.car_id
    WHERE cars.slug = %s
    GROUP BY cars.id
    """, (slug,))
    car = cursor.fetchone()
    cursor.close()
    conn.close()

    if car is None:
        return "Car not found", 404

    car['images'] = car['images'].split(',') if car['images'] else []
    return render_template('car.html', car=car)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
