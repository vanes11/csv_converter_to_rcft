from data_converter import rcf_to_rca_format as rca_converter
from data_converter import rcf_to_graph_context as gca_converter
from data_converter import data_config as config

K, R = config("car_person.json")
rca_converter(K, R, "car_person_r.rcft", inverse_relation = True)
rca_converter(K, R, "car_person.rcft")
gca_converter(K, R, "car_person.p")