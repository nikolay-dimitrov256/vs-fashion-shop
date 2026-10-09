window.addEventListener("DOMContentLoaded", initShippingForm);

function initShippingForm() {
    // Get elements
    const shippingMethodSelectElement = document.getElementById('id_shipping_method');
    const townInputElement = document.getElementById('id_town');

    // Hide/show fields
    const shippingMethod = shippingMethodSelectElement.value;
    if (['spad', 'ecad'].includes(shippingMethod)) {
        hideOfficeFields();
        showAddressFields();
    } else if (['spof', 'ecof'].includes(shippingMethod)) {
        hideAddressFields();
        showOfficeFields();
    } else {
        // fallback for unknown values
        hideOfficeFields();
        hideAddressFields();
    }

    // Clear the town input, so the user types in his town again
    townInputElement.value = '';

    // Init shipping method
    shippingMethodSelectElement.addEventListener('change', initShippingMethod);

    // Init town field
    townInputElement.addEventListener('input', (e) => initTownField(townInputElement.value.trim()));
}

function initShippingMethod() {
    // Clear fields
    const townInputElement = document.getElementById('id_town');
    const officeSelectElement = document.getElementById('id_office');
    townInputElement.value = '';
    officeSelectElement.innerHTML = '';
    officeSelectElement.value = '';

    // Get elements
    const shippingMethodSelectElement = document.getElementById('id_shipping_method');
    const addressValues = ['spad', 'ecad'];
    const officeValues = ['spof', 'ecof'];
    const shippingMethod = shippingMethodSelectElement.value;

    if(addressValues.includes(shippingMethod)) { // The method is address

        hideOfficeFields();

        showAddressFields();

    } else if (officeValues.includes(shippingMethod)) { // The method is office

        hideAddressFields();

        showOfficeFields();
    }
}

function hideOfficeFields() {
    const townDivElement = document.getElementById('div_id_town');
    const officeDivElement = document.getElementById('div_id_office');
    const officeElements = [townDivElement, officeDivElement];

    officeElements.forEach(element => {
        element.style.display = 'none';
    });
}

function showOfficeFields() {
    const townDivElement = document.getElementById('div_id_town');
    const officeDivElement = document.getElementById('div_id_office');
    const officeElements = [townDivElement, officeDivElement];

    officeElements.forEach(element => {
        element.style.display = 'block';
    })
}

function showAddressFields() {
    const shippingFormElement = document.getElementById('shipping-form');
    const hiddenDivElement = document.getElementById('hidden-fields');
    const addressDivElement = hiddenDivElement.querySelector('#address-fields');
    const submitButtonElement = shippingFormElement.querySelector('button');
    const commentDivElement = document.getElementById('div_id_comment');

    if(addressDivElement) {
        shippingFormElement.append(addressDivElement);
        shippingFormElement.append(commentDivElement);
        shippingFormElement.append(submitButtonElement);
    }
}

function hideAddressFields() {
    const shippingFormElement = document.getElementById('shipping-form');
    const hiddenDivElement = document.getElementById('hidden-fields');
    const addressDivElement = shippingFormElement.querySelector('#address-fields');

    if(addressDivElement) {
        hiddenDivElement.append(addressDivElement);
    }
}

function initTownField(query) {
    const suggestionsUlElement = document.getElementById('town-suggestions');
    const shippingMethodSelectElement = document.getElementById('id_shipping_method');
    const shippingMethod = shippingMethodSelectElement.value;

    if (!query || query.length < 2) {
        suggestionsUlElement.innerHTML = '';
        suggestionsUlElement.style.display = 'none';
        document.getElementById('id_office').innerHTML = '';
        return;
    }

    if (shippingMethod == 'spof') {
        fetchSpeedyTowns(query);
    } else if (shippingMethod == 'ecof') {
        fetchEcontTowns(query);
    }
    
}

function fetchSpeedyTowns(query) {
    const baseUrl = window.location.origin;
    const url = `${baseUrl}/api/proxy/speedy/towns/`;

    const params = {
        // 'language': 'BG',
        // 'countryId': '100',  // Bulgaria
        'name': query,
    };

    fetch(
        url,
        {
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify(params)
        }
    )
    .then(response => response.json())
    .then(data => {
        makeSpeedyTownLiElements(data.sites);
        populateSpeedyOfficeOptions(data.sites.map(town => town.id));
    })
    .catch(error => console.error(error));
}

function fetchEcontTowns(query) {
    const params = new URLSearchParams({
        name: query
    });

    const baseUrl = window.location.origin;
    const url = `${baseUrl}/api/proxy/econt/towns/?${params}`;

    fetch(
        url,
        {
            method: 'GET',
            headers: {'Content-type': 'application/json'}
        }
    )
    .then(response => response.json())
    .then(data => {
        const normalizedQuery = query.trim().toLowerCase();
        const exactTowns = data.filter(town => town.name.trim().toLowerCase() === normalizedQuery);
        
        if (exactTowns.length) {
            populateEcontOfficeOptions(exactTowns.map(town => town.id));
        }

        makeEcontTownLiElements(data);
    })
    .catch(error => console.error(error));
}

function makeSpeedyTownLiElements(towns) {
    const suggestionsUlElement = document.getElementById('town-suggestions');
    const townInputElement = document.getElementById('id_town');

    suggestionsUlElement.innerHTML = '';
    suggestionsUlElement.style.display = 'block';

    const liElements = towns.map((town) => {
        const liElement = document.createElement('li');
        liElement.textContent = `${town.postCode}-${town.name}-${town.region}`;
        liElement.style.cursor = 'pointer';
        liElement.addEventListener('click', () => {
            townInputElement.value = `${town.postCode}-${town.name}`;
            populateSpeedyOfficeOptions([town.id]);
            suggestionsUlElement.innerHTML = '';
            suggestionsUlElement.style.display = 'none';
            townInputElement.dispatchEvent(new Event('change'));
        });

        return liElement;
    });
    
    suggestionsUlElement.append(...liElements);
}

function makeEcontTownLiElements(data) {
    const suggestionsUlElement = document.getElementById('town-suggestions');
    const townInputElement = document.getElementById('id_town');

    suggestionsUlElement.innerHTML = '';
    suggestionsUlElement.style.display = 'block';

    const liElements = data.map((town) => {
        const liElement = document.createElement('li');
        liElement.textContent = `${town.postCode}-${town.name}-${town.regionName}`;
        liElement.style.cursor = 'pointer';
        liElement.addEventListener('click', () => {
            townInputElement.value = `${town.postCode}-${town.name}`;
            populateEcontOfficeOptions([town.id]);
            suggestionsUlElement.innerHTML = '';
            suggestionsUlElement.style.display = 'none';
            townInputElement.dispatchEvent(new Event('change'));
        });

        return liElement;
    });
    
    suggestionsUlElement.append(...liElements);
}

function populateSpeedyOfficeOptions(townIds) {
    const officeSelectElement = document.getElementById('id_office');
    officeSelectElement.innerHTML = '';
    
    if(townIds.length === 0) {
        return;
    }
    
    const baseUrl = window.location.origin;
    const url = `${baseUrl}/api/proxy/speedy/offices/`;

    for (let townId of townIds) {
        const params = {
            'language': 'BG',
            'countryId': '100',  // Bulgaria
            'siteId': townId,
        };

        fetch(
            url,
            {
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(params)
            }
        )
        .then(response => response.json())
        .then(data => makeSpeedyOfficeOptions(data))
        .catch(error => console.error(error));
    }
    
}

function populateEcontOfficeOptions(townIds) {
    const officeSelectElement = document.getElementById('id_office');
    officeSelectElement.innerHTML = '';
    
    if(townIds.length === 0) {
        return;
    }
    
    const baseUrl = window.location.origin;
    const url = `${baseUrl}/api/proxy/econt/offices/`;

    const requests = townIds.map(townId => {
        const params = {
            'cityID': townId,
        };

        return fetch(
            url,
            {
                method: 'POST',
                headers: {'Content-type': 'application/json'},
                body: JSON.stringify(params)
            }
        )
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            return response.json();
        })
    });

    Promise.allSettled(requests)
    .then(results => {
        const offices = results
                            .filter(result => result.status === 'fulfilled')
                            .flatMap(result => result.value)
                            .flatMap(town => town.offices);
        console.log(offices)
        makeEcontOfficeOptions(offices);
    })
    .catch(error => console.error(error));
}

function makeSpeedyOfficeOptions(data) {
    if (data.offices.length === 0) {
        return;
    }
    
    const officeSelectElement = document.getElementById('id_office');

    const officeOptionElements = data.offices.map(office => {
        const optionElement = document.createElement('option');
        const optionText = `${office.id}, ${office.name}, ${office.address.localAddressString}`;
        optionElement.textContent = optionText;
        optionElement.value = optionText;

        return optionElement;
    });

    officeSelectElement.append(...officeOptionElements);
}

function makeEcontOfficeOptions(offices) {
    if (offices.length === 0) {
        return;
    }

    const officeSelectElement = document.getElementById('id_office');

    const officeOptionElements = offices.map(office => {
        const optionElement = document.createElement('option');
        const optionText = `${office.id}, ${office.name}, ${office.address.fullAddress}`;
        optionElement.textContent = optionText;
        optionElement.value = optionText;

        return optionElement;
    });

    officeSelectElement.append(...officeOptionElements);
}