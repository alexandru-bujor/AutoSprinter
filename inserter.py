import mysql.connector
import json
import re


# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="autosprinter"
    )


# Function to clean numeric values (mileage, engine capacity, price)
def clean_numeric(value):
    """Extracts only numeric values from a string, returns 0 if empty."""
    if not value:
        return 0
    return int(''.join(re.findall(r'\d+', value)))  # Extract numbers


# Function to insert car data
def insert_car_data(json_data):
    conn = get_db_connection()
    cursor = conn.cursor()

    for car in json_data:
        print(f"\nProcessing: {car.get('titlu', 'Unknown Title')}")

        detalii = car.get("detalii", {})
        general = detalii.get("General", {})
        caracteristici = detalii.get("Caracteristici", {})

        # Extract images safely
        images = car.get("imagini", [])
        thumbnail = images[0] if images else "default.jpg"  # Default image if none available

        # Extract values safely
        car_values = (
            car.get("id", None),  # ID
            str(car.get("id", "")),  # Slug
            car.get("titlu", None),  # Name
            general.get("Model", None),  # Model
            clean_numeric(caracteristici.get("An de fabricație", "0")),  # Year
            general.get("Înmatriculare", None),  # Registration
            caracteristici.get("Tip combustibil", None),  # Fuel
            caracteristici.get("Cutie de viteze", None),  # Transmission
            caracteristici.get("Tip caroserie", None),  # Body Type
            caracteristici.get("Cabină", None),  # Transport Type (Cabin Type)
            None,  # Color (if needed, extract from JSON)
            clean_numeric(caracteristici.get("Capacitate motor", "0")),  # Engine Capacity
            None,  # Seats (if available, extract from JSON)
            clean_numeric(caracteristici.get("Distanță parcursă", "0 km")),  # Mileage
            caracteristici.get("Tracțiune", None),  # Drive Type
            clean_numeric(car.get("preț", "0")),  # ✅ Price added
            None,  # Contact phone (if available, extract from JSON)
            None,  # Monthly rate (if available, extract from JSON)
            thumbnail  # Thumbnail image
        )

        # Print extracted values for debugging
        print("Extracted values:", car_values)

        insert_car_sql = """
        INSERT INTO cars (id, slug, name, model, year, registration, fuel, transmission, body_type, transport_type, 
                          color, engine_capacity, seats, mileage, drive_type, price, contact_phone, monthly_rate, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        try:
            cursor.execute(insert_car_sql, car_values)
            car_id = cursor.lastrowid  # Get the inserted car ID

            # Insert only the first 10 images
            insert_image_sql = "INSERT INTO car_images (car_id, image_url) VALUES (%s, %s)"
            for img in images[:10]:  # Select up to 10 images
                cursor.execute(insert_image_sql, (car_id, img))

            print(f"✅ Inserted: {car['titlu']} (ID: {car_id}) with {len(images)} images")

        except mysql.connector.Error as err:
            print(f"❌ Error inserting {car.get('titlu', 'Unknown Title')}: {err}")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ All data inserted successfully!")


if __name__ == "__main__":
    with open("static/foto_auto/detalii.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    insert_car_data(data)
