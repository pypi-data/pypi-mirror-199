
def f_finalscore(score):
	a,b,c = "","",""
	if score > 449:
		a = "DIAK LOS"
		b = "A"
		c = "PROLONGO KONTRATU"
	elif score > 349:
		a = "DIAK"
		b = "B"
		c = "PROLONGO KONTRATU"
	elif score > 299:
		a = "SUFICIENTE"
		b = "C"
		c = "CHAMA DE ATENSAUN"
	else:
		a = "LADIAK"
		b = "D"
		c = "HAPARA KONTRATU"
	return a,b,c