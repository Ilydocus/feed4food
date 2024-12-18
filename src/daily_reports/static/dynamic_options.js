function addItem() {
    const container = document.getElementById('items-container');
    const itemIndex = container.children.length;
    const itemDiv = document.createElement('div');

    const itemNames = JSON.parse(document.getElementById('item-names').textContent);
    let options = '<option value="">Select an item</option>';
    itemNames.forEach(name => {
        options += `<option value="${name}">${name}</option>`;
    });

    itemDiv.innerHTML = `
        <label>Item:</label>
        <select name="item-select" onchange="showOptions(this, ${itemIndex})">
        ${options}
        </select>
        <div id="item-attributes-${itemIndex}"></div>
    `;
    container.appendChild(itemDiv);
}

async function showOptions(select, itemIndex) {
    const optionsDiv = document.getElementById(`item-attributes-${itemIndex}`);
    optionsDiv.innerHTML = '';
    const selectedValue = select.value;
    if (selectedValue != "") {
        try {
            const option_attr = await fetch(`get_item/${selectedValue}`).then(response => response.json());
            optionsDiv.innerHTML = `
                <label>Quantity (in ${option_attr.unit}'s):</label>
                <input type="number" name="quantity" step="0.01" />
            `;
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
}

function submitForm() {

    const startDate = document.querySelector('#id_start_date');
    const endDate = document.querySelector('#id_end_date');
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (!startDate || !endDate) {
        alert('Please ensure the date fields are correctly filled out.');
        return;
    }
    
    const items = [];
    console.log(document.querySelectorAll('#items-container > div'))
    document.querySelectorAll('#items-container > div').forEach((itemDiv, itemIndex) => {
        const itemName = itemDiv.querySelector(`select[name='item-select']`).value;
        const quantity = itemDiv.querySelector(`input[name='quantity']`).value;
        
        items.push({
            item_name: itemName,
            quantity: quantity,
        })
    });

    fetch('', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 
                  'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({start_date: startDate.value, end_date: endDate.value, location: "none", items}),
    }).then(response => response.json()).then(data => {
        alert('Report submitted successfully!');
    });
}