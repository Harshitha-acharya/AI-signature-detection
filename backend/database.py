import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Harshitha@3664",
        database="signguard"
    )


def save_analysis(
    real_signature,
    doubted_signature,
    similarity,
    forgery_risk,
    pixel_similarity,
    shape_similarity,
    stroke_similarity,
    result
):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO signature_analysis
        (
            real_signature,
            doubted_signature,
            similarity,
            forgery_risk,
            pixel_similarity,
            shape_similarity,
            stroke_similarity,
            result
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        real_signature,
        doubted_signature,
        similarity,
        forgery_risk,
        pixel_similarity,
        shape_similarity,
        stroke_similarity,
        result
    )

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()