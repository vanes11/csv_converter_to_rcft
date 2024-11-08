#import random
import csv
import json
#from itertools import * # to transpose files




# JSON : JavaScript Object Notation

def data_config(config_file):
    """ read the json file that encode the information about the 
    relational context family : file name, identifier, source/target data
    K: dictionary describing formal context
    R : dictionary describing the relational context """

    with open(config_file) as f:
        data = json.load(f)   
        keys = list(data.keys())
        K = data[keys[0]]
        R = data[keys[1]]

    return K, R


        


def rcf_to_rca_format(K, R, rca_data, scaling = "exist", inverse_relation = False):
    """ K dictionary describing formal context (context.scv : "context_id"),  R : dictionary describing the relational context (relation name, source, target)
    - "scaling" represents the quantifier to be used, by default it is "exist".
    - The booleen "inverse_relation" indicates the consideration of inverse relationships. by default, inverse relations are not considered
    -  "rca_data" is the name of the .crft file to be constructed i.e a string of the form:rca_data.crft """
  

    with open(rca_data, 'w') as textfile:
        # formal context file reading
        for file in K.keys() : 
            with open(file, 'r') as csvfile:
                lecteur_csv = csv.reader(csvfile)
                header = next(lecteur_csv)
                textfile.write("FormalContext "+ header[0] +'\n')
                textfile.write("algo fca \n")          
                header[0] = ''
                line = '|'.join(str(e) for e in header)
                line = '|'+line +'|'
                textfile.write(line + '\n')

                for row in lecteur_csv:
                    line  = '|'.join(str(e) for e in row) 
                    line  =  '|'+line +'| \n'  
                    textfile.write(line) 
                textfile.write('\n')  

        for file in R : 
            # relational context reading
            with open(file["nom"], 'r') as csvfile:
                lecteur_csv = csv.reader(csvfile)
                header = next(lecteur_csv)

                textfile.write("RelationalContext "+ header[0] +'\n')

                textfile.write("source "+ K[file["source"]]+'\n')
                textfile.write("target "+ K[file["target"]] +'\n')
                textfile.write("scaling "+ scaling +'\n')

                header[0] = ''
                line = '|'.join(str(e) for e in header)
                line = '|'+line +'|'
                textfile.write(line+ '\n')

                for row in lecteur_csv:
                    line  = '|'.join(str(e) for e in row) 
                    line  =  '|'+line +'| \n'  
                    textfile.write(line)   
                textfile.write('\n')  

    # inverse relationship processing

        if inverse_relation :
            for file in R : 
                with open(file["nom"], 'r') as csvfile:
                    lecteur_csv = zip(*csv.reader(csvfile))  # file transposition. In this transposed version, each line is a tuple
                   
                    header = list(next(lecteur_csv))
                    textfile.write("RelationalContext "+ header[0]+'_r' +'\n')    # add the string “_r” to the relationship name to indicate that it is an inverse relationship

                    textfile.write("source "+ K[file["target"]]+'\n')    # the source becomes the target and vice versa
                    textfile.write("target "+ K[file["source"]] +'\n')
                    textfile.write("scaling "+ scaling +'\n')

                    header[0] = ''
                    line = '|'.join(str(e) for e in header)
                    line = '|'+line +'|'
                    textfile.write(line+ '\n')

                    for row in lecteur_csv:
                        line  = '|'.join(str(e) for e in row) 
                        line  =  '|'+line +'| \n'  
                        textfile.write(line)   
                    textfile.write('\n')  


       


def rcf_to_graph_context(K, R, graph_context):
    """K dictionary describing formal context (context.scv : "context_id"),  
    R : dictionary describing the relational context (relation name, source, target)
    "graph_context" is the name of the .p file to be constructed i.e the string of the form : graph_context.p"""
    
    # formal context file reading
    with open(graph_context, 'w') as textfile:
        textfile.write(':-' + '\n')

        for file in K.keys():
            with open(file, 'r') as csvfile:
                lecteur_csv = csv.reader(csvfile)
                attributes = next(lecteur_csv)
                
                textfile.write('% ' +'contexte '+attributes[0] +'\n')

                for row in lecteur_csv:

                    ligne =''
                    ligne +=  row[0] + ' : ['

                    for i in range(1,len(row)):
                    
                        if row[i] =='x':
                            ligne += attributes[i]+' , '
                   
                    if ligne[-1] != "[": #newly added
                        ligne = ligne[:-3] # delete the last 3 characters " , "

                    ligne += '],'
                    textfile.write(ligne +'\n')

                textfile.write('\n')


    #relational context reading
        for file in R :            
            with open(file["nom"], 'r') as csvfile:
                lecteur_csv = csv.reader(csvfile)
            
                attributes = next(lecteur_csv)
                textfile.write('% ' +'contexte  relationnel '+attributes[0] +'\n')

                for j,row in enumerate(lecteur_csv):
                    ligne =''
                    ligne +=  row[0] + ' : [' + attributes[0]+' '

                    for i in range(1,len(row)):
                    
                        if row[i] =='x':
                            ligne += attributes[i]+' & '
                    
                    if ligne[-2] == "&":
                        ligne = ligne[:-3]

                    else:
                        ligne = row[0] + ' : ['   #for objects that do not have relationships i.e. when row = [R1].
                
                    ligne += '],'

                    textfile.write(ligne +'\n')
                textfile.write('\n')
            
    
    # modification of the last line of the file to mark the end of the file with '.'.'
    with open(graph_context) as textfile:
        lignes = textfile.readlines()
        del lignes[-1] # the last line is '\n'
        line = lignes[-1][ : -2] # [: -2] to remove '\n' and ','
        lignes[-1] = line +'.\n'

    with open(graph_context, 'w') as textfile:
        for line in lignes:
            textfile.write(line)




if __name__ =="__main__":

    K, R  = data_config("car_person.json")
    rcf_to_rca_format(K, R, "car_person_r.rcft", inverse_relation = True)
    rcf_to_rca_format(K, R, "car_person.rcft")
    rcf_to_graph_context(K, R, "car_person.p")
    
