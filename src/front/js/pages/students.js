import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from 'react-router-dom';
import { StudentCard } from "../component/studentCard/studentCard"
import { Loader } from "../component/loader/loader"
import swal from 'sweetalert'
import "../../styles/students.css"


export const Students = () => {
  const { store, actions } = useContext(Context);
  const [loaded, setLoaded] = useState("loadedEmpty")
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [address, setAddress] = useState("")
  const [phone, setPhone] = useState("")
  const [goal, setGoal] = useState("")
  const [loader, setLoader] = useState(false)
  const [searchStudent, setSearchStudent] = useState("")
  const [searchResult, setSearchResults] = useState([])
  const navigate = useNavigate()
  const students = store.allStudents

// UseEffect encargado de verificar si el usuario que navega tiene token

useEffect(() => {
  const getProfileData = async () => {
    let logged = await actions.getProfile();
    console.log(logged);
    if (logged === false) {
      swal({
        title: "Please",
        text: "USER NOT LOGGED IN! You will be redirected to login.",
        icon: "warning",
        buttons: {
          confirm: {
            text: "Return to Login",
            className: "custom-swal-button",
          },
        },
        timer: 4000,
        closeOnClickOutside: false,
      }).then(() => {
        navigate("/login");
      });
    }
  };
  getProfileData();
}, []);

  //  SE LLAMA A FUNCIÓN DESPUÉS DE TENER TOKEN

  useEffect(() => {
    actions.getAllStudents()
    setLoaded("fullLoaded")
  }, [store.token]);




  // FUNCIÓN PARA MANEJAR EL INPUT DEL SEARCH

  const handleInputChange = (e) => {
    const inputValue = e.target.value

    setSearchStudent(inputValue)
  }


  // FUNCIÓN PARA MANEJAR EL INPUT DE BUSQUEDA

  const handleEnterKeyPress = (e) => {
    e.preventDefault();
    const searchStudentUpperCase = searchStudent.toUpperCase();
    const filteredStudents = students.filter(student => {
      return student.name.toUpperCase().includes(searchStudentUpperCase);
    });


    if (filteredStudents.length > 0) {
      setSearchResults(filteredStudents)
      setSearchStudent("");
    } else {
      swal("Sorry", "no matches found", "warning", {
        buttons: {
          confirm: {
            text: "Try Again",
            className: "custom-swal-button",
          }
        },
        timer: 4000,
      });
      setSearchStudent("")
    }
  }

  // FUNCIÓN PARA AGREGAR ESTUDIANTES

  const handleCreateStudent = async (e) => {
    e.preventDefault()
    if (!name || !email || !address || !phone || !goal) {
      swal("Please", "Fields cannot be empty", "warning", {
        buttons: {
          confirm: {
            text: "Try Again",
            className: "custom-swal-button",
          }
        },
        timer: 4000,
      });
      return;
    } else if (!/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/.test(email)) {
      swal("Please", "enter a valid email address, mail can only contain letters numbers periods hyphens and the underscore", "error", {
        buttons: {
          confirm: {
            text: "Try Again",
            className: "custom-swal-button",
          }
        },
        timer: 4000,
      });
      return;
    }

    let response = await actions.createOneStudent(name, email, address, phone, goal);

    if (response === true) {

      swal("Good job!", "successfully created user.", "success", {
        buttons: {
          confirm: {
            text: "OK",
            className: "custom-swal-button",
          }
        },
        timer: 4000,
      });


      
      setName("");
      setEmail("");
      setAddress("");
      setPhone("");
      setGoal("");

      actions.getAllStudents()

    } else if (response.request.status === 402) {
      swal("Sorry", "An account with this email already exists", "error", {
        buttons: {
          confirm: {
            text: "Try Again",
            className: "custom-swal-button",
          }
        },
        timer: 4000,
      });
    } else {
      swal("Sorry", "An unexpected error has occurred", "error", {
        buttons: {
          confirm: {
            text: "Try Again",
            className: "custom-swal-button",
          }
        },
        timer: 4000,
      });
    };
  }

  const resetReturnData = () => {
    setName("");
    setEmail("");
    setAddress("");
    setPhone("");
    setGoal("");
  }

  // SE RENDERIZAN TARJETAS Y SE INCLUYE MODAL

  return (
    <div className="student-main-container">
      <div className="student-navbar">
        <div>
          <h5 className="student-headboard d-flex gap-2  justify-content-start"> Students
            <button className="add-button-student" data-bs-toggle="modal" data-bs-target="#addStudentModal">
              +
            </button>

          </h5>
        </div>

        {/* INICIO DEL MODAL  */}
        
          <div className="modal fade student-modal-main-container" id="addStudentModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content studentsContent">
                <form action="" className="student-modal-form_main">
                  <p className="modal-student-brand mb-0 h1 "><i className="fa-solid fa-bucket me-2"></i>Lesson Bucket</p>
                  <p className="student-modal-heading">Add student to my list</p>
                  <div className="student-modal-inputContainer">
                    <input type="text" className="student-modal-inputField" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
                  </div>

                  <div className="student-modal-inputContainer">
                    <input type="email" className="student-modal-inputField" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
                  </div>

                  <div className="student-modal-inputContainer">
                    <input type="text" className="student-modal-inputField" placeholder="Address" value={address} onChange={(e) => setAddress(e.target.value)} />
                  </div>

                  <div className="student-modal-inputContainer">
                    <input type="text" className="student-modal-inputField" placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} />
                  </div>

                  <div className="student-modal-inputContainer">
                    <input type="text" className="student-modal-inputField" placeholder="Goal" value={goal} onChange={(e) => setGoal(e.target.value)} />
                  </div>
                  <div className="student-modal-button-container" >
                    <button type="button" className="student-modal-button student-modal-button-create" onClick={handleCreateStudent}>Create new student</button>
                    <button type="button" className="student-modal-button student-modal-button-return" data-bs-dismiss="modal" onClick={() => { resetReturnData() }}>return</button>
                  </div>
                </form>
              </div>
            </div>
          </div>


          {/* // FIN DEL MODAL */}

          {/* //  INICIO FUNCIÓN SEARCH */}

        
        <div className="searchbarStyle ">
          <input
            className="student-search-input"
            placeholder="Search..."
            required=""
            value={searchStudent}
            onChange={(e) => handleInputChange(e)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                handleEnterKeyPress(e);
              }
            }}

          />

          {/* FIN FUNCIÓN SEARCH  */}

          <button className="student-button-refresh px-4 py-1" onClick={() => { actions.getAllStudents(); setSearchResults([]) }}>Refresh</button>
        </div>

      </div>
      {store.allStudents && store.allStudents.length > 0 ? (
        <>
          <div className="row d-flex flex-wrap justify-content-start gap-0">
            {loaded === "fullLoaded" && (
              (searchResult.length > 0 ? searchResult : students).map(student => (
                <div className="col-3" key={student.id}>
                  <StudentCard
                    id={student.id}
                    name={student.name}
                    phone={student.phone}
                    email={student.email}
                    address={student.address}
                    goal={student.goal}
                  />
                </div>
              ))
            )}
          </div>
        </>
      ) : (
        <div className="recover-pass-main">
          {store.logged ? (
            <div>
              <h1 className="loading-screen">The student list is empty. Please include your students in the + icon to get started.</h1>
            </div>
          ) : (
            <div className="recover-login">
              <form className="recover-form">
                <label htmlFor="recover-chk" aria-hidden="true">
                  ¡USER NOT LOGGED IN!
                </label>
                <h3 className="recover-instruction">
                  Please, If you press the button to be redirected to Login
                </h3>
                {loader && <Loader view="recoverPass" />}
                <div className="container-fluid">
                  <div className="row ">
                    <div className="col">
                      <button
                        className="recover-button-return student-noLogin-button"
                        type="button"
                        onClick={() => {
                          setLoader(true);
                          setTimeout(() => {
                            setLoader(false);
                            navigate("/login");
                          }, 1000);
                        }}
                      >
                        Return to Login
                      </button>
                    </div>
                  </div>
                </div>
              </form>
            </div>

          )}
        </div>
      )}
    </div>
  )
};
