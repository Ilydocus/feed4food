function addItem() {
    const template = document.getElementById('form-template').textContent;
    const container = document.getElementById('form-container');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const formCount = parseInt(totalForms.value, 10);
    const newFormRow = document.createElement('div');

    newFormRow.class = `row`;
    newFormRow.innerHTML = template;

    // Append the new row and increment TOTAL_FORMS
    container.appendChild(newFormRow);
    totalForms.value = formCount + 1;
    enableSearchableDropdown();
}

function enableSearchableDropdown() {
    $(document).ready(function() {
        $('[name="item"]').select2();
    });
}

function updateUnit(itemSelect) {
    // Get the selected option
    const selectedUnit = itemSelect.options[itemSelect.selectedIndex].getAttribute('data-unit');

    const row = itemSelect.closest('.row');
    const unitDisplay = row.querySelector('.unit-display');
    unitDisplay.textContent = selectedUnit;
    const unitDisplay2 = row.querySelector('.unit-display2');
    unitDisplay2.textContent = selectedUnit;
}


function deleteRow(button) {
    const container = document.getElementById('form-container');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const formCount = parseInt(totalForms.value, 10);

    // Remove the row
    button.closest(".row").remove();

    // Decrement TOTAL_FORMS
    totalForms.value = formCount - 1;
}

function submitForm() {
    const startDate = document.getElementById('id_start_date');
    const endDate = document.getElementById('id_end_date');

    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    if (!startDate || !endDate) {
        alert('Please ensure the date fields are correctly filled out.');
        return;
    }

    const items = [];
    document.querySelectorAll('#form-container > div').forEach((itemDiv) => {
        const itemName = itemDiv.querySelector('select[name$="item"]').value;
        const quantity = itemDiv.querySelector('input[name$="quantity"]').value;
        
        items.push({
            item_name: itemName,
            quantity: quantity,
        });
    });
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({start_date: startDate.value, end_date: endDate.value, city : city.value, location : location.value, garden : garden.value, items
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function getCurrency(priceSelect) {
    const currency = document.getElementById('id_currency');
    const row = priceSelect.closest('.row');
    const currencyDisplay = row.querySelector('.currency-display');
    currencyDisplay.textContent = currency;
}