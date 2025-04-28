window.addEventListener("DOMContentLoaded", initShippingForm);

function initShippingForm() {
    // Get elements
    const shippingMethodSelectElement = document.getElementById('id_shipping_method');
    const townInputElement = document.getElementById('id_town');

    // Hide office fields
    const shippingMethod = shippingMethodSelectElement.value;
    if (!['spof', 'ecof'].includes(shippingMethod)) {
        hideOfficeFields();
        
        if (['spad', 'ecad'].includes(shippingMethod)) {
            showAddressFields();
        }
    }
    

    // Init shipping method
    shippingMethodSelectElement.addEventListener('change', initShippingMethod);

    // Init town field
    townInputElement.addEventListener('input', (e) => initTownField(townInputElement.value.trim()));
}

function initShippingMethod() {
    // Clear fields
    const townInputElement = document.getElementById('id_town');
    const officeSelectElement = document.getElementById('id_office');
    const hiddenInputElement = document.getElementById('town_id');
    townInputElement.value = '';
    officeSelectElement.innerHTML = '';
    officeSelectElement.value = '';
    hiddenInputElement.value = '';

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
        document.getElementById('town_id').value = '';
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
    .then(data => makeSpeedyTownLiElements(data))
    .catch(error => console.error(error));
}

function fetchEcontTowns(query) {
    const baseUrl = window.location.origin;
    const url = `${baseUrl}/api/proxy/econt/towns/?name=${query}`;

    fetch(
        url,
        {
            method: 'GET',
            headers: {'Content-type': 'application/json'}
        }
    )
    .then(response => response.json())
    .then(data => makeEcontTownLiElements(data))
    .catch(error => console.error(error));
}

function makeSpeedyTownLiElements(data) {
    const towns = data.sites;
    const suggestionsUlElement = document.getElementById('town-suggestions');
    const townInputElement = document.getElementById('id_town');
    const hiddenInputElement = document.getElementById('town_id');

    suggestionsUlElement.innerHTML = '';
    suggestionsUlElement.style.display = 'block';

    const liElements = towns.map((town) => {
        const liElement = document.createElement('li');
        liElement.textContent = `${town.postCode}-${town.name}-${town.region}`;
        liElement.style.cursor = 'pointer';
        liElement.addEventListener('click', () => {
            townInputElement.value = `${town.postCode}-${town.name}`;
            hiddenInputElement.value = town.id;
            populateSpeedyOfficeOptions();
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
    const hiddenInputElement = document.getElementById('town_id');

    suggestionsUlElement.innerHTML = '';
    suggestionsUlElement.style.display = 'block';

    const liElements = data.map((town) => {
        const liElement = document.createElement('li');
        liElement.textContent = `${town.postCode}-${town.name}-${town.regionName}`;
        liElement.style.cursor = 'pointer';
        liElement.addEventListener('click', () => {
            townInputElement.value = `${town.postCode}-${town.name}`;
            hiddenInputElement.value = town.id;
            populateEcontOfficeOptions();
            suggestionsUlElement.innerHTML = '';
            suggestionsUlElement.style.display = 'none';
            townInputElement.dispatchEvent(new Event('change'));
        });

        return liElement;
    });
    
    suggestionsUlElement.append(...liElements);
}

function populateSpeedyOfficeOptions() {
    const hiddenInputElement = document.getElementById('town_id');
    const siteId = hiddenInputElement.value;
    
    if(!siteId) {
        return;
    }
    
    const baseUrl = window.location.origin;
    const url = `${baseUrl}/api/proxy/speedy/offices/`;

    const params = {
        'language': 'BG',
        'countryId': '100',  // Bulgaria
        'siteId': siteId,
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

function populateEcontOfficeOptions() {
    const hiddenInputElement = document.getElementById('town_id');
    const townId = hiddenInputElement.value;
    
    if(!townId) {
        return;
    }
    
    const baseUrl = window.location.origin;
    const url = `${baseUrl}/api/proxy/econt/offices/`;

    const params = {
        'cityID': townId,
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
    .then(data => makeEcontOfficeOptions(data))
    .catch(error => console.error(error));
}

function makeSpeedyOfficeOptions(data) {
    const officeSelectElement = document.getElementById('id_office');

    const officeOptionElements = data.offices.map(office => {
        const optionElement = document.createElement('option');
        const optionText = `${office.id}, ${office.name}, ${office.address.localAddressString}`;
        optionElement.textContent = optionText;
        optionElement.value = optionText;

        return optionElement;
    });

    officeSelectElement.innerHTML = '';
    officeSelectElement.append(...officeOptionElements);
}

function makeEcontOfficeOptions(data) {
    const officeSelectElement = document.getElementById('id_office');

    const officeOptionElements = data.offices.map(office => {
        const optionElement = document.createElement('option');
        const optionText = `${office.id}, ${office.name}, ${office.address.fullAddress}`;
        optionElement.textContent = optionText;
        optionElement.value = optionText;

        return optionElement;
    });

    officeSelectElement.innerHTML = '';
    officeSelectElement.append(...officeOptionElements);
}