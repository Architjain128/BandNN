docker build . -t BAND-NN
docker run -d --name BAND-NN-v1 -p 80:80 BAND-NN