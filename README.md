# langpro-container

```
docker build . -t langpro
docker run -it -p 8080:80 --rm -v $(pwd)/LangPro_demo:/langpro langpro

```

(old) demo interface is served on http://localhost:8080/


Curl example:

```
curl 'http://localhost:8080/api/foo/' -d'{"prover_config":["allInt", "aall"], "premises":["Every man is working", "Everybody who is working has an expensive car"], "hypothesis":"Every man owns a car", "ral":200, "senses":"all"}' -H 'Content-Type: application/json'
```
