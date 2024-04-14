class Course:
    def __init__(self, name: str, level: int, duration: int):
        """
        Initializes a new Course object.
        """
        self.name = name
        self.prerequisites = set()
        self.level = level
        self.duration = duration

    def add_prerequisite(self, prerequisite_course: set):
        """
        Adds a set of prerequisite course to this course.
        """
        self.prerequisites = prerequisite_course

    def __str__(self):
        """
        Returns a string representation of the Course object.
        """
        return f"Course: {self.name}"
