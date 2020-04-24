The python script(indri.py) can interact with user with accept parameter from linux command line and run relative bash
command in the python program.

The basic usage is as below:

usage: indri.py [-h] [-corpus CORPUS] [-topic TOPIC] [-query QUERY] [-eval]

interact with indri.

optional arguments:
  -h, --help      show this help message and exit
  -corpus CORPUS  create indexing
  -topic TOPIC    modify topic
  -query QUERY    modify query command
  -eval           carry evaluation


The program covers the steps from modifying index XML file, creating indexing for corpus, modifying topic in query XML,
modifying query command in XML, and carry evaluation.
In oder to make the script working, the following three files should be in the same path.

                my_queries.xml
                my_index_parameters.xml
                indri.py

Note: the step to change evaluation file path is not included in the script. Because when I carry the lab, I found I
never change the evaluation file once decide which evaluation file to be used. So user need to modify the hard coded
evaluation file path in the script.

                if args.eval:
                    command = "trec_eval -q -m official assessments/assessments2004/qrels_EN
                    my_run1_rankings.trec"
                    subprocess.call(command, shell=True)


Example of the running:


python3 indri.py -topic "211"

python3 indri.py -query "#combine(#syn(war conflict) #uw(peru ecuador))"

python3 indri.py -eval



