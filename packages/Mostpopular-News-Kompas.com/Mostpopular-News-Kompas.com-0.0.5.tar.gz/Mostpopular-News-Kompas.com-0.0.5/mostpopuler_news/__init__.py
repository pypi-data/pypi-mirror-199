from bs4 import BeautifulSoup
import requests


def data_extraction():
    """
    Examples of the 10 most popular news

    A.Istri Pamer Harta, Ini Alasan LHKPN Pejabat Kemensetneg Esha Rahmansah Tak Bisa Ditelusuri
    Dibaca 22.974 kali

    B.Isak Tangis Iringi Jenazah Syabda Perkasa Belawa dan Ibunya Saat Tiba di Rumah Duka
    Dibaca 15.648 kali

    C.Viral, Foto Istrinya Pamer Tas Mewah Hermes dan Gucci, Sekda Riau: Itu KW, Belinya di Mangga Dua
    Dibaca 15.375 kali

    D.Kronologi Syabda Perkasa Belawa Meninggal Kecelakaan, Pahlawan Piala Thomas Berpulang...
    Dibaca 14.137 kali

    E.Kabar Duka, Tunggal Putra Indonesia Syabda Perkasa Belawa Meninggal Dunia
    Dibaca 13.526 kali

    F.Luhut ke IMF: Kalian Jangan Macam-macam...
    Dibaca 13.431 kali

    G.Saat "Netizen" Bantu KPK Bongkar Pejabat yang Pamer Harta...
    Dibaca 8.932 kali

    H.Sempat Terbengkalai di Bandara YIA, 38 Calon Jemaah Umrah Asal Rembang Pulang,
    Seorang Perantara Dilaporkan sebagai Penipu
    Dibaca 8.370 kali

    I.Kala Megawati Semprot Ribuan Kades yang Minta Anggaran Jumbo...
    Dibaca 7.712 kali

    J.Kapolda Jateng Resmi Pecat 5 Polisi yang Jadi Calo Penerimaan Bintara Polri 2022
    Dibaca 7.358 kali
    :return:
    """
    try:
        content = requests.get("https://www.kompas.com/")
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, "html.parser")

        result = soup.find("div", {"class": "most__list  clearfix"})
        result = soup.findChildren("h4")

        i = 0
        A = None
        B = None
        C = None
        D = None
        E = None
        F = None
        G = None
        H = None
        I = None
        J = None
        for res in result:
            if i == 1:
                A = res.text
            elif i == 2:
                B = res.text
            elif i == 3:
                C = res.text
            elif i == 4:
                D = res.text
            elif i == 5:
                E = res.text
            elif i == 6:
                F = res.text
            elif i == 7:
                G = res.text
            elif i == 8:
                H = res.text
            elif i == 9:
                I = res.text
            elif i == 10:
                J = res.text
            i = i + 1

        results = dict()
        results["A"] = A
        results["B"] = B
        results["C"] = C
        results["D"] = D
        results["E"] = E
        results["F"] = F
        results["G"] = G
        results["H"] = H
        results["I"] = I
        results["J"] = J
        return results
    else:
        return None


def data_show(result):
    if result is None:
        print("Couldn't find the Most Popular News data from the Kompas.com site")
        return
    print("\nThe 10 most popular news based on Kompas.com site")
    print(f"1. {result['A']}")
    print(f"2. {result['B']}")
    print(f"3. {result['C']}")
    print(f"4. {result['D']}")
    print(f"5. {result['E']}")
    print(f"6. {result['F']}")
    print(f"7. {result['G']}")
    print(f"8. {result['H']}")
    print(f"9. {result['I']}")
    print(f"10. {result['J']}")


if __name__ == '__main__':
    result = data_extraction()
    data_show(result)
