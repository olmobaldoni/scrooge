class Saldo:
    # costructor
    def __init__(self, saldo_iniziale):
        # instance attributes
        if saldo_iniziale == '':
            self.saldo_iniziale = 0
        else:
            self.saldo_iniziale = float(saldo_iniziale)

    # @property
    # def sale(self):
    #     print('property.getter')
    #     return self.saldo_iniziale
    #
    #
    # @sale.setter
    # def sale(self, value):
    #     self.saldo_iniziale = value

    def __repr__(self):
        return 'Saldo = {}'.format(self.saldo_iniziale)
        # return str(self.__dict__)

    def bilancio(self, income, outflow):
        return self.saldo_iniziale + income - outflow


class Entrata:
    # costructor
    def __init__(self, income):
        # instance attributes
        if income == '':
            self.income = 0
        else:
            self.income = float(income)

    def __repr__(self):
        return 'Entrata = {};   Tipo = {}'.format(self.income, type(self.income))
        # return str(self.__dict__)


class Uscita:
    # costructor
    def __init__(self, outflow):
        # instance attributes
        if outflow == '':
            self.outflow = 0
        else:
            self.outflow = float(outflow)

    def __repr__(self):
        return 'Uscita = {}'.format(self.outflow)
        # return str(self.__dict__)
