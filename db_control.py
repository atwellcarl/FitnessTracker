import sqlite3

con  = sqlite3.connect("Fitness.db")


c = con.cursor()


def commit():
    con.commit()


def close():
    con.close()


def is_user(user_name, password):
    query = """SELECT UserName, Password FROM User
                    WHERE UserName = "{}" AND Password = "{}"
                    """.format(user_name, password)
    c.execute(query)
    user = c.fetchone()

    # Return false if query found nothing
    if(user == None):
        return False

    return True


def check_unique(str_key, table_name, table_attribute):
    key_query = """SELECT {} FROM {}""".format(table_attribute, table_name)
    c.execute(key_query)
    keys = c.fetchone()
    if(keys != None):
        for key in keys:
            if(key == str_key):
                return False
    return True


def create_user(user_name, first_name, last_name, password):
    # Check if user_name is taken
    if(not check_unique(user_name, "User", "UserName")):
        return False

    insert = """ INSERT INTO User (UserName, FirstName, LastName, Password)
                    VALUES("{}", "{}", "{}", "{}")
                    """.format(user_name, first_name, last_name, password)
    c.execute(insert)
    commit()
    return True


def create_exercise(exercise_name, movement_type):
    # Check if exercise_name is unique
    if(not check_unique(exercise_name, "Exercise", "ExerciseName")):
        return False

    insert = """INSERT INTO Exercise (ExerciseName, Type)
                    VALUES("{}", "{}")
                    """.format(exercise_name, movement_type)
    c.execute(insert)
    commit()
    return True


def create_workout(type, hours, minutes):
    insert = """INSERT INTO Workout(Type, Hours, Minutes)
                VALUES("{}", "{}", "{}")
                """.format(type, hours, minutes)
    c.execute(insert)
    commit()
    return c.lastrowid


def create_completed_exercise(exercise_name, workout_ID, reps, sets, weight):
    insert = """INSERT INTO CompletedExercise(ExerciseName, WorkoutID, Reps, Sets, Weight)
                    VALUES("{}", "{}", "{}", "{}", "{}")
                    """.format(exercise_name, workout_ID, reps, sets, weight)
    c.execute(insert)
    commit()
    return True

def create_exercise_record(user_name, exercise_name, max_reps, max_sets, max_weight, num_used):
    insert = """INSERT INTO ExerciseRecord(UserName, ExerciseName, MaxReps, MaxSets, MaxWeight, NumUsed)
                    VALUES("{}", "{}", "{}", "{}", "{}", "{}")
                    """.format(user_name, exercise_name, max_reps, max_sets, max_weight, num_used)

    c.execute(insert)
    commit()
    return True

def create_has_workout(user_name, workout_ID, month, day, year):
    insert = """INSERT INTO HasWorkout(UserName, WorkoutID, Month, Day, Year)
                    VALUES("{}", "{}", "{}", "{}", "{}")
                    """.format(user_name, workout_ID, month, day, year)
    c.execute(insert)
    commit()
    return True
