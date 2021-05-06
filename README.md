# API exercise for adding data to two different tables

***

Build the docker image
```
docker build --tag usr-loc-api .
```

Run as container

```
docker run -dp 5000:5000 usr-loc-api
```

Try some api call

```
localhost:5000/users
```

---


## Appendix

Problem open Docker GUI? 

Quit Docker Desktop 
and run:

```
rm -r Library/Application\ Support/Docker\ Desktop/ 
```
it should relaunch now
