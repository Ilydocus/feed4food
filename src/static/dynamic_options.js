function addProduct() {
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
    updateProductChoices();
    //enableSearchableDropdown();
}

function addWasteAction() {
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
    updateWasteChoices();
}

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
}

function addNewRow() {
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
}

function addGroup() {
    addNewRow();
    updateGroupOptions();
}

function addInput() {
    addNewRow();
    updateInputChoices();
}

function addRainfall() {
    const template = document.getElementById('rainfall-form-template').textContent;
    const container = document.getElementById('rainwater-form-container');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const formCount = parseInt(totalForms.value, 10);
    const newFormRow = document.createElement('div');

    newFormRow.class = `row`;
    newFormRow.innerHTML = template;

    // Append the new row and increment TOTAL_FORMS
    container.appendChild(newFormRow);
    totalForms.value = formCount + 1;
    //enableSearchableDropdown();
}

function addIrrigation() {
    const template = document.getElementById('irrigation-form-template').textContent;
    const container = document.getElementById('irrigation-form-container');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS2');
    const formCount = parseInt(totalForms.value, 10);
    const newFormRow = document.createElement('div');

    newFormRow.class = `row`;
    newFormRow.innerHTML = template;

    // Append the new row and increment TOTAL_FORMS
    container.appendChild(newFormRow);
    totalForms.value = formCount + 1;
    //enableSearchableDropdown();
    initializeExistingForms();//Make the periodic fields disappear
}

function initializeExistingForms() {
        const periodCheckboxes = document.querySelectorAll('input[name$="period"]');
        periodCheckboxes.forEach(function(checkbox) {
            const irrigation_row = checkbox.closest('.irrigation_row') || document;
            const endDateInput = irrigation_row.querySelector('input[name$="end_date"]');
            const frequencyTimesInput = irrigation_row.querySelector('input[name$="frequency_times"]');
            const unitInput = irrigation_row.querySelector('.times-display'); 
            const frequencyIntervalInput = irrigation_row.querySelector('.interval');
            
            if (endDateInput) {
                const endDateField = endDateInput.closest('.col-md-2');
                
                if (checkbox.checked) {
                    endDateField.style.display = 'block';
                } else {
                    endDateField.style.display = 'none';
                }
            }
            if (frequencyTimesInput) {
                const frequencyTimesField = frequencyTimesInput.closest('.col-md-2');
                
                if (checkbox.checked) {
                    frequencyTimesField.style.display = 'block';
                } else {
                    frequencyTimesField.style.display = 'none';
                }
            }
            if (unitInput) {
                const unitField = unitInput.closest('.col-md-1');
                
                if (checkbox.checked) {
                    unitField.style.display = 'block';
                } else {
                    unitField.style.display = 'none';
                }
            }
            if (frequencyIntervalInput) {
                const frequencyIntervalField = frequencyIntervalInput.closest('.col-md-2');
                
                if (checkbox.checked) {
                    frequencyIntervalField.style.display = 'block';
                } else {
                    frequencyIntervalField.style.display = 'none';
                }
            }
        });
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
    if(unitDisplay){
        unitDisplay.textContent = selectedUnit;
    }
}

function updateUnitCultivation(itemSelect) {
    // Get the selected option
    const selectedUnit = itemSelect.options[itemSelect.selectedIndex].getAttribute('cultivation-unit');

    const row = itemSelect.closest('.row');
    const unitDisplay = row.querySelector('.unit-cultivation-display');
    if(unitDisplay){
        unitDisplay.textContent = selectedUnit;
    }
}

function updateUnitInput(inputSelect) {
    // Get the selected option
    const selectedUnit = inputSelect.options[inputSelect.selectedIndex].getAttribute('data-unit');

    const row = inputSelect.closest('.row');
    const unitDisplay = row.querySelector('.unit-input-display');
    unitDisplay.textContent = selectedUnit;
}

function updateUnitAndCurrency(itemSelect) {
    // Get the selected option for unit
    const selectedUnit = itemSelect.options[itemSelect.selectedIndex].getAttribute('data-unit');

    const row = itemSelect.closest('.row');
    const unitDisplay = row.querySelector('.unit-display');
    if (unitDisplay){
        unitDisplay.textContent = selectedUnit;
    }

    // Get the selected option for currency
    const currencyField = document.getElementById('id_currency');
    if (currencyField){
        const currency = currencyField.options[currencyField.selectedIndex].text;
        const currencyDisplay = row.querySelector('.unitandcurrency-display');
        if (currencyDisplay){
            currencyDisplay.textContent = currency + " per " + selectedUnit;
        }
    }
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

function submitProductionForm() {
    const productionDate = document.getElementById('id_production_date');

    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    if (!productionDate) {
        alert('Please ensure the date fields are correctly filled out.');
        return;
    }

    const items = [];
    document.querySelectorAll('#form-container > div').forEach((itemDiv) => {
        const itemName = itemDiv.querySelector('select[name$="name"]').value;
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
        body: JSON.stringify({production_date: productionDate.value, city : city.value, location : location.value, garden : garden.value, items:items
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function submitSalesForm() {
    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');
    const currency = document.getElementById('id_currency');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const salesActions = [];
    document.querySelectorAll('#form-container > div').forEach((salesActionsDiv) => {
        
        const sale_date = salesActionsDiv.querySelector('input[name$="sale_date"]').value;
        const sale_location = salesActionsDiv.querySelector('input[name$="sale_location"]').value;
        const product = salesActionsDiv.querySelector('select[name$="product"]').value;
        const price = salesActionsDiv.querySelector('input[name$="price"]').value;
        const quantity = salesActionsDiv.querySelector('input[name$="quantity"]').value;
        
        salesActions.push({
            product: product,
            quantity: quantity,
            sale_date: sale_date,
            sale_location: sale_location,
            price: price,
        });

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
    const month = document.getElementById('id_month');
    const year = document.getElementById('id_year');
    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');
    const currency = document.getElementById('id_currency');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    // if (!startDate || !endDate) {
    //     alert('Please ensure the date fields are correctly filled out.');
    //     return;
    // }

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
        body: JSON.stringify({month : month.value, year : year.value, city : city.value, location : location.value, garden : garden.value,currency: currency.value, 
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

function submitEventForm() {
    const city = document.getElementById('id_city');
    const currency = document.getElementById('id_currency');
    const event_date = document.getElementById('id_event_date');
    const event_name = document.getElementById('id_event_name');
    const event_loc = document.getElementById('id_event_loc');
    const event_type = document.getElementById('id_event_type');
    const event_desc = document.getElementById('id_event_desc');
    const event_costs = document.getElementById('id_event_costs');
    const event_costs_desc = document.getElementById('id_event_costs_desc');
    const event_revenues = document.getElementById('id_event_revenues');
    const event_revenues_desc = document.getElementById('id_event_revenues_desc');
    const total_invited = document.getElementById('id_total_invited');
    const total_participants = document.getElementById('id_total_participants');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    const eventGroupDetails = [];
    document.querySelectorAll('#form-container > div').forEach((eventInvitedDetailsDiv) => {
        
        const name = eventInvitedDetailsDiv.querySelector('select[name$="name"]').value;
        const number_invited = eventInvitedDetailsDiv.querySelector('input[name$="number_invited"]').value;
        const number_participant = eventInvitedDetailsDiv.querySelector('input[name$="number_participant"]').value;

        eventGroupDetails.push({
            name: name,
            number_invited: number_invited,
            number_participant: number_participant,
        });

    
    });
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({city : city.value, currency: currency.value, event_date: event_date.value,
            event_name: event_name.value, event_loc: event_loc.value, event_type: event_type.value,
            event_desc: event_desc.value, event_costs: event_costs.value, event_costs_desc: event_costs_desc.value,
            event_revenues: event_revenues.value, event_revenues_desc: event_revenues_desc.value, total_invited: total_invited.value,
            total_participants: total_participants.value, eventGroupDetails: eventGroupDetails
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred: ' + error.message);
    });
}

function updateGroupOptions() {
    const citySelect = document.getElementById('id_city');
    const groupSelects = document.querySelectorAll('.group-name-select');
    //const groupSelects = document.getElementById('id_name');
    
    if (!citySelect.value) {
        // Clear all group select options if no city selected
        groupSelects.forEach(select => {
            select.innerHTML = '<option value="">---------</option>';
        });
        return;
    }
    
    // Make AJAX request to get filtered groups
    fetch(`/demographicReport/get-groups-by-city/?city=${citySelect.value}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .then(response => response.json())
    .then(data => {
        // Update all group select dropdowns
        groupSelects.forEach(select => {
            const currentValue = select.value;
            //console.log('Current value before clearing:', currentValue);
            select.innerHTML = '<option value=""> Select group </option>';
            
            data.groups.forEach(group => {
                const option = document.createElement('option');
                option.value = group.name;
                option.textContent = group.name;
                if (group.name === currentValue) {
                    option.selected = true;
                }
                select.appendChild(option);
            });
        });
    })
    .catch(error => {
        console.error('Error fetching groups:', error);
    });
}

// Update group options when new forms are added dynamically
// function updateNewGroupForm() {
//     // Call this function when adding new demographic group forms
//     updateGroupOptions();
// }

function submitDemographicForm() {
    
    const city = document.getElementById('id_city');
    const data_date = document.getElementById('id_data_date');
    const total_population = document.getElementById('id_total_population');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    const demographicGroupDetails = [];
    document.querySelectorAll('#form-container > div').forEach((groupDetailsDiv) => {
        
        const name = groupDetailsDiv.querySelector('select[name$="name"]').value;
        const population = groupDetailsDiv.querySelector('input[name$="population"]').value;

        demographicGroupDetails.push({
            name: name,
            population: population,
        });

    
    });
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({city : city.value, data_date: data_date.value,
            total_population: total_population.value, demographicGroupDetails: demographicGroupDetails
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function submitCultivationForm() {
    const cultivationDate = document.getElementById('id_cultivation_date');

    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    if (!cultivationDate) {
        alert('Please ensure the date fields are correctly filled out.');
        return;
    }

    const items = [];
    document.querySelectorAll('#form-container > div').forEach((itemDiv) => {
        const itemName = itemDiv.querySelector('select[name$="name"]').value;
        const area_cultivated = itemDiv.querySelector('input[name$="area_cultivated"]').value;
        
        items.push({
            name: itemName,
            area_cultivated: area_cultivated,
        });
    });
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({cultivation_date: cultivationDate.value, city : city.value, location : location.value, garden : garden.value, items
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function submitInputForm() {
    const applicationDate = document.getElementById('id_application_date');

    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    if (!applicationDate) {
        alert('Please ensure the date fields are correctly filled out.');
        return;
    }

    const inputs = [];
    document.querySelectorAll('#form-container > div').forEach((itemDiv) => {
        const inputName = itemDiv.querySelector('select[name$="name_input"]').value;
        const productName = itemDiv.querySelector('select[name$="name_product"]').value;
        const area = itemDiv.querySelector('input[name$="area"]').value;
        const quantity = itemDiv.querySelector('input[name$="quantity"]').value;
        
        inputs.push({
            name_input: inputName,
            name_product: productName,
            area: area,
            quantity: quantity,
        });
    });
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({application_date: applicationDate.value, city : city.value, location : location.value, garden : garden.value, inputs
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function submitLLUseForm() {
    
    const city = document.getElementById('id_city');
    const report_date = document.getElementById('id_report_date');
    const gardens_in_use = document.getElementById('id_gardens_in_use');
    const total_ll_participants = document.getElementById('id_total_ll_participants');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    const llUseGroupDetails = [];
    document.querySelectorAll('#form-container > div').forEach((groupDetailsDiv) => {
        
        const name = groupDetailsDiv.querySelector('select[name$="name"]').value;
        const ll_participants = groupDetailsDiv.querySelector('input[name$="ll_participants"]').value;

        llUseGroupDetails.push({
            name: name,
            ll_participants: ll_participants,
        });

    
    });
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({city : city.value, report_date: report_date.value,
            gardens_in_use: gardens_in_use.value, total_ll_participants: total_ll_participants.value, llUseGroupDetails: llUseGroupDetails
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function submitWasteForm() {
    
    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const actions = [];
    document.querySelectorAll('#form-container > div').forEach((itemDiv) => { 
        const date = itemDiv.querySelector('input[name$="date"]').value; 
        const wasteType = itemDiv.querySelector('select[name$="wasteType"]').value;
        const wasteAction = itemDiv.querySelector('select[name$="wasteAction"]').value;
        const quantity = itemDiv.querySelector('input[name$="quantity"]').value;
        
        actions.push({
            date: date,
            wasteType: wasteType,
            wasteAction: wasteAction,
            quantity: quantity,
        });
    });
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({city : city.value, location : location.value, garden : garden.value, actions: actions
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function submitWaterForm() {
    
    const city = document.getElementById('id_city');
    const location = document.getElementById('id_location');
    const garden = document.getElementById('id_garden');

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const rainfalls = [];
    const elements_r = document.querySelectorAll('#rainwater-form-container > div');
    if (elements_r.length > 0){
        elements_r.forEach((itemDiv) => {
            const start_date = itemDiv.querySelector('input[name$="start_date"]').value;
            const end_date = itemDiv.querySelector('input[name$="end_date"]').value;
            const quantity = itemDiv.querySelector('input[name$="quantity"]').value;
            
            rainfalls.push({
                start_date: start_date,
                end_date: end_date,
                quantity: quantity,
            });
        });
    }
    const irrigations = [];
    const elements_i = document.querySelectorAll('#irrigation-form-container > div');
    if (elements_i.length > 0){
        elements_i.forEach((itemDiv) => {
            const start_date = itemDiv.querySelector('input[name$="start_date"]').value;
            end_date = null;
            const end_dateElement =itemDiv.querySelector('input[name$="end_date"]');
            if(end_dateElement!== null){
                end_date = itemDiv.querySelector('input[name$="end_date"]').value;
            }
            const period = itemDiv.querySelector('input[name$="period"]').checked;
            frequency_times = 0;
            const frequency_timesElement =itemDiv.querySelector('input[name$="frequency_times"]');
            if (frequency_timesElement !==null){
                frequency_times = itemDiv.querySelector('input[name$="frequency_times"]').value;
            }
            frequency_interval = null;
            const frequency_intervalElement = itemDiv.querySelector('select[name$="frequency_interval"]');
            if (frequency_intervalElement !== null){
                frequency_interval = itemDiv.querySelector('select[name$="frequency_interval"]').value;
            }
            const quantity = itemDiv.querySelector('input[name$="quantity"]').value;
            const source = itemDiv.querySelector('select[name$="source"]').value;
            
            irrigations.push({
                start_date: start_date,
                end_date: end_date,
                period: period,
                frequency_times: frequency_times,
                frequency_interval: frequency_interval,
                quantity: quantity,
                source: source,
            });
        });
    }
    
    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({city : city.value, location : location.value, garden : garden.value, rainfalls: rainfalls, irrigations: irrigations
        })
    })
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
    });
}

function updateProductChoices() {
    const citySelect = document.querySelector('#id_city');
    const cityId = citySelect.value;
    
    if (!cityId) {
        // Reset all product selects to empty if no city selected
        resetProductSelects();
        return;
    }
    
    // Make AJAX request to get products for the selected city
    fetch(`/productionReport/get-products-by-city/?city_id=${cityId}`)
        .then(response => response.json())
        .then(data => {
            updateAllProductSelects(data.products);
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });
}

function updateAllProductSelects(products) {
    // Find all product select elements
    const productSelects = document.querySelectorAll('.product-name-select');
    
    productSelects.forEach(select => {
        const currentValue = select.value;
        
        // Clear existing options
        select.innerHTML = '<option value="">Select Product</option>';
        
        // Add new options
        products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.name;
            option.textContent = product.name;
            option.setAttribute('data-unit', product.unit);
            option.setAttribute('cultivation-unit', product.cultivation_type);
            
            // Restore selection if it still exists
            if (product.name === currentValue) {
                option.selected = true;
            }
            
            select.appendChild(option);
        });
        
        // Update unit display for this select
        updateUnit(select);
        updateUnitCultivation(select);
        updateUnitAndCurrency(select);
    });
}

function resetProductSelects() {
    const productSelects = document.querySelectorAll('.product-name-select');
    
    productSelects.forEach(select => {
        select.innerHTML = '<option value="">Select Product</option>';
        
        // Clear unit display
        const unitDisplay = select.closest('.row').querySelector('.unit-display');
        if (unitDisplay) {
            unitDisplay.textContent = '';
        }
        const unitDisplay_c = select.closest('.row').querySelector('.unit-cultivation-display');
        if (unitDisplay_c) {
            unitDisplay_c.textContent = '';
        }
    });
}

function updateWasteChoices() {
    const citySelect = document.querySelector('#id_city');
    const cityId = citySelect.value;
    
    if (!cityId) {
        // Reset all product selects to empty if no city selected
        resetWasteSelects();
        return;
    }
    
    // Make AJAX request to get products for the selected city
    fetch(`/wasteReport/get-wastetypes-by-city/?city_id=${cityId}`)
        .then(response => response.json())
        .then(data => {
            updateAllWasteSelects(data.types);
        })
        .catch(error => {
            console.error('Error fetching waste types', error);
        });
}

function updateAllWasteSelects(types) {
    // Find all waste select elements
    const wasteSelects = document.querySelectorAll('.waste-type-select');
    
    wasteSelects.forEach(select => {
        const currentValue = select.value;
        
        // Clear existing options
        select.innerHTML = '<option value="">Select type</option>';
        
        // Add new options
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type.name;
            option.textContent = type.name;
            option.setAttribute('data-unit', type.unit);
            
            // Restore selection if it still exists
            if (type.name === currentValue) {
                option.selected = true;
            }
            
            select.appendChild(option);
        });
        
        // Update unit display for this select
        updateUnitCultivation(select);
    });
}

function resetWasteSelects() {
    const wasteSelects = document.querySelectorAll('.waste-type-select');
    
    wasteSelects.forEach(select => {
        select.innerHTML = '<option value="">Select type</option>';
        
        // Clear unit display
        const unitDisplay = select.closest('.row').querySelector('.unit-display');
        if (unitDisplay) {
            unitDisplay.textContent = '';
        }
    });
}

function updateInputChoices() {
    const citySelect = document.querySelector('#id_city');
    const cityId = citySelect.value;
    
    if (!cityId) {
        // Reset all inputs/product selects to empty if no city selected
        resetInputSelects();
        resetProductSelects();
        return;
    }
    
    // Make AJAX request to get inputs for the selected city
    fetch(`/productionReport/get-products-by-city/?city_id=${cityId}`)
        .then(response => response.json())
        .then(data => {
            updateAllProductSelects(data.products);
        })
        .catch(error => {
            console.error('Error fetching products', error);
        });
    // Make AJAX request to get inputs for the selected city
    fetch(`/inputReport/get-inputs-by-city/?city_id=${cityId}`)
        .then(response => response.json())
        .then(data => {
            updateAllInputSelects(data.inputs);
        })
        .catch(error => {
            console.error('Error fetching inputs', error);
        });
}

function updateAllInputSelects(inputs) {
    // Find all input select elements
    const inputSelects = document.querySelectorAll('.input-name-select');
    
    inputSelects.forEach(select => {
        const currentValue = select.value;
        
        // Clear existing options
        select.innerHTML = '<option value="">Select Input</option>';
        
        // Add new options
        inputs.forEach(type => {
            const option = document.createElement('option');
            option.value = type.name;
            option.textContent = type.name;
            option.setAttribute('data-unit', type.unit);
            
            // Restore selection if it still exists
            if (type.name === currentValue) {
                option.selected = true;
            }
            
            select.appendChild(option);
        });
        
        // Update unit display for this select
        updateUnitInput(select);
    });
}

function resetInputSelects() {
    const inputSelects = document.querySelectorAll('[name*="name_input"]');
    
    inputSelects.forEach(select => {
        select.innerHTML = '<option value="">Select input</option>';
        
        // Clear unit display
        const unitDisplay = select.closest('.row').querySelector('.unit-input-display');
        if (unitDisplay) {
            unitDisplay.textContent = '';
        }
    });
}

