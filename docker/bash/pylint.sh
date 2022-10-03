cd ../app
echo "Running pylint..."
echo ""
echo ""
echo ">>>"
echo "main.py"
pylint main.py
echo "<<<"
echo ""
cd ./scripts
for filename in ./*.py; do
    if [ "$filename" != "./__init__.py" ]; then
        echo ">>>"
        echo "$filename"
        pylint "$filename"
        echo "<<<"
        echo ""
    fi
done
