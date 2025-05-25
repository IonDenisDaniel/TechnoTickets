def mostPopular(lista_bilete):
    statistica_bilete = {}

    for bilet in lista_bilete:
        denumire = bilet.event.denumire
        if denumire in statistica_bilete:
            statistica_bilete[denumire] += 1
        else:
            statistica_bilete[denumire] = 1

    sort_statistica_bilete = dict(sorted(statistica_bilete.items(), key=lambda item: item[1], reverse = True))

    return sort_statistica_bilete
