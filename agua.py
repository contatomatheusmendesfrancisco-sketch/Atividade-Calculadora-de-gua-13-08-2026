"""
Matheus Mendes Francisco - 13/08/26
----------------------------------------------------------------------------------------
O Programa calcula de forma automática o quanto uma pessoa deve ingerir de água, 
tudo isso considerando o peso corporal dela, atividade física e situação climática
----------------------------------------------------------------------------------------
Fórmulas: 
meta de ml's: peso * 35 * fator atividade * fator clima
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from math import ceil

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_INTERFACE = os.path.join(PASTA, 'agua.glade')

class Aplicacao:
    def __init__(self):
        self.construtor = Gtk.Builder()
        self.construtor.add_from_file(ARQUIVO_INTERFACE)
        self.construtor.connect_signals(self)

        self.janela = self.construtor.get_object('janPrincipal')

        self.cmbAtividade = self.construtor.get_object('cmbAtividade')
        self.spnPeso = self.construtor.get_object('spnPeso')
        self.chkClima = self.construtor.get_object('chkClima')
        self.lblResultado = self.construtor.get_object('lblResultado')
        
        self.bntCalcular = self.construtor.get_object('bntCalcular')
        self.bntLimpar = self.construtor.get_object('bntLimpar')

        self.bntCalcular.connect('clicked', self.ao_calcular)
        self.bntLimpar.connect("clicked", self.bntLimpar_clicked)

        self.janela.show_all()
        self.janela.connect("destroy", Gtk.main_quit)

    def fator_da_atividade(self):
        idAtividade = self.cmbAtividade.get_active_id()
        return idAtividade
        
    def calcular_meta(self, peso, fatorAtividade, climaQuente):
        fatorClima = 1.10 if climaQuente else 1.0
        return peso * 35 * fatorAtividade * fatorClima

    def contar_copos(self, metaMl):
        return ceil(metaMl / 250)

    def ao_calcular(self, button=None):
        peso = self.spnPeso.get_value()

        idAtividade = self.fator_da_atividade()
        fatores_atividade = {
            "leve": 1.0,
            "moderado": 1.15,
            "intenso": 1.30
        }
        fatorAtividade = fatores_atividade.get(idAtividade, 1.0)
        climaQuente = self.chkClima.get_active()

        if peso > 0:
            meta = self.calcular_meta(peso, fatorAtividade, climaQuente)
            copos = self.contar_copos(meta)
            self.lblResultado.set_text(f"Meta: {meta/1000:.0f}L's" "\n"f"({copos} copos de 250ml)")
        else:
            self.lblResultado.set_text("Por favor, defina o seu peso!")

    def bntLimpar_clicked(self, button=None):
        self.spnPeso.set_value(0)
        self.cmbAtividade.set_active(0)
        self.chkClima.set_active(False)
        self.lblResultado.set_text("------------------------")

if __name__ == '__main__':
    Aplicacao()
    Gtk.main()
