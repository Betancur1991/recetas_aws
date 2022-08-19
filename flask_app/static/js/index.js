var formlogin=document.getElementById('formlogin');

formlogin.onsubmit= function(event) {
    event.preventDefault();

    var formulario= new FormData(formlogin);

    fetch("/login",{method: 'POST', body: formulario})
        .then(response => response.json())
        .then(data => {
            console.log(data)

            if(data.message=="correcto"){
                window.location.href="/dashboard"
            }

            var mensajeAlerta = document.getElementById('mensajeAlerta');
            mensajeAlerta.innerText = data.message;
            mensajeAlerta.classList.add('alert')
            mensajeAlerta.classList.add('alert-danger')

        });
}