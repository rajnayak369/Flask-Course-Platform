from flask import Flask, request, jsonify
from source.course_platform import Platform
from source.user import User
# from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

platform = Platform()  # Create a global Platform instance
platform.add_course("HTML", 1, 8)
platform.add_course("CSS", 2, 12)
platform.add_course("JavaScript", 4, 16, {"HTML", "CSS"})
platform.add_course("Python", 3, 10)
platform.add_course("Java", 3, 10)
platform.add_course("React", 3, 10, {"JavaScript"})
platform.add_course("Django", 5, 21, {"JavaScript", "Python"})

@app.route('/home')
@cross_origin()
def home():
    try:
        courses = list(platform.courses.keys())
        print(courses)
        response_data = {
            "courses": courses
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)})
    
    
    
@app.route('/add', methods=['POST'])
@cross_origin()
def add_course():
    try:
        # Get JSON data from request
        data = request.json
        print(data)
        platform.add_course(data['courseName'], int(data['courseRating']), int(data['courseDuration']), set(data['coursePrerequisite']))
        return jsonify({'message': 'Data received successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

    
@app.route('/enroll', methods=['POST'])
@cross_origin()
def enroll_course():
    try:
        # Get JSON data from request
        data = request.json
        print(data)
        # platform.add_course(data['courseName'], int(data['courseRating']), int(data['courseDuration']), set(data['coursePrerequisite']))
        course_path, duration,regular_path, reg_duration, parallel_courses = platform.course_enroll(data['enrollCourse'], set(data['completedCourses']),
                                                                         set(data['interestedCourses']), float(data['performanceRating']))
        if course_path:
            print("Optimised path for ", data['enrollCourse'], "->", course_path, "and duration ", duration)
            print("parallel courses you can take from the above personalised path are ", parallel_courses)
        else:
            print(f"You cannot enroll in '{data['enrollCourse']}' yet. it has cycle")
        enrollable_courses = platform.get_personalized_enrollable_courses(data['completedCourses'],
                                                                          data['interestedCourses'])
        response_data = {
            "coursePath": course_path,
            "duration":duration,
            "regPath": regular_path,
            "regduration":reg_duration,
            "parallelCourses":parallel_courses,
            "enrollableCourses":enrollable_courses
        }
        # Get all enrollable courses
        
        print(f"Enrollable Courses: {enrollable_courses}")
        return jsonify(response_data)
    except Exception as e:
        print
        return jsonify({'error': str(e)})


@app.route('/home1')
@cross_origin()
def index():
    try:
        platform.add_course("HTML", 1, 8)
        platform.add_course("CSS", 2, 12)
        platform.add_course("JavaScript", 4, 16, {"HTML", "CSS"})
        platform.add_course("Python", 3, 10)
        platform.add_course("Java", 3, 10)
        platform.add_course("React", 3, 10, {"JavaScript"})
        platform.add_course("Django", 5, 21, {"JavaScript", "Python"})

        user = User("Sairaj")
        user.add_completed_course("HTML")
        user.add_completed_course("CSS")
        user.interested_courses = {"Java", "CSS", "Python"}

        # Check if user can enroll in a course
        course_name = "Django"
        course_path, duration, parallel_courses = platform.course_enroll(course_name, user.completed_courses,
                                                                         user.interested_courses, user.performance)

        if course_path:
            print("Optimised path for ", course_name, "->", course_path, "and duration ", duration)
            print("parallel courses you can take from the above personalised path are ", parallel_courses)
        else:
            print(f"You cannot enroll in '{course_name}' yet. it has cycle")
        response_data = {
                "course_path": course_path,
                "duration": duration,
                "parallel_courses": parallel_courses
            }
        return jsonify(response_data)
    except Exception as e:
        print("Error occurred: ", e)


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)