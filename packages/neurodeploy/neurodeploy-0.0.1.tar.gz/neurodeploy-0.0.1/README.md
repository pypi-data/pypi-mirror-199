
#Generate doc
sphinx-apidoc -o doc/source/ ./neurodeploy
sphinx-build -b html doc/source doc/build
sphinx-build -b pdf doc/source doc/build
#find pdf under doc/build
##################################"

venv 
python -m venv  venv
source venv/bin/activate

subcmd -> querie -> utils -> query // get data
                 -> proceess -> utils ->  file //process data
#######################################################################
//help
 python cli.py  --help
 python cli.py  model --help

1-Auth to API

 - By getting yout token
   //user login
   python cli.py  user login  --user-name YOUR_MODEL_NAME  --password YOUR_PASSWORD
 or:
 - By config your key /secret/ 
    python cli.py  config
    provide your name , access key , secret_key

2- create and upload your model
 
 //model push
 python cli.py model push --model-name YOUR_MODEL_NAME --file-path /YOUR_PATH/YOUR_MODEL_FILE_NAME

3- predict your model
 python cli.py model predict --model-name YOUR_MODEL_NAME  --user-name USER_NAME --data '{"payload": [[1, 2, 3, 4, 5]]}'


Other useful cmd: 

//model delete
 python cli.py  model delete  --model-name YOUR_MODEL_NAME
//model list
 python cli.py  model list
//model_get
 python cli.py  model get  --model-name YOUR_MODEL_NAME

###############################################
run test sh test.py 
###############################################
build package

python -m pip install –-user –-upgrade setuptools wheel
python setup.py sdist bdist_wheel

twine check dist/*
twine upload dist/*
python -m twine upload dist/*
###############################################
//create credential
 python cli.py  credentials create --credentials-name CREDENTIAL_NAME  --credentials-desc CREDENTIAL_DESC
//delete credential
 python cli.py  credentials delete  --credentials-name CREDENTIAL_NAME
//list credentials
 python cli.py  credentials list




