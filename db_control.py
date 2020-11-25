import sqlite3

con  = sqlite3.connect("Fitness.db")


c = con.cursor()


def commit():
    con.commit()


def close():
    con.close()


#-------------------------------------------------------------------------------
# CONTAINS METHODS ---------------------------------------------------------------
#-------------------------------------------------------------------------------
def contains_exercise(exercise_name):
    query = """SELECT ExerciseName FROM Exercise
                    WHERE ExerciseName = "{}";
                    """.format(exercise_name)
    c.execute(query)
    commit()
    if(c.fetchone() != None):
        return True
    return False

def contains_user(user_name, password):
    query = """SELECT UserName, Password FROM User
                    WHERE UserName = "{}" AND Password = "{}";
                    """.format(user_name, password)
    c.execute(query)
    user = c.fetchone()

    # Return false if query found nothing
    if(user == None):
        return False

    return True


def check_unique(str_key, table_name, table_attribute):
    key_query = """SELECT {} FROM {};""".format(table_attribute, table_name)
    c.execute(key_query)
    keys = c.fetchone()
    if(keys != None):
        for key in keys:
            if(key == str_key):
                return False
    return True


#-------------------------------------------------------------------------------
# CREATE METHODS ---------------------------------------------------------------
#-------------------------------------------------------------------------------
def create_user(user_name, first_name, last_name, password):
    # Check if user_name is taken
    if(not check_unique(user_name, "User", "UserName")):
        return False

    insert = """ INSERT INTO User (UserName, FirstName, LastName, Password)
                    VALUES("{}", "{}", "{}", "{}");
                    """.format(user_name, first_name, last_name, password)
    c.execute(insert)
    commit()
    return True


def create_exercise(exercise_name, movement_type):
    # Check if exercise_name is unique
    if(not check_unique(exercise_name, "Exercise", "ExerciseName")):
        return False

    insert = """INSERT INTO Exercise (ExerciseName, Type)
                    VALUES("{}", "{}");
                    """.format(exercise_name, movement_type)
    c.execute(insert)
    commit()
    return True


def create_workout(type, hours, minutes):
    insert = """INSERT INTO Workout(Type, Hours, Minutes)
                    VALUES("{}", "{}", "{}");
                """.format(type, hours, minutes)
    c.execute(insert)
    commit()
    return c.lastrowid


def create_completed_exercise(exercise_name, workout_ID, reps, sets, weight):
    insert = """INSERT INTO CompletedExercise(ExerciseName, WorkoutID, Reps, Sets, Weight)
                    VALUES("{}", "{}", "{}", "{}", "{}");
                    """.format(exercise_name, workout_ID, reps, sets, weight)
    c.execute(insert)
    commit()
    return True


def create_exercise_record(user_name, exercise_name, max_reps, max_sets, max_weight, num_used):
    insert = """INSERT INTO ExerciseRecord(UserName, ExerciseName, MaxReps, MaxSets, MaxWeight, NumUsed)
                    VALUES("{}", "{}", "{}", "{}", "{}", "{}");
                    """.format(user_name, exercise_name, max_reps, max_sets, max_weight, num_used)

    c.execute(insert)
    commit()
    return True

def create_has_workout(user_name, workout_ID, month, day, year):
    insert = """INSERT INTO HasWorkout(UserName, WorkoutID, Month, Day, Year)
                    VALUES("{}", "{}", "{}", "{}", "{}");
                    """.format(user_name, workout_ID, month, day, year)
    c.execute(insert)
    commit()
    return True


#-------------------------------------------------------------------------------
# GET METHODS ------------------------------------------------------------------
#-------------------------------------------------------------------------------
def get_exercise_record(user_name, exercise_name):
    query = """SELECT MaxReps, MaxSets, MaxWeight, NumUsed, ExerciseRecordID
                    FROM ExerciseRecord
                    WHERE UserName = "{}" AND ExerciseName = "{}";
                    """.format(user_name, exercise_name)
    c.execute(query)
    commit()
    record = c.fetchone()
    return record

# GROUP 2
def search_exercise_record(search_word, user_name, limit, offset):
    query = """SELECT ExerciseName, NumUsed, MaxReps, MaxSets, MaxWeight, Type
                    FROM ExerciseRecord NATURAL JOIN Exercise
                    WHERE ExerciseRecord.UserName = "{}" AND Exercise.ExerciseName LIKE "%{}%"
                    LIMIT {}
                    OFFSET {};""".format(user_name, search_word, limit, offset)
    c.execute(query)
    commit()
    search_results = c.fetchall()
    return search_results

def get_fav_exercise(user_name):
    query = """SELECT MAX(ExerciseRecord.NumUsed), Exercise.ExerciseName
                    FROM User NATURAL JOIN ExerciseRecord
                    JOIN Exercise ON Exercise.ExerciseName = ExerciseRecord.ExerciseName
                    WHERE UserName = "{}";""".format(user_name)
    c.execute(query)
    commit()
    fav_exercise = c.fetchone()
    return fav_exercise


def get_hours_workedout(user_name, month):
    query = """SELECT (sum(Hours) * 60 + sum(Minutes))/60 AS HoursWorked
                    FROM User NATURAL JOIN HasWorkout
                    JOIN Workout ON HasWorkout.WorkoutID = Workout.WorkoutID
                    WHERE UserName = "{}" AND HasWorkout.Month = {};
                    """.format(user_name, month)
    c.execute(query)
    commit()
    total_hours = c.fetchone()
    return total_hours

# GROUP 3
def get_tot_app_percentage(month, user_name):
    query = """SELECT CAST(PersonalHours AS FLOAT)/CAST(TotHours AS FLOAT)
                    FROM (SELECT UserName, (CAST(sum(Workout.Hours) AS FLOAT)) + CAST(sum(Workout.Minutes) AS FLOAT)/60 AS PersonalHours, TotalHours.HoursWorked AS TotHours
                            FROM User NATURAL JOIN HasWorkout
                            JOIN Workout ON HasWorkout.WorkoutID = Workout.WorkoutID
                            JOIN (SELECT (CAST(sum(Workout.Hours) AS FLOAT)) + CAST(sum(Workout.Minutes) AS FLOAT)/60 AS HoursWorked
                                    FROM User NATURAL JOIN HasWorkout
                                    JOIN Workout ON HasWorkout.WorkoutID = Workout.WorkoutID
                                    WHERE HasWorkout.Month = {}) AS TotalHours
                            WHERE HasWorkout.Month = {} AND UserName = "{}")
                         """.format(month, month, user_name)
    c.execute(query)
    commit()
    percentage = c.fetchone()
    return percentage

# GROUP 1
def get_workout_type_count(user_name):
    query = """SELECT Workout.Type, count(*) AS NumType
                    FROM User
                    JOIN HasWorkout ON HasWorkout.UserName = User.UserName
                    NATURAL JOIN Workout
                    WHERE User.UserName = "{}"
                    GROUP BY Workout.Type
                    ORDER BY NumType DESC;""".format(user_name)
    c.execute(query)
    commit()
    types = c.fetchall()
    return types

#-------------------------------------------------------------------------------
# UPDATE METHODS ---------------------------------------------------------------
#-------------------------------------------------------------------------------
def update_records(exercise_record_id, max_rep, max_sets, max_weight, num_used):
    update = """UPDATE ExerciseRecord
                    SET MaxReps = "{}", MaxSets = "{}", MaxWeight = "{}",
                        NumUsed = "{}"
                    WHERE ExerciseRecordID = "{}";
                    """.format(max_rep, max_sets, max_weight, num_used, exercise_record_id)
    c.execute(update)
    commit()
    return True
