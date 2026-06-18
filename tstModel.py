from model.model import Model

mymodel=Model()
graph= mymodel.buildGraph("vacuole")
print(mymodel.getGraphDetails())
components_max=mymodel.getInfoConnessa()
for cm in components_max:
    print(cm)


