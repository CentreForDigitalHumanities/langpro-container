#!/bin/bash

chmod +x parsers/rebank_candc/rebank_dist/bin/*

pushd parsers/rebank_candc/models/
ln -s pos_quotes pos
ln -s muc ner
ln -s chunk_quotes chunk
popd

# create langpro_bin binary on-fly because the binary 
# should be compatible with the local swipl version; no +x is needed.
echo "Compiling langpro binary...";
if swipl --toplevel=halt --stand_alone=true --foreign=save \
    -o nat_lang_pro/langpro_bin \
    -c /git_LangPro/prolog/main.pl \
       /git_LangPro/prolog/task/online_demo.pl \
       /git_LangPro/WNProlog/wn.pl; then
    echo "Done: langpro_bin created!";
else
    echo "Compilation failed!" >&2
    exit 1
fi    