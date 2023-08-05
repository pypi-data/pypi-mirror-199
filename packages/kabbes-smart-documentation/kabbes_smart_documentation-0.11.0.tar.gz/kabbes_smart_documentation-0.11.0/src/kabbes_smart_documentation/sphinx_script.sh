sphinx-apidoc -o . ./src
make html
rm -rf docs
mv _build/html docs