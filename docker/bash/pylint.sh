cd ../app
echo "Running pylint..."
echo ""
echo ""
echo ""
for filename in ./*.py; do
    if [ "$filename" != "./__init__.py" ]; then
        echo ">>>"
        echo "$filename"
        pylint "$filename"
        echo "<<<"
        echo ""
    fi
done
read varname
