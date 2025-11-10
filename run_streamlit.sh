#!/bin/bash
source /home/FranklinFranklinski/cloudprotocol/venv/bin/activate
cd /home/FranklinFranklinski/cloudprotocol
streamlit run app.py --server.port=8501 --server.enableCORS=false

#!/bin/bash
source /home/FranklinFranklinski/.virtualenvs/cloudprotocol/bin/activate
cd /home/FranklinFranklinski/cloudprotocol
streamlit run app.py --server.enableCORS=false --server.port=8501
