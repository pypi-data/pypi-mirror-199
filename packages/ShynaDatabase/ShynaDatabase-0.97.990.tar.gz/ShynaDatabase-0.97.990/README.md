# ShynaDatabase

***Suggested: Not to use***

This package will take care of cleaning the database and querying the database. More functionality will be added as I process.

***_Note_***: Make sure to update the default_database before running any query otherwise it won't work at all.
User , host and password are as per environment variable. 
```
Shdatabase
    1) check_connectivity : Check database connectivity
    2) create_insert_update_or_delete: as per name, no return
    3) select_from_table : return output as list
    4) set_date_system: update last run in status_db
    5) insert_or_update_or_delete_with_status: as per name, return will True or False
    
ShynaUpdateDistance
    1) Update distance from previous location, update speed and update distance from home
````
