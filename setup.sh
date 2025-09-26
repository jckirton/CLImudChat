fileDir=$(dirname $0)

# echo $fileDir/.venv

python3 -m venv $fileDir/.venv

source $fileDir/.venv/bin/activate

# echo "$fileDir/requirements.txt"
pip install -r $fileDir/requirements.txt

$fileDir/.venv/bin/python $fileDir/setup.py

rm $0