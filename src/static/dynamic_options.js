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
}

function updateUnitAndCurrency(itemSelect) {
    // Get the selected option for unit
    const selectedUnit = itemSelect.options[itemSelect.selectedIndex].getAttribute('data-unit');

    const row = itemSelect.closest('.row');
    const unitDisplay = row.querySelector('.unit-display');
    unitDisplay.textContent = selectedUnit;
    //Second occurence
    //const unitDisplay2 = row.querySelector('.unitandcurrency-display');
    //unitDisplay2.textContent = selectedUnit;

    // Get the selected option for currency
    const currency = document.getElementById('id_currency').value;
    const currencyDisplay = row.querySelector('.unitandcurrency-display');
    currencyDisplay.textContent = currency + " per " + selectedUnit;
}

function updateCurrency(currencySelect) {
    const row = currencySelect.closest('.row');

    // Get the selected option for currency
    const currency = document.getElementById('id_currency').value;
    const currencyDisplay = row.querySelector('.currency-display');
    currencyDisplay.textContent = currency;
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

function submitSalesForm() {
    //console.log("Coucou"); //How to print to console browser
    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');
    const currency = document.getElementById('id_currency');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    // if (!sale_date1) {
    //     alert('Please ensure the date fields are correctly filled out.');
    //     return;
    // }
    // console.log("Coucou2");

    const salesActions = [];
    document.querySelectorAll('#form-container > div').forEach((salesActionsDiv) => {
        
        const sale_date = salesActionsDiv.querySelector('input[name$="sale_date"]').value;
        const sale_location = salesActionsDiv.querySelector('input[name$="sale_location"]').value;
        const product = salesActionsDiv.querySelector('select[name$="what"]').value;
        const price = salesActionsDiv.querySelector('input[name$="price"]').value;
        const quantity = salesActionsDiv.querySelector('input[name$="quantity"]').value;
        
        salesActions.push({
            product: product,
            quantity: quantity,
            sale_date: sale_date,
            sale_location: sale_location,
            price: price,
        });
    //console.log(salesActions);
    });
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({city : city.value, location : location.value, garden : garden.value,currency: currency.value, salesActions
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function submitFinancialForm() {
    const startDate = document.getElementById('id_start_date');
    const endDate = document.getElementById('id_end_date');
    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');
    const currency = document.getElementById('id_currency');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    if (!startDate || !endDate) {
        alert('Please ensure the date fields are correctly filled out.');
        return;
    }

    const exp_workforce = document.getElementById('id_exp_workforce');
    const exp_purchase = document.getElementById('id_exp_purchase');
    const exp_others = document.getElementById('id_exp_others');
    const exp_others_desc = document.getElementById('id_exp_others_desc');
    const fun_feed4food = document.getElementById('id_fun_feed4food');
    const fun_others = document.getElementById('id_fun_others');
    const fun_others_desc = document.getElementById('id_fun_others_desc');
    const rev_restaurant = document.getElementById('id_rev_restaurant');
    const rev_others = document.getElementById('id_rev_others');
    const rev_others_desc = document.getElementById('id_rev_others_desc');
    
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({startDate : startDate.value, endDate : endDate.value, city : city.value, location : location.value, garden : garden.value,currency: currency.value, 
            exp_workforce : exp_workforce.value, exp_purchase : exp_purchase.value, exp_others : exp_others.value, exp_others_desc : exp_others_desc.value, 
            fun_feed4food : fun_feed4food.value, fun_others : fun_others.value, fun_others_desc : fun_others_desc.value, rev_restaurant : rev_restaurant.value,
            rev_others : rev_others.value, rev_others_desc : rev_others_desc.value
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}
