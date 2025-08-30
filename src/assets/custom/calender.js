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

          console.log("Fetchinfo " , fetchInfo) ;

          $.ajax({
            url : `${GET_BASE_URL}/api/v1/patients` ,
            type :"GET" ,
            data : {
              start: fetchInfo.startStr ,
              end: fetchInfo.endStr ,
            } ,
          success: (data) => {
            // console.log("getdata", data);

            let events = [];

            data.forEach(patient => {
              patient.appointment_patient.forEach(appt => {
            
                let start = `${appt.appdate}T${appt.apptime}`;
        
                let endTime = new Date(start);
                endTime.setMinutes(endTime.getMinutes() + 30);
                events.push({
                  title: patient.firstname ,
                  start: start,
                  end: endTime.toISOString(),
                  backgroundColor: appt.status === "0" ? "green" : "lightblue",
                  extendedProps: {
                    appointment : appt.id ,
                    patientid : patient.patient ,
                    patient: patient.firstname + " " + patient.lastname,
                    status: appt.status
                  }
                });
              });
            });

            // console.log("Getevents " , events)
            successCallback(events);
          }
          })
        },

        eventDidMount: function(info) {
          // make event container a clipping context
          info.el.style.position = 'relative';
          info.el.style.overflow = 'hidden';

          let getAppointmentId = info.event.extendedProps.appointment;

          const main = info.el.querySelector('.fc-event-main');
          if (main) main.style.paddingRight = '56px';

          // icon wrapper
          const wrapper = document.createElement('div');
          wrapper.style.gap = '0.2rem';

          // edit button
          const editBtn = document.createElement('button');
          editBtn.className = 'fc-event-edit';
          editBtn.title = 'Edit'
          const editIcon = document.createElement('i');
          editIcon.className = 'bx bx-edit-alt';
          editBtn.appendChild(editIcon);
          editBtn.setAttribute('data-id', info.event.id);

          

          editBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            // alert('Edit clicked for appointment ID: ' + getAppointmentId);
            window.location.href = `/patients/edit-patient-appointment?appointment=${getAppointmentId}`
          });

          // cancel button
          const cancelBtn = document.createElement('button');
          cancelBtn.className = 'fc-event-cancel';
          cancelBtn.title = 'Cancel'
          const cancelIcon = document.createElement('i');
          cancelIcon.className = 'bx bx-undo';
          cancelBtn.appendChild(cancelIcon);
          cancelBtn.setAttribute('data-id', info.event.id);

          cancelBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            alert('Cancel clicked for appointment ID: ' + getAppointmentId);
          });

          // add both to wrapper
          wrapper.appendChild(editBtn);
          wrapper.appendChild(cancelBtn);

          // append wrapper to event
          info.el.appendChild(wrapper);
        },

        dateClick: (info)=>{
            // console.log("getinfof" , info)
            let clinicID =  $(document).find('#clinic').val();
            let doctorId =  $(document).find('#doctor').val()
            $('#slotModal').data('dateslot' , info.dateStr).modal('show');
            $('#slotModal').data('clinic' , clinicID);
            $('#slotModal').data('doctor' , doctorId)


            $('#slotModal').on('click' , '#confirmSlot' , (e)=>{
                let date = $("#slotModal").data("dateslot");    

                let clinicid =  $("#slotModal").data("clinic");
                let doctor =  $("#slotModal").data("doctor");

                if(!clinicid){
                  $('#slotModal').modal('hide');
                    Swal.fire({
                      title: 'Error!',
                      text: 'Please choose clinic',
                      icon: 'error',
                      confirmButtonText: 'OK'
                    });
                    return
                }


                if (!doctor){
                  $('#slotModal').modal('hide');
                  Swal.fire({
                      title: 'Error!',
                      text: 'Please choose doctor',
                      icon: 'error',
                      confirmButtonText: 'OK'
                  })

                  return
                }

                let getdate =  date.split('T')[0]
                let gettime =  date.split('T')[1].slice(0,5)


                window.location.href = `/patients/add-patient?date=${getdate}&time=${gettime}&clinicid=${clinicid}&doctor=${doctor}`

            });
        },
    });

      calendar.render();
    });