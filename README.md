Steps to get it running

1. Activate your venv in Command Prompt:
   ..venv\\Scripts\\activate
2. Ensure pip exists:
   python -m ensurepip --upgrade
3. Install your package in editable mode:
   python -m pip install -e .
4. Test the import:
   python -c "import race\_pace; print(race\_pace.file)"

The expected output should be something like "C:\\Users\\RichardWood\\Documents\\race\_pace\\src\\race\_pace\\\_\_init\_\_.py

"



5\. Run the GUI:

python -m race\_pace

