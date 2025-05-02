#!/bin/bash

chmod +x parsers/rebank_candc/rebank_dist/bin/*

pushd parsers/rebank_candc/models/
ln -s pos_quotes pos
ln -s muc ner
ln -s chunk_quotes chunk
popd
