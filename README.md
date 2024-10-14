
## Setup/Run Instructions

### Clone Repo and setup python env
```shell
git clone git clone https://github.com/dwpoulos/isoneFTR.git
cd isoneFTR
python -m venv .venv

Windows:  .venv\Scripts\activate
Mac/Linux:  source .venv/bin/activate

pip install -r requirements.txt
```

Run FTR Valuation for month (Example August 2024)
```shell
python ftr_valuation.py 08/2024
```
Result written as csv to current folder

 Example:  
 ##### **ftr_profit_loss20248.csv**


## Database
For Database can use docker-compose.yml to start up db on localhost port 5432
Credentials postgres/postgres
```shell
docker compose up
```
Ideally run scripts in ddl folder to create tables using tool such as dbeaver
or
open terminal in docker
```shell
docker exec -it isone-db bash
psql -U postgres
{run ddl scripts}
```

Return to project folder and run scripts in ddl folder
Load LMP data for day
```shell

python lmp_data_load.py 20241002

```


