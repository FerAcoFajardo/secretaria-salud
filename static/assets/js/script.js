// import Swal from '../node_modules/sweetalert2';

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


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
            let curp = document.querySelector('#curp-input').value;
            let formdata = new FormData();

            formdata.append("curp", curp);
            formdata.append("huella", huella);


            // console.log(formdata);

            let requestOptions = {
                method: 'POST',
                body: formdata,
                headers: { 'X-CSRFToken': csrftoken },
                redirect: 'follow',
                csrfmiddlewaretoken: '{{ csrf_token() }}'
            };

            // console.log(requestOptions)
            return fetch(`http://localhost:8000/get-info/`, requestOptions)
                .then(response => response.json())
                .then(data => {
                    console.log(data);
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
                            text: `Paciente ${data.paciente.nombre}`,
                            // imageUrl: 'https://res.cloudinary.com/twenty20/private_images/t_standard-fit/v1618540156/photosp/371b7901-4b1f-453c-b3fb-ae40efb8f153/371b7901-4b1f-453c-b3fb-ae40efb8f153.jpg',
                            confirmButtonColor: '#48cae4',
                        })
                    })

                    displayResults(data);
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

    document.getElementById('patientName').append(document.createElement('p').innerHTML = `${response.paciente.nombre}`);
    document.getElementById('datosGenerales').append(document.createElement('p').innerHTML = `${response.paciente.sexo} - ${response.paciente.fecha_nacimiento}`);
    document.getElementById('curp').append(document.createElement('p').innerHTML = `Curp - ${response.paciente.curp}`);
    await manageFiles(response.files);

    document.getElementById('pacienteArea').style.display = 'block';
    document.getElementById('zona2').style.display = 'block';
    document.getElementById('zona3').style.display = 'block';
    document.getElementById('zona4').style.display = 'block';

    let lista_consultas = document.querySelector("#lista-contultas");

    // Iterate over consultas
    for (let i = 0; i < response.consultas.length; i++) {
        let consulta = response.consultas[i];
        // Create li element
        let li = document.createElement('li');
        // Add class to li element
        li.setAttribute('class', 'flex flex-col items-center space-y-2');

        // Create span element
        let span = document.createElement('span');
        // Add class to span element
        span.setAttribute('class', 'block bg-white p-4 rounded-full');
        // Add onClick event to span element
        // span.onclick = downloadFile;
        // span.id = 'downloadFile';
        // Add href attribute to span element
        span.setAttribute('href', '#');

        // Create img element
        let img = document.createElement('img');
        // Add class to img element
        img.classList.add('w-16');
        // Add src attribute to img element
        img.setAttribute('src', '../static/assets/img/medical-history.png');

        // Append image to first span
        span.appendChild(img);

        // Create span element
        let span2 = document.createElement('span');
        // Add class to span element
        span2.setAttribute('class', 'text-xs text-gray-500');

        // Append texto to span
        span2.appendChild(document.createTextNode(consulta.comentarios_consulta));

        // Append spand to li
        li.appendChild(span);
        li.appendChild(span2);
        
        // Append li to ul
        lista_consultas.appendChild(li);
    }
    
    
    let lista_laboratorios = document.querySelector("#lista-laboratorios");

    // Iterate over consultas
    for (let i = 0; i < response.laboratorios.length; i++) {
        let laboratorio = response.laboratorios[i];
        // Create li element
        let li = document.createElement('li');
        // Add class to li element
        li.setAttribute('class', 'flex flex-col items-center space-y-2');

        // Create span element
        let span = document.createElement('span');
        // Add class to span element
        span.setAttribute('class', 'block bg-white p-4 rounded-full');
        // Add onClick event to span element
        span.onclick = downloadFile;
        span.id = 'downloadFile';
        // Add href attribute to span element
        span.setAttribute('href', '#');

        // Create img element
        let img = document.createElement('img');
        // Add class to img element
        img.classList.add('w-16');
        // Add src attribute to img element
        img.setAttribute('src', '../static/assets/img/research.png');

        // Append image to first span
        span.appendChild(img);

        // Create span element
        let span2 = document.createElement('span');
        // Add class to span element
        span2.setAttribute('class', 'text-xs text-gray-500');

        // Append texto to span
        span2.appendChild(document.createTextNode(laboratorio.comentarios_laboratorio));

        // Append spand to li
        li.appendChild(span);
        li.appendChild(span2);
        
        // Append li to ul
        lista_laboratorios.appendChild(li);
    }

}

async function manageFiles(files) {

}

