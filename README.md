# metmuseum-oa-explore
Tools to explore Met museum's openaccess datasets

met_objects.sql contains the converted CSV dataset as a MySQL table. All records for items classified as "Paintings" have been populated with link to full-size image as well as collection info.

Once you get the SQL file you can restore it using (make sure you create "themet" database first):
```
mysql -u USER -p themet < met_objects.sql
```

Please see
[Exploring The Metropolitan Museum of Art's Open Access Initiative dataset](https://avital.ca/notes/exploring-met-museums-openaccess-dataset) for more details
