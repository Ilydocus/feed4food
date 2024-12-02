
select 'text' as component, '
# Feed4Food daily report

Here you can upload all measures which should be reported daily. 
' as contents_md;

--Overall form
select 'form' as component, 'Enter a daily report' as title,
	case when :vegetables is null 
        then 'Next'
        else 'Upload your data'
    end as validate,
    case when :vegetables is null
        then ''
        else 'confirmation_daily.sql'
    end as action;

-- Select the date
select 'date' as type, 'report_date' as name, 'Report date' as label, 'What day is the report for' as placeholder,
date('now', '-6 months') as min, date('now') as max, --Cannot input for measurements in the future or older than 6 months (can be changed)
CAST(:report_date AS TEXT) as value,
8 as width; 

--select the list of measures which are in the database as should be reported daily - I do it in a shorter way for now

--- First metric - L of harvested water
-- Enter value
select 'number' as type, 0.01 AS step, 'measurement1_value' as name, 'L of water harvested' as label, 'Enter the measured value' as placeholder,
CAST(:measurement1_value AS REAL) as value,
8 as width ;


--- Second metric - Kg of produced vegetables
select 'number' as type, 'vegetables' as name, 'Number of types of product harvested/produced' as label, 'How many different products should be reported?' as placeholder, 1 as min, 10 as max,
coalesce(:vegetables, 1) as value, -- Default to 1 vegetable -- See over the variable name
--:vegetables is not null as readonly, -- The number of adults field is readonly once it's selected
8 as width; -- The number of adults field takes a third of the width of the form

create temporary table if not exists vegetableTypes as
select 1 as id, 'Tomato' as vegetableType union all
select 2, 'Cucumber' union all
select 3, 'Onion'; 

---I need to be able to add a random number of lines for all vegetables needed - for now do it fixed based on the input above

--TODO Only show the below once the number is selected
-- First step: Select the vegetable
--select 'select' as type, 'vegetableSelected' as name, 'Product' as label, 'Select the product' as placeholder, -- The measureSelected field takes the entire width of the form, unless it's already selected
--CAST(:vegetableSelected AS INTEGER) as value, -- We keep the value of the measureSelected in the form. All form fields are submitted as text TODO check if this is a wanted behaviour
--json_group_array(json_object('value', id, 'label', vegetableType)) as options
--from vegetableTypes;

-- Third step: Enter value
--select 'number' as type, 0.01 AS step, 'measurement_value' as name, 'Value' as label, 'Enter the measured value' as placeholder,
--CAST(:measurement_value AS REAL) as value,
--8 as width 
--where :measurement_date is not null; -- Only show value when date is selected

with recursive vegetable_ids as (
    select 0 as id, 0 as product_type union all
    select id + 1 as id,
         'Product'
        as product_type
    from vegetable_ids
    where id < CAST(:vegetables AS INTEGER)
)

-- First step: Select the vegetable
select 'select' as type, printf('%s_names[]', product_type) as name, printf('Product %d', id) as label,  true as searchable, 'Select a product' as empty_option,
--CAST(:vegetableSelected AS INTEGER) as value,
(select json_group_array(json_object('value', vegetableType, 'label', vegetableType)) 
from vegetableTypes)as options,
6 as width--,
from vegetable_ids
where id>0 and :vegetables is not null;

with recursive vegetable_ids as (
    select 0 as id, 0 as product_type union all
    select id + 1 as id,
         'Product'
        as product_type
    from vegetable_ids
    where id < CAST(:vegetables AS INTEGER)
)

-- Second step: Enter value
select 'number' as type, 0.01 AS step, printf('%s_values[]', product_type) as name, printf('Value for product %d', id) as label, 'Enter the measured value' as placeholder,
CAST(:measurement_value AS REAL) as value,
6 as width 
from vegetable_ids
where id>0 and :vegetables is not null;

--Can I have the insert into statement here or does it have to be on the confirmation page. 

select 
    'button' as component,
	'center' as justify;
select 
    '/index.sql' as link,
    'Home'            as title;




