# langpro-container

Before cloning the repository, install and enable [git-lfs][git-lfs]. If you already cloned the repository before seeing this instruction, keep reading.

[git-lfs]: https://git-lfs.com/

After cloning the repository, run the following commands once in order to obtain a local copy of LangPro:

``` sh
git submodule init
# customize clone URL in .git/config before proceeding (if needed)
git submodule update
```

If you installed git-lfs only after cloning this repository, now run `git lfs pull`. You need to do this only once.

After pulling in new changes that update to a later commit of LangPro, run `git submodule update` again.

Build a langpro image and run the container while mounting this and LangPro git directories in the container.
On the startup of the container, the langpro binary file will be compiled and will be used by the api calls.
```
docker build . -t langpro
docker run -it -p 8080:80 --rm -v $(pwd)/LangPro_demo:/langpro  -v $(pwd)/LangPro:/git_LangPro  langpro
```

(old) demo interface is served on http://localhost:8080/


Curl example:

```
# Example with two premises
curl 'http://localhost:8080/api/prove/' -H 'Content-Type: application/json' -d '{"prover_config":["allInt", "aall"], "premises":["Every man is working", "Everybody who is working has an expensive car"], "hypothesis":"Every man owns a car", "ral":200, "senses":"all"}'

# Example with user knowledge injection "guinea pig is small animal" and "snoring means sleeping"
curl 'http://localhost:8080/api/prove/' -H 'Content-Type: application/json' -d '{"premises": ["A guinea pig is snoring"], "hypothesis": "A small animal is sleeping", "prover_config": ["allInt", "aall"], "ral": 200, "kb": ["isa_wn(guinea pig, small animal)", "isa_wn(snore,sleep)"], "senses": "all"}'

# Example with a knowledge about disjoint/incompatible relation
curl 'http://localhost:8080/api/prove/' -H 'Content-Type: application/json' -d '{"premises": ["A hamster is jumping"], "hypothesis": "A hamster is resting", "prover_config": ["allInt", "aall"], "ral": 200, "kb": ["disj(rest,jump)"], "senses": "all"}'

# Specifying the parser argument
# note that certain parsers might fail to parse sentences of certain problems, e.g., "re-cc" fails for this input problem
curl 'http://localhost:8080/api/prove/' -H 'Content-Type: application/json' -d '{"premises": ["A woman is putting on lipstick"], "hypothesis": "There is no woman putting on lipstick", "prover_config": ["allInt", "aall"], "ral": 200, "kb": [], "senses": "all", "parser": "cc"}'
```

Python example with LangPro API:

```
# make sure to have LangPro cloned in the same dir as langpro-container
# display only CCG trees for a pre-specified sample problem with id 1
python3 LangPro_demo/call.py -i 1 -r ccg_tree

# display trees/terms and proofs for a custom NLI problem
python3 LangPro_demo/call.py -p "Some cats are hungry" "No cat is sleeping" -c "There is a hungry cat that is not sleeping"

# display proofs for a custom NLI problem with input knowledge
python3 LangPro_demo/call.py -r proof -p "A guinea pig is snoring" -c "A small animal is sleeping" -k "isa_wn(guinea pig, small animal)" "isa_wn(snore,sleep)"

# for help
# python3 LangPro_demo/call.py -h
```
