class User:
    def __init__(self, name: str):
        """
        Initializes a new User object.
        """
        self.name = name
        self.performance = 1
        self.completed_courses = set()
        self.interested_courses = set()

    def update_performance(self, level: float):
        """
        Updates the performance level of the user.
        """
        self.performance = level

    def add_completed_course(self, course_name: str):
        """
        Adds a completed course to the user's profile.
        """
        self.completed_courses.add(course_name)

    def add_interested_course(self, course_name: str):
        """
       Adds an interested course to the user's profile.
       """
        self.interested_courses.add(course_name)

    def __str__(self):
        """
        Returns a string representation of the User object.
        """
        return f"User name: {self.name}"
