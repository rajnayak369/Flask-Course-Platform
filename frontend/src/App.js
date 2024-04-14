import {useState, useEffect} from 'react';
import { Container, Row, Col } from "react-bootstrap";
import './App.css';
import CreatableSelect from "react-select/creatable";
import {
  VerticalTimeline,
  VerticalTimelineElement,
} from "react-vertical-timeline-component";
import "react-vertical-timeline-component/style.min.css";

function App() {
  const [courses, setCourses] = useState([]);
  const [avaliableCourses, setAvaliableCourses] = useState([]);
  const [selectedCompletedCourses, setSelectedCompletedCourses] = useState([]);
  const [prerequisite, setPrerequisite ] = useState([])
  const [interested , setInterested ] = useState([])
  const [path, setPath] = useState([])
  const [pathDuration, setPathDuration] = useState()
  const [parallelCourses, setParallelCourses] = useState([])
  const [independentCourses, setIndependentCourses] = useState([])
  const [regPath, setRegPath] = useState([])
  const [regPathDuration, setRegPathDuration] = useState()





  const rating = [
    { value: "1", label: "1" },
    { value: "2", label: "2" },
    { value: "3", label: "3" },
    { value: "4", label: "4" },
    { value: "5", label: "5" },
  ];

  const duration = [
    { value: "1", label: "1" },
    { value: "2", label: "2" },
    { value: "3", label: "3" },
    { value: "4", label: "4" },
    { value: "5", label: "5" },
    { value: "6", label: "6" },
    { value: "7", label: "7" },
    { value: "8", label: "8" },
    { value: "9", label: "9" },
    { value: "10", label: "10" },
  ];

  function createOptions(names) {
    return names.map(name => ({
      value: name,
      label: name
    }));
  }
  
  const fetchHomeData = () => {
    fetch("/home").then(response => {
      if(response.status === 200){
        return response.json()
      }else {
        throw new Error("Failed to fetch data: " + response.statusText);
      }
    }) .then(data => {
      console.log(data);
      const options = createOptions(data.courses);
      setCourses(options);
      setAvaliableCourses(options) // Update state with parallel_courses
      if (pathDuration == null){
        setPathDuration(0)
        setRegPathDuration(0)
      }
    })
    .then(error => console.log(error))
  };

  useEffect(() => {
    fetchHomeData();
  },[])

  const handleAddSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target); // Get form data from the event object
    // Convert form data to JSON
    const jsonData = {};
    formData.forEach((value, key) => {
      if (key === "coursePrerequisite"){
        const predata = prerequisite.map((item) => item.value);
        jsonData[key] = predata;
      }else {
        jsonData[key] = value;
      }
    });
    // Send POST request with form data to /add endpoint
    fetch('/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jsonData),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Success:', data);
      fetchHomeData();
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  const handleEnrollSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target); // Get form data from the event object
    // Convert form data to JSON
    const jsonData = {};
    formData.forEach((value, key) => {
      if (key === "completedCourses"){
        const data1 = selectedCompletedCourses.map((item) => item.value);
        jsonData[key] = data1;
      } else if(key === "interestedCourses"){
        const data2 = interested.map((item) => item.value);
        jsonData[key] = data2;
      }
      else {
        jsonData[key] = value;
      }
    });
    console.log("enroll:", jsonData)
    // Send POST request with form data to /add endpoint
    fetch('/enroll', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(jsonData),
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Success:', data);
      setPath(data.coursePath)
      setPathDuration(data.duration)
      setParallelCourses(data.parallelCourses)
      setIndependentCourses(data.enrollableCourses)
      setRegPath(data.regPath)
      setRegPathDuration(data.regduration)
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  
  const handlePrerequisite = (selectedOption) => {
    setPrerequisite(selectedOption);
  };
  const handleInterested = (selectedOption) => {
    setInterested(selectedOption);
  };

  const handleChange = (selectedOption) => {
      setSelectedCompletedCourses(selectedOption);
      // Filter out selected courses from courses array
      const remainingCourses = courses.filter(course => !selectedOption.some(selected => selected.value === course.value));
      setAvaliableCourses(remainingCourses);
  };

  return (
    <div className="App">
       
     <section className="contact" id="contact-us">
    
          <Container>
          <div className='courses'>
              <b>Courses:</b>
            {courses.map((course, index) => (
                <b key={index}>{course.value} </b>
              ))}
            </div>
            <Row className="align-items-center">
              
              <Col size={12} md={6} className='box'>
                <h2 >Add Course</h2>
                    
                    <form onSubmit={handleAddSubmit} >
                      <Row>
                    
                        <Col size={12} sm={6} className="px-1">
                          <input type="text"  placeholder="Course Name" name='courseName' required/>
                        </Col>
                     
                        <Col size={12} className="px-1">
                        <CreatableSelect className='select-react'
                          options={courses}
                          isMulti
                          placeholder="Course prerequisite"
                          name='coursePrerequisite'
                          onChange={handlePrerequisite}
                        />
                      
                        </Col>
                        <Col size={12} className="px-1">
                        <CreatableSelect className='select-react'
                          options={duration}
                          placeholder="Course duration"
                          required
                          name='courseDuration'
                        />
                        </Col>
                        
                        <Col size={12} className="px-1">
                        <CreatableSelect className='select-react'
                          options={rating}
                          placeholder="Difficulty rating"
                          required
                          name='courseRating'
                        />
                        </Col>
                        <Col size={12} className="px-1">
                          <button type="submit"><span>Add</span></button>
                        </Col>
                      
                      </Row>
                    </form>
 
              </Col>
              <Col size={12} md={6} className='box'>
              <h2 >Enroll Course</h2>
              <form onSubmit={handleEnrollSubmit}>
                      <Row>
                      <Col size={12} className="px-1">
                        <CreatableSelect className='select-react'
                          options={courses}
                          onChange={handleChange}
                          isMulti
                          placeholder="Completed courses"
                          name='completedCourses'
                        />
                      </Col>
                        <Col size={12} className="px-1">
                        <CreatableSelect className='select-react'
                          options={avaliableCourses}
                          placeholder="Select Course"
                          required
                          name='enrollCourse'
                        />
                      
                        </Col>
                        <Col size={12} className="px-1">
                        <CreatableSelect className='select-react'
                          options={courses}
                          isMulti
                          placeholder="Interests to include"
                          required
                          onChange={handleInterested}
                          name='interestedCourses'
                        />
                        </Col>
                        
                        <Col size={12} className="px-1">
                        <CreatableSelect className='select-react'
                          options={rating}
                          placeholder="performance rating"
                          required
                          name='performanceRating'
                        />
                        </Col>
                        <Col size={12} className="px-1">
                          <button type="submit"><span>Add</span></button>
                        </Col>
                      
                      </Row>
                    </form>
              </Col>
              <Col size={12} md={6} className='box'>
                <h2 >Learning path</h2>
                <div className='path'>
                  
                <div className='path1'>
                <h4 >Personalised {pathDuration} hrs</h4>

                <VerticalTimeline layout='1-column-left'>
                  {path.map((element) => {
                    

                    return (
                      <VerticalTimelineElement
                        key={element}
                      >
                    
                        <h5 className="vertical-timeline-element-subtitle">
                          {element}
                        </h5>
                      </VerticalTimelineElement>
                    );
                  })}
                </VerticalTimeline>
                </div>
                <diV className="path1">
                  <h4 >Regular {regPathDuration} hrs</h4>

                <VerticalTimeline layout='1-column-left'>
                  {regPath.map((element) => {
                    

                    return (
                      <VerticalTimelineElement
                        key={element}
                      >
                    
                        <h5 className="vertical-timeline-element-subtitle">
                          {element}
                        </h5>
                      </VerticalTimelineElement>
                    );
                  })}

                </VerticalTimeline>
                </diV>
                </div>
                <br></br>
                <p>Parallel courses to choose from path:</p>

                <div className='courses ind'>
                  {parallelCourses.map((course) => (
                      <b >{course}  </b>
                    ))}
                  </div>

                  <br></br>
                <p>More Independent courses to choose:</p>

                <div className='courses ind'>
                  {independentCourses.map((course) => (
                      <b >{course}  </b>
                    ))}
                  </div>
 
              </Col>
            </Row>
            
          </Container>

        </section>
    </div>
  );
}

export default App;


