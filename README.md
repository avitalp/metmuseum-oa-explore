# metmuseum-oa-explore
Tools to explore Met museum's openaccess datasets

met_objects.sql contains the converted CSV dataset as a MySQL table. All records for items classified as "Paintings" have been populated with link to full-size image as well as collection info.

Once you get the SQL file you can restore it using (make sure you create "themet" database first):
```
mysql -u USER -p themet < met_objects.sql
```

Please see
[Exploring The Metropolitan Museum of Art's Open Access Initiative dataset](https://avital.ca/notes/exploring-met-museums-openaccess-dataset) for more details

## UPDATE
It seems downloads of the SQL file count against my default 1GB Git LFS quota which was maxed out pretty quickly. This prevents me from being able to update the file often. This bandwidth policy doesn't make sense to me, so I'll only be updating the raw file when the billing cycle resets/allows. As an updated alternative, I've added the file `met_objects.sql.gz`. Simply do `gunzip met_objects.sql.gz` and you'll get the original file.
