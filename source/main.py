from course_platform import Platform
from user import User


def get_path():
    """
    Run a demo of course enrollment and path generation for a user.
    """
    try:
        platform = Platform()
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

        # Get all enrollable courses
        enrollable_courses = platform.get_personalized_enrollable_courses(user.completed_courses,
                                                                          user.interested_courses)
        print(f"Enrollable Courses: {enrollable_courses}")
    except Exception as e:
        print("Error occurred: ", e)


if __name__ == "__main__":
    get_path()
