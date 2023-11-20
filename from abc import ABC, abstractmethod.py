from abc import ABC, abstractmethod


class Konto(ABC):
    # Statisches Atribut für den Nmen der Bank
    bankname = "SPK"

    def __init__(self, inhaber, kontonr):
        """Initialisiert ein Konto mit den grundlegenden Attributen.
        param inhaber: Name des Kontoinhabers als string
        param kontonr: Kontonummer als int 
        """
        self.inhaber = inhaber
        self.kontonr = kontonr
        self.kontostand = 0.0  # Bei Objektinitialisierung steht der Kontostand auf 0.0

    @abstractmethod #Idnikator für abstrakte methode
    def einzahlen(self, betrag):
        """
        Erhöht den Kontostand um den eingezahlten Betrag.

        :param betrag: Einzuzahlender Betrag (float)
        """
        pass

    @abstractmethod #Indikator für abstrakte methode 
    def auszahlen(self, betrag):
        """Verringert den Kontostand um den auszuzahlenden Betrag wenn möglich.
        :param betrag: Auszuzahlender Betrag (float)
        :return: True wenn die Auszahlung erfolgreich war False wenn nihct 
        """
        pass

    @abstractmethod #indikator für abstrakte methode
    def zinsberechnung(self):
        """Standard-Zinsberechnung für alle Kontotypen. Muss in den Subklassen überschrieben werden.
        :return: True, wenn Zinsen berechnet wurde False wenn nicht 
        """
        pass

    def __str__(self):
        """Gibt eine String-Repräsentation des Kontos zurück.
        :return: String-Repräsentation des Kontos
        """
        return f"{self.__class__.__name__} (Inhaber {self.inhaber}, Kontonr. {self.kontonr}, Bank {Konto.bankname}) mit Kontostand {self.kontostand}"


class Sparbuch(Konto):
    # Standard-Habenzinssatz für Sparbücher
    zinssatz_haben_standard = 0.01

    def __init__(self, inhaber, kontonr, zinssatz_haben=None):
        """Initialisiert ein Sparbuch mit spezifischen Attributen.
        :param inhaber: Name des Kontoinhabers (string)
        :param kontonr: Kontonummer (int)
        :param zinssatz_haben: Haben-Zinssatz (float)
        """
        super().__init__(inhaber, kontonr)
        # Wenn kein Zinssatz übergeben wird, wird der Standard-Zinssatz verwendet
        self.zinssatz_haben = zinssatz_haben or self.zinssatz_haben_standard

    def einzahlen(self, betrag):
        """Erhöht den Kontostand um den eingezahlten Betrag.
        :param betrag: Einzuzahlender Betrag (float)
        """
        self.kontostand += betrag

    def auszahlen(self, betrag):
        """Verringert den Kontostand um den auszuzahlenden Betrag, wenn möglich.
        :param betrag: der Auszuzahlende Betrag (float)
        :return: True, wenn die Auszahlung erfolgreich war ansonsten false
        """
        if self.kontostand - betrag >= 0:
            self.kontostand -= betrag
            return True
        return False

    def zinsberechnung(self):
        """Berechnet die Habenzinsen und aktualisiert den Kontostand.
        :return: True wweil Habenzinsen immer berechnet werden
        """
        self.kontostand += self.kontostand * self.zinssatz_haben
        return True


class Girokonto(Sparbuch):
    # Standard-Sollzinssatz für Girokonten
    zinssatz_soll_standard = 0.12
    # Standard-Habenzinssatz für Girokonten
    zinssatz_haben_standard = 0.01

    def __init__(self, inhaber, kontonr, kreditlimit, zinssatz_soll=None, zinssatz_haben=None):
        """Initialisiert ein Girokonto mit spezifischen Attributen.
        :param inhaber: Name des Kontoinhabers (string)
        :param kontonr: Kontonummer (int)
        :param kreditlimit: Kreditlimit (float)
        :param zinssatz_soll: Soll-Zinssatz (float)
        :param zinssatz_haben: Haben-Zinssatz (float)
        """
        super().__init__(inhaber, kontonr, zinssatz_haben)
        self.kreditlimit = kreditlimit
        # Wenn keine Zinssätze übergeben werden, werden die Standard-Zinssätze verwendet
        self.zinssatz_soll = zinssatz_soll or self.zinssatz_soll_standard
        self.zinssatz_haben = zinssatz_haben or self.zinssatz_haben_standard

    def auszahlen(self, betrag):
        """Verringert den Kontostand um den auszuzahlenden Betrag, wenn möglich.
        :param betrag: Auszuzahlender Betrag (float)
        :return: True wenn die Auszahlung erfolgreich war wenn nicht dann flase
        """
        if self.kontostand - betrag >= -self.kreditlimit:
            self.kontostand -= betrag
            return True
        return False

    def zinsberechnung(self):
        """Berechnet die Zinsen für das Girokonto und aktualisiert den Kontostand.
        :return: True da Zinsen immer berechnet werden
        """
        if self.kontostand < 0:
            # Berechnung der Sollzinsen, wenn der Kontostand negativ ist
            self.kontostand -= abs(self.kontostand) * self.zinssatz_soll
        else:
            # Berechnung der Habenzinsen, wenn der Kontostand positiv ist
            super().zinsberechnung()
        return True


class Bausparkonto(Sparbuch):
    # Standard-Habenzinssatz für Bausparkonten
    zinssatz_haben_standard = 0.01

    def __init__(self, inhaber, kontonr, zuteilungsbetrag, zinssatz_haben=None):
        """Initialisiert ein Bausparkonto mit spezifischen Attributen.
        :param inhaber: Name des Kontoinhabers (string)
        :param kontonr: Kontonummer (int)
        :param zuteilungsbetrag: Zuteilungsbetrag (float)
        :param zinssatz_haben: Haben-Zinssatz (float)
        """
        super().__init__(inhaber, kontonr, zinssatz_haben)
        self.zuteilungsbetrag = zuteilungsbetrag

    def zinsberechnung(self):
        """Berechnet die Habenzinsen, wenn der Kontostand den Zuteilungsbetrag nicht überschritten hat.
        :return: True wenn Habenzinsen berechnet wurden ansonsten false
        """
        if self.kontostand < self.zuteilungsbetrag:
            # Berechnung der Habenzinsen wenn der Kontostand den Zuteilungsbetrag nicht überschritten hat
            super().zinsberechnung()
            return True
        return False

    def auszahlen(self, betrag):
        """Verringert den Kontostand um den auszuzahlenden Betrag, wenn möglich.
        :param betrag: Auszuzahlender Betrag (float)
        :return: True wenn die Auszahlung erfolgreich war sonst False 
        """
        if self.kontostand - betrag >= 0:
            self.kontostand -= betrag
            return True
        return False


def main():
    # Beispieltests
    sb = Sparbuch('Küppers', 12345)
    print(sb)  # Sparbuch (Inhaber Küppers, Kontonr. 12345, Bank SPK) mit Kontostand 0.0
    sb.einzahlen(1000.0)
    print(sb.kontostand)  # 1000.0
    sb.zinsberechnung()
    print(sb.kontostand)  # 1010.0

    gk = Girokonto('Mustermann', 56789, 500.0)
    print(gk)  # Girokonto (Inhaber Mustermann, Kontonr. 56789, Bank SPK) mit Kontostand 0.0
    gk.auszahlen(100.0)
    print(gk.kontostand)  # -100.0
    gk.zinsberechnung()
    print(gk.kontostand)  # -112.0

    bk = Bausparkonto('Meier', 98765, 2000.0)
    print(bk)  # Bausparkonto (Inhaber Meier, Kontonr. 98765, Bank SPK) mit Kontostand 0.0
    bk.einzahlen(1500.0)
    print(bk.kontostand)  # 1500.0
    bk.zinsberechnung()
    print(bk.kontostand)  # 1515.0
    bk.auszahlen(1000.0)
    print(bk.kontostand)  # 515.0


if __name__ == "__main__":
    main()
