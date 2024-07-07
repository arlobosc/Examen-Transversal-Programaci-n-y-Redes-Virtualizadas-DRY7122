while True:
	vlan = int(input("ingrese VLAN: "))
	print(vlan)
	if vlan <= 1005:
		print("Rango normal de VLAN")
	elif vlan <= 4094:
		print("Rango extendido de VLAN")
	else:
		print("Rango invalido de VLAN")

	pregunta = input("Seguir consultando? (S/N): ")
	if pregunta.lower() != "s":
		break
