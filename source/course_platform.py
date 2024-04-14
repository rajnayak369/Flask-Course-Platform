import heapq
from course import Course


class Platform:

    def __init__(self):
        """
        Initializes a new Platform object.
        """
        self.courses = {}  # Dictionary to store courses with name as key and Course object as value
        self.prerequisite_map = {}  # Graph representation with courses as keys and list of dependent courses as values


    def add_course(self, course_name: str, level: int, duration: int, prerequisites={}):
        """
        Adds a new course to the platform.

        Raises:
            ValueError: If the course name already exists or if the level or duration is invalid.
        """
        if course_name in self.courses:
            raise ValueError(f"Course '{course_name}' already exists")
        if not 1 <= level <= 5:
            raise ValueError("Level must be an integer between 1 and 5")
        if duration <= 0:
            raise ValueError("Duration must be a positive integer")
        course = Course(course_name, level, duration)
        self.courses[course_name] = course
        self.prerequisite_map[course_name] = []
        for prerequisite in prerequisites:
            if prerequisite not in self.courses:
                raise ValueError(f"Prerequisite '{prerequisite}' not found")
            self.prerequisite_map[course_name].append(prerequisite)
        course.add_prerequisite(prerequisites)  # Add prerequisite to the course object

    def update_completed_list(self, completed_courses:set):
        added_courses = set()  # Set to keep track of courses that have been added

        # Function to recursively add prerequisites
        def add_prereq(course):
            if course not in completed_courses:
                completed_courses.add(course)  # Add the course to completedCourses set
                added_courses.add(course)  # Add the course to addedCourses set
                
            for prereq in self.prerequisite_map[course]:
                # Recursively add prerequisites
                add_prereq(prereq)

        # Loop through each completed course
        for course in completed_courses.copy():
            # Check if the course has prerequisites and if it has not been added before
            if course not in added_courses:
                add_prereq(course)  # Add prerequisites


    def course_enroll(self, course_name: str, completed: set, area_interests: set, performance: float):
        """
       Enrolls a user in a course on the platform.

       Returns:
           Tuple: A tuple containing the enrolled course path, its duration, and parallel courses.
       """
        if course_name not in self.courses:
            raise ValueError(f"Course '{course_name}' not found")
        visited = set()  # Track visited courses
        # Track Processed courses to avoid processing it again if a different prerequisite lead to the same node
        processed = set()
        print(completed)
        self.update_completed_list(completed)
        print(completed)
        regular_course_path, personalized_course_path = self._can_enroll_helper(course_name, visited, processed,
                                                                                completed)
        if not regular_course_path:
            raise ValueError(
                f"Course '{course_name}' circular dependency detected. Consider revising course prerequisites.")
        if not personalized_course_path:
            raise ValueError(
                f"Course '{course_name}' and its prerequisites has been already completed by the user.")
        # return regular_course_path
        print("Initial course path: ", regular_course_path, "and duration",
              sum([self.courses[c].duration for c in regular_course_path]))
        personalized_course_path, parallel_courses = self._generate_personalized_learning_path(personalized_course_path,
                                                                                               area_interests,
                                                                                               completed,
                                                                                               performance)

        return personalized_course_path, sum(
            [self.courses[c].duration for c in personalized_course_path]),regular_course_path,sum([self.courses[c].duration for c in regular_course_path]), parallel_courses

    def _can_enroll_helper(self, course_name: str, visited: set, processed: set, completed: set):
        """
       Generates a personalized learning path for a user based on completed courses using topological sort.

       Returns:
           Tuple: A tuple containing the regular learning path and personalized learning path.
       """
        if course_name in visited:
            return []  # Cycle detected, return empty list
        visited.add(course_name)
        regular_course_path = []  # Regular course path which is common for every user
        personalized_course_path = []  # Personalized course path for this user
        for dependent in self.prerequisite_map[course_name]:
            # Recursively check if dependent courses can be enrolled in
            if dependent not in processed:
                start_courses_for_dependent, start_personalized_course_path = self._can_enroll_helper(dependent,
                                                                                                      visited,
                                                                                                      processed,
                                                                                                      completed)
                if start_courses_for_dependent:
                    # If dependent can be enrolled in, add it as a potential starting point
                    regular_course_path.extend(start_courses_for_dependent)
                    personalized_course_path.extend(start_personalized_course_path)
                else:
                    # If dependent has a circular dependency, return empty list
                    return []
        regular_course_path.append(course_name)
        # if course_name not in completed:
        if course_name not in completed:
            personalized_course_path.append(course_name)
        # Remove course_name from visited only after processing all dependents
        visited.remove(course_name)
        processed.add(course_name)
        return regular_course_path, personalized_course_path

    def _generate_personalized_learning_path(self, courses: list, area_interests: set, completed: set,
                                             performance: float):
        """
        Generates a personalized learning path for a user based on completed courses, area interests, and performance.

        Returns:
            Tuple: A tuple containing the updated personalized learning path and parallel courses related to this path.
        """
        interested_course, independent_courses_left, personalized_path = self.get_personalized_enrollable_courses(
            completed,
            area_interests,
            courses)
        heap = []
        for course in interested_course:
            if performance < 4:
                heap.append((self.courses[course].level, course))
            else:
                heap.append((-self.courses[course].level, course))
        heapq.heapify(heap)

        updated_interested_course = []
        for level, course in heap:
            updated_interested_course.append(course)
        # print("updated_interested_course", updated_interested_course, "interested_course", interested_course)
        # print("independent_courses_left:", independent_courses_left, "Reminder:", personalized_path)
        updated_personalized_path = updated_interested_course + independent_courses_left + personalized_path
        parallel_courses = updated_interested_course + independent_courses_left
        return updated_personalized_path, parallel_courses

    def get_personalized_enrollable_courses(self, completed: set, area_interests: set, courses=[]):
        """
        Returns personalized enrollable courses based on user data.

        Parameters:
            completed (set): A set of completed course names by the user.
            area_interests (set): A set of course areas of interest for the user.
            courses (list): A list of potential courses to consider.

        Returns:
            Tuple: A tuple containing the enrollable courses which are independent courses, and remaining courses left.
        """
        # Returns a list of all enrollable courses (no outstanding prerequisites)
        is_remove = True
        if not courses:
            courses = list(self.courses)
            is_remove = False
        enrollable_interested = []
        enrollable_rest = []
        for course_name in courses[:]:
            enrollable_course = None
            if not self.prerequisite_map[course_name] and course_name not in completed:
                enrollable_course = course_name
                if is_remove:
                    courses.remove(course_name)
            elif self.prerequisite_map[course_name] and course_name not in completed:
                is_independent = True
                for prereq in self.prerequisite_map[course_name]:
                    if prereq not in completed:
                        is_independent = False
                        break
                if is_independent:
                    enrollable_course = course_name
                    if is_remove:
                        courses.remove(course_name)
            if enrollable_course:
                if enrollable_course in area_interests:
                    enrollable_interested.append(enrollable_course)
                else:
                    enrollable_rest.append(enrollable_course)
        if is_remove:
            return enrollable_interested, enrollable_rest, courses
        return enrollable_interested + enrollable_rest
