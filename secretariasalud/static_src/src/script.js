// import Swal from '../node_modules/sweetalert2';


const giveAccess = () => {
    let show = false;
    event.preventDefault();
    swal.fire({
        title: 'Ingresa la huella del paciente',
        input: 'text',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Confirmar',
        confirmButtonColor: '#38bdf8',
        showLoaderOnConfirm: true,
        // preConfirm: (login) => {
        //   return fetch(`//api.github.com/users/${login}`)
        //     .then(response => {
        //       if (!response.ok) {
        //         throw new Error(response.statusText)
        //       }
        //       return response.json()
        //     })
        //     .catch(error => {
        //       Swal.showValidationMessage(
        //         `Request failed: ${error}`
        //       )
        //     })
        // },
        allowOutsideClick: () => !Swal.isLoading()
    }).then(async () => {
        let timerInterval
        await Swal.fire({
            title: 'Procesando Huella',
            timer: 2000,
            timerProgressBar: true,
            didOpen: () => {
                Swal.showLoading()
                const b = Swal.getHtmlContainer().querySelector('b')
                timerInterval = setInterval(() => {
                    b.textContent = Swal.getTimerLeft()
                }, 100)
            },
            willClose: () => {
                clearInterval(timerInterval)
            }
        })
    }).then(() => {
        Swal.fire({
            title: `Acceso Permitido`,
            text: 'Paciente Joaquin Guzman',
            imageUrl: '../assets/joaquin.png',
            confirmButtonColor: '#48cae4',
        })
        document.getElementById('pacienteArea').style.display = 'block';
        document.getElementById('zona2').style.display = 'block';
        document.getElementById('zona3').style.display = 'block';
        document.getElementById('zona4').style.display = 'block';


    })
}

const downloadFile = () => {
    event.preventDefault();
    Swal.fire({
        title: 'Seguro que quiere descargar este archivo?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#48cae4',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si, descargar',
        cancelButtonText: 'Cancelar',
      }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                position: 'top-end',
                icon: 'success',
                title: 'Descargado con exito.',
                showConfirmButton: false,
                timer: 1500
              })
        }
      })
}