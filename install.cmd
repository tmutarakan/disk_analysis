$path = "venv"
if (Test-Path $path){
	Remove-Item -LiteralPath $path -Force -Recurse
}
python -m venv venv
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\pip install -r requirements.txt