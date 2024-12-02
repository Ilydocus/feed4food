-- This demonstrates how to build multi-step forms using the `form` component, and hidden inputs.
--select 'dynamic' as component, properties FROM example WHERE component = 'shell' LIMIT 1;

select 'text' as component, '
# Feed4Food measure upload

Here you can upload measurement values for a specific measure. 
' as contents_md;

create temporary table if not exists measures as
select 1 as id, 'L of water harvested' as measure union all
select 2, 'other measure 1' union all
select 3, 'other measure 2' union all
select 4, 'other measure 3';

select 'form' as component, 'Enter a measure value' as title,
    case when :measurement_date is null 
        then 'Next'
        else 'Upload your data'
    end as validate,
    case when :measurement_date is null 
        then ''
        else 'confirmation.sql' -- confirmation page
    end as action;

-- First step: Select measure to add data for
select 'select' as type, 'measureSelected' as name, 'Measure' as label, 'Select the measure' as placeholder, true as searchable,
case when :measureSelected is null then 12 else 6 end as width, -- The measureSelected field takes the entire width of the form, unless it's already selected
CAST(:measureSelected AS INTEGER) as value, -- We keep the value of the measureSelected in the form. All form fields are submitted as text TODO check if this is a wanted behaviour
json_group_array(json_object('value', id, 'label', measure)) as options
from measures;

-- Second step: Enter the date for the measurement
select 'date' as type, 'measurement_date' as name, 'Measurement date' as label, 'When was the measurement taken' as placeholder,
date('now', '-6 months') as min, date('now') as max, --Cannot input for measurements in the future or older than 6 months (can be changed)
CAST(:measurement_date AS TEXT) as value,
8 as width -- Trying to force it to be below, not sure this is the correct way
where :measureSelected is not null; -- Only show date when measure is selected

-- Third step: Enter value
select 'number' as type, 0.01 AS step, 'measurement_value' as name, 'Value' as label, 'Enter the measured value' as placeholder,
CAST(:measurement_value AS REAL) as value,
8 as width 
where :measurement_date is not null; -- Only show value when date is selected

-- Fourth step: Make sure everything is entered - somehow I need this
select 'text' as component, '
Your data has been uploaded.  
' as contents_md where :measurement_value is not null;

select 
    'button' as component,
	'center' as justify;
select 
    '/index.sql' as link,
    'Home'            as title;



