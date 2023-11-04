# Database for Real Estate Management

## Commands to run the application:
- To **build the docker image** navigate to the Real_estate/flask_app and run the following command:
```bash
docker build -t real_estate_image .
```

- Run a container based on the image using the following command:
```bash
docker run -p 5000:5000 real_estate_image
```

(for the case something is already running on port 5000 - chose another port):
```bash
docker run -p 5001:5000 real_estate_image
```

- Accessing the Application: Once the container is running, you should be able to access your Flask application by:
```bash
  http://localhost:5000
```

(for the case something is already running on port 5000 - chose another port):
```bash
 http://localhost:5001
```

property_geneva = Property(location='Geneva', size=110, rooms=4.0, building_year=2005)
