document.addEventListener('DOMContentLoaded', () => {
    const loginLink = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-link');
    const sectorInfoUser = document.getElementById('info-of-user');
    const sectorPlacesUser = document.getElementById('places-of-user');
    const fullNombreUser = document.getElementById('full-name-user');
    let currentEditingPlaceId = null;

    /*##########################################################
    -------------- LOGICA DE AUTENTICACION ---------------------
    ############################################################*/

    // #-#-# función para verificar la autenticación #-#-#
    async function checkAuthentication() {
        const accessToken = localStorage.getItem('access_token');
        const userId = localStorage.getItem('user_id');

        if (accessToken && userId) {
            if (loginLink) {
                loginLink.style.display = 'none'; // ocultamos el enlace de login si el usuario ya está autenticado
            }
            if (logoutButton) {
                logoutButton.style.display = 'block';
                logoutButton.onclick = () => { // detectamos el cierre de sesión
                    localStorage.removeItem('access_token');
                    localStorage.removeItem('user_id');      // eliminamos el token de acceso y el id del almacenamiento local
                    window.location.reload();               // redirigimos al usuario a la página principal
                };
            }
            await renderDetails(userId);
            opcionesFooter();
        } else {
            if (loginLink) {
                loginLink.style.display = 'block'; // mostramos el enlace de login si el usuario no está autenticado
            }
            if (logoutButton) {
                logoutButton.style.display = 'none'; // ocultamos el botón de logout si el usuario no está autenticado
            }
            if (fullNombreUser) { // verificamos si el elemento existe
                fullNombreUser.innerText = 'Por favor, inicie sesión para ver su perfil.';
            }
            if (sectorInfoUser) {
                 sectorInfoUser.innerHTML = ''; // Limpia el contenido si hay algo previo
            }
            if (sectorPlacesUser) {
                sectorPlacesUser.innerHTML = ''; // Limpia el contenido si hay algo previo
            }
        }
    }

    /*-#-#-#-#-#- LOGICA PARA MOSTRAR LA INFORMACION DEL USER -#-#-#-#-#-
    ##################################################################### */
    async function fetchDataUser(userId) {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            console.error('No se encontró el token de acceso para fetchDataUser.');
            checkAuthentication(); // Forzar una re-verificación de autenticación
            return null;
        }
        const url = `http://localhost:5000/api/v1/users/${userId}`;
        const requestOptions = { // creamos un header general
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        };
        try {
            const response = await fetch(url, requestOptions);
            if (!response.ok) {
                // manejamos la no autorizacion del cliente
                if (response.status === 401) {
                    console.error('Unauthorized access - invalid token');
                    localStorage.removeItem('access_token'); // eliminamos el token de acceso
                    localStorage.removeItem('user_id'); // eliminamos el id del usuario
                    checkAuthentication(); // volvemos a verificar la autenticación
                    return null;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data; // devolvemos los datos del usuario
        } catch (error) {
            console.error('Error fetching place details:', error);
            //mostramos un mensaje de error en vez del nombre del usuario
            if (fullNombreUser) {
                fullNombreUser.innerText = 'Error al cargar los datos.';
            }
            return null; // devolvemos null en caso de error
        }
    }
    async function renderDetails(userId) {
        const user = await fetchDataUser(userId);

        if (user === null) {
            if (fullNombreUser) {
                fullNombreUser.innerText = 'No se pudo cargar la información del perfil.';
            }
            return;
        }
        if (fullNombreUser) {
            fullNombreUser.innerText = `${user.first_name} ${user.last_name}`; // mostramos el nombre en el header
            sectorInfoUser.innerHTML = `
                                    <fieldset><legend><b>First Name: </b></legend><p class="data-api">${user.first_name}</p></fieldset>
                                    <br>
                                    <fieldset><legend><b>Last Name: </b></legend><p class="data-api">${user.last_name}</p></fieldset>
                                    <br>
                                    <fieldset><legend><b>Email: </b></legend><p class="data-api">${user.email}</p></fieldset>
                                `;
        }
        renderPlacesUser(userId);
    }
    /*   -#-#-#-#- LOGICA PARA MOSTRAR LOS PLACES DEL USUARIO -#-#-#-#- 
    ###################################################################*/
    async function renderPlacesUser(userId) {
        const accessToken = localStorage.getItem('access_token');
        if (!accessToken) {
            sectorPlacesUser.innerHTML = '<p>No tienes acceso para ver esta información.</p>';
            return;
        }
        const url = `http://localhost:5000/api/v1/users/${userId}/places`;
        const requestOptions = {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        };

        try {
            const response = await fetch(url, requestOptions);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }

            const places = await response.json();
            console.log("Datos de lugares recibidos del servidor:", places);
            
            // Limpiamos el contenido previo y añadimos el título
            sectorPlacesUser.innerHTML = `<h4>Tus Places</h4>`;

            if (places && places.length > 0) {
                const placesHtml = places.map(place => `
                    <div class="place-card">
                        <h5>${place.title}</h5>
                        <p>Precio por noche: $${place.price}</p>
                        <a class="link-Place" href="/places?id=${place.id}" data-place-id="${place.id}">Ver detalles</a>
                    </div>
                `).join('');
                sectorPlacesUser.innerHTML += placesHtml;
            } else {
                sectorPlacesUser.innerHTML += '<p>No tienes Places publicados aún.</p>';
            }

        } catch (error) {
            console.error('Error al obtener los places del usuario:', error);
            sectorPlacesUser.innerHTML = `<p class="error-message">Error al cargar tus lugares: ${error.message}</p>`;
        }
    }

    /*-#-#-#-#-# LOGICA PARA LAS ACCIONES DEL FOOTER -#-#-#-#-#-
    ############################################################ */
    async function opcionesFooter() {
        const botonEditar = document.getElementById('botonEditar');
        const dialogEditar = document.getElementById('dialogoEditar');
        const cerrarDialogoEditar = document.getElementById('cerrarDialogoEditar');
        const formActualizarPerfil = document.getElementById('form-update-perfil');
        const botonActualizarPlace = document.getElementById('actualizarPlace');
        const dialogoActualizarPlace = document.getElementById('dialogoActualizarPlace');
        const cerrarFuncionActualizar = document.getElementById('cerrarFuncionActualizar');
        const cerrarDialogPlace = document.getElementById('cerrarDialogoPlace');
        const overlay = document.getElementById('overlay');
        const addAmenitiesToPlace = document.getElementById('addAmenitiesToPlace');
        if (addAmenitiesToPlace) {
            addAmenitiesToPlace.addEventListener('click', async () => {
                // Llama a la función de asociación con el ID almacenado
                const accessToken = localStorage.getItem('access_token');
                if (currentEditingPlaceId) {
                    await asociateAmenityToPlace(accessToken, currentEditingPlaceId);
                } else {
                    alert('No se pudo encontrar el Place ID.');
                }
            });
        }

        let editing = false;

        /*-#-#-#-#-#- EDITAR INFO USUARIO -#-#-#-#-#-
        --------------------------------------------- */
        botonEditar.addEventListener('click', () => {
            dialogEditar.showModal();
        });
        cerrarDialogoEditar.addEventListener('click', () => {
            dialogEditar.close();
        });
        formActualizarPerfil.addEventListener('submit', async (event) => {
            event.preventDefault();
            const accessToken = localStorage.getItem('access_token');
            const userId = localStorage.getItem('user_id');
            const formData = new FormData(formActualizarPerfil);
            const datosDelForm = Object.fromEntries(formData.entries());
            const datosParaEnviar = {};

            for (const key in datosDelForm) {
                const value = datosDelForm[key];
                if (value !== '' && value !== null && value !== undefined) {
                    datosParaEnviar[key] = value;
                }
            }
            try {
                const urlUpdate = `http://127.0.0.1:5000/api/v1/users/${userId}`;
                const response = await fetch(urlUpdate, {
                    method: 'PUT', // para enviar los datos
                    headers: {
                        'Content-Type': 'application/json', // para enviarlos en JSON
                        'Authorization': `Bearer ${accessToken}`
                    },
                    body: JSON.stringify(datosParaEnviar)
                });
                const data = await response.json(); //se parsea la respuesta json del server
                if (response.ok){
                    console.log('update exitoso:', data);
                    alert('¡Update exitoso!');
                    // se redirige al usuario al index.html
                    dialogEditar.close();
                    await renderDetails(userId);
                } else {
                    console.error('Error en el registro:', data.error);
                    alert(data.error || 'Error desconocido en el registro.');
                    dialogEditar.close();
                }
            } catch (error) {
            // Captura errores de red
            console.error('Error de red o del servidor:', error);
            alert('No se pudo conectar con el servidor. Verifica tu conexión o la URL de la API.');
            dialogEditar.close();
            }
        });

        /*-#-#-#-#-#- LOGICA PARA EDITAR INFO DE PLACES -#-#-#-#-#-
        ------------ Y EFECTO DEL BOTON ACTUALIZAR PLACES ---------
        ------------------------------------------------------------ */
        async function manejoPlaceLinkClick(event) {
            const placeId = event.currentTarget.getAttribute('data-place-id');
            const botonActualizarInfo = document.getElementById('ActualizarDataPlace');

            if (editing) {
                event.preventDefault();
                console.log('Intentando actualizar place');
                dialogoActualizarPlace.showModal();
                currentEditingPlaceId = placeId;
                const placeData = await editarPlaces(placeId);
                if (placeData) {
                    const title = document.getElementById('title').value = placeData.title;
                    const price = document.getElementById('price').value = placeData.price;
                    const description = document.getElementById('description').value = placeData.description;
                    const accessToken = localStorage.getItem('access_token');
                    await addPlaceAmenities(accessToken, placeId);

                }

            } else {
                console.log(`Navegando a los detalles del lugar`);
            }
        };
        async function editarPlaces(place_id){
            const accessToken = localStorage.getItem('access_token');
            if (!accessToken) {
                console.error('No se encontró el token de acceso para fetchDataUser.');
                checkAuthentication(); // Forzar una re-verificación de autenticación
                return null;
        }
            urlPlace = `http://127.0.0.1:5000/api/v1/places/${place_id}`;
            const requestPlaceInfo = {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            };
            try {
                const response = await fetch(urlPlace, requestPlaceInfo);
                if (!response.ok) {
                    throw new Error('No se pudo obtener la información del place.');
                }
                const data = await response.json();
                console.log("Datos del place recibidos:", data);
                return data;
            } catch (error) {
                console.error('Error al obtener la información del place:', error);
                alert('Error al cargar la información del lugar.');
            }

        };
        botonActualizarPlace.addEventListener('click', () => {
            editing = true;
            overlay.style.display = 'block';
            overlay.classList.add('show');
            sectorPlacesUser.style.zIndex = 10;
            sectorPlacesUser.style.backgroundColor = '#fff';
            sectorPlacesUser.style.boxShadow = '#fff 0 0 10px 3px';

            const linkActualizar = document.querySelectorAll('.link-Place');
            linkActualizar.forEach(link => {
                link.textContent = 'Actualizar';
                link.addEventListener('click', manejoPlaceLinkClick); 
            });
        });
        cerrarFuncionActualizar.addEventListener('click', () => {
            editing = false;
            overlay.style.display = 'none';
            sectorPlacesUser.style.zIndex = 2;
            sectorPlacesUser.style.backgroundColor = '#fafafa';
            sectorPlacesUser.style.boxShadow = 'none';
            const linkActualizar = document.querySelectorAll('.link-Place');
            linkActualizar.forEach(link => {
                link.textContent = 'Ver detalles';
                link.href = `/places?id=${link.getAttribute('data-place-id')}`;
                });
        });

        cerrarDialogPlace.addEventListener('click', () => {
            dialogoActualizarPlace.close();
            editing = false;
            overlay.style.display = 'none';
            sectorPlacesUser.style.zIndex = 2;
            sectorPlacesUser.style.backgroundColor = '#fafafa';
            sectorPlacesUser.style.boxShadow = 'none';
            const linkActualizar = document.querySelectorAll('.link-Place');
            linkActualizar.forEach(link => {
                link.textContent = 'Ver detalles';
                link.href = `/places?id=${link.getAttribute('data-place-id')}`;
                })
        });
        // Agrego eventListener para el evento submit
        const formUpdatePlace = document.getElementById('form-update-place');
        formUpdatePlace.addEventListener('submit', async (event) => {
            event.preventDefault(); // evita recargar pagina
            const accessToken = localStorage.getItem('access_token');
            const placeId = currentEditingPlaceId;
            if (!accessToken || !placeId) {
                alert('error: autenticacion o Place');
                return;
            }
            try {
                // Lógica para actualizar los datos del place (título, precio, descripción)
                const formData = new FormData(formUpdatePlace);
                const datosParaEnviar = Object.fromEntries(formData.entries());
                                
                const urlUpdatePlace = `http://127.0.0.1:5000/api/v1/places/${placeId}`;
                const response = await fetch(urlUpdatePlace, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${accessToken}`
                    },
                    body: JSON.stringify(datosParaEnviar)
                });
            
                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.message || 'Error desconocido al actualizar el place.');
                }
            
                console.log('Place actualizado exitosamente.');
                
                // Lógica para actualizar los amenities
                await updatePlaceAmenities(accessToken, placeId);
            
                alert('¡Place y amenities actualizados exitosamente!');
                dialogoActualizarPlace.close();
                await renderPlacesUser(localStorage.getItem('user_id'));
                
            } catch (error) {
                console.error('Error en el proceso de actualización:', error);
                alert(`Error al actualizar: ${error.message}`);
            }
        });

    }
    checkAuthentication();
});


    /* -#-#-#-#- FUNCION PARA AÑADIR LAS AMENITIES AL PLACE -#-#-#-#- 
    ------------------------------------------------------------------*/
    async function addPlaceAmenities(accessToken, place_id) {
        const amenityList = document.getElementById('amenityList');
        const urlAmenities = 'http://127.0.0.1:5000/api/v1/amenities/';
        const requestOptionsGet = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }   // hasta aca capturamos los elementos y preparamos una peticion para la api
        };
        try {
            const response = await fetch(urlAmenities, requestOptionsGet);
            if (!response.ok) { // manejamos la no autorizacion del cliente
                if (response.status === 401) {
                    console.error('Unauthorized access - invalid token');
                    localStorage.removeItem('access_token'); // eliminamos el token de acceso
                    localStorage.removeItem('user_id'); // eliminamos el id del usuario
                    checkAuthentication(); // volvemos a verificar la autenticación
                    return null;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json(); // obtenemos las amenities
            listOfAllAmenities = []; // creamos una lista para guardar los nombre y poder manejar cuando las amenities ya existen
            amenityList.innerHTML = '';
            data.forEach(amenity => { // mostramos cada amenity dinamicamente
                listOfAllAmenities.push(amenity.name.toLowerCase());
                const li = document.createElement('li');
                li.classList.add('lista-items');
                li.innerHTML = `
                        <p>
                            <span>${amenity.name}</span>
                            <input type="checkbox" name="amenitisCreadas" id="${amenity.name}">
                        </p>
                `;
                amenityList.appendChild(li); // las agregamos al sector donde se deben mostrar
            });
        } catch (error) {
            console.error('Error al obtener amenities:', error);
        }
    }

    async function updatePlaceAmenities(accessToken, placeId) {
    try {
        // Obtengo la lista de amenities actualmente asociados
        const urlGetAmenities = `http://127.0.0.1:5000/api/v1/places/${placeId}`;
        const responseGet = await fetch(urlGetAmenities, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${accessToken}` }
        });
        if (!responseGet.ok) {
                throw new Error(`Error al obtener amenities existentes: ${responseGet.status}`);
            }
        const placeData = await responseGet.json();
        const existingAmenities = placeData['amenities'];
        const existingAmenityNames = new Set(existingAmenities.map(amenity => amenity.name));

        // Obtengo la lista de amenities seleccionadas
        const selectedAmenities = new Set();
        document.querySelectorAll('[name="amenitisCreadas"]:checked').forEach(checkbox => {
            selectedAmenities.add(checkbox.id);
        });

        // logica para agregar o eliminar asociacion de amenitis
        const amenitiesToAdd = [...selectedAmenities].filter(name => !existingAmenityNames.has(name));
        const amenitiesToRemove = [...existingAmenityNames].filter(name => !selectedAmenities.has(name));

        const promises = [];
        const urlBase = 'http://127.0.0.1:5000/api/v1/places';

        // peticiones POST para agregar nuevas amenities
        amenitiesToAdd.forEach(name => {
            const url = `${urlBase}/${placeId}/amenities`;
            const promise = fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({'name': name })
            }).then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                            throw new Error(`Error POST al asociar "${name}": ${errorData.message}`);
                    });
                }
                return response.json();
            });
            promises.push(promise);
        });

        // peticiones DELETE para eliminar amenities
        amenitiesToRemove.forEach(name => {
            const url = `${urlBase}/${placeId}/amenities`;
            const promise = fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify({'name': name })
            }).then(response => {
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(`Error DELETE al desasociar "${name}": ${errorData.message}`);
                    });
                }
                // DELETE generalmente no devuelve un cuerpo, por lo que devolvemos un objeto simple
                return { message: 'Desasociación exitosa' };
            });
            promises.push(promise);
        });

        // Espero a que todas las promesas se resuelvan
        await Promise.all(promises);
        console.log('Amenities actualizadas exitosamente.')
        } catch (error) {
            console.error('Error al actualizar amenities:', error);
            throw error;
        }
    }