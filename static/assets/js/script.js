// import Swal from '../node_modules/sweetalert2';


const giveAccess = () => {
    let show = false;
    event.preventDefault();
    swal.fire({
        title: 'Ingresa la huella del paciente',
        input: 'file',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonText: 'Confirmar',
        confirmButtonColor: '#38bdf8',
        showLoaderOnConfirm: true,
        preConfirm: (huella) => {
            // Message from home.html
            let curp = document.getElementById('curp').innerHTML;
            console.log(huella)
            let formdata = new FormData();

            formdata.append("curp", curp);
            formdata.append("huella", huella, "huella.jpg");

            console.log(formdata);

            let requestOptions = {
                method: 'POST',
                body: formdata,
                redirect: 'follow'
            };

            console.log(requestOptions)
            return fetch(`https://secretaria-salud.herokuapp.com/get-info/`, requestOptions)
                .then(response => {
                    console.log(response);
                    if (!response.ok) {
                        throw new Error(response.statusText)
                    }
                    let timerInterval
                    Swal.fire({
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
                    }).then(() => {
                        Swal.fire({
                            title: `Acceso Permitido`,
                            text: 'Paciente Joaquin Guzman',
                            // imageUrl: 'https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1618540156/photosp/371b7901-4b1f-453c-b3fb-ae40efb8f153/371b7901-4b1f-453c-b3fb-ae40efb8f153.jpg',
                            confirmButtonColor: '#48cae4',
                        })
                    })

                    displayResults(response);
                })
                .catch(error => {
                    Swal.showValidationMessage(
                        `Request failed: ${error}`
                    )
                })
        },
        allowOutsideClick: () => !Swal.isLoading()
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

async function displayResults(response) {
    document.getElementById('patientName').appendChild(document.createElement('p').innerHTML = `${response.name}`);
    document.getElementById('datosGenerales').appendChild(document.createElement('p').innerHTML = `${response.sexo} - ${reponse.edad}`);
    document.getElementById('curp').appendChild(document.createElement('p').innerHTML = `Curp - ${response.curp}`);
    await manageFiles(response.files);

    document.getElementById('pacienteArea').style.display = 'block';
    document.getElementById('zona2').style.display = 'block';
    document.getElementById('zona3').style.display = 'block';
    document.getElementById('zona4').style.display = 'block';
}

async function manageFiles(files) {

}

