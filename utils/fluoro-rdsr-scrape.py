import pydicom
def ScrapeData(file_name):
    ds = pydicom.read_file(file_name, force=True)


    d2 = ds.ContentSequence
    count = 0
    values=[]
    for d in d2:
        meaning =d[list(d.keys())[2]][0].CodeMeaning 
        # print(meaning)
        res = []
        vals ={}
        if meaning =="Irradiation Event X-Ray Data":
            count+=1
            content = d.ContentSequence
            vals = {}
            for c in content:

                try:
                    keys = list(c.keys())
                    # print(f"Type of c[keys[-2]: {type(c[keys[-2]])},\nType of c[keys[-1]]: {type(c[keys[-1]][0])}")

                    p =(c[keys[-1]][0])
                    if type(p) is str:
                        vals[c[keys[-2]][0].CodeMeaning] =c[keys[-1]].value 
                        # print(c[keys[-1]].value, vals)
                    elif type(p) is pydicom.dataset.Dataset:
                        if "CodeMeaning" in p:
                            vals[c[keys[-2]][0].CodeMeaning] =p.CodeMeaning 

                            # print("DS:",p.CodeMeaning, vals)
                        else:
                            # print("No code meaning", "MeasurementUnitsCodeSequence" in p)
                            if "MeasurementUnitsCodeSequence" in p:
                                vals[c[keys[-2]][0].CodeMeaning] =[p.NumericValue,p.MeasurementUnitsCodeSequence[0].CodeMeaning]

                                # print(p.MeasurementUnitsCodeSequence[0].CodeMeaning,p.NumericValue, vals)

                except Exception:
                    print(Exception)
            vals["id"]=ds.StudyID+ds.StudyDate
            values.append(vals)
    print(f"Values:{values},\n(Length: {len(values)})==(Irradiation Event Count: {count}),\nStudyID: {ds.StudyID}")
    return values
if __name__=="__main__":
    file_name = input("Enter file name")
    ScrapeData(file_name)
