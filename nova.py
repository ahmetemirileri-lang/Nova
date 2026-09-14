print("Nova")



degiskenler = {}
ekran = []


while True:
	kod = input(">")
	
	#ekrana yazdırma
	if kod.startswith("yaz("):
		metin = kod [4:-1]
		if metin.startswith('"') and metin.endswith('"'):
			ekran.append(metin)
			print(metin.strip('"'))
			
		
		elif metin in degiskenler:
			ekran.append(metin)
			print(degiskenler[metin])
		
	#input sistemi	
	if kod.startswith("soru(") and "=" in kod:
		metin = kod [5:-1]
		if metin.startswith('"') and metin.endswith('"'):
			ekran.append(metin.strip('"'))
			cevap = input(metin.strip('"'))
			
		elif metin in degiskenler:
			input(degiskenler[metin])
			
	
		
	
	#değişken sistemi
	if "=" in kod and not kod.startswith("eğer "):
		isim, deger = kod.split("=")
		isim = isim.strip()
		deger = deger.strip()
		
	
			
		if deger.startswith("soru("):
			metin = deger[5:-1]
			if metin.startswith('"') and metin.endswith('"'):
			   	 cevap = input(metin.strip('"'))
			    
			   	 cevap = cevap.strip()
			   	 
			if cevap.isdigit():
			  			cevap = int(cevap)
			  		
			   
			    
			    	
			    	
		degiskenler[isim] = cevap
  	
		if "+" in deger:
			sayı, sayı2 = deger.split("+")
			
			sayı = sayı.strip()
			sayı2 = sayı2.strip()
			
		
			
			if sayı in degiskenler:
				sayı = degiskenler[sayı]
			elif sayı.isdigit():
				sayı = int(sayı)
				
				
			if sayı2 in degiskenler:
				sayı2  = degiskenler[sayı2]
			elif sayı2.isdigit():
				sayı2 = int(sayı2)
			
				
				
			
			
			
				
		
			
			deger = sayı + sayı2
			
			
			
		
		
		elif "-" in deger:
			sayı, sayı2 = deger.split("-")
			
			sayı = sayı.strip()
			sayı2 = sayı2.strip()
			
		
			
			if sayı in degiskenler:
				sayı = degiskenler[sayı]
			elif sayı.isdigit():
				sayı = int(sayı)
				
				
			if sayı2 in degiskenler:
				sayı2  = degiskenler[sayı2]
			elif sayı2.isdigit():
				sayı2 = int(sayı2)
			
			
			deger = sayı - sayı2
			
		elif "x" in deger:
			sayı, sayı2 = deger.split("x")
			
			sayı = sayı.strip()
			sayı2 = sayı2.strip()
			
		
			
			if sayı in degiskenler:
				sayı = degiskenler[sayı]
			elif sayı.isdigit():
				sayı = int(sayı)
				
				
			if sayı2 in degiskenler:
				sayı2  = degiskenler[sayı2]
			elif sayı2.isdigit():
				sayı2 = int(sayı2)
			
			deger = sayı * sayı2
			
		elif "/" in deger:
		      sayı, sayı2 = deger.split("/")
		      sayı = sayı.strip()
		      sayı2 = sayı2.strip()
		      
		      if sayı in degiskenler:
		            sayı = degiskenler[sayı]
		            
		      elif sayı.isdigit():
		            sayı = int(sayı)
		            
		      if sayı2 in degiskenler:
		            sayı2 = degiskenler[sayı2]
		            
		      elif sayı2.isdigit():
		            sayı2 =  int(sayı2)
		            
		      deger = sayı/sayı2
              
		      
		      
				
		   
		elif deger.isdigit():
		  		      	deger = int(deger)
		  		      	
		  		      		 		 	
		
		if not deger.startswith("soru("):
			degiskenler[isim] = deger
		
		
		#sil komutu
	if kod.startswith("sil("):
		degiskenler.clear()
		ekran.clear()
		print("\033[H\033[J", end="")
		
	#if ama türkçe	
	if kod.startswith("eğer "):
		koşul, komut = kod[5:].split(":", 1)
		
		koşul = koşul.strip()
		komut = komut.strip()
		
		if ">" in koşul:
			isim,  sayı = koşul.split(">", 1)
			isim = isim.strip()
			sayı = int(sayı.strip())
			
			if isim in degiskenler and degiskenler[isim] > sayı:
				if komut.startswith("yaz("):
					metin = komut[4:-1]
					
					if metin.startswith('"') and metin.endswith('"'):
						print(metin.strip('"'))
						
					elif metin in degiskenler:
						print(degiskenler[metin])
						
		elif "<" in koşul:
			isim, sayı = koşul.split("<", 1)
			isim = isim.strip()
			sayı = int(sayı.strip())
			
			if isim in degiskenler and degiskenler[isim] < sayı:
				if komut.startswith("yaz("):
					metin = komut[4:-1]
					
					if metin.startswith('"') and metin.endswith('"'):
						print(metin.strip('"'))
						
					elif metin in degiskenler:
						print(degiskenler[metin])
						
						
		
		elif "=" in koşul:
			isim, sayı = koşul.split("=", 1)
			isim = isim.strip()
			sayı = int(sayı.strip())
			if isim in degiskenler and degiskenler[isim] == sayı:
				if komut.startswith ("yaz("):
					metin = komut[4:-1]	
					
					
					if metin.startswith('"') and metin.endswith('"'):
						print(metin.strip('"'))
						
					elif metin in degiskenler:
						print(degiskenler[metin])
					
					

						
			

	
