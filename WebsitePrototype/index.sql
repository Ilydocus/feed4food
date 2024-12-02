select 'text' as component, '
# Feed4Food measure upload

Here you can upload your collected data according to the defined [data collection protocol](https://www.google.com). 
' as contents_md;



drop table if exists input_choices;
create temporary table if not exists input_choices as 
select 'Add value for a given measure' as title, 'measure-form' as folder,  '' as description union all
select 'Fill in daily report form', 'daily-report-form', '' union all
select 'Upload a measurement file', 'file-form', ''


select 'tab' as component, true as center;
select 'Select your input method' as title, 'All input methods' as description, '?' as link, $db is null as active;


select 'card' as component;
select title, description,
    format('images/%s.PNG', folder) as top_image,
    folder || '.sql' as link
from input_choices;
-- 'https://github.com/sqlpage/SQLPage/tree/main/examples/' || folder as link




