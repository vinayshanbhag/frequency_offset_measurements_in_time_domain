import pyvisa
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import re, string
import time

pattern = re.compile('[\W_]+')

FNAME=f"{pattern.sub('_',datetime.now().isoformat())}_ocxo_phase.csv"
RUNTIME_HOURS = 24
SAMPLE_DELAY = 0.3281
RUN_COUNT = int((1/(SAMPLE_DELAY*1.5236))*3600*RUNTIME_HOURS)
SCOPE = '<TCP/USB address of the scope>'

def main():
    rm = pyvisa.ResourceManager()
    sds = rm.open_resource(SCOPE)

    sds.read_termination='\r\n'
    sds.write_termination='\r\n'
    sds.timeout=40000
    sds.write("CHDR OFF")
    sds.write("MEAD PHA,c1-c2")   
    pd.DataFrame(columns=['timestamp','measured_phase_diff']).to_csv(FNAME,index=None)
    data =[]
    for i in tqdm(range(RUN_COUNT)):
        t,p = datetime.now().isoformat(),float(sds.query("C1-C2:MEAD? PHA").split(',')[1].strip())
        if p<0: p = 360+p
        data.append([t,p])
        if len(data)>300:
            pd.DataFrame(data).to_csv(FNAME,mode="a",index=None, header=None)
            data =[]
        time.sleep(SAMPLE_DELAY)

    pd.DataFrame(data).to_csv(FNAME,mode="a",index=None, header=None)

if __name__=='__main__':
    main()


 
