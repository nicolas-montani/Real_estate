--Comile the image--
cd flask_app
docker build --tag real_estate .

--Launch Compose--
cd flask_compose 
docker compose up -d

--Go to --
localhost:5000