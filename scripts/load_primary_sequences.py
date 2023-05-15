from inscription.models import Sequence
import csv

def run():
    Sequence.objects.all().delete()
    #inputcsv = 'scripts/inscriptions/load_sample.csv'
    #inputcsv = 'scripts/inscriptions/Indus_Database_Sheet1.csv'
    inputcsv = 'scripts/inscriptions/df200.csv'
    csv_file = open(inputcsv,'r')
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)
    
    
    for row in csv_reader:
        csv_obj = Sequence(
            seqid=row[0],
            seq_in_num=row[1],
            links='x',
            cisi_id=row[2],
            wells_id=row[3],
            site=row[4],
            artefact_type=row[5],
            material_type=row[6],
            field_symbol=row[7],
            excavation_number=row[8],
            area=row[9],
            remark=row[10]
        )
        csv_obj.save()
        print(row)