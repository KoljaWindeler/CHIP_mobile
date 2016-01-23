locationOfScript=$(dirname "$(readlink -e "$0")")
cd $locationOfScript/python;
python3 main.py
