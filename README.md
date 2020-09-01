# Telecom_Carrier #

## Run Developer Mode ##
```
 docker-compose up --build
```

## Run Production Mode ##
```
 docker-compose -f docker-compose-prod.yml  up --build
```

Add ```-d``` to the end of the commands to run in the background.

## Run Test ##

A test docker environment has also been created.
```
 docker-compose -f docker-compose-test.yml up --abort-on-container-exit;
```

## Documentation ##

Existe uma documentação publicada no site do POSTMAN:

https://documenter.getpostman.com/view/7335439/TVCe18Th

## Attention ##
A role-based authorization system has been created. To facilitate testing the application, you can select your role in the register. Available roles are 'user' and 'manager'.
