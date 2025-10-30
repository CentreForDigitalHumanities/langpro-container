# langpro-container

Clone LangPro repository (`nl`, the default branch for now) in the same place as this repo.

```
git clone git@github.com:kovvalsky/LangPro.git
```

Build a langpro image and run the container while mounting this and LangPro git directories in the container.
On the startup of the container, the langpro binary file will be compiled and will be used by the api calls.
```
docker build . -t langpro
docker run -it -p 8080:80 --rm -v $(pwd)/LangPro_demo:/langpro  -v $(pwd)/../LangPro:/git_LangPro  langpro
```

(old) demo interface is served on http://localhost:8080/


Curl example:

```
curl 'http://localhost:8080/api/foo/' -d'{"prover_config":["allInt", "aall"], "premises":["Every man is working", "Everybody who is working has an expensive car"], "hypothesis":"Every man owns a car", "ral":200, "senses":"all"}' -H 'Content-Type: application/json'
```

Python example with LangPro API:

```
# make sure to have LangPro cloned in the same dir as langpro-container
# display only CCG trees for a pre-specified sample problem with id 1
python3 LangPro_demo/call.py -i 1 -r tree

# display trees/terms and proofs for a custom NLI problem 
python3 LangPro_demo/call.py -p "Some cats are hungry" "No cat is sleeping" -c "There is a hungry cat that is not sleeping"

# for help
# python3 LangPro_demo/call.py -h
```
