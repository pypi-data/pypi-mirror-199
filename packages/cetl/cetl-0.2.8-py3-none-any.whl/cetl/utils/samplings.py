import numpy as np

def generate_batches(samples_in_batch=100, items_list=None):
    population=len(items_list)
    batches =[]
    batch=[]
    for i in np.arange(population):
        if len(batch) < samples_in_batch-1:
            batch.append(items_list[i])
        else:
            batch.append(items_list[i])
            batches.append(batch)
            batch=[]

        if i == population-1 and len(batch)>0:
            batches.append(batch)
        
    return batches