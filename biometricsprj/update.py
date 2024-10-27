def update_personalizations(user_id):
    lighting = input("Enter lighting level (low/medium/high): ")
    music = input("Enter music type: ")
    fan = input("Enter fan level (low/medium/high): ")
    tv = input("Enter TV mode (movie/sports/news): ")
    
    query = """
    INSERT INTO personalizations (user_id, lighting_level, music_type, fan_level, tv_mode)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    lighting_level = VALUES(lighting_level), music_type = VALUES(music_type),
    fan_level = VALUES(fan_level), tv_mode = VALUES(tv_mode)
    """
    
    cursor.execute(query, (user_id, lighting, music, fan, tv))
    db.commit()
    print(f"Personalizations updated for User ID {user_id}.")

# Call this function when you want to update the settings for a user
update_personalizations(authenticated_user_id)
