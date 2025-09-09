  $(()=> {
    let calendarEl = document.getElementById('calendar');
    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'timeGridWeek,timeGridDay,dayGridMonth'
        },
        slotMinTime: "08:00:00",   //! start time
        slotMaxTime: "24:00:00",   //! end time
        slotDuration: "00:30:00",  //! 30 min slots
        slotLabelInterval: "00:30:00",
        // events: [
        //   {
        //     title: 'Vimla Kumari\nLAB TEST (Ankit Shah)\nDuration: 20 mins\nPaid',
        //     start: '2025-08-25T10:00:00',
        //     end: '2025-08-25T10:20:00',
        //     backgroundColor: 'lightgreen', // status: 'Pending'
        //     extendedProps: {
        //       patient: 'Vimla Kumari',
        //       status: 'Pending'
        //     }
        //   },
        // ],
        events : function(fetchInfo, successCallback, failureCallback) {

        //  console.log("Fetchinfo " , fetchInfo) ;

          $.ajax({
            url : `${GET_BASE_URL}/api/v1/patients` ,
            type :"GET" ,
            data : {
              start: fetchInfo.startStr ,
              end: fetchInfo.endStr ,
            } ,
          success: (data) => {

            let events = [];

            data.forEach(patient => {
              patient.appointment_patient.forEach(appt => {
            
                let start = `${appt.appdate}T${appt.apptime}`;

                let statusColors = {
                    "0": "green",  
                    "1": "red",
                    "2": "darkgreen",
                    "3": "orange"
                };
        
                let endTime = new Date(start);
                endTime.setMinutes(endTime.getMinutes() + 30);
                events.push({
                  title: patient.firstname ,
                  start: start,
                  end: endTime.toISOString(),
                  backgroundColor:  statusColors[appt.is_active] || "lightblue",
                  extendedProps: {
                    appointment : appt.id ,
                    patientid : patient.patient ,
                    patient: patient.firstname + " " + patient.lastname,
                    status: appt.status ,
                    isactive : appt.is_active
                  }
                });
              });
            });


            successCallback(events);
          }
          })
        },

        eventDidMount: function(info) {
          info.el.style.position = 'relative';
          info.el.style.overflow = 'hidden';

          let today = new Date();
          let day = today.getDay();
          let diff = today.getDate() - day + (day === 0 ? -6 : 1); 
          let mondayOfWeek = new Date(today.setDate(diff)); 
          mondayOfWeek.setHours(0,0,0,0);

          let eventDate = new Date(info.event.start);

          if (eventDate > mondayOfWeek) {
              // info.el.style.pointerEvents = 'none' ;
              // info.el.style.opacity = '0.5'; 


            let getAppointmentId = info.event.extendedProps.appointment;

            const main = info.el.querySelector('.fc-event-main');
            if (main) main.style.paddingRight = '56px';

            const wrapper = document.createElement('div');
            wrapper.style.gap = '0.2rem';

            
           // console.log("herethis is " , parseInt(info.event.extendedProps.isactive) )
            if ((parseInt(info.event.extendedProps.isactive) == 0 ) || parseInt(info.event.extendedProps.isactive) == 3  ){

      
            const editBtn = document.createElement('button');
            editBtn.className = 'fc-event-edit';
            editBtn.title = 'Edit'
            const editIcon = document.createElement('i');
            editIcon.className = 'bx bx-edit-alt';
            editBtn.appendChild(editIcon);
            editBtn.setAttribute('data-id', info.event.id);

            

            editBtn.addEventListener('click', (e) => {
              e.stopPropagation();
              window.location.href = `/patients/edit-patient-appointment?appointment=${getAppointmentId}`
            });

            
            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'fc-event-cancel';
            cancelBtn.title = 'Cancel'
            const cancelIcon = document.createElement('i');
            cancelIcon.className = 'bx bx-undo';
            cancelBtn.appendChild(cancelIcon);
            cancelBtn.setAttribute('data-id', info.event.id);

            cancelBtn.addEventListener('click', (e) => {
              e.stopPropagation();
              $.ajax({
                url : `${GET_BASE_URL}/api/v1/get-appointment` ,
                tpe : "GET" ,
                data : {
                  appointment : getAppointmentId
                } ,
                success : (data) =>{
                  // console.log("onappointment" , data)

                  let getdata =  data[0].status

                  if(parseInt(getdata) != 0){
                    Swal.fire({
                      title : "Error" ,
                      text :" Oops ! You are not allowed to cancel" ,
                      icon :'error' ,
                      confirmButtonText: 'OK'
                    })
                  }else{
                        Swal.fire({
                          title: 'Confirm Cancellation',
                          text: "Do you want to continue canceling this appointment?",
                          icon: 'warning',
                          showCancelButton: true,
                          confirmButtonText: 'Yes, Continue',
                          cancelButtonText: 'No, Cancel'
                      }).then((result) => {
                          if(result.isConfirmed){
                              $.ajax({
                                  url:  `${GET_BASE_URL}/api/v1/appointment/cancel/?id=${getAppointmentId}` ,
                                  type: 'PATCH',
                                  data: {
                                      // id : getAppointmentId ,
                                      status : "1"
                                  },
                                  success: function(response){
                                      Swal.fire({
                                          title: 'Success',
                                          text: 'Appointment has been cancelled successfully!',
                                          icon: 'success',
                                          confirmButtonText: 'OK'
                                      }).then(() => {
                                          setTimeout(() => {
                                            location.reload();
                                          }, 1200);
                                      });
                                  },
                                  error: function(xhr){
                                      Swal.fire({
                                          title: 'Error',
                                          text: 'Failed to cancel appointment. Please try again.',
                                          icon: 'error',
                                          confirmButtonText: 'OK'
                                      });
                                  }
                              });
                          }
                      });

                  }


                }
              })
            });

            // add both to wrapper
            wrapper.appendChild(editBtn);
            wrapper.appendChild(cancelBtn);

            // append wrapper to event
              info.el.appendChild(wrapper);
            }
          } 
        },

        dateClick: (info)=>{
          // console.log("getinfof" , info)

          let currentDate =  new Date().toISOString().slice(0,10);
          let getEventDate =  new Date(info.dateStr).toISOString().slice(0,10)
          
          if(getEventDate >= currentDate){
              let clinicID =  $(document).find('#clinic').val();
              let doctorId =  $(document).find('#doctor').val();
              let patientSelect =  $(document).find('#patient').val();

              $('#slotModal').data('dateslot' , info.dateStr).modal('show');
              $('#slotModal').data('clinic' , clinicID);
              $('#slotModal').data('doctor' , doctorId);
              $('#slotModal').data('patientSelect' , patientSelect);
              


              $('#slotModal').on('click' , '#confirmSlot' , (e)=>{
                  let date = $("#slotModal").data("dateslot");    

                  let clinicid =  $("#slotModal").data("clinic");
                  let doctor =  $("#slotModal").data("doctor");
                  

                  if(!clinicid || parseInt(clinicid) <= 0){
                    $('#slotModal').modal('hide');
                      Swal.fire({
                        title: 'Error!',
                        text: 'Please choose clinic',
                        icon: 'error',
                        confirmButtonText: 'OK'
                      });
                      return
                  }


                  if (!doctor || parseInt(doctor) <= 0){
                      $('#slotModal').modal('hide');
                      Swal.fire({
                          title: 'Error!',
                          text: 'Please choose doctor',
                          icon: 'error',
                          confirmButtonText: 'OK'
                      })

                    return ;
                  }

                  let getdate =  date.split('T')[0]
                  let gettime =  date.split('T')[1].slice(0,5)

                  let params = new URLSearchParams();

                  if (patientSelect && parseInt(patientSelect) > 0){
                      params.append("patient", patientSelect);
                  }

                  // console.log(patientSelect)
                  params.append("date", getdate);
                  params.append("time", gettime);params.append("clinicid", clinicid);
                  params.append("doctor", doctor);
                  // console.log("here " , params , patientSelect);
                  // return

                  window.location.href = `/patients/add-patient-appointment/?${params.toString()}`

              });
                        
          }
        },
    });

      calendar.render();
    });