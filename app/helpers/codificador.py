
def codificar(coordenadas):
    #Recibe string con formato [ [a,b], [c,d] ] y devuelve string con formato a#b@c#d
    st = []
    if isinstance(eval(coordenadas),list):
        lista_coord = eval(coordenadas)
        for index, coord in enumerate(lista_coord):
            if(index!=len(lista_coord)-1):
                st.extend((str(coord[0]),'#',str(coord[1]),'@'))
            else:
                st.extend((str(coord[0]),'#',str(coord[1])))
    return ''.join(st)

def decodificar(coordenadas):
    #Recibe string con formato a#b@c#d y devuelve una lista [ [a,b], [c,d] ]
    list = []
    for coord in coordenadas.split('@'):
        lat,long = coord.split('#')
        list.append([lat,long])

    return list


def decodificar_para_json(coordenadas):
    #Recibe string con formato a#b@c#d y devuelve una lista [ [a,b], [c,d] ]
    list = []
    for coord in coordenadas.split('@'):
        lat,long = coord.split('#')
        list.append(['lat: ',lat,'long: ',long])

    return list