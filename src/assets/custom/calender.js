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
        slotDuration: "00:15:00",  //! 30 min slots
        slotLabelInterval: "00:30:00",
        events: [
          {
            title: 'Vimla Kumari\nLAB TEST (Ankit Shah)\nDuration: 20 mins\nPaid',
            start: '2025-08-25T10:00:00',
            end: '2025-08-25T10:20:00',
            backgroundColor: 'lightgreen', // status: 'Pending'
            extendedProps: {
              patient: 'Vimla Kumari',
              status: 'Pending'
            }
          },
        ],
        dateClick: (info)=>{
            // console.log("getinfof" , info)
            let clinicID =  $(document).find('#clinic').val();
            let doctorId =  $(document).find('#doctor').val()
            $('#slotModal').data('dateslot' , info.dateStr).modal('show');
            $('#slotModal').data('clinic' , clinicID);
            $('#slotModal').data('doctor' , doctorId)
            // console.log('doctorId' , doctorId)
            // return
            

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

                // console.log("geta " , doctor)

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
                // console.log(date);
                // return  false

                window.location.href = `/patients/add-patient?date=${getdate}&time=${gettime}&clinicid=${clinicid}&doctor=${doctor}`

            });
        },
    });

      calendar.render();
    });