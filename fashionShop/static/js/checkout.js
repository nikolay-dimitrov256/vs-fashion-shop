window.addEventListener("DOMContentLoaded", initShippingForm);

function initShippingForm() {
    // Get elements
    const shippingMethodSelectElement = document.getElementById('id_shipping_method');
    const townInputElement = document.getElementById('id_town');

    // Hide office fields
    hideOfficeFields();

    // Init shipping method
    shippingMethodSelectElement.addEventListener('change', initShippingMethod)

    // Init town field
    townInputElement.addEventListener('input', (e) => initTownField(townInputElement.value.trim()));
}

function initShippingMethod() {
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

    if(addressDivElement) {
        shippingFormElement.append(addressDivElement);
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

    if (!query || query.length < 2) {
        suggestionsUlElement.innerHTML = '';
        suggestionsUlElement.style.display = 'none';
        return;
    }

    const baseUrl = window.location.origin
    const url = `${baseUrl}/api/proxy/speedy/towns/`;

    const params = {
        'language': 'BG',
        'countryId': '100',  // Bulgaria
        'name': query,
    }

    fetch(
        url,
        {
            method: 'POST',
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify(params)
        }
    )
    .then(response => response.json())
    .then(data => makeTownLiElements(data))
    .catch(error => console.log(error));
}

function makeTownLiElements(data) {
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
            populateOfficeOptions();
            suggestionsUlElement.innerHTML = '';
            suggestionsUlElement.style.display = 'none';
            townInputElement.dispatchEvent(new Event('change'));
        });

        return liElement;
    });
    
    suggestionsUlElement.append(...liElements);
}

function populateOfficeOptions() {
    const hiddenInputElement = document.getElementById('town_id');
    
    const baseUrl = window.location.origin
    const url = `${baseUrl}/api/proxy/speedy/offices/`;

    const params = {
        'language': 'BG',
        'countryId': '100',  // Bulgaria
        'name': query,
    }

}