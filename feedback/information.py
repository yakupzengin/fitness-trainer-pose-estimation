def get_exercise_info(exercise_type):
    exercises = {
        "hammer_curl": {
            "name": "Hammer Curl",
            "target_muscles": ["Biceps", "Brachialis"],
            "equipment": "Dumbbells",
            "reps": 8,
            "sets": 1,
            "rest_time": "60 seconds",
            "benefits": [
                "Improves bicep and forearm strength",
                "Enhances grip strength"
            ]
        },
        "push_up": {
            "name": "Push-Up",
            "target_muscles": ["Chest", "Triceps", "Shoulders"],
            "equipment": "Bodyweight",
            "reps": 10,
            "sets": 1,
            "rest_time": "45 seconds",
            "benefits": [
                "Builds upper body strength",
                "Improves core stability"
            ]
        },
        "squat": {
            "name": "Squat",
            "target_muscles": ["Quads", "Glutes", "Hamstrings"],
            "equipment": "Bodyweight or Barbell",
            "reps": 2,
            "sets": 3,
            "rest_time": "60 seconds",
            "benefits": [
                "Builds lower body strength",
                "Improves mobility and balance"
            ]
        }
    }

    return exercises.get(exercise_type, {})
