import cv2
from imutils.video import WebcamVideoStream
import imutils
import numpy as np
import os
from PIL import Image
import PIL
from PIL import ImageOps
def izleri_analizet(cap,sonframeno,minimum_frame_izi):
 (arr,globalw) = kisitespit_Dizi(vs,sonframeno)
 arrydk=arr
 boyut=len(arrydk)
 kisisay=0
 for say in range(0,boyut):
 if arrydk[say][4]!=-1:
 try:
 arriztkp2 = iz_takip(arrydk, say)
 if(len(arriztkp2)>minimum_frame_izi):
 #arriztkp2 = iz_takip(arrydk, 22)
 kisisay=kisisay+1
 kisi_iz_kayit(arrydk, arriztkp2, cap,kisisay,globalw)
 arrydk=dizioptimize(arrydk, arriztkp2)
 except Exception as ex:
 print(ex)
 print(" ")
------------
def dizioptimize(kisilerar,kisiizar):
 boyut=len(kisiizar)
 for t in range(0,boyut):
 index = kisiizar[t]
 kisilerar[index][4]=-1
 return kisilerar
------------
def kisi_iz_kayit(kisilerar,kisiizar,capt,kisisayi,globalw)
 videoad="pragyol"#BU BÖLÜM GELEN DEĞERE GÖRE DEĞİŞECEK
 dosyaolustur(videoad)
 altyol="kisi"+str(kisisayi)#BU BÖLÜM GELEN DEĞERE GÖRE DEĞİŞECEK
 for k in range(0,len(kisiizar)):
 index=kisiizar[k]
 resimad=str(k)
 x=kisilerar[index][0]
 y=kisilerar[index][1]
 w=kisilerar[index][2]
 h=kisilerar[index][3]
 frameno=kisilerar[index][4]
 ilerigidilmemiktar=50
 resim =siluet_donusum(x, y, w, h, frameno, ilerigidilmemiktar, capt)
 resimkaydet(videoad, altyol, resimad, resim,globalw)
 norm_resim =kisiyi_al(x, y, w, h, frameno,capt)
 norm_resimkaydet(videoad, altyol, resimad, norm_resim,globalw)
------------
def resimkaydet(ustdizin,resim_dizin,resimad,resim,globalw):
 yol1=ustdizin+"/"+resim_dizin+"_silutet"
 yol=yol1+"/"+resimad+".jpeg"
 dosyaolustur(yol1)
 mesaj = yol1 + "Adlı Dizinde Fotoğraflar Oluşturuldu"
 print(yol1)
 #resim = imutils.resize(resim, width=globalw,height=,)
 #resim = resim.resize((int(globalw), int(globalw*2.7)), Image.ANTIALIAS)
 res = PIL.Image.fromarray(resim)
 #res =ImageOps.expand(res, border=globalw) # ,fill=0 yani siyah şeklinde değiştirilebilir
 res = ImageOps.fit(res,(int(globalw), int(globalw*2.7)),method=0, bleed=0.0, centering=(0.5, 0.5))
 res.save(yol)
------------
def norm_resimkaydet(ustdizin,resim_dizin,resimad,resim,globalw):
 yol1=ustdizin+"/"+resim_dizin+"_normal"
 yol=yol1+"/"+resimad+".jpeg"
 dosyaolustur(yol1)
 mesaj=yol1+"Adlı Dizinde Fotoğraflar Oluşturuldu"
 print(yol1)
 #resim = imutils.resize(resim, width=globalw,height=globalw*2)
 #resim = resim.resize((int(globalw), int(globalw*2.7)), Image.ANTIALIAS)
 res = PIL.Image.fromarray(resim)
 # res =ImageOps.expand(res, border=globalw) # ,fill=0 yani siyah şeklinde değiştirilebilir
 res = ImageOps.fit(res, (int(globalw), int(globalw * 2.7)), method=0, bleed=0.0, centering=(0.5, 0.5))
 res.save(yol)
def dosyaolustur(dizin_ad):
 if not os.path.exists(dizin_ad):
 os.mkdir(dizin_ad)
------------
def kisiyi_al(x,y,w,h,frameno,captre):
 vs1 = captre
 vs1.set(1,frameno)
 ret, ss1 = vs1.read()
 ss1 = imutils.resize(ss1, width=2000)
 kisi= ss1[ y:y+h,x:x+w]
 return (kisi)
------------
def siluet_donusum(x,y,w,h,frameno,ilerigidilmemiktar,captre):
 ileridekiframe = frameno + ilerigidilmemiktar
 vs1 = captre
 vs1.set(1,frameno)
 ret, ss1 = vs1.read()
 ss1 = imutils.resize(ss1, width=2000)
 vs = captre
 vs.set(1,ileridekiframe)
 ret, ss = vs.read()
 ss = imutils.resize(ss, width=2000)
 crop_img1= ss1[ y:y+h,x:x+w]
 crop_img= ss[ y:y+h,x:x+w]
 yenibasx=int(round(w/4))
 yenibasy=int(round(h/4))
 arkaortalama = np.average(crop_img)
 ortaya_zoom1=crop_img1[ yenibasy:h-yenibasy,yenibasx:w-yenibasx]
 insanlıortalama = np.average(ortaya_zoom1)#BU ALAN ÇOK ÖNEMLİ
 ortalamalar_farki=insanlıortalama-arkaortalama#BURADA POZİTİF VEYA NEGATİFE
 esik_deger=128+ortalamalar_farki
 (thresh, esiklenmis11) = cv2.threshold(crop_img1, esik_deger, 255,1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
 (thresh, esiklenmis12) = cv2.threshold(crop_img1, esik_deger, 255,0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
 (thresh, esiklenmis21) = cv2.threshold(crop_img, esik_deger, 255,1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
 (thresh, esiklenmis22) = cv2.threshold(crop_img, esik_deger, 255,0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
 farktr1=esiklenmis11-esiklenmis21
 farktr2=esiklenmis12-esiklenmis22
 farktr3=esiklenmis21-esiklenmis11
 farktr4=esiklenmis22-esiklenmis12
 #Hangisi sonuç daha büyükse beyaz daha çoktur.O alınmalıdır
 sonuc1_farklar_ort=np.average(farktr1)#farktr4 ile benzerdir
 sonuc2_farklar_ort=np.average(farktr3)#farktr2 ile benzerdir
 sonuc_fark=1
 if(sonuc1_farklar_ort>sonuc2_farklar_ort):
 sonuc_fark=(farktr1+farktr4)-(farktr2+farktr3)*2#BU ALAN İF'İLE HANGİSİ BÜYÜKSE ONA GÖRE UYGULANACAK
 else:
 sonuc_fark=(farktr2+farktr3)-(farktr1+farktr4)*2
 return (sonuc_fark)
------------
def iz_takip(dizi,sira):
 dizi1=dizi
 sira1=sira
 arriz = []
 index_eski=sira1
 arriz.append(index_eski)
 r=1
 while True:
 (doluluk,index_yeni)=sonraki_iz(dizi1,index_eski)
 if doluluk==0:
 (index_yeni)=eslesme(dizi1, index_eski, 2)
 if index_yeni==0:
 (index_yeni) = eslesme(dizi1, index_eski, 3)
 if index_yeni==0:
 r=0
 if(r!=0):
 arriz.append(index_yeni)
 index_eski=index_yeni
 else:
 break
 return arriz
------------
def sonraki_iz(dizi,sira):
 dizit=dizi
 sirat=sira
 xa=dizit[sirat][0]
 ya=dizit[sirat][1]
 wa=dizit[sirat][2]
 ha=dizit[sirat][3]
 ucxa=xa+wa
 ucya=ya+ha
 tolw = wa * 0.1#BU TOLERANS DEĞERLERİ ÇOK ÖNEMLİ DEĞİŞTİRİLEBİLİR
 tolh = ha * 0.1#BU TOLERANS DEĞERLERİ ÇOK ÖNEMLİ DEĞİŞTİRİLEBİLİR
 xil = xa+tolw#olabilecek ilerideki kordinat
 yil= ya+tolh#olabilecek yukarıdaki kordinat
 xger = xa-tolw#olabilecek gerideki kordinat
 yger= ya-tolh#olabilecek aşağıdaki kordinat
 (frbas, frbit) = aralik_bilgi(dizit, sirat)
 frsay=frbas
 sonrakiizindex=1
 frileri=0
 while True:
 if(frbit==-1):
 sonrakiizindex = 0
 break
 xb = dizit[frsay][0]
 yb = dizit[frsay][1]
 wb = dizit[frsay][2]
 hb = dizit[frsay][3]
 ucxb = xb + wb
 ucyb = yb + hb
 farkx=abs(xb-xa)
 farky=abs(yb-ya)
 farkucx=abs(ucxa-ucxb)
 farkucy=abs(ucya-ucyb)
 if (farkx<tolw and farkucx<tolw and farky<tolh and farkucy<tolh):
 break
 #if (((xb<xil and xb>xger) and (yb<yil and yb >yger)) and ((xb+wb<xil+wa and xb+wb>xger+wa) and (yb+hb<yil+ha and yb+hb
>yger+ha))):
 # sonrakiizindex=frsay
 # break
 if (frsay>frbit):#BURADA frileri eğer o frame'de yok ise işaretleme yapılır
 frileri=frileri+1
 (frbas, frbit) = aralik_bilgi(dizit, frbit)
 frsay=frbas
 if frileri==2:
 sonrakiizindex = 0#BUNUN DEĞİŞTİRİLDİĞİ BAŞKA BİR YER YOK DİKKAT BU
 #BU ÖNEMLİ
 break
 #if (frileri==2):
 #frsay=0#DİKKAT BURADA DÖNÜŞ 0 İSE SONRAKİ FRAME BULUNAMADI DEMEKTİR
 #break
 frsay = frsay + 1
 return (sonrakiizindex,frsay)
------------
def eslesme(dizi, sira, n_frame_ileri):
 dizit1 = dizi
 sirat1 = sira
 fr_iler=n_frame_ileri
 mevcut_frm_no=dizit1[sirat1][4]
 if(mevcut_frm_no==-1):
 return 0
 ist_frame_no=mevcut_frm_no+fr_iler
 (frm_bas,frm_bit)=frame_aralik_bilgi(dizit1, ist_frame_no)
 xa = dizit1[sirat1][0]
 ya = dizit1[sirat1][1]
 wa = dizit1[sirat1][2]
 ha = dizit1[sirat1][3]
 ucxa = xa + wa
 ucya = ya + ha
 tolw = (wa * 0.1)*fr_iler # BU TOLERANS DEĞERLERİ ÇOK ÖNEMLİ DEĞİŞTİRİLEBİLİR
 tolh = (ha * 0.1)*fr_iler # BU TOLERANS DEĞERLERİ ÇOK ÖNEMLİ DEĞİŞTİRİLEBİLİR
 fr_say = frm_bas
 while True:
 if (frm_bit == -1):
 fr_say = 0
 break
 xb = dizit1[fr_say][0]
 yb = dizit1[fr_say][1]
 wb = dizit1[fr_say][2]
 hb = dizit1[fr_say][3]
 ucxb = xb + wb
 ucyb = yb + hb
 farkx = abs(xb - xa)
 farky = abs(yb - ya)
 farkucx = abs(ucxa - ucxb)
 farkucy = abs(ucya - ucyb)
 if (farkx < tolw and farkucx < tolw and farky < tolh and farkucy < tolh):
 break
 fr_say = fr_say + 1
 if(fr_say>frm_bit):
 fr_say=0
 break
 return (fr_say)
------------
def aralik_bilgi(dizi,sira):
 sirat=sira
 framenum=dizi[sirat][4]
 try:
 while dizi[sirat][4]==framenum:
 sirat=sirat+1
 fbas=sirat
 framenum=dizi[sirat][4]
 while dizi[sirat][4]==framenum:
 sirat=sirat+1
 fbit=sirat
 except:
 fbas=0
 fbit = -1
 return (fbas,fbit)
------------
def frame_aralik_bilgi(dizi,istenen_frame_no):
 dzi=dizi
 frm_baslangic=0
 frm_bitis=0
 ist_framno = istenen_frame_no
 mevcut_index=0
 mevcut_frame_no=0
 try:
 while (mevcut_frame_no<ist_framno):
 mevcut_frame_no=dzi[mevcut_index][4]
 frm_baslangic = mevcut_index
 mevcut_index = mevcut_index + 1
 mevcut_frame_no1=0
 mevcut_index1=0
 ist_framno1=ist_framno+1
 while (mevcut_frame_no1 < ist_framno1):
 mevcut_frame_no1 = dzi[mevcut_index1][4]
 frm_bitis = mevcut_index1
 mevcut_index1 = mevcut_index1 + 1
33
 except:
 frm_baslangic=0
 frm_bitis=-1
 return (frm_baslangic,frm_bitis-1)
------------
def inside(r, q):
 rx, ry, rw, rh = r
 qx, qy, qw, qh = q
 return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh
------------
def draw_detections(img, rects, thickness = 1):
 for x, y, w, h in rects:
 pad_w, pad_h = int(0.15*w), int(0.05*h)
 cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)
------------
def kisitespit_Dizi(vs,framesayi):
 print("%d .Frame'e Kadar Analiz Yapılacaktır."%framesayi)
 hog = cv2.HOGDescriptor()
 hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )
 say=0
 #iz = [[0] * 5] * 1000#BU ARTTIRILABİLİR İLERİDE DAHA ÇOK KİŞİ TESPİT EDİLECEĞİ İÇİN
 arr = []
 length_fr = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))#BU KAÇ FRAMEDEN OLUŞTUĞU BİLGİSİNİ VERİR ÖNEMLİ
 yuzdeframe_mik = str((100 * framesayi) / length_fr)
 print("Mevcut Video'da %d Adet Frame Bulunmaktadır."%length_fr)
 print("Framelerin Yüzde %s Kadarı Analiz Edilecektir"%yuzdeframe_mik)
 globalw = 0
 print("")
 frno=0
 while True:
 _, frame = vs.read()
 frame = imutils.resize(frame, width=2000)
 gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 gray = cv2.GaussianBlur(gray, (21, 21), 0)
 say=say+1
34
 found, w = hog.detectMultiScale(frame, winStride=(8,8), padding=(32,32), scale=1.05)
 found_filtered = []
 for ri, r in enumerate(found):
 for qi, q in enumerate(found):
 if ri != qi and inside(r, q):
 break
 else:
 found_filtered.append(r)
 kx1=0
 kx2=0
 framedeki_kisi=0
 for (x,y,w,h) in found_filtered:
 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
 kx1=x
 if kx2!=kx1:
 framedeki_kisi=framedeki_kisi+1
 arr.append([x,y,w,h,say])
 if(w>globalw):
 globalw=w
 #print ("x=%d y=%d w=%d h=%d say=%d" %(x ,y ,w, h,say))
 #cv2.imshow('image',frame)
 kx2=x
 #key = cv2.waitKey(1) & 0xFF
 print("%d .Frame'de Bulunan Kişiler Tespit Edildi %d Adet Kişi Bulunuyor"%(say,framedeki_kisi))
 if say==framesayi:#BURADA GİDİLMEK İSTENEN YAKLAŞIK FRAME DEĞERİ VERİLİR
 break
 return (arr,globalw)
------------
vs = cv2.VideoCapture('TownCentreXVID.avi')
sonframe=10
minimum_frameiz=10
izleri_analizet(vs,sonframe,minimum_frameiz)
cv2.destroyAllWindows()
vs.stop()
