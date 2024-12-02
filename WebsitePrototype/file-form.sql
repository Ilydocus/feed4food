select 'text' as component, '
# Feed4Food file report

Here you can upload a file containing measurements. For formatting the file correctly, see the [data collection protocol](https://www.google.com).
' as contents_md;

set data_url = sqlpage.read_file_as_data_url(sqlpage.uploaded_file_path('my_file'));

--select 'card' as component, 1 as columns where $data_url is not null;
--select 'Your picture' as title,
--    $data_url as top_image,
--    'Uploaded file type: ' || sqlpage.uploaded_file_mime_type('my_file') as description
--where $data_url is not null;

select 'form' as component, 'Upload file' as validate;
select 'my_file' as name, 'file' as type, 'Measurement file' as label;

select 
    'button' as component,
	'center' as justify;
select 
    '/index.sql' as link,
    'Home'            as title;

