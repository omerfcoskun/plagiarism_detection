import numpy as np
import PyPDF2
import pdfplumber
import os
import pypandoc

class LCS(list):
    def lcs(m1,m2):

        common=[]

        for i in range (0,len(m1)):
            all_common = []
            Index = len(m1[i])
            max_length = 0

            matris = np.array([[0 for a in range(len(m2[0]) + 1)] for b in range(len(m1[i]) + 1)])
            for z in range(1, len(m1[i]) + 1):
                for y in range(1, len(m2[0]) + 1):
                    if m1[i][z - 1] == m2[0][y - 1]:
                        matris[z][y] = matris[z - 1][y - 1] + 1

                        if matris[z][y] > max_length:
                            max_length = matris[z][y]
                            Index = z

            common.append(m1[i][Index - max_length:Index])
        return common

class First:

    def file(m_1, m_2,w):


        file_m1 = open(m_1, "r", encoding="utf8")
        file_m2 = open(m_2, "r", encoding="utf8")

        s1 = LCS([])
        s2 = LCS([])
        sonuc = []

        for line in file_m1:
            if line == '\n':
                continue
            else:
                s1.append(line)

        metin2 = file_m2.readlines()
        sicim = ""
        for i in range(len(metin2)):
            for j in range(len(metin2[i])):
                if metin2[i] == '\n':
                    continue
                elif metin2[i][j] == '\n':
                    sicim = sicim + ' '
                else:
                    sicim = sicim + metin2[i][j]
        s2.append(sicim)

        common2 = LCS([])
        for i in range(len(s1)):
            y = len(s1[i])

            if (s1[i][y - 1:] == '\n'):
                common2.append(s1[i][:y - 1])
            else:
                common2.append(s1[i])

        common3 = LCS([])
        for i in range(len(s2)):
            z = len(s2[i])

            if (s2[i][z - 1:] == '\n'):
                common3.append(s2[i][:z - 1])
            else:
                common3.append(s2[i])

        result = common2.lcs(common3)

        if w=='E':
            file_wl = open(r"C:\Users\ASUS\Desktop\tasarım\proje\whitelist.txt", encoding="utf8")
            whitelist = file_wl.readlines()
            ortak = []

            counter=0
            for i in range(len(result)):
                switch = 0
                for j in range(len(whitelist)):

                    if result[i][:len(whitelist[j])] == whitelist[j]:
                        switch = 1
                        counter=counter+len(whitelist[j])
                        break
                    else:
                        continue
                if switch == 0:
                    ortak.append(result[i])
                else:
                    continue







        uzunluk = 0
        for i in range(len(s1)):
            uzunluk += len(list(s1[i]))

        uzunluk2 = 0
        for i in range(len(s2)):
            uzunluk2 += len(list(s2[i]))

        uzunluk3 = 0
        if w=='E':
            for i in range(len(ortak)):
                uzunluk3 += len(list(ortak[i]))
            oran = (uzunluk3 / (uzunluk-counter)) * 100
            if oran>=94:
                oran=100
            sonuc.append(round(oran))
            sonuc.append(m_2[len(m_2) - 9:])
            sonuc.append(ortak)

        else:
            for i in range(len(result)):
                uzunluk3 += len(list(result[i]))
            oran = (uzunluk3 / uzunluk) * 100
            if oran>=94:
                oran=100

            sonuc.append(round(oran))
            sonuc.append(m_2[len(m_2) - 9:])
            sonuc.append(result)


        return sonuc

    def pdf_read(a_1,a_2):
        f = open("metin1.txt", "w", encoding="utf8")
        d = open("metin2.txt", "w", encoding="utf8")
        pdfFileObj = open(a_1, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        pages = pdfReader.numPages
        pdfFileObj2 = open(a_2, 'rb')
        pdfReader2 = PyPDF2.PdfFileReader(pdfFileObj2)
        pages2 = pdfReader2.numPages

        with pdfplumber.open(a_1) as pdf:
            for i in range(pages):
                first_page=pdf.pages[i]
                f.write(first_page.extract_text())

            f.close()

        with pdfplumber.open(a_2) as pdf:
            for i in range(pages2):
                first_page=pdf.pages[i]
                d.write(first_page.extract_text())
            d.close()

    def converter(d_1, d_2):
        output = pypandoc.convert_file(d_1, 'plain', outputfile="metin1.txt")
        assert output == ""

        output = pypandoc.convert_file(d_2, 'plain', outputfile="metin2.txt")
        assert output == ""


if __name__=='__main__':
    while True:

        type = input("Hangi türdeki dosyaları karşılaştırmak istiyorsunuz? TXT(1), PDF(2), DOCX(3):")
        liste=input("Geçer listesi kullanmak istiyor musunuz? Evet(E), Hayır(H):")

        if type == '1':
            path =r"C:\Users\ASUS\Desktop\tasarım\proje\kod"
            os.chdir(path)


            for file in os.listdir():

                dosya = []
                for file2 in os.listdir():

                        file_path = f"{path}\{file}"
                        file_path2=f"{path}\{file2}"
                        if file_path==file_path2:
                            continue
                        else:
                          kod = First.file(file_path,file_path2,liste)
                          dosya.append(kod)
                maks = 0
                for i in range(len(dosya)):
                    maks = max(maks, dosya[i][0])

                for j in range (len(dosya)):
                    if dosya[j][0]==maks:
                        print("\n",file,"ile",dosya[j][1],"arasında","%",dosya[j][0],"oranında benzerlik bulunmaktadır.")
                        print(dosya[j][2])

                        a=open(file,"a",encoding="utf8")
                        x=file,"ile",dosya[j][1],"arasında",dosya[j][0],"kadar benzerlik vardır"
                        a.write("\n{} {} {} {} {} {} {}\n".format(file,"ile",dosya[j][1],"arasında","%",dosya[j][0],"oranında benzerlik bulunmaktadır."))
                        a.close()

        elif type=='2':
            path = r"C:\Users\ASUS\Desktop\tasarım\proje\pdf"
            os.chdir(path)

            for file in os.listdir():
                dosya = []
                if file.endswith(".pdf"):

                    for file2 in os.listdir():
                        if file2.endswith(".pdf"):

                            file_path = f"{path}\{file}"
                            file_path2 = f"{path}\{file2}"
                            if file_path == file_path2:
                                continue
                            else:
                                kod = First.pdf_read(file_path, file_path2)
                                txt2 = First.file("metin1.txt", "metin2.txt",liste)
                                txt2[1]=file2
                                dosya.append(txt2)
                    maks = 0
                    for i in range(len(dosya)):
                        maks = max(maks, dosya[i][0])

                    for j in range(len(dosya)):
                        if dosya[j][0] == maks:
                            print(file, "ile", dosya[j][1], "arasında", "%", dosya[j][0], "oranında benzerlik bulunmaktadır.")
                            print(dosya[j][2])
        else:
            path = r"C:\Users\ASUS\Desktop\tasarım\proje\word"
            os.chdir(path)

            for file in os.listdir():
                dosya = []
                if file.endswith(".docx"):

                    for file2 in os.listdir():
                        if file2.endswith(".docx"):

                            file_path = f"{path}\{file}"
                            file_path2 = f"{path}\{file2}"
                            if file_path == file_path2:
                                continue
                            else:
                                kod = First.converter(file_path, file_path2)
                                txt2 = First.file("metin1.txt", "metin2.txt",liste)
                                txt2[1] = file2
                                dosya.append(txt2)
                    maks = 0
                    for i in range(len(dosya)):
                        maks = max(maks, dosya[i][0])

                    for j in range(len(dosya)):
                        if dosya[j][0] == maks:
                            print(file, "ile", dosya[j][1], "arasında", "%", dosya[j][0], "oranında benzerlik bulunmaktadır.")
                            print(dosya[j][2])



