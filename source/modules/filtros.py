def filtrarProyectos(data: list) -> list:
    newName: str = ''
    lekeadData: list = []
    names: list = ['GDD','GT', 'GP0007', 'RDG', 'SP000BN'] #, 'GT', 'GP0007', 'RDG', 'SP000BN'
    for project in data:
        for name in names:
            if (project.get('key')== name):
                if ( (project.get('name').find('-')) != -1):
                    indice = project.get('name').find('')
                    newName = project.get('name').split('-')[1][1:]
                    
                    project['name'] = newName.capitalize()
                else: project['name'] = project['name'].capitalize()  
                lekeadData.append(project)
    return lekeadData