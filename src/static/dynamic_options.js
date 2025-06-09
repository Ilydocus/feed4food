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
    enableSearchableDropdown();
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
    enableSearchableDropdown();
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
    unitDisplay.textContent = selectedUnit;
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
        body: JSON.stringify({production_date: productionDate.value, city : city.value, location : location.value, garden : garden.value, items
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
    .then(response => response.json())
    .then(data => {
        alert('Report submitted successfully!');
        window.location.href = data.redirect_url;
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
            select.innerHTML = '<option value="">---------</option>';
            
            data.groups.forEach(group => {
                const option = document.createElement('option');
                option.value = group.id;
                option.textContent = group.name;
                if (group.id == currentValue) {
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
        const inputName = itemDiv.querySelector('select[name$="input_name"]').value;
        const productName = itemDiv.querySelector('select[name$="product_name"]').value;
        const area = itemDiv.querySelector('input[name$="area"]').value;
        const quantity = itemDiv.querySelector('input[name$="quantity"]').value;
        
        inputs.push({
            input_name: inputName,
            product_name: productName,
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
        const date = itemDiv.querySelector('select[name$="date"]').value;
        const wasteType = itemDiv.querySelector('select[name$="wasteType"]').value;
        const wasteAction = itemDiv.querySelector('input[name$="wasteAction"]').value;
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
    document.querySelectorAll('#rainwater-form-container > div').forEach((itemDiv) => {
        const start_date = itemDiv.querySelector('select[name$="start_date"]').value;
        const end_date = itemDiv.querySelector('select[name$="end_date"]').value;
        const quantity = itemDiv.querySelector('input[name$="quantity"]').value;
        
        rainfalls.push({
            start_date: start_date,
            end_date: end_date,
            quantity: quantity,
        });
    });
    const irrigations = [];
    document.querySelectorAll('#irrigation-form-container > div').forEach((itemDiv) => {
        const start_date = itemDiv.querySelector('select[name$="start_date"]').value;
        const end_date = itemDiv.querySelector('select[name$="end_date"]').value;
        const period = itemDiv.querySelector('input[name$="period"]').value;
        const frequency_times = itemDiv.querySelector('input[name$="frequency_times"]').value;
        const frequency_interval = itemDiv.querySelector('input[name$="frequency_interval"]').value;
        const quantity = itemDiv.querySelector('input[name$="quantity"]').value;
        
        irrigations.push({
            start_date: start_date,
            end_date: end_date,
            period: period,
            frequency_times: frequency_times,
            frequency_interval: frequency_interval,
            quantity: quantity,
        });
    });
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

