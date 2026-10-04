import ast
import operator
import os


print("Nova 0.7")


degiskenler = {}
ekran = []



# HATA SİSTEMİ


def hata(mesaj):
    print(f"Hata: {mesaj}")



# DEĞİŞKEN / İFADE SİSTEMİ

class NovaExpressionEvaluator(ast.NodeVisitor):

    def visit_Constant(self, node):
        # String, int, float, bool 
        return node.value

    def visit_Name(self, node):
        isim = node.id

        if isim in degiskenler:
            return degiskenler[isim]

        raise NameError(f"'{isim}' değişkeni bulunamadı.")

    def visit_BinOp(self, node):
        sol = self.visit(node.left)
        sag = self.visit(node.right)

        if isinstance(node.op, ast.Add):
            return sol + sag

        if isinstance(node.op, ast.Sub):
            return sol - sag

        if isinstance(node.op, ast.Mult):
            return sol * sag

        if isinstance(node.op, ast.Div):
            if sag == 0:
                raise ZeroDivisionError("Bir sayı 0'a bölünemez.Bölünürse 0 çıkar")

            return sol / sag

        raise ValueError("Bu matematik işlemi şimdilik yok")

    def visit_UnaryOp(self, node):
        deger = self.visit(node.operand)

        if isinstance(node.op, ast.USub):
            return -deger

        if isinstance(node.op, ast.UAdd):
            return +deger

        raise ValueError("Desteklenmeyen işaret")

    def generic_visit(self, node):
        raise ValueError("Geçersiz ifade")


def ifade_coz(ifade):
    ifade = ifade.strip()

    if not ifade:
        raise ValueError("Boş ifade kullanılamaz")

    # Nova'daki x = çarpma işaretini Python AST için * yapıyoruz.
    # Sadece bağımsız bir x operatörünü değiştirmek için token mantığı
    # kullanıyoruz.
    ifade = ifade.replace(" x ", " * ")

    try:
        agac = ast.parse(ifade, mode="eval")
        sonuc = NovaExpressionEvaluator().visit(agac.body)
        return sonuc

    except SyntaxError:
        raise SyntaxError("Geçersiz ifade.")

    except Exception as e:
        raise e



# PARANTEZ KONTROLÜ

def komut_parantez_kontrol(kod, komut):
    baslangic = f"{komut}("

    if not kod.startswith(baslangic):
        return False

    if not kod.endswith(")"):
        hata(f"{komut} komutunun parantezi kapatılmamış")
        return False

    return True



# YAZ KOMUTU


def yaz_komutu(kod):
    if not komut_parantez_kontrol(kod, "yaz"):
        return False

    metin = kod[4:-1].strip()

    if not metin:
        hata("yaz() komutu boş bırakılamaz")
        return True

    try:
        sonuc = ifade_coz(metin)

        ekran.append(sonuc)
        print(sonuc)

    except NameError as e:
        hata(str(e))

    except Exception:
        hata("yaz() içinde geçersiz bir ifade var")

    return True



# SORU KOMUTU

def soru_komutu(kod):
    if not komut_parantez_kontrol(kod, "soru"):
        return None

    metin = kod[5:-1].strip()

    if not metin:
        return input()

    try:
        prompt = ifade_coz(metin)

        if not isinstance(prompt, str):
            prompt = str(prompt)

        cevap = input(prompt)

        # Sayıysa otomatik olarak int veya float yap
        cevap = cevap.strip()

        try:
            if cevap.startswith("-") or cevap.startswith("+"):
                sayi_kismi = cevap[1:]
            else:
                sayi_kismi = cevap

            if sayi_kismi.isdigit():
                cevap = int(cevap)

            elif (
                sayi_kismi.count(".") == 1
                and sayi_kismi.replace(".", "").isdigit()
            ):
                cevap = float(cevap)

        except ValueError:
            pass

        return cevap

    except NameError as e:
        hata(str(e))

    except Exception:
        hata("soru() içinde geçersiz bir ifade var.")

    return None



# DEĞİŞKEN ATAMA


def degisken_ata(kod):

    if "=" not in kod:
        return False

    # İlk = işaretinden böl
    isim, deger = kod.split("=", 1)

    isim = isim.strip()
    deger = deger.strip()

    if not isim:
        hata("Değişken adı boş bırakılamaz")
        return True

    # Değişken adının geçerli olup olmadığını kontrol et
    if not isim.replace("_", "a").isalnum():
        hata(f"'{isim}' geçerli bir değişken adı değil")
        return True

    # Değişken adı rakamla başlayamaz
    if isim[0].isdigit():
        hata(f"'{isim}' geçerli bir değişken adı değil.")
        return True

    if not deger:
        hata("Değişkene boş değer verilemez.")
        return True

    try:

        # soru()
        if deger.startswith("soru("):

            if not deger.endswith(")"):
                hata("soru() komutunun parantezi kapatılmamış.")
                return True

            cevap = soru_komutu(deger)

            if cevap is not None:
                degiskenler[isim] = cevap

            return True

        # Normal ifade
        sonuc = ifade_coz(deger)
        degiskenler[isim] = sonuc

    except NameError as e:
        hata(str(e))

    except ZeroDivisionError as e:
        hata(str(e))

    except TypeError:
        hata("Uyumsuz veri türleriyle işlem yapılamaz.")

    except SyntaxError:
        hata("Geçersiz sözdizimi.")

    except Exception:
        hata("Değişken değerinde geçersiz bir ifade var.")

    return True


# SİL KOMUTU


def sil_komutu(kod):

    if not komut_parantez_kontrol(kod, "sil"):
        return False

    metin = kod[4:-1].strip()

    if metin:
        hata("sil() komutu parametre kabul etmez.")
        return True

    degiskenler.clear()
    ekran.clear()

    # Windows
    if os.name == "nt":
        os.system("cls")

    # Linux / Pardus / macOS
    else:
        os.system("clear")

    return True



# KOŞUL DEĞERLENDİRME


def kosul_coz(kosul):

    kosul = kosul.strip()

    operatorler = [
        (">=", operator.ge),
        ("<=", operator.le),
        ("==", operator.eq),
        ("!=", operator.ne),
        (">", operator.gt),
        ("<", operator.lt),
        ("=", operator.eq)
    ]

    for sembol, islem in operatorler:

        if sembol in kosul:

            sol, sag = kosul.split(sembol, 1)

            sol = sol.strip()
            sag = sag.strip()

            if not sol or not sag:
                raise SyntaxError("Koşul eksik")

            sol_deger = ifade_coz(sol)
            sag_deger = ifade_coz(sag)

            try:
                return islem(sol_deger, sag_deger)

            except TypeError:
                raise TypeError(
                    "Koşuldaki değerlerin türleri karşılaştırılamıyor"
                )

    raise SyntaxError("Geçerli bir karşılaştırma operatörü bulunamadı")



# KOMUT ÇALIŞTIRMA


def komut_calistir(kod):

    kod = kod.strip()

    if not kod:
        return

    # -----------------------------------------------------
    # yorum
    # -----------------------------------------------------

    if kod.startswith("#"):
        return

    # -----------------------------------------------------
    # yaz()
    # -----------------------------------------------------

    if kod.startswith("yaz("):
        yaz_komutu(kod)
        return

    # -----------------------------------------------------
    # soru()
    # -----------------------------------------------------

    if kod.startswith("soru("):

        if "=" not in kod:
            soru_komutu(kod)

        return

    # -----------------------------------------------------
    # sil()
    # -----------------------------------------------------

    if kod.startswith("sil("):
        sil_komutu(kod)
        return

    # -----------------------------------------------------
    # eğer
    # -----------------------------------------------------

    if kod.startswith("eğer "):
        eger_komutu(kod)
        return

    # -----------------------------------------------------
    # değilse
    # -----------------------------------------------------

    if kod == "değilse":
        hata("'değilse' tek başına kullanılamaz.")
        return

    # -----------------------------------------------------
    # değişken
    # -----------------------------------------------------

    if "=" in kod:
        degisken_ata(kod)
        return

    # -----------------------------------------------------
    # bilinmeyen komut
    # -----------------------------------------------------

    hata(f"Bilinmeyen komut: {kod}")



# EĞER KOMUTU


def eger_komutu(kod):

    icerik = kod[5:].strip()

    if ":" not in icerik:
        hata("eğer komutunda ':' bulunamadı")
        return

    kosul, komut = icerik.split(":", 1)

    kosul = kosul.strip()
    komut = komut.strip()

    if not kosul:
        hata("eğer koşulu boş bırakılamaz")
        return

    if not komut:
        hata("eğer komutunun çalıştıracağı komut bulunamadı")
        return

    try:

        sonuc = kosul_coz(kosul)

        if sonuc:
            komut_calistir(komut)

    except NameError as e:
        hata(str(e))

    except ValueError as e:
        hata(str(e))

    except TypeError as e:
        hata(str(e))

    except SyntaxError as e:
        hata(str(e))

    except Exception:
        hata("Koşul değerlendirilirken bilinmeyen bir hata oluştu")



# ANA NOVA DÖNGÜSÜ


while True:

    try:

        kod = input(">")

        # çıkış komutu
        if kod.strip() in ("çık", "cik", "exit","cikis","çıkış"):
            print("Nova kapatıldı.")
            break

        komut_calistir(kod)

    except KeyboardInterrupt:
        print("Nova kapatıldı.")
        break

    except EOFError:
        print("Nova kapatıldı.")
        break

    except Exception as e:
        hata(f"Beklenmeyen hata: {e}")
